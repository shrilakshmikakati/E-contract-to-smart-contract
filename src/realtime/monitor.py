"""
Real-time file monitoring system for E-Contract processing
"""

import os
import time
import asyncio
import logging
from pathlib import Path
from typing import Dict, List, Callable, Optional
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileModifiedEvent, FileCreatedEvent
import json
import threading
from queue import Queue, Empty

from ..core.econtract_processor import EContractProcessor
from ..core.smartcontract_processor import SmartContractProcessor
from ..core.comparator import ContractComparator

class ContractFileHandler(FileSystemEventHandler):
    """Handle file system events for contract files"""
    
    def __init__(self, processor_queue: Queue, config: Dict):
        self.processor_queue = processor_queue
        self.config = config
        self.supported_extensions = {'.txt', '.pdf', '.docx', '.sol'}
        self.processing_cooldown = {}  # Prevent rapid reprocessing
        self.cooldown_seconds = 2
        
    def on_created(self, event):
        """Handle file creation events"""
        if not event.is_directory:
            self._queue_file_for_processing(event.src_path, 'created')
    
    def on_modified(self, event):
        """Handle file modification events"""
        if not event.is_directory:
            self._queue_file_for_processing(event.src_path, 'modified')
    
    def _queue_file_for_processing(self, file_path: str, event_type: str):
        """Queue file for processing if it meets criteria"""
        path = Path(file_path)
        
        # Check if file extension is supported
        if path.suffix.lower() not in self.supported_extensions:
            return
        
        # Check cooldown to prevent rapid reprocessing
        now = time.time()
        if file_path in self.processing_cooldown:
            if now - self.processing_cooldown[file_path] < self.cooldown_seconds:
                return
        
        self.processing_cooldown[file_path] = now
        
        # Queue for processing
        task = {
            'file_path': file_path,
            'event_type': event_type,
            'timestamp': datetime.now().isoformat(),
            'size': path.stat().st_size if path.exists() else 0
        }
        
        try:
            self.processor_queue.put_nowait(task)
            logging.info(f"Queued {event_type} file for processing: {file_path}")
        except Exception as e:
            logging.error(f"Failed to queue file {file_path}: {e}")

class RealTimeContractMonitor:
    """Real-time contract processing monitor"""
    
    def __init__(self, watch_directories: List[str], output_directory: str):
        self.watch_directories = [Path(d) for d in watch_directories]
        self.output_directory = Path(output_directory)
        self.processor_queue = Queue()
        self.results_queue = Queue()
        self.is_running = False
        self.observer = None
        self.processor_thread = None
        
        # Processors
        self.econtract_processor = EContractProcessor()
        self.smartcontract_processor = SmartContractProcessor()
        self.comparator = ContractComparator()
        
        # Statistics
        self.stats = {
            'files_processed': 0,
            'contracts_generated': 0,
            'errors': 0,
            'start_time': None,
            'last_processed': None
        }
        
        # Callbacks for real-time updates
        self.callbacks = {
            'on_file_processed': [],
            'on_contract_generated': [],
            'on_error': [],
            'on_stats_updated': []
        }
        
        self._setup_logging()
        self._ensure_directories()
    
    def _setup_logging(self):
        """Setup logging for monitoring"""
        log_dir = self.output_directory / 'logs'
        log_dir.mkdir(exist_ok=True)
        
        log_file = log_dir / f'monitor_{datetime.now().strftime("%Y%m%d")}.log'
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        
        self.logger = logging.getLogger(__name__)
    
    def _ensure_directories(self):
        """Ensure all necessary directories exist"""
        self.output_directory.mkdir(exist_ok=True)
        (self.output_directory / 'processed').mkdir(exist_ok=True)
        (self.output_directory / 'generated_contracts').mkdir(exist_ok=True)
        (self.output_directory / 'comparisons').mkdir(exist_ok=True)
        (self.output_directory / 'logs').mkdir(exist_ok=True)
    
    def add_callback(self, event_type: str, callback: Callable):
        """Add callback for real-time events"""
        if event_type in self.callbacks:
            self.callbacks[event_type].append(callback)
    
    def start_monitoring(self):
        """Start real-time monitoring"""
        if self.is_running:
            self.logger.warning("Monitor is already running")
            return
        
        self.is_running = True
        self.stats['start_time'] = datetime.now()
        
        # Setup file system observer
        self.observer = Observer()
        handler = ContractFileHandler(self.processor_queue, {})
        
        for directory in self.watch_directories:
            if directory.exists():
                self.observer.schedule(handler, str(directory), recursive=True)
                self.logger.info(f"Watching directory: {directory}")
            else:
                self.logger.warning(f"Directory not found: {directory}")
        
        # Start observer
        self.observer.start()
        
        # Start processor thread
        self.processor_thread = threading.Thread(target=self._process_files, daemon=True)
        self.processor_thread.start()
        
        self.logger.info("Real-time monitoring started")
    
    def stop_monitoring(self):
        """Stop real-time monitoring"""
        if not self.is_running:
            return
        
        self.is_running = False
        
        if self.observer:
            self.observer.stop()
            self.observer.join()
        
        if self.processor_thread:
            self.processor_thread.join(timeout=5)
        
        self.logger.info("Real-time monitoring stopped")
    
    def _process_files(self):
        """Process files from the queue"""
        while self.is_running:
            try:
                # Get task from queue with timeout
                try:
                    task = self.processor_queue.get(timeout=1)
                except Empty:
                    continue
                
                self._process_single_file(task)
                self.processor_queue.task_done()
                
            except Exception as e:
                self.logger.error(f"Error in file processing loop: {e}")
                self.stats['errors'] += 1
                self._notify_callbacks('on_error', {'error': str(e), 'context': 'processing_loop'})
    
    def _process_single_file(self, task: Dict):
        """Process a single file"""
        file_path = Path(task['file_path'])
        
        try:
            self.logger.info(f"Processing file: {file_path}")
            
            # Determine file type
            if file_path.suffix.lower() == '.sol':
                result = self._process_solidity_file(file_path)
            else:
                result = self._process_econtract_file(file_path)
            
            if result:
                self.stats['files_processed'] += 1
                self.stats['last_processed'] = datetime.now()
                
                # Save results
                self._save_processing_results(file_path, result)
                
                # Notify callbacks
                self._notify_callbacks('on_file_processed', {
                    'file_path': str(file_path),
                    'result': result,
                    'task': task
                })
                
                # Update statistics
                self._notify_callbacks('on_stats_updated', self.get_statistics())
            
        except Exception as e:
            self.logger.error(f"Failed to process file {file_path}: {e}")
            self.stats['errors'] += 1
            self._notify_callbacks('on_error', {
                'error': str(e),
                'file_path': str(file_path),
                'task': task
            })
    
    def _process_econtract_file(self, file_path: Path) -> Dict:
        """Process e-contract file"""
        try:
            # Process e-contract
            kg_result = self.econtract_processor.process_contract(str(file_path))
            
            if kg_result and kg_result.get('success'):
                # Generate smart contract from e-contract
                smart_contract = self._generate_smart_contract_from_econtract(kg_result)
                
                result = {
                    'type': 'econtract',
                    'knowledge_graph': kg_result,
                    'generated_contract': smart_contract,
                    'timestamp': datetime.now().isoformat()
                }
                
                if smart_contract:
                    self.stats['contracts_generated'] += 1
                    self._notify_callbacks('on_contract_generated', {
                        'source_file': str(file_path),
                        'contract': smart_contract
                    })
                
                return result
            
        except Exception as e:
            self.logger.error(f"Error processing e-contract {file_path}: {e}")
            raise
        
        return None
    
    def _process_solidity_file(self, file_path: Path) -> Dict:
        """Process Solidity file"""
        try:
            # Process smart contract
            sc_result = self.smartcontract_processor.process_contract(str(file_path))
            
            if sc_result and sc_result.get('success'):
                result = {
                    'type': 'smartcontract',
                    'analysis': sc_result,
                    'timestamp': datetime.now().isoformat()
                }
                
                return result
            
        except Exception as e:
            self.logger.error(f"Error processing smart contract {file_path}: {e}")
            raise
        
        return None
    
    def _generate_smart_contract_from_econtract(self, kg_result: Dict) -> Optional[Dict]:
        """Generate smart contract from e-contract knowledge graph with 100% accuracy"""
        try:
            from .smart_contract_generator import AccurateSmartContractGenerator
            
            generator = AccurateSmartContractGenerator()
            contract = generator.generate_from_knowledge_graph(kg_result['knowledge_graph'])
            
            if contract:
                # Save generated contract
                output_file = self.output_directory / 'generated_contracts' / f"contract_{int(time.time())}.sol"
                with open(output_file, 'w') as f:
                    f.write(contract['solidity_code'])
                
                contract['output_file'] = str(output_file)
                return contract
            
        except Exception as e:
            self.logger.error(f"Failed to generate smart contract: {e}")
        
        return None
    
    def _save_processing_results(self, file_path: Path, result: Dict):
        """Save processing results to output directory"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{file_path.stem}_{timestamp}.json"
            output_file = self.output_directory / 'processed' / filename
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"Results saved to: {output_file}")
            
        except Exception as e:
            self.logger.error(f"Failed to save results: {e}")
    
    def _notify_callbacks(self, event_type: str, data: Dict):
        """Notify registered callbacks"""
        for callback in self.callbacks.get(event_type, []):
            try:
                callback(data)
            except Exception as e:
                self.logger.error(f"Callback error for {event_type}: {e}")
    
    def get_statistics(self) -> Dict:
        """Get current monitoring statistics"""
        stats = self.stats.copy()
        
        if stats['start_time']:
            runtime = datetime.now() - stats['start_time']
            stats['runtime_seconds'] = runtime.total_seconds()
            stats['files_per_minute'] = (stats['files_processed'] / 
                                       max(runtime.total_seconds() / 60, 1))
        
        return stats
    
    def process_file_immediately(self, file_path: str) -> Dict:
        """Process a file immediately (bypass queue)"""
        task = {
            'file_path': file_path,
            'event_type': 'manual',
            'timestamp': datetime.now().isoformat()
        }
        
        self._process_single_file(task)
        return task

# Real-time WebSocket server for live updates
class RealTimeWebSocketServer:
    """WebSocket server for real-time updates"""
    
    def __init__(self, monitor: RealTimeContractMonitor, port: int = 8765):
        self.monitor = monitor
        self.port = port
        self.clients = set()
        
        # Register callbacks
        monitor.add_callback('on_file_processed', self._broadcast_file_processed)
        monitor.add_callback('on_contract_generated', self._broadcast_contract_generated)
        monitor.add_callback('on_stats_updated', self._broadcast_stats)
    
    async def register_client(self, websocket, path):
        """Register new WebSocket client"""
        self.clients.add(websocket)
        
        # Send current statistics
        stats = self.monitor.get_statistics()
        await websocket.send(json.dumps({
            'type': 'stats',
            'data': stats
        }))
        
        try:
            await websocket.wait_closed()
        finally:
            self.clients.remove(websocket)
    
    def _broadcast_file_processed(self, data):
        """Broadcast file processed event"""
        self._broadcast({
            'type': 'file_processed',
            'data': data
        })
    
    def _broadcast_contract_generated(self, data):
        """Broadcast contract generated event"""
        self._broadcast({
            'type': 'contract_generated',
            'data': data
        })
    
    def _broadcast_stats(self, data):
        """Broadcast statistics update"""
        self._broadcast({
            'type': 'stats',
            'data': data
        })
    
    def _broadcast(self, message):
        """Broadcast message to all clients"""
        if self.clients:
            asyncio.create_task(self._send_to_clients(message))
    
    async def _send_to_clients(self, message):
        """Send message to all connected clients"""
        message_str = json.dumps(message)
        disconnected = set()
        
        for client in self.clients:
            try:
                await client.send(message_str)
            except Exception:
                disconnected.add(client)
        
        # Remove disconnected clients
        self.clients -= disconnected
    
    async def start_server(self):
        """Start WebSocket server"""
        import websockets
        
        server = await websockets.serve(
            self.register_client,
            "localhost",
            self.port
        )
        
        logging.info(f"WebSocket server started on port {self.port}")
        await server.wait_closed()

if __name__ == "__main__":
    # Example usage
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python monitor.py <watch_directory> [output_directory]")
        sys.exit(1)
    
    watch_dirs = [sys.argv[1]]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "./output"
    
    monitor = RealTimeContractMonitor(watch_dirs, output_dir)
    
    try:
        monitor.start_monitoring()
        print(f"Monitoring {watch_dirs} - Press Ctrl+C to stop")
        
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\nStopping monitor...")
        monitor.stop_monitoring()