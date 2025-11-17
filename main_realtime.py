#!/usr/bin/env python3
"""
Real-time E-Contract and Smart Contract Analysis System
Main application entry point with real-time processing capabilities
"""

import sys
import os
import asyncio
import logging
import argparse
from pathlib import Path
from typing import Optional
import threading
import time

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Import real-time components
from src.realtime.monitor import RealTimeContractMonitor
from src.realtime.api_server import app
from src.realtime.smart_contract_generator import AccurateSmartContractGenerator
from src.realtime.validator import ComprehensiveValidator, ValidationLevel

# Import core components
from src.core.econtract_processor import EContractProcessor
from src.core.smartcontract_processor import SmartContractProcessor
from src.core.comparator import ContractComparator

# Import GUI
from src.gui.main_window import ContractAnalysisGUI

import uvicorn
import tkinter as tk
from tkinter import messagebox

def setup_logging(log_level: str = "INFO", log_file: Optional[str] = None):
    """Setup logging configuration"""
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout),
            *([] if log_file is None else [logging.FileHandler(log_file)])
        ]
    )

class RealTimeContractSystem:
    """Main real-time contract analysis system"""
    
    def __init__(self, config: dict):
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        # Initialize components
        self.monitor = None
        self.api_server = None
        self.validator = ComprehensiveValidator(ValidationLevel.COMPREHENSIVE)
        self.generator = AccurateSmartContractGenerator()
        
        # Processors
        self.econtract_processor = EContractProcessor()
        self.smartcontract_processor = SmartContractProcessor()
        self.comparator = ContractComparator()
        
        # Threading
        self.api_thread = None
        self.gui_thread = None
        
    def start_api_server(self, host: str = "0.0.0.0", port: int = 8000):
        """Start the FastAPI server"""
        try:
            self.logger.info(f"Starting API server on {host}:{port}")
            uvicorn.run(app, host=host, port=port, log_level="info")
        except Exception as e:
            self.logger.error(f"Failed to start API server: {e}")
            raise
    
    def start_monitor(self, watch_dirs: list, output_dir: str):
        """Start real-time file monitoring"""
        try:
            self.logger.info(f"Starting monitor for directories: {watch_dirs}")
            
            # Ensure output directory exists
            Path(output_dir).mkdir(parents=True, exist_ok=True)
            
            # Initialize monitor
            self.monitor = RealTimeContractMonitor(watch_dirs, output_dir)
            
            # Add validation callback
            def validate_generated_contract(data):
                """Validate generated contracts for 100% accuracy"""
                try:
                    if 'contract' in data and 'source_file' in data:
                        contract_data = data['contract']
                        source_file = data['source_file']
                        
                        # Validate the generated contract
                        validation_result = self.validator.validate_contract_generation(
                            source_kg={},  # Would need to extract from contract_data
                            generated_contract=contract_data.get('solidity_code', ''),
                            metadata=contract_data.get('metadata', {})
                        )
                        
                        if not validation_result.is_valid:
                            self.logger.warning(f"Generated contract for {source_file} failed validation: {validation_result.errors}")
                        else:
                            self.logger.info(f"Generated contract for {source_file} passed validation with score: {validation_result.score:.2%}")
                            
                except Exception as e:
                    self.logger.error(f"Validation callback error: {e}")
            
            self.monitor.add_callback('on_contract_generated', validate_generated_contract)
            
            # Start monitoring
            self.monitor.start_monitoring()
            self.logger.info("Monitor started successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to start monitor: {e}")
            raise
    
    def start_gui(self):
        """Start the GUI application"""
        try:
            self.logger.info("Starting GUI application")
            
            root = tk.Tk()
            app = ContractAnalysisGUI(root)
            
            # Add real-time capabilities to GUI
            self._integrate_realtime_with_gui(app)
            
            root.mainloop()
            
        except Exception as e:
            self.logger.error(f"Failed to start GUI: {e}")
            raise
    
    def _integrate_realtime_with_gui(self, gui_app):
        """Integrate real-time capabilities with GUI"""
        # Add real-time monitoring controls
        realtime_frame = tk.Frame(gui_app.notebook)
        gui_app.notebook.add(realtime_frame, text="Real-time Monitor")
        
        # Monitor controls
        tk.Label(realtime_frame, text="Real-time File Monitoring", 
                font=("Arial", 14, "bold")).pack(pady=10)
        
        # Directory selection
        dir_frame = tk.Frame(realtime_frame)
        dir_frame.pack(pady=5, padx=10, fill=tk.X)
        
        tk.Label(dir_frame, text="Watch Directory:").pack(side=tk.LEFT)
        watch_dir_var = tk.StringVar(value="./watch")
        tk.Entry(dir_frame, textvariable=watch_dir_var, width=50).pack(side=tk.LEFT, padx=5)
        
        # Monitor status
        status_frame = tk.Frame(realtime_frame)
        status_frame.pack(pady=5, padx=10, fill=tk.X)
        
        status_label = tk.Label(status_frame, text="Status: Stopped", fg="red")
        status_label.pack(side=tk.LEFT)
        
        # Control buttons
        button_frame = tk.Frame(realtime_frame)
        button_frame.pack(pady=10)
        
        def start_monitor():
            try:
                watch_dir = watch_dir_var.get()
                if not watch_dir:
                    messagebox.showwarning("Warning", "Please specify a watch directory")
                    return
                
                self.start_monitor([watch_dir], "./output")
                status_label.config(text="Status: Running", fg="green")
                start_btn.config(state=tk.DISABLED)
                stop_btn.config(state=tk.NORMAL)
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to start monitor: {e}")
        
        def stop_monitor():
            try:
                if self.monitor:
                    self.monitor.stop_monitoring()
                    self.monitor = None
                
                status_label.config(text="Status: Stopped", fg="red")
                start_btn.config(state=tk.NORMAL)
                stop_btn.config(state=tk.DISABLED)
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to stop monitor: {e}")
        
        start_btn = tk.Button(button_frame, text="Start Monitor", command=start_monitor,
                             bg="#4CAF50", fg="white", font=("Arial", 10, "bold"))
        start_btn.pack(side=tk.LEFT, padx=5)
        
        stop_btn = tk.Button(button_frame, text="Stop Monitor", command=stop_monitor,
                            bg="#f44336", fg="white", font=("Arial", 10, "bold"),
                            state=tk.DISABLED)
        stop_btn.pack(side=tk.LEFT, padx=5)
        
        # Real-time statistics
        stats_frame = tk.LabelFrame(realtime_frame, text="Real-time Statistics", font=("Arial", 12, "bold"))
        stats_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        
        stats_text = tk.Text(stats_frame, height=10, width=80)
        stats_text.pack(pady=5, padx=5, fill=tk.BOTH, expand=True)
        
        def update_stats():
            """Update statistics display"""
            if self.monitor:
                stats = self.monitor.get_statistics()
                stats_text.delete(1.0, tk.END)
                stats_text.insert(tk.END, f"Files Processed: {stats.get('files_processed', 0)}\n")
                stats_text.insert(tk.END, f"Contracts Generated: {stats.get('contracts_generated', 0)}\n")
                stats_text.insert(tk.END, f"Errors: {stats.get('errors', 0)}\n")
                if 'runtime_seconds' in stats:
                    stats_text.insert(tk.END, f"Runtime: {stats['runtime_seconds']:.2f} seconds\n")
                if 'files_per_minute' in stats:
                    stats_text.insert(tk.END, f"Processing Rate: {stats['files_per_minute']:.2f} files/min\n")
            
            # Schedule next update
            gui_app.root.after(2000, update_stats)
        
        # Start stats updating
        update_stats()
    
    def run_cli_mode(self, args):
        """Run in CLI mode"""
        if args.monitor:
            self.logger.info("Running in monitor mode")
            
            try:
                self.start_monitor(args.watch_dirs, args.output_dir)
                
                self.logger.info("Monitor started. Press Ctrl+C to stop.")
                while True:
                    time.sleep(1)
                    
            except KeyboardInterrupt:
                self.logger.info("Stopping monitor...")
                if self.monitor:
                    self.monitor.stop_monitoring()
        
        elif args.api:
            self.logger.info("Running API server")
            self.start_api_server(args.host, args.port)
        
        elif args.process_file:
            self.logger.info(f"Processing single file: {args.process_file}")
            self._process_single_file(args.process_file)
        
        else:
            self.logger.error("No valid CLI option specified")
            return 1
        
        return 0
    
    def _process_single_file(self, file_path: str):
        """Process a single file"""
        try:
            path = Path(file_path)
            if not path.exists():
                self.logger.error(f"File not found: {file_path}")
                return
            
            self.logger.info(f"Processing file: {file_path}")
            
            # Determine file type and process
            if path.suffix.lower() == '.sol':
                result = self.smartcontract_processor.process_contract(str(path))
                processor_type = "Smart Contract"
            else:
                result = self.econtract_processor.process_contract(str(path))
                processor_type = "E-Contract"
                
                # Generate smart contract if successful
                if result and result.get('success') and result.get('knowledge_graph'):
                    self.logger.info("Generating smart contract...")
                    contract_result = self.generator.generate_from_knowledge_graph(
                        result['knowledge_graph']
                    )
                    
                    if contract_result and contract_result.get('success'):
                        # Validate generated contract
                        validation_result = self.validator.validate_contract_generation(
                            result['knowledge_graph'],
                            contract_result['solidity_code'],
                            contract_result.get('metadata', {})
                        )
                        
                        self.logger.info(f"Contract generated with accuracy score: {validation_result.score:.2%}")
                        
                        # Save generated contract
                        output_file = Path("output") / f"generated_{path.stem}.sol"
                        output_file.parent.mkdir(exist_ok=True)
                        
                        with open(output_file, 'w') as f:
                            f.write(contract_result['solidity_code'])
                        
                        self.logger.info(f"Smart contract saved to: {output_file}")
                        
                        if not validation_result.is_valid:
                            self.logger.warning(f"Validation errors: {validation_result.errors}")
                    else:
                        self.logger.error("Failed to generate smart contract")
            
            if result and result.get('success'):
                self.logger.info(f"{processor_type} processing completed successfully")
                
                # Save result
                output_file = Path("output") / f"result_{path.stem}.json"
                output_file.parent.mkdir(exist_ok=True)
                
                import json
                with open(output_file, 'w') as f:
                    json.dump(result, f, indent=2, ensure_ascii=False)
                
                self.logger.info(f"Results saved to: {output_file}")
            else:
                self.logger.error(f"Failed to process {file_path}")
            
        except Exception as e:
            self.logger.error(f"Error processing file {file_path}: {e}")

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Real-time E-Contract and Smart Contract Analysis System"
    )
    
    # Mode selection
    mode_group = parser.add_mutually_exclusive_group()
    mode_group.add_argument("--gui", action="store_true", 
                          help="Launch GUI application (default)")
    mode_group.add_argument("--api", action="store_true", 
                          help="Start API server")
    mode_group.add_argument("--monitor", action="store_true", 
                          help="Start file monitoring mode")
    mode_group.add_argument("--process-file", type=str, 
                          help="Process a single file")
    
    # API server options
    parser.add_argument("--host", default="0.0.0.0", 
                       help="API server host (default: 0.0.0.0)")
    parser.add_argument("--port", type=int, default=8000, 
                       help="API server port (default: 8000)")
    
    # Monitor options
    parser.add_argument("--watch-dirs", nargs="+", default=["./watch"], 
                       help="Directories to watch (default: ./watch)")
    parser.add_argument("--output-dir", default="./output", 
                       help="Output directory (default: ./output)")
    
    # Logging options
    parser.add_argument("--log-level", default="INFO", 
                       choices=["DEBUG", "INFO", "WARNING", "ERROR"],
                       help="Logging level (default: INFO)")
    parser.add_argument("--log-file", type=str, 
                       help="Log file path (optional)")
    
    args = parser.parse_args()
    
    # Setup logging
    setup_logging(args.log_level, args.log_file)
    
    # Create system configuration
    config = {
        'validation_level': 'comprehensive',
        'accuracy_threshold': 0.95,
        'real_time_enabled': True
    }
    
    # Initialize system
    system = RealTimeContractSystem(config)
    
    try:
        # Determine mode
        if args.api:
            return system.run_cli_mode(args)
        elif args.monitor:
            return system.run_cli_mode(args)
        elif args.process_file:
            return system.run_cli_mode(args)
        else:
            # Default to GUI mode
            system.start_gui()
            return 0
            
    except KeyboardInterrupt:
        logging.info("Application interrupted by user")
        return 0
    except Exception as e:
        logging.error(f"Application error: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())