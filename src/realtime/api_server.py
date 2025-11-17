"""
Real-time API server for E-Contract and Smart Contract analysis
Provides REST API and WebSocket endpoints for real-time processing
"""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, File, UploadFile, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import asyncio
import json
import logging
import os
import tempfile
import shutil
from pathlib import Path
from typing import List, Dict, Optional, Set
from datetime import datetime
import uvicorn
from pydantic import BaseModel
import websockets

from .monitor import RealTimeContractMonitor
from .smart_contract_generator import AccurateSmartContractGenerator
from ..core.econtract_processor import EContractProcessor
from ..core.smartcontract_processor import SmartContractProcessor
from ..core.comparator import ContractComparator

# Pydantic models for API
class ProcessRequest(BaseModel):
    file_path: str
    contract_type: Optional[str] = None

class GenerateContractRequest(BaseModel):
    knowledge_graph: Dict
    contract_type: Optional[str] = None

class ComparisonRequest(BaseModel):
    econtract_kg: Dict
    smartcontract_kg: Dict

class MonitorConfig(BaseModel):
    watch_directories: List[str]
    output_directory: str
    auto_process: bool = True

# Global state
app = FastAPI(
    title="E-Contract Real-time Analysis API",
    description="Real-time processing and analysis of E-Contracts and Smart Contracts",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variables
monitor: Optional[RealTimeContractMonitor] = None
websocket_connections: Set[WebSocket] = set()
processors = {
    'econtract': EContractProcessor(),
    'smartcontract': SmartContractProcessor(),
    'comparator': ContractComparator(),
    'generator': AccurateSmartContractGenerator()
}

# Statistics
stats = {
    'total_requests': 0,
    'successful_processing': 0,
    'failed_processing': 0,
    'contracts_generated': 0,
    'active_connections': 0,
    'start_time': datetime.now()
}

@app.on_event("startup")
async def startup_event():
    """Initialize the application"""
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    logger.info("Starting E-Contract Real-time Analysis API")
    
    # Create temp directories
    os.makedirs("temp/uploads", exist_ok=True)
    os.makedirs("temp/outputs", exist_ok=True)

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    global monitor
    if monitor:
        monitor.stop_monitoring()
    
    # Close all WebSocket connections
    for connection in websocket_connections.copy():
        await connection.close()

# WebSocket endpoint for real-time updates
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time updates"""
    await websocket.accept()
    websocket_connections.add(websocket)
    stats['active_connections'] = len(websocket_connections)
    
    try:
        # Send initial stats
        await websocket.send_text(json.dumps({
            'type': 'stats',
            'data': get_current_stats()
        }))
        
        # Keep connection alive and handle messages
        while True:
            try:
                message = await websocket.receive_text()
                data = json.loads(message)
                
                # Handle different message types
                if data.get('type') == 'ping':
                    await websocket.send_text(json.dumps({'type': 'pong'}))
                elif data.get('type') == 'get_stats':
                    await websocket.send_text(json.dumps({
                        'type': 'stats',
                        'data': get_current_stats()
                    }))
                
            except WebSocketDisconnect:
                break
            except Exception as e:
                logging.error(f"WebSocket error: {e}")
                break
    
    finally:
        websocket_connections.discard(websocket)
        stats['active_connections'] = len(websocket_connections)

async def broadcast_to_websockets(message: Dict):
    """Broadcast message to all connected WebSocket clients"""
    if websocket_connections:
        message_str = json.dumps(message)
        disconnected = set()
        
        for connection in websocket_connections:
            try:
                await connection.send_text(message_str)
            except:
                disconnected.add(connection)
        
        # Remove disconnected clients
        websocket_connections.difference_update(disconnected)
        stats['active_connections'] = len(websocket_connections)

def get_current_stats() -> Dict:
    """Get current system statistics"""
    runtime = datetime.now() - stats['start_time']
    return {
        **stats,
        'runtime_seconds': runtime.total_seconds(),
        'success_rate': (stats['successful_processing'] / max(stats['total_requests'], 1)) * 100,
        'monitor_active': monitor is not None and monitor.is_running if monitor else False
    }

# API Endpoints

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "E-Contract Real-time Analysis API",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "process_file": "/process/file",
            "process_upload": "/process/upload", 
            "generate_contract": "/generate/contract",
            "compare_contracts": "/compare",
            "monitor": "/monitor",
            "websocket": "/ws",
            "stats": "/stats"
        }
    }

@app.get("/stats")
async def get_stats():
    """Get system statistics"""
    return get_current_stats()

@app.post("/process/file")
async def process_file(request: ProcessRequest, background_tasks: BackgroundTasks):
    """Process a file from file system"""
    stats['total_requests'] += 1
    
    try:
        file_path = Path(request.file_path)
        if not file_path.exists():
            raise HTTPException(status_code=404, detail="File not found")
        
        # Determine processor based on file extension
        if file_path.suffix.lower() == '.sol':
            processor = processors['smartcontract']
            process_type = 'smartcontract'
        else:
            processor = processors['econtract']
            process_type = 'econtract'
        
        # Process file
        result = processor.process_contract(str(file_path))
        
        if result and result.get('success'):
            stats['successful_processing'] += 1
            
            # If it's an e-contract, optionally generate smart contract
            if process_type == 'econtract' and result.get('knowledge_graph'):
                background_tasks.add_task(
                    generate_smart_contract_background,
                    result['knowledge_graph'],
                    str(file_path)
                )
            
            # Broadcast update via WebSocket
            await broadcast_to_websockets({
                'type': 'file_processed',
                'data': {
                    'file_path': str(file_path),
                    'process_type': process_type,
                    'success': True,
                    'timestamp': datetime.now().isoformat()
                }
            })
            
            return {
                'success': True,
                'process_type': process_type,
                'result': result,
                'timestamp': datetime.now().isoformat()
            }
        else:
            stats['failed_processing'] += 1
            raise HTTPException(status_code=500, detail="Processing failed")
    
    except Exception as e:
        stats['failed_processing'] += 1
        logging.error(f"File processing error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/process/upload")
async def process_upload(file: UploadFile = File(...), background_tasks: BackgroundTasks = None):
    """Process an uploaded file"""
    stats['total_requests'] += 1
    
    try:
        # Save uploaded file temporarily
        temp_dir = Path("temp/uploads")
        temp_file = temp_dir / f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{file.filename}"
        
        with open(temp_file, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Process the file
        request = ProcessRequest(file_path=str(temp_file))
        result = await process_file(request, background_tasks)
        
        # Clean up temp file
        temp_file.unlink()
        
        return result
    
    except Exception as e:
        stats['failed_processing'] += 1
        logging.error(f"Upload processing error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate/contract")
async def generate_contract(request: GenerateContractRequest):
    """Generate smart contract from knowledge graph"""
    stats['total_requests'] += 1
    
    try:
        generator = processors['generator']
        result = generator.generate_from_knowledge_graph(request.knowledge_graph)
        
        if result and result.get('success'):
            stats['successful_processing'] += 1
            stats['contracts_generated'] += 1
            
            # Save generated contract
            output_dir = Path("temp/outputs")
            contract_file = output_dir / f"contract_{datetime.now().strftime('%Y%m%d_%H%M%S')}.sol"
            
            with open(contract_file, 'w') as f:
                f.write(result['solidity_code'])
            
            result['output_file'] = str(contract_file)
            
            # Broadcast update
            await broadcast_to_websockets({
                'type': 'contract_generated',
                'data': {
                    'contract_file': str(contract_file),
                    'accuracy_score': result.get('accuracy_score', 0),
                    'timestamp': datetime.now().isoformat()
                }
            })
            
            return result
        else:
            stats['failed_processing'] += 1
            raise HTTPException(status_code=500, detail=result.get('error', 'Generation failed'))
    
    except Exception as e:
        stats['failed_processing'] += 1
        logging.error(f"Contract generation error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/compare")
async def compare_contracts(request: ComparisonRequest):
    """Compare e-contract and smart contract knowledge graphs"""
    stats['total_requests'] += 1
    
    try:
        comparator = processors['comparator']
        
        # Perform comparison
        comparison_result = comparator.compare_contracts(
            request.econtract_kg,
            request.smartcontract_kg
        )
        
        if comparison_result and comparison_result.get('success'):
            stats['successful_processing'] += 1
            
            # Broadcast update
            await broadcast_to_websockets({
                'type': 'comparison_completed',
                'data': {
                    'similarity_score': comparison_result.get('similarity_score', 0),
                    'timestamp': datetime.now().isoformat()
                }
            })
            
            return comparison_result
        else:
            stats['failed_processing'] += 1
            raise HTTPException(status_code=500, detail="Comparison failed")
    
    except Exception as e:
        stats['failed_processing'] += 1
        logging.error(f"Comparison error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/monitor/start")
async def start_monitor(config: MonitorConfig):
    """Start real-time file monitoring"""
    global monitor
    
    try:
        if monitor and monitor.is_running:
            return {"message": "Monitor is already running"}
        
        # Create output directory if it doesn't exist
        Path(config.output_directory).mkdir(parents=True, exist_ok=True)
        
        # Initialize monitor
        monitor = RealTimeContractMonitor(
            config.watch_directories,
            config.output_directory
        )
        
        # Add callbacks for WebSocket broadcasting
        monitor.add_callback('on_file_processed', broadcast_file_processed)
        monitor.add_callback('on_contract_generated', broadcast_contract_generated)
        monitor.add_callback('on_error', broadcast_error)
        monitor.add_callback('on_stats_updated', broadcast_stats_update)
        
        # Start monitoring
        monitor.start_monitoring()
        
        return {
            "message": "Monitor started successfully",
            "config": config.dict(),
            "timestamp": datetime.now().isoformat()
        }
    
    except Exception as e:
        logging.error(f"Failed to start monitor: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/monitor/stop")
async def stop_monitor():
    """Stop real-time file monitoring"""
    global monitor
    
    try:
        if not monitor or not monitor.is_running:
            return {"message": "Monitor is not running"}
        
        monitor.stop_monitoring()
        monitor = None
        
        return {
            "message": "Monitor stopped successfully",
            "timestamp": datetime.now().isoformat()
        }
    
    except Exception as e:
        logging.error(f"Failed to stop monitor: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/monitor/status")
async def get_monitor_status():
    """Get monitor status"""
    if monitor:
        return {
            "running": monitor.is_running,
            "statistics": monitor.get_statistics(),
            "timestamp": datetime.now().isoformat()
        }
    else:
        return {
            "running": False,
            "message": "Monitor not initialized",
            "timestamp": datetime.now().isoformat()
        }

@app.get("/download/{file_type}/{filename}")
async def download_file(file_type: str, filename: str):
    """Download generated files"""
    try:
        if file_type == "contract":
            file_path = Path("temp/outputs") / filename
        elif file_type == "result":
            file_path = Path("temp/results") / filename
        else:
            raise HTTPException(status_code=400, detail="Invalid file type")
        
        if not file_path.exists():
            raise HTTPException(status_code=404, detail="File not found")
        
        return FileResponse(
            path=file_path,
            filename=filename,
            media_type='application/octet-stream'
        )
    
    except Exception as e:
        logging.error(f"Download error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Background tasks
async def generate_smart_contract_background(knowledge_graph: Dict, source_file: str):
    """Generate smart contract in background"""
    try:
        generator = processors['generator']
        result = generator.generate_from_knowledge_graph(knowledge_graph)
        
        if result and result.get('success'):
            stats['contracts_generated'] += 1
            
            # Save generated contract
            output_dir = Path("temp/outputs")
            contract_file = output_dir / f"auto_{datetime.now().strftime('%Y%m%d_%H%M%S')}.sol"
            
            with open(contract_file, 'w') as f:
                f.write(result['solidity_code'])
            
            # Broadcast update
            await broadcast_to_websockets({
                'type': 'auto_contract_generated',
                'data': {
                    'source_file': source_file,
                    'contract_file': str(contract_file),
                    'accuracy_score': result.get('accuracy_score', 0),
                    'timestamp': datetime.now().isoformat()
                }
            })
    
    except Exception as e:
        logging.error(f"Background contract generation error: {e}")

# WebSocket callback functions
async def broadcast_file_processed(data: Dict):
    """Broadcast file processed event"""
    await broadcast_to_websockets({
        'type': 'monitor_file_processed',
        'data': data
    })

async def broadcast_contract_generated(data: Dict):
    """Broadcast contract generated event"""
    await broadcast_to_websockets({
        'type': 'monitor_contract_generated',
        'data': data
    })

async def broadcast_error(data: Dict):
    """Broadcast error event"""
    await broadcast_to_websockets({
        'type': 'monitor_error',
        'data': data
    })

async def broadcast_stats_update(data: Dict):
    """Broadcast stats update"""
    await broadcast_to_websockets({
        'type': 'monitor_stats',
        'data': data
    })

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    }

# Static files for web interface
app.mount("/static", StaticFiles(directory="static"), name="static")

if __name__ == "__main__":
    uvicorn.run(
        "api_server:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )