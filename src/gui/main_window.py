"""
Main GUI application for E-Contract and Smart Contract Analysis System
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import os
import threading
import json
from typing import Dict, Any, Optional
from datetime import datetime

from ..core.econtract_processor import EContractProcessor
from ..core.smartcontract_processor import SmartContractProcessor
from ..core.comparator import ContractComparator
from ..utils.config import Config
from ..utils.file_handler import FileHandler

class MainWindow:
    """Main GUI window for the contract analysis system"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("E-Contract and Smart Contract Analysis System")
        self.root.geometry(f"{Config.WINDOW_WIDTH}x{Config.WINDOW_HEIGHT}")
        
        # Initialize processors
        self.econtract_processor = EContractProcessor()
        self.smartcontract_processor = SmartContractProcessor()
        self.comparator = ContractComparator()
        
        # State variables
        self.current_econtract_path = tk.StringVar()
        self.processing_status = tk.StringVar(value="Ready")
        
        # Results storage
        self.econtract_kg = None
        self.smartcontract_kg = None
        self.generated_contract_result = None
        self.comparison_results = None
        
        self._setup_gui()
        self._setup_menu()
        
    def _setup_gui(self):
        """Setup the main GUI layout"""
        
        # Main container with padding
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="Contract Analysis System", 
                               font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # File Selection Section
        self._create_file_selection_section(main_frame, 1)
        
        # Processing Controls Section
        self._create_processing_controls_section(main_frame, 2)
        
        # Results Display Section
        self._create_results_section(main_frame, 3)
        
        # Status Bar
        self._create_status_bar(main_frame, 4)
    
    def _create_file_selection_section(self, parent, row):
        """Create file selection section"""
        
        # File Selection Frame
        file_frame = ttk.LabelFrame(parent, text="File Selection", padding="10")
        file_frame.grid(row=row, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        file_frame.columnconfigure(1, weight=1)
        
        # E-Contract File
        ttk.Label(file_frame, text="E-Contract File:").grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        
        econtract_entry = ttk.Entry(file_frame, textvariable=self.current_econtract_path, width=50)
        econtract_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(5, 5), pady=(0, 5))
        
        ttk.Button(file_frame, text="Browse...", 
                  command=self._browse_econtract_file).grid(row=0, column=2, pady=(0, 5))
        
        # Generated Smart Contract Display
        ttk.Label(file_frame, text="Generated Smart Contract:").grid(row=1, column=0, sticky=tk.W, pady=(0, 5))
        
        self.generated_contract_info = tk.StringVar(value="No smart contract generated yet")
        contract_label = ttk.Label(file_frame, textvariable=self.generated_contract_info, 
                                 foreground="gray", width=50, anchor="w")
        contract_label.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(5, 5), pady=(0, 5))
        
        self.download_button = ttk.Button(file_frame, text="Download Contract", 
                                        command=self._download_generated_contract, 
                                        state="disabled")
        self.download_button.grid(row=1, column=2, pady=(0, 5))
    
    def _create_processing_controls_section(self, parent, row):
        """Create processing controls section"""
        
        # Processing Controls Frame
        controls_frame = ttk.LabelFrame(parent, text="Processing Controls", padding="10")
        controls_frame.grid(row=row, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Button frame
        button_frame = ttk.Frame(controls_frame)
        button_frame.grid(row=0, column=0, columnspan=3)
        
        # Processing buttons
        ttk.Button(button_frame, text="Process E-Contract", 
                  command=self._process_econtract).grid(row=0, column=0, padx=(0, 15))
        
        ttk.Button(button_frame, text="Generate Smart Contract", 
                  command=self._generate_smart_contract, 
                  style="Accent.TButton").grid(row=0, column=1, padx=(0, 15))
        
        ttk.Button(button_frame, text="Analyze Generated Contract", 
                  command=self._analyze_generated_contract).grid(row=0, column=2, padx=(0, 15))
        
        ttk.Button(button_frame, text="Compare & Validate", 
                  command=self._compare_and_validate).grid(row=0, column=3, padx=(0, 15))
        
        ttk.Button(button_frame, text="Deploy Contract", 
                  command=self._prepare_deployment).grid(row=0, column=4, padx=(0, 0))
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(controls_frame, variable=self.progress_var, 
                                          mode='determinate', length=400)
        self.progress_bar.grid(row=1, column=0, columnspan=3, pady=(10, 0), sticky=(tk.W, tk.E))
    
    def _create_results_section(self, parent, row):
        """Create results display section"""
        
        # Results Frame
        results_frame = ttk.LabelFrame(parent, text="Results", padding="10")
        results_frame.grid(row=row, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        results_frame.columnconfigure(0, weight=1)
        results_frame.rowconfigure(0, weight=1)
        
        # Notebook for tabbed results
        self.results_notebook = ttk.Notebook(results_frame)
        self.results_notebook.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # E-Contract Results Tab
        self.econtract_tab = ttk.Frame(self.results_notebook)
        self.results_notebook.add(self.econtract_tab, text="E-Contract Analysis")
        
        self.econtract_text = scrolledtext.ScrolledText(self.econtract_tab, wrap=tk.WORD, 
                                                       width=80, height=20)
        self.econtract_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5, pady=5)
        self.econtract_tab.columnconfigure(0, weight=1)
        self.econtract_tab.rowconfigure(0, weight=1)
        
        # Smart Contract Results Tab
        self.smartcontract_tab = ttk.Frame(self.results_notebook)
        self.results_notebook.add(self.smartcontract_tab, text="Generated Smart Contract")
        
        self.smartcontract_text = scrolledtext.ScrolledText(self.smartcontract_tab, wrap=tk.WORD,
                                                           width=80, height=20)
        self.smartcontract_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5, pady=5)
        self.smartcontract_tab.columnconfigure(0, weight=1)
        self.smartcontract_tab.rowconfigure(0, weight=1)
        
        # Comparison Results Tab
        self.comparison_tab = ttk.Frame(self.results_notebook)
        self.results_notebook.add(self.comparison_tab, text="Comparison Results")
        
        self.comparison_text = scrolledtext.ScrolledText(self.comparison_tab, wrap=tk.WORD,
                                                        width=80, height=20)
        self.comparison_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5, pady=5)
        self.comparison_tab.columnconfigure(0, weight=1)
        self.comparison_tab.rowconfigure(0, weight=1)
        
        # Visualization Tab
        self.visualization_tab = ttk.Frame(self.results_notebook)
        self.results_notebook.add(self.visualization_tab, text="Visualizations")
        
        # Visualization controls
        viz_controls_frame = ttk.Frame(self.visualization_tab)
        viz_controls_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=5, pady=5)
        
        ttk.Button(viz_controls_frame, text="Show E-Contract Graph", 
                  command=self._show_econtract_graph).grid(row=0, column=0, padx=(0, 10))
        
        ttk.Button(viz_controls_frame, text="Show Smart Contract Graph", 
                  command=self._show_smartcontract_graph).grid(row=0, column=1, padx=(0, 10))
        
        ttk.Button(viz_controls_frame, text="Show Comparison Graph", 
                  command=self._show_comparison_graph).grid(row=0, column=2, padx=(0, 10))
        
        # Export buttons
        ttk.Button(viz_controls_frame, text="Export Graphs", 
                  command=self._export_knowledge_graph).grid(row=0, column=3, padx=(0, 10))
        
        ttk.Button(viz_controls_frame, text="Export All Results", 
                  command=self._export_all_results, 
                  style="Accent.TButton").grid(row=0, column=4)
        
        self.visualization_text = scrolledtext.ScrolledText(self.visualization_tab, wrap=tk.WORD,
                                                           width=80, height=18)
        self.visualization_text.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5, pady=5)
        self.visualization_tab.columnconfigure(0, weight=1)
        self.visualization_tab.rowconfigure(1, weight=1)
    
    def _create_status_bar(self, parent, row):
        """Create status bar"""
        
        status_frame = ttk.Frame(parent)
        status_frame.grid(row=row, column=0, columnspan=3, sticky=(tk.W, tk.E))
        
        ttk.Label(status_frame, text="Status:").grid(row=0, column=0)
        
        status_label = ttk.Label(status_frame, textvariable=self.processing_status)
        status_label.grid(row=0, column=1, sticky=tk.W, padx=(5, 0))
    
    def _setup_menu(self):
        """Setup menu bar"""
        
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New Analysis", command=self._new_analysis)
        file_menu.add_separator()
        
        # Export submenu
        export_menu = tk.Menu(file_menu, tearoff=0)
        export_menu.add_command(label="Export E-Contract Results", command=self._export_econtract_results)
        export_menu.add_command(label="Export Smart Contract Results", command=self._export_smartcontract_results)
        export_menu.add_command(label="Export Generated Contract", command=self._export_generated_contract)
        export_menu.add_command(label="Export Comparison Results", command=self._export_comparison_results)
        export_menu.add_separator()
        export_menu.add_command(label="Export Knowledge Graph (GraphML)", command=self._export_knowledge_graph)
        export_menu.add_command(label="Export Knowledge Graph (JSON)", command=self._export_knowledge_graph_json)
        export_menu.add_command(label="Export All Results", command=self._export_all_results)
        file_menu.add_cascade(label="Export", menu=export_menu)
        
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        # View menu
        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="View", menu=view_menu)
        view_menu.add_command(label="Clear Results", command=self._clear_results)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self._show_about)
    
    def _browse_econtract_file(self):
        """Browse for e-contract file"""
        
        file_path = filedialog.askopenfilename(
            title="Select E-Contract File",
            filetypes=[
                ("Text files", "*.txt"),
                ("PDF files", "*.pdf"),
                ("Word documents", "*.docx"),
                ("Markdown files", "*.md"),
                ("All files", "*.*")
            ]
        )
        
        if file_path:
            self.current_econtract_path.set(file_path)
    
    def _download_generated_contract(self):
        """Download the generated smart contract"""
        
        if not self.generated_contract_result:
            messagebox.showerror("Error", "No smart contract generated yet")
            return
        
        contract_code = self.generated_contract_result.get('contract_code', '')
        if not contract_code:
            messagebox.showerror("Error", "No contract code available")
            return
        
        # Ask user where to save
        file_path = filedialog.asksaveasfilename(
            title="Save Smart Contract",
            defaultextension=".sol",
            filetypes=[
                ("Solidity files", "*.sol"),
                ("All files", "*.*")
            ],
            initialname=f"generated_contract_{datetime.now().strftime('%Y%m%d_%H%M%S')}.sol"
        )
        
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(contract_code)
                
                # Also save deployment parameters
                deploy_params = self.generated_contract_result.get('deployment_parameters', {})
                if deploy_params:
                    param_file = file_path.replace('.sol', '_deployment_params.json')
                    with open(param_file, 'w', encoding='utf-8') as f:
                        json.dump(deploy_params, f, indent=2)
                
                messagebox.showinfo("Success", f"Contract saved to:\n{file_path}\n\nDeployment parameters saved to:\n{param_file if deploy_params else 'Not available'}")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save contract: {str(e)}")
    
    def _process_econtract(self):
        """Process e-contract in background thread"""
        
        if not self.current_econtract_path.get():
            messagebox.showerror("Error", "Please select an e-contract file first")
            return
        
        def process():
            try:
                self.processing_status.set("Processing e-contract...")
                self._update_progress(10)
                
                # Process the contract
                self.econtract_kg = self.econtract_processor.process_contract_file(
                    self.current_econtract_path.get()
                )
                
                self._update_progress(80)
                
                # Display results
                self._display_econtract_results()
                
                self._update_progress(100)
                self.processing_status.set("E-contract processing completed")
                
            except Exception as e:
                messagebox.showerror("Processing Error", f"Error processing e-contract: {str(e)}")
                self.processing_status.set("Error processing e-contract")
            finally:
                self._update_progress(0)
        
        threading.Thread(target=process, daemon=True).start()
    
    def _generate_smart_contract(self):
        """Generate smart contract from e-contract analysis"""
        
        if not self.econtract_kg:
            messagebox.showerror("Error", "Please process an e-contract first")
            return
        
        def generate():
            try:
                self.processing_status.set("Generating smart contract from e-contract...")
                self._update_progress(10)
                
                # Prepare e-contract analysis data
                econtract_analysis = {
                    'entities': self.econtract_kg.entities,
                    'relationships': self.econtract_kg.relationships,
                    'knowledge_graph': self.econtract_kg,
                    'metadata': self.econtract_kg.metadata
                }
                
                self._update_progress(30)
                
                # Generate smart contract
                generation_result = self.smartcontract_processor.generate_smart_contract_from_econtract(
                    econtract_analysis
                )
                
                self._update_progress(70)
                
                if 'error' in generation_result:
                    messagebox.showerror("Generation Error", generation_result['error'])
                    return
                
                # Display generation results
                self._display_generation_results(generation_result)
                
                # If accuracy is high enough, store as smart contract knowledge graph
                if generation_result.get('deployment_ready', False):
                    self.smartcontract_kg = generation_result.get('knowledge_graph')
                    messagebox.showinfo("Success", 
                        f"Smart contract generated successfully!\n"
                        f"Accuracy Score: {generation_result.get('accuracy_score', 0):.2%}\n"
                        f"Ready for deployment: {generation_result.get('deployment_ready', False)}")
                else:
                    messagebox.showwarning("Generation Warning", 
                        f"Smart contract generated with accuracy: {generation_result.get('accuracy_score', 0):.2%}\n"
                        f"Please review before deployment.\n"
                        f"Recommendations: {', '.join(generation_result.get('recommendations', []))}")
                
                self._update_progress(100)
                self.processing_status.set("Smart contract generation completed")
                
            except Exception as e:
                messagebox.showerror("Generation Error", f"Error generating smart contract: {str(e)}")
                self.processing_status.set("Error generating smart contract")
            finally:
                self._update_progress(0)
        
        threading.Thread(target=generate, daemon=True).start()
    
    def _analyze_generated_contract(self):
        """Analyze the generated smart contract"""
        
        if not self.generated_contract_result:
            messagebox.showerror("Error", "No smart contract generated yet")
            return
        
        contract_code = self.generated_contract_result.get('contract_code', '')
        if not contract_code:
            messagebox.showerror("Error", "No contract code available")
            return
        
        def analyze():
            try:
                self.processing_status.set("Analyzing generated smart contract...")
                self._update_progress(10)
                
                # Process the generated contract through analysis
                self.smartcontract_kg = self.smartcontract_processor.process_contract_content(contract_code)
                
                self._update_progress(80)
                
                # Display results in smart contract tab
                self._display_smartcontract_results()
                
                self._update_progress(100)
                self.processing_status.set("Contract analysis completed")
                
                messagebox.showinfo("Success", "Generated smart contract analyzed successfully!")
                
            except Exception as e:
                messagebox.showerror("Analysis Error", f"Error analyzing contract: {str(e)}")
                self.processing_status.set("Error analyzing contract")
            finally:
                self._update_progress(0)
        
        threading.Thread(target=analyze, daemon=True).start()
    
    def _compare_and_validate(self):
        """Compare e-contract with generated smart contract and validate"""
        
        if not self.econtract_kg:
            messagebox.showerror("Error", "Please process an e-contract first")
            return
        
        if not self.generated_contract_result:
            messagebox.showerror("Error", "Please generate a smart contract first")
            return
        
        def compare():
            try:
                self.processing_status.set("Comparing and validating contracts...")
                self._update_progress(10)
                
                # Ensure we have the smart contract knowledge graph
                if not self.smartcontract_kg:
                    contract_code = self.generated_contract_result.get('contract_code', '')
                    self.smartcontract_kg = self.smartcontract_processor.process_contract_content(contract_code)
                
                self._update_progress(40)
                
                # Run comparison
                self.comparison_results = self.comparator.compare_knowledge_graphs(
                    self.econtract_kg, self.smartcontract_kg
                )
                
                self._update_progress(80)
                
                # Display results
                self._display_comparison_results()
                
                # Show validation summary
                accuracy = self.generated_contract_result.get('accuracy_score', 0)
                similarity = self.comparison_results.get('summary', {}).get('overall_similarity_score', 0)
                
                validation_msg = f"""Contract Validation Results:
                
Generation Accuracy: {accuracy:.2%}
Contract Similarity: {similarity:.2%}
Deployment Ready: {'Yes' if accuracy >= 0.95 else 'No'}

Recommendation: {'Contract is ready for deployment' if accuracy >= 0.95 and similarity >= 0.8 else 'Review contract before deployment'}"""
                
                messagebox.showinfo("Validation Results", validation_msg)
                
                self._update_progress(100)
                self.processing_status.set("Comparison and validation completed")
                
            except Exception as e:
                messagebox.showerror("Comparison Error", f"Error during comparison: {str(e)}")
                self.processing_status.set("Error during comparison")
            finally:
                self._update_progress(0)
        
        threading.Thread(target=compare, daemon=True).start()
    
    def _prepare_deployment(self):
        """Prepare contract for deployment"""
        
        if not self.generated_contract_result:
            messagebox.showerror("Error", "No smart contract generated yet")
            return
        
        accuracy = self.generated_contract_result.get('accuracy_score', 0)
        if accuracy < 0.95:
            if not messagebox.askyesno("Warning", 
                f"Contract accuracy is {accuracy:.2%}, which is below the recommended 95% threshold.\n\nDo you want to proceed with deployment preparation?"):
                return
        
        # Create deployment information window
        deploy_window = tk.Toplevel(self.root)
        deploy_window.title("Contract Deployment Information")
        deploy_window.geometry("600x700")
        deploy_window.transient(self.root)
        deploy_window.grab_set()
        
        # Main frame
        main_frame = ttk.Frame(deploy_window, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        deploy_window.columnconfigure(0, weight=1)
        deploy_window.rowconfigure(0, weight=1)
        
        # Title
        ttk.Label(main_frame, text="Smart Contract Deployment Information", 
                 font=('Arial', 14, 'bold')).grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Deployment info text
        deploy_text = scrolledtext.ScrolledText(main_frame, width=70, height=35, wrap=tk.WORD)
        deploy_text.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        main_frame.rowconfigure(1, weight=1)
        
        # Generate deployment information
        deploy_info = self._generate_deployment_info()
        deploy_text.insert(tk.END, deploy_info)
        deploy_text.config(state=tk.DISABLED)
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=2, column=0, columnspan=2, pady=(10, 0))
        
        ttk.Button(button_frame, text="Save Deployment Package", 
                  command=lambda: self._save_deployment_package()).pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(button_frame, text="Close", 
                  command=deploy_window.destroy).pack(side=tk.LEFT)
    
    def _process_smartcontract(self):
        """Process smart contract in background thread"""
        
        if not self.current_smartcontract_path.get():
            messagebox.showerror("Error", "Please select a smart contract file first")
            return
        
        def process():
            try:
                self.processing_status.set("Processing smart contract...")
                self._update_progress(10)
                
                # Process the contract
                self.smartcontract_kg = self.smartcontract_processor.process_contract_file(
                    self.current_smartcontract_path.get()
                )
                
                self._update_progress(80)
                
                # Display results
                self._display_smartcontract_results()
                
                self._update_progress(100)
                self.processing_status.set("Smart contract processing completed")
                
            except Exception as e:
                messagebox.showerror("Processing Error", f"Error processing smart contract: {str(e)}")
                self.processing_status.set("Error processing smart contract")
            finally:
                self._update_progress(0)
        
        threading.Thread(target=process, daemon=True).start()
    
    def _compare_contracts(self):
        """Compare processed contracts"""
        
        if not self.econtract_kg or not self.smartcontract_kg:
            messagebox.showerror("Error", "Please process both contracts first")
            return
        
        def compare():
            try:
                self.processing_status.set("Comparing contracts...")
                self._update_progress(10)
                
                # Compare the contracts
                self.comparison_results = self.comparator.compare_knowledge_graphs(
                    self.econtract_kg, self.smartcontract_kg
                )
                
                self._update_progress(80)
                
                # Display results
                self._display_comparison_results()
                
                self._update_progress(100)
                self.processing_status.set("Contract comparison completed")
                
            except Exception as e:
                messagebox.showerror("Comparison Error", f"Error comparing contracts: {str(e)}")
                self.processing_status.set("Error comparing contracts")
            finally:
                self._update_progress(0)
        
        threading.Thread(target=compare, daemon=True).start()
    
    def _integrated_analysis(self):
        """Perform integrated analysis of both contracts"""
        
        if not self.current_econtract_path.get() or not self.current_smartcontract_path.get():
            messagebox.showerror("Error", "Please select both contract files first")
            return
        
        def analyze():
            try:
                self.processing_status.set("Performing integrated analysis...")
                self._update_progress(10)
                
                # Read contract files
                econtract_text = FileHandler.read_text_file(self.current_econtract_path.get())
                smartcontract_code = FileHandler.read_text_file(self.current_smartcontract_path.get())
                
                self._update_progress(20)
                
                # Perform integrated analysis
                self.comparison_results = self.comparator.integrated_contract_analysis(
                    econtract_text, smartcontract_code
                )
                
                self._update_progress(80)
                
                # Update knowledge graphs
                comparison_data = self.comparator.comparison_results
                latest_comparison = list(comparison_data.keys())[-1]
                
                self.econtract_kg = comparison_data[latest_comparison]['econtract_graph']
                self.smartcontract_kg = comparison_data[latest_comparison]['smartcontract_graph']
                
                # Display all results
                self._display_econtract_results()
                self._display_smartcontract_results()
                self._display_comparison_results()
                
                self._update_progress(100)
                self.processing_status.set("Integrated analysis completed")
                
            except Exception as e:
                messagebox.showerror("Analysis Error", f"Error in integrated analysis: {str(e)}")
                self.processing_status.set("Error in integrated analysis")
            finally:
                self._update_progress(0)
        
        threading.Thread(target=analyze, daemon=True).start()
    
    def _display_econtract_results(self):
        """Display e-contract analysis results"""
        
        if not self.econtract_kg:
            return
        
        # Get statistics and summary
        stats = self.econtract_kg.get_statistics()
        
        # Build display text
        result_text = "=== E-CONTRACT ANALYSIS RESULTS ===\n\n"
        
        # Basic statistics
        result_text += "KNOWLEDGE GRAPH STATISTICS:\n"
        result_text += f"Total Entities: {stats['basic_metrics']['total_entities']}\n"
        result_text += f"Total Relationships: {stats['basic_metrics']['total_relationships']}\n"
        result_text += f"Graph Density: {stats['basic_metrics']['graph_density']:.3f}\n"
        result_text += f"Connected: {'Yes' if stats['basic_metrics']['is_connected'] else 'No'}\n\n"
        
        # Entity types distribution
        if 'entity_types' in stats:
            result_text += "ENTITY TYPES DISTRIBUTION:\n"
            for entity_type, count in stats['entity_types'].items():
                result_text += f"  {entity_type}: {count}\n"
            result_text += "\n"
        
        # Relationship types distribution
        if 'relationship_types' in stats:
            result_text += "RELATIONSHIP TYPES DISTRIBUTION:\n"
            for rel_type, count in stats['relationship_types'].items():
                result_text += f"  {rel_type}: {count}\n"
            result_text += "\n"
        
        # Key entities
        result_text += "KEY ENTITIES:\n"
        entity_count = 0
        for entity_id, entity_data in self.econtract_kg.entities.items():
            if entity_count >= 10:  # Limit display
                break
            result_text += f"  {entity_data.get('text', 'Unknown')} ({entity_data.get('type', 'Unknown')})\n"
            entity_count += 1
        
        if len(self.econtract_kg.entities) > 10:
            result_text += f"  ... and {len(self.econtract_kg.entities) - 10} more entities\n"
        
        # Display in text widget
        self.econtract_text.delete(1.0, tk.END)
        self.econtract_text.insert(tk.END, result_text)
        
        # Switch to e-contract tab
        self.results_notebook.select(self.econtract_tab)
    
    def _display_smartcontract_results(self):
        """Display smart contract analysis results"""
        
        if not self.smartcontract_kg:
            return
        
        # Get statistics
        stats = self.smartcontract_kg.get_statistics()
        
        # Build display text
        result_text = "=== SMART CONTRACT ANALYSIS RESULTS ===\n\n"
        
        # Basic statistics
        result_text += "KNOWLEDGE GRAPH STATISTICS:\n"
        result_text += f"Total Entities: {stats['basic_metrics']['total_entities']}\n"
        result_text += f"Total Relationships: {stats['basic_metrics']['total_relationships']}\n"
        result_text += f"Graph Density: {stats['basic_metrics']['graph_density']:.3f}\n"
        result_text += f"Connected: {'Yes' if stats['basic_metrics']['is_connected'] else 'No'}\n\n"
        
        # Entity types distribution
        if 'entity_types' in stats:
            result_text += "ENTITY TYPES DISTRIBUTION:\n"
            for entity_type, count in stats['entity_types'].items():
                result_text += f"  {entity_type}: {count}\n"
            result_text += "\n"
        
        # Relationship types distribution
        if 'relationship_types' in stats:
            result_text += "RELATIONSHIP TYPES DISTRIBUTION:\n"
            for rel_type, count in stats['relationship_types'].items():
                result_text += f"  {rel_type}: {count}\n"
            result_text += "\n"
        
        # Contract structure
        result_text += "SMART CONTRACT STRUCTURE:\n"
        entity_categories = {}
        for entity_data in self.smartcontract_kg.entities.values():
            category = entity_data.get('category', 'OTHER')
            entity_categories[category] = entity_categories.get(category, 0) + 1
        
        for category, count in entity_categories.items():
            result_text += f"  {category}: {count}\n"
        result_text += "\n"
        
        # Key entities
        result_text += "KEY ENTITIES:\n"
        entity_count = 0
        for entity_id, entity_data in self.smartcontract_kg.entities.items():
            if entity_count >= 10:  # Limit display
                break
            result_text += f"  {entity_data.get('text', 'Unknown')} ({entity_data.get('type', 'Unknown')})\n"
            entity_count += 1
        
        if len(self.smartcontract_kg.entities) > 10:
            result_text += f"  ... and {len(self.smartcontract_kg.entities) - 10} more entities\n"
        
        # Display in text widget
        self.smartcontract_text.delete(1.0, tk.END)
        self.smartcontract_text.insert(tk.END, result_text)
        
        # Switch to smart contract tab
        self.results_notebook.select(self.smartcontract_tab)
    
    def _display_comparison_results(self):
        """Display contract comparison results"""
        
        if not self.comparison_results:
            return
        
        # Build display text
        result_text = "=== CONTRACT COMPARISON RESULTS ===\n\n"
        
        # Summary
        summary = self.comparison_results.get('summary', {})
        result_text += "COMPARISON SUMMARY:\n"
        result_text += f"Overall Similarity Score: {summary.get('overall_similarity_score', 0):.3f}\n"
        result_text += f"Entity Matches: {summary.get('total_entity_matches', 0)}\n"
        result_text += f"Relationship Matches: {summary.get('total_relation_matches', 0)}\n"
        result_text += f"E-Contract Entity Coverage: {summary.get('entity_coverage_econtract', 0):.1%}\n"
        result_text += f"Smart Contract Entity Coverage: {summary.get('entity_coverage_smartcontract', 0):.1%}\n"
        result_text += f"E-Contract Relation Coverage: {summary.get('relation_coverage_econtract', 0):.1%}\n"
        result_text += f"Smart Contract Relation Coverage: {summary.get('relation_coverage_smartcontract', 0):.1%}\n\n"
        
        # Compliance Assessment
        compliance = self.comparison_results.get('compliance_assessment', {})
        result_text += "COMPLIANCE ASSESSMENT:\n"
        result_text += f"Overall Compliance Score: {compliance.get('overall_compliance_score', 0):.3f}\n"
        result_text += f"Compliance Level: {compliance.get('compliance_level', 'Unknown')}\n"
        result_text += f"Is Compliant: {'Yes' if compliance.get('is_compliant', False) else 'No'}\n"
        
        if compliance.get('compliance_issues'):
            result_text += "Compliance Issues:\n"
            for issue in compliance['compliance_issues']:
                result_text += f"  - {issue}\n"
        result_text += "\n"
        
        # Recommendations
        recommendations = self.comparison_results.get('recommendations', [])
        if recommendations:
            result_text += "RECOMMENDATIONS:\n"
            for i, recommendation in enumerate(recommendations, 1):
                result_text += f"{i}. {recommendation}\n"
            result_text += "\n"
        
        # Entity Analysis
        entity_analysis = self.comparison_results.get('entity_analysis', {})
        match_quality = entity_analysis.get('match_quality_distribution', {})
        if match_quality:
            result_text += "ENTITY MATCH QUALITY DISTRIBUTION:\n"
            for quality, count in match_quality.items():
                result_text += f"  {quality.replace('_', ' ').title()}: {count}\n"
            result_text += "\n"
        
        # Top Entity Matches
        entity_matches = entity_analysis.get('matches', [])
        if entity_matches:
            result_text += "TOP ENTITY MATCHES:\n"
            # Sort by similarity score and show top 10
            sorted_matches = sorted(entity_matches, key=lambda x: x.get('similarity_score', 0), reverse=True)
            for i, match in enumerate(sorted_matches[:10], 1):
                e_entity = match['econtract_entity']
                s_entity = match['smartcontract_entity']
                score = match.get('similarity_score', 0)
                result_text += f"{i}. {e_entity.get('text', 'Unknown')} ↔ {s_entity.get('text', 'Unknown')} (Score: {score:.3f})\n"
            
            if len(sorted_matches) > 10:
                result_text += f"  ... and {len(sorted_matches) - 10} more matches\n"
        
        # Enhanced insights (if available)
        if 'detailed_insights' in self.comparison_results:
            insights = self.comparison_results['detailed_insights']
            
            result_text += "\nDETAILED INSIGHTS:\n"
            
            # Implementation completeness
            completeness = insights.get('implementation_completeness', {})
            result_text += f"Implementation Completeness: {completeness.get('completeness_level', 'Unknown')}\n"
            result_text += f"Production Ready: {'Yes' if completeness.get('is_production_ready', False) else 'No'}\n"
            
            # Semantic gaps
            gaps = insights.get('semantic_gaps', [])
            if gaps:
                result_text += "Semantic Gaps:\n"
                for gap in gaps:
                    result_text += f"  - {gap}\n"
            
            # Risk assessment
            risks = insights.get('risk_assessment', [])
            if risks:
                result_text += "Implementation Risks:\n"
                for risk in risks:
                    result_text += f"  - {risk.get('type', 'Unknown')}: {risk.get('description', 'No description')} (Severity: {risk.get('severity', 'Unknown')})\n"
        
        # Display in text widget
        self.comparison_text.delete(1.0, tk.END)
        self.comparison_text.insert(tk.END, result_text)
        
        # Switch to comparison tab
        self.results_notebook.select(self.comparison_tab)
    
    def _display_generation_results(self, generation_result):
        """Display smart contract generation results"""
        
        # Store the generation result for export
        self.generated_contract_result = generation_result
        
        # Build display text
        result_text = "=== SMART CONTRACT GENERATION RESULTS ===\n\n"
        
        # Generation Summary
        result_text += "GENERATION SUMMARY:\n"
        result_text += f"Contract Type: {generation_result.get('contract_type', 'Unknown')}\n"
        result_text += f"Accuracy Score: {generation_result.get('accuracy_score', 0):.2%}\n"
        result_text += f"Deployment Ready: {'Yes' if generation_result.get('deployment_ready', False) else 'No'}\n"
        result_text += f"Generated At: {generation_result.get('generated_at', 'Unknown')}\n"
        result_text += f"Source Hash: {generation_result.get('source_hash', 'Unknown')}\n\n"
        
        # Validation Results
        validation = generation_result.get('validation_results', {})
        result_text += "VALIDATION RESULTS:\n"
        result_text += f"Overall Accuracy: {validation.get('overall_accuracy', 0):.2%}\n"
        result_text += f"Is Accurate: {'Yes' if validation.get('is_accurate', False) else 'No'}\n"
        
        # Individual validation scores
        for check_name, check_result in validation.items():
            if isinstance(check_result, dict) and 'score' in check_result:
                result_text += f"  {check_name.replace('_', ' ').title()}: {check_result['score']:.2%}\n"
                if check_result.get('issues'):
                    for issue in check_result['issues']:
                        result_text += f"    - {issue}\n"
        
        result_text += "\n"
        
        # Security Analysis
        security = validation.get('security_analysis', {})
        if security:
            result_text += "SECURITY ANALYSIS:\n"
            result_text += f"Security Score: {security.get('score', 0):.2%}\n"
            result_text += f"Is Secure: {'Yes' if security.get('secure', False) else 'No'}\n"
            if security.get('issues'):
                result_text += "Security Issues:\n"
                for issue in security['issues']:
                    result_text += f"  - {issue}\n"
            result_text += "\n"
        
        # Gas Estimation
        gas_info = generation_result.get('gas_estimation', {})
        if gas_info:
            result_text += "GAS ESTIMATION:\n"
            result_text += f"Deployment Gas: {gas_info.get('deployment', 0):,}\n"
            result_text += f"Function Call Gas: {gas_info.get('function_call', 0):,}\n"
            result_text += f"Storage Write Gas: {gas_info.get('storage_write', 0):,}\n"
            result_text += f"Storage Read Gas: {gas_info.get('storage_read', 0):,}\n\n"
        
        # Recommendations
        recommendations = generation_result.get('recommendations', [])
        if recommendations:
            result_text += "RECOMMENDATIONS:\n"
            for i, recommendation in enumerate(recommendations, 1):
                result_text += f"{i}. {recommendation}\n"
            result_text += "\n"
        
        # Contract Code Preview (first 1000 characters)
        contract_code = generation_result.get('contract_code', '')
        if contract_code:
            result_text += "CONTRACT CODE PREVIEW:\n"
            result_text += "=" * 50 + "\n"
            preview = contract_code[:1000]
            if len(contract_code) > 1000:
                preview += "\n... (truncated) ..."
            result_text += preview + "\n"
            result_text += "=" * 50 + "\n\n"
        
        # Deployment Parameters
        deploy_params = generation_result.get('deployment_parameters', {})
        if deploy_params:
            constructor_params = deploy_params.get('constructor_params', {})
            result_text += "DEPLOYMENT PARAMETERS:\n"
            for param, value in constructor_params.items():
                result_text += f"  {param}: {value}\n"
            result_text += f"Gas Limit: {deploy_params.get('gas_limit', 'Unknown'):,}\n"
            result_text += f"Gas Price: {deploy_params.get('gas_price', 'Unknown'):,} wei\n"
        
        # Display in smart contract tab
        self.smartcontract_text.delete(1.0, tk.END)
        self.smartcontract_text.insert(tk.END, result_text)
        
        # Save contract code to file
        if contract_code:
            try:
                output_file = os.path.join(Config.OUTPUTS_DIR, "generated_contract.sol")
                os.makedirs(Config.OUTPUTS_DIR, exist_ok=True)
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(contract_code)
                result_text += f"\nContract saved to: {output_file}\n"
                self.smartcontract_text.insert(tk.END, f"\nContract saved to: {output_file}\n")
            except Exception as e:
                result_text += f"\nError saving contract: {str(e)}\n"
        
        # Update GUI elements
        contract_type = generation_result.get('contract_type', 'Unknown')
        accuracy = generation_result.get('accuracy_score', 0)
        self.generated_contract_info.set(f"{contract_type} - Accuracy: {accuracy:.1%} - Generated: {datetime.now().strftime('%H:%M:%S')}")
        
        # Enable download button
        self.download_button.config(state="normal")
        
        # Switch to smart contract tab
        self.results_notebook.select(self.smartcontract_tab)
    
    def _show_econtract_graph(self):
        """Show e-contract knowledge graph visualization"""
        if not self.econtract_kg:
            messagebox.showwarning("Warning", "No e-contract processed yet")
            return
        
        try:
            output_path = os.path.join(Config.OUTPUTS_DIR, "econtract_graph.png")
            success = self.econtract_kg.visualize(output_path)
            
            if success:
                self._display_visualization_info("E-Contract Knowledge Graph", output_path)
            else:
                messagebox.showerror("Error", "Failed to generate visualization")
        
        except Exception as e:
            messagebox.showerror("Visualization Error", f"Error creating visualization: {str(e)}")
    
    def _show_smartcontract_graph(self):
        """Show smart contract knowledge graph visualization"""
        if not self.smartcontract_kg:
            messagebox.showwarning("Warning", "No smart contract processed yet")
            return
        
        try:
            output_path = os.path.join(Config.OUTPUTS_DIR, "smartcontract_graph.png")
            success = self.smartcontract_kg.visualize(output_path)
            
            if success:
                self._display_visualization_info("Smart Contract Knowledge Graph", output_path)
            else:
                messagebox.showerror("Error", "Failed to generate visualization")
        
        except Exception as e:
            messagebox.showerror("Visualization Error", f"Error creating visualization: {str(e)}")
    
    def _show_comparison_graph(self):
        """Show comparison visualization"""
        if not self.comparison_results:
            messagebox.showwarning("Warning", "No comparison results available")
            return
        
        self._display_visualization_info("Comparison Analysis", None)
    
    def _display_visualization_info(self, title: str, image_path: Optional[str]):
        """Display visualization information"""
        
        viz_text = f"=== {title.upper()} ===\n\n"
        
        if image_path and os.path.exists(image_path):
            viz_text += f"Visualization saved to: {image_path}\n\n"
            viz_text += "The knowledge graph has been visualized and saved as an image file.\n"
            viz_text += "You can view the image using your default image viewer.\n\n"
        
        if self.econtract_kg:
            viz_text += "E-CONTRACT GRAPH INFORMATION:\n"
            e_stats = self.econtract_kg.get_statistics()
            viz_text += f"  Entities: {e_stats['basic_metrics']['total_entities']}\n"
            viz_text += f"  Relationships: {e_stats['basic_metrics']['total_relationships']}\n"
            viz_text += f"  Density: {e_stats['basic_metrics']['graph_density']:.3f}\n\n"
        
        if self.smartcontract_kg:
            viz_text += "SMART CONTRACT GRAPH INFORMATION:\n"
            s_stats = self.smartcontract_kg.get_statistics()
            viz_text += f"  Entities: {s_stats['basic_metrics']['total_entities']}\n"
            viz_text += f"  Relationships: {s_stats['basic_metrics']['total_relationships']}\n"
            viz_text += f"  Density: {s_stats['basic_metrics']['graph_density']:.3f}\n\n"
        
        if self.comparison_results:
            viz_text += "COMPARISON INFORMATION:\n"
            summary = self.comparison_results.get('summary', {})
            viz_text += f"  Overall Similarity: {summary.get('overall_similarity_score', 0):.3f}\n"
            viz_text += f"  Entity Matches: {summary.get('total_entity_matches', 0)}\n"
            viz_text += f"  Relationship Matches: {summary.get('total_relation_matches', 0)}\n"
        
        self.visualization_text.delete(1.0, tk.END)
        self.visualization_text.insert(tk.END, viz_text)
        
        # Switch to visualization tab
        self.results_notebook.select(self.visualization_tab)
    
    def _update_progress(self, value):
        """Update progress bar"""
        self.progress_var.set(value)
        self.root.update_idletasks()
    
    def _new_analysis(self):
        """Start a new analysis"""
        result = messagebox.askyesno("New Analysis", "Clear all current results and start a new analysis?")
        if result:
            self._clear_results()
            self.current_econtract_path.set("")
            self.current_smartcontract_path.set("")
            self.processing_status.set("Ready for new analysis")
    
    def _clear_results(self):
        """Clear all result displays"""
        self.econtract_text.delete(1.0, tk.END)
        self.smartcontract_text.delete(1.0, tk.END)
        self.comparison_text.delete(1.0, tk.END)
        self.visualization_text.delete(1.0, tk.END)
        
        self.econtract_kg = None
        self.smartcontract_kg = None
        self.comparison_results = None
        
        self.processing_status.set("Results cleared")
    
    def _export_results(self):
        """Export analysis results"""
        if not any([self.econtract_kg, self.smartcontract_kg, self.comparison_results]):
            messagebox.showwarning("Warning", "No results to export")
            return
        
        output_dir = filedialog.askdirectory(title="Select Export Directory")
        if not output_dir:
            return
        
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            export_dir = os.path.join(output_dir, f"contract_analysis_{timestamp}")
            os.makedirs(export_dir, exist_ok=True)
            
            exported_files = []
            
            # Export e-contract results
            if self.econtract_kg:
                e_results = self.econtract_kg.export_to_formats(
                    os.path.join(export_dir, "econtract_kg")
                )
                exported_files.extend([f"econtract_kg.{fmt}" for fmt, success in e_results.items() if success])
            
            # Export smart contract results
            if self.smartcontract_kg:
                s_results = self.smartcontract_kg.export_to_formats(
                    os.path.join(export_dir, "smartcontract_kg")
                )
                exported_files.extend([f"smartcontract_kg.{fmt}" for fmt, success in s_results.items() if success])
            
            # Export comparison results
            if self.comparison_results:
                comparison_path = os.path.join(export_dir, "comparison_results.json")
                if FileHandler.write_json_file(comparison_path, self.comparison_results):
                    exported_files.append("comparison_results.json")
            
            # Export visualizations
            if self.econtract_kg:
                viz_path = os.path.join(export_dir, "econtract_visualization.png")
                if self.econtract_kg.visualize(viz_path):
                    exported_files.append("econtract_visualization.png")
            
            if self.smartcontract_kg:
                viz_path = os.path.join(export_dir, "smartcontract_visualization.png")
                if self.smartcontract_kg.visualize(viz_path):
                    exported_files.append("smartcontract_visualization.png")
            
            messagebox.showinfo("Export Complete", 
                              f"Results exported to: {export_dir}\n\nExported files:\n" + 
                              "\n".join(exported_files))
            
        except Exception as e:
            messagebox.showerror("Export Error", f"Error exporting results: {str(e)}")
    
    def _export_econtract_results(self):
        """Export e-contract analysis results"""
        if not self.econtract_kg:
            messagebox.showerror("Error", "No e-contract results to export")
            return
        
        export_dir = filedialog.askdirectory(title="Select Export Directory")
        if not export_dir:
            return
        
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # Export knowledge graph
            kg_path = os.path.join(export_dir, f"econtract_kg_{timestamp}")
            self.econtract_kg.export_to_formats(kg_path)
            
            # Export statistics
            stats_path = os.path.join(export_dir, f"econtract_stats_{timestamp}.json")
            with open(stats_path, 'w') as f:
                json.dump(self.econtract_kg.get_statistics(), f, indent=2)
            
            # Export visualization
            viz_path = os.path.join(export_dir, f"econtract_visualization_{timestamp}.png")
            self.econtract_kg.visualize(viz_path)
            
            messagebox.showinfo("Export Complete", f"E-contract results exported to: {export_dir}")
            
        except Exception as e:
            messagebox.showerror("Export Error", f"Error exporting e-contract results: {str(e)}")
    
    def _export_smartcontract_results(self):
        """Export smart contract analysis results"""
        if not self.smartcontract_kg:
            messagebox.showerror("Error", "No smart contract results to export")
            return
        
        export_dir = filedialog.askdirectory(title="Select Export Directory")
        if not export_dir:
            return
        
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # Export knowledge graph
            kg_path = os.path.join(export_dir, f"smartcontract_kg_{timestamp}")
            self.smartcontract_kg.export_to_formats(kg_path)
            
            # Export statistics
            stats_path = os.path.join(export_dir, f"smartcontract_stats_{timestamp}.json")
            with open(stats_path, 'w') as f:
                json.dump(self.smartcontract_kg.get_statistics(), f, indent=2)
            
            # Export visualization
            viz_path = os.path.join(export_dir, f"smartcontract_visualization_{timestamp}.png")
            self.smartcontract_kg.visualize(viz_path)
            
            messagebox.showinfo("Export Complete", f"Smart contract results exported to: {export_dir}")
            
        except Exception as e:
            messagebox.showerror("Export Error", f"Error exporting smart contract results: {str(e)}")
    
    def _export_generated_contract(self):
        """Export generated smart contract code"""
        if not hasattr(self, 'generated_contract_result') or not self.generated_contract_result:
            messagebox.showerror("Error", "No generated contract to export")
            return
        
        file_path = filedialog.asksaveasfilename(
            title="Export Generated Smart Contract",
            defaultextension=".sol",
            filetypes=[("Solidity files", "*.sol"), ("All files", "*.*")]
        )
        
        if not file_path:
            return
        
        try:
            # Export the contract code
            with open(file_path, 'w') as f:
                f.write(self.generated_contract_result.get('contract_code', ''))
            
            # Also export deployment parameters and validation results
            base_path = file_path.rsplit('.', 1)[0]
            
            # Export deployment parameters
            deploy_path = f"{base_path}_deployment.json"
            with open(deploy_path, 'w') as f:
                json.dump({
                    'deployment_parameters': self.generated_contract_result.get('deployment_parameters', {}),
                    'gas_estimation': self.generated_contract_result.get('gas_estimation', {}),
                    'accuracy_score': self.generated_contract_result.get('accuracy_score', 0),
                    'deployment_ready': self.generated_contract_result.get('deployment_ready', False)
                }, f, indent=2)
            
            # Export validation results
            validation_path = f"{base_path}_validation.json"
            with open(validation_path, 'w') as f:
                json.dump(self.generated_contract_result.get('validation_results', {}), f, indent=2)
            
            messagebox.showinfo("Export Complete", 
                f"Generated contract exported:\n"
                f"- Contract: {file_path}\n"
                f"- Deployment: {deploy_path}\n"
                f"- Validation: {validation_path}")
            
        except Exception as e:
            messagebox.showerror("Export Error", f"Error exporting generated contract: {str(e)}")
    
    def _export_comparison_results(self):
        """Export contract comparison results"""
        if not self.comparison_results:
            messagebox.showerror("Error", "No comparison results to export")
            return
        
        export_dir = filedialog.askdirectory(title="Select Export Directory")
        if not export_dir:
            return
        
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # Export comparison results as JSON
            results_path = os.path.join(export_dir, f"comparison_results_{timestamp}.json")
            with open(results_path, 'w') as f:
                json.dump(self.comparison_results, f, indent=2, default=str)
            
            # Export comparison summary as CSV
            csv_path = os.path.join(export_dir, f"comparison_summary_{timestamp}.csv")
            summary = self.comparison_results.get('summary', {})
            
            with open(csv_path, 'w') as f:
                f.write("Metric,Value\n")
                for key, value in summary.items():
                    f.write(f"{key},{value}\n")
            
            # Export differences as text report
            report_path = os.path.join(export_dir, f"comparison_report_{timestamp}.txt")
            with open(report_path, 'w') as f:
                f.write("CONTRACT COMPARISON REPORT\n")
                f.write("=" * 50 + "\n\n")
                
                f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                
                if 'summary' in self.comparison_results:
                    f.write("SUMMARY\n")
                    f.write("-" * 20 + "\n")
                    for key, value in summary.items():
                        f.write(f"{key}: {value}\n")
                    f.write("\n")
                
                if 'differences' in self.comparison_results:
                    f.write("IDENTIFIED DIFFERENCES\n")
                    f.write("-" * 30 + "\n")
                    differences = self.comparison_results['differences']
                    for i, diff in enumerate(differences[:10], 1):  # Limit to first 10
                        f.write(f"{i}. {diff}\n")
                    f.write("\n")
                
                if 'recommendations' in self.comparison_results:
                    f.write("RECOMMENDATIONS\n")
                    f.write("-" * 20 + "\n")
                    for rec in self.comparison_results['recommendations']:
                        f.write(f"• {rec}\n")
            
            messagebox.showinfo("Export Complete", f"Comparison results exported to: {export_dir}")
            
        except Exception as e:
            messagebox.showerror("Export Error", f"Error exporting comparison results: {str(e)}")
    
    def _export_knowledge_graph(self):
        """Export knowledge graphs in GraphML format"""
        if not self.econtract_kg and not self.smartcontract_kg:
            messagebox.showerror("Error", "No knowledge graphs to export")
            return
        
        export_dir = filedialog.askdirectory(title="Select Export Directory")
        if not export_dir:
            return
        
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            exported_files = []
            
            if self.econtract_kg:
                e_path = os.path.join(export_dir, f"econtract_graph_{timestamp}")
                results = self.econtract_kg.export_to_formats(e_path)
                if results.get('graphml'):
                    exported_files.append(f"econtract_graph_{timestamp}.graphml")
            
            if self.smartcontract_kg:
                s_path = os.path.join(export_dir, f"smartcontract_graph_{timestamp}")
                results = self.smartcontract_kg.export_to_formats(s_path)
                if results.get('graphml'):
                    exported_files.append(f"smartcontract_graph_{timestamp}.graphml")
            
            if exported_files:
                messagebox.showinfo("Export Complete", 
                    f"Knowledge graphs exported to: {export_dir}\n\n"
                    f"Files: {', '.join(exported_files)}")
            else:
                messagebox.showwarning("Export Warning", "No files were exported successfully")
            
        except Exception as e:
            messagebox.showerror("Export Error", f"Error exporting knowledge graphs: {str(e)}")
    
    def _export_knowledge_graph_json(self):
        """Export knowledge graphs in JSON format"""
        if not self.econtract_kg and not self.smartcontract_kg:
            messagebox.showerror("Error", "No knowledge graphs to export")
            return
        
        export_dir = filedialog.askdirectory(title="Select Export Directory")
        if not export_dir:
            return
        
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            exported_files = []
            
            if self.econtract_kg:
                e_path = os.path.join(export_dir, f"econtract_graph_{timestamp}")
                results = self.econtract_kg.export_to_formats(e_path)
                if results.get('json'):
                    exported_files.append(f"econtract_graph_{timestamp}.json")
            
            if self.smartcontract_kg:
                s_path = os.path.join(export_dir, f"smartcontract_graph_{timestamp}")
                results = self.smartcontract_kg.export_to_formats(s_path)
                if results.get('json'):
                    exported_files.append(f"smartcontract_graph_{timestamp}.json")
            
            if exported_files:
                messagebox.showinfo("Export Complete", 
                    f"Knowledge graphs exported to: {export_dir}\n\n"
                    f"Files: {', '.join(exported_files)}")
            else:
                messagebox.showwarning("Export Warning", "No files were exported successfully")
            
        except Exception as e:
            messagebox.showerror("Export Error", f"Error exporting knowledge graphs: {str(e)}")
    
    def _export_all_results(self):
        """Export all available results to a single directory"""
        export_dir = filedialog.askdirectory(title="Select Export Directory")
        if not export_dir:
            return
        
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            results_dir = os.path.join(export_dir, f"contract_analysis_results_{timestamp}")
            os.makedirs(results_dir, exist_ok=True)
            
            exported_items = []
            
            # Export e-contract results
            if self.econtract_kg:
                econtract_dir = os.path.join(results_dir, "econtract")
                os.makedirs(econtract_dir, exist_ok=True)
                
                # Knowledge graph
                kg_path = os.path.join(econtract_dir, "knowledge_graph")
                self.econtract_kg.export_to_formats(kg_path)
                
                # Statistics
                stats_path = os.path.join(econtract_dir, "statistics.json")
                with open(stats_path, 'w') as f:
                    json.dump(self.econtract_kg.get_statistics(), f, indent=2)
                
                # Visualization
                viz_path = os.path.join(econtract_dir, "visualization.png")
                self.econtract_kg.visualize(viz_path)
                
                exported_items.append("E-contract analysis results")
            
            # Export smart contract results
            if self.smartcontract_kg:
                smartcontract_dir = os.path.join(results_dir, "smartcontract")
                os.makedirs(smartcontract_dir, exist_ok=True)
                
                # Knowledge graph
                kg_path = os.path.join(smartcontract_dir, "knowledge_graph")
                self.smartcontract_kg.export_to_formats(kg_path)
                
                # Statistics
                stats_path = os.path.join(smartcontract_dir, "statistics.json")
                with open(stats_path, 'w') as f:
                    json.dump(self.smartcontract_kg.get_statistics(), f, indent=2)
                
                # Visualization
                viz_path = os.path.join(smartcontract_dir, "visualization.png")
                self.smartcontract_kg.visualize(viz_path)
                
                exported_items.append("Smart contract analysis results")
            
            # Export generated contract
            if hasattr(self, 'generated_contract_result') and self.generated_contract_result:
                generated_dir = os.path.join(results_dir, "generated_contract")
                os.makedirs(generated_dir, exist_ok=True)
                
                # Contract code
                contract_path = os.path.join(generated_dir, "contract.sol")
                with open(contract_path, 'w') as f:
                    f.write(self.generated_contract_result.get('contract_code', ''))
                
                # Deployment parameters
                deploy_path = os.path.join(generated_dir, "deployment.json")
                with open(deploy_path, 'w') as f:
                    json.dump({
                        'deployment_parameters': self.generated_contract_result.get('deployment_parameters', {}),
                        'gas_estimation': self.generated_contract_result.get('gas_estimation', {}),
                        'accuracy_score': self.generated_contract_result.get('accuracy_score', 0),
                        'deployment_ready': self.generated_contract_result.get('deployment_ready', False)
                    }, f, indent=2)
                
                # Validation results
                validation_path = os.path.join(generated_dir, "validation.json")
                with open(validation_path, 'w') as f:
                    json.dump(self.generated_contract_result.get('validation_results', {}), f, indent=2)
                
                exported_items.append("Generated smart contract")
            
            # Export comparison results
            if self.comparison_results:
                comparison_dir = os.path.join(results_dir, "comparison")
                os.makedirs(comparison_dir, exist_ok=True)
                
                # Full results
                results_path = os.path.join(comparison_dir, "results.json")
                with open(results_path, 'w') as f:
                    json.dump(self.comparison_results, f, indent=2, default=str)
                
                # Summary CSV
                csv_path = os.path.join(comparison_dir, "summary.csv")
                summary = self.comparison_results.get('summary', {})
                with open(csv_path, 'w') as f:
                    f.write("Metric,Value\n")
                    for key, value in summary.items():
                        f.write(f"{key},{value}\n")
                
                exported_items.append("Comparison results")
            
            # Create a summary report
            summary_path = os.path.join(results_dir, "export_summary.txt")
            with open(summary_path, 'w') as f:
                f.write("CONTRACT ANALYSIS EXPORT SUMMARY\n")
                f.write("=" * 50 + "\n\n")
                f.write(f"Export Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Export Directory: {results_dir}\n\n")
                f.write("Exported Items:\n")
                for item in exported_items:
                    f.write(f"• {item}\n")
                f.write(f"\nTotal Items Exported: {len(exported_items)}\n")
            
            if exported_items:
                messagebox.showinfo("Export Complete", 
                    f"All results exported to: {results_dir}\n\n"
                    f"Exported items:\n" + "\n".join(f"• {item}" for item in exported_items))
            else:
                messagebox.showwarning("Export Warning", "No results available to export")
            
        except Exception as e:
            messagebox.showerror("Export Error", f"Error exporting all results: {str(e)}")
    
    def _show_about(self):
        """Show about dialog"""
        about_text = """E-Contract and Smart Contract Analysis System

This system implements advanced techniques for analyzing and comparing 
e-contracts with smart contracts using:

• Natural Language Processing (NLP)
• Abstract Syntax Tree (AST) analysis
• Knowledge graph construction
• Dependency parsing
• Automated comparison algorithms

Developed based on research in contract analysis and blockchain technology.

The system helps ensure that smart contracts faithfully implement 
the specifications outlined in e-contracts, addressing challenges in:
- Complexity discrepancy
- Regulatory compliance  
- Semantic alignment

Version 1.0
"""
        messagebox.showinfo("About", about_text)
    
    def run(self):
        """Start the GUI application"""
        # Ensure output directories exist
        Config.create_directories()
        
        # Center the window
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (Config.WINDOW_WIDTH // 2)
        y = (self.root.winfo_screenheight() // 2) - (Config.WINDOW_HEIGHT // 2)
        self.root.geometry(f"{Config.WINDOW_WIDTH}x{Config.WINDOW_HEIGHT}+{x}+{y}")
        
        self.root.mainloop()
    
    def _generate_deployment_info(self):
        """Generate comprehensive deployment information"""
        
        if not self.generated_contract_result:
            return "No contract generated yet."
        
        info_lines = []
        
        info_lines.append("SMART CONTRACT DEPLOYMENT PACKAGE")
        info_lines.append("=" * 50)
        info_lines.append("")
        
        # Contract Information
        info_lines.append("CONTRACT INFORMATION:")
        info_lines.append(f"Type: {self.generated_contract_result.get('contract_type', 'Unknown')}")
        info_lines.append(f"Accuracy Score: {self.generated_contract_result.get('accuracy_score', 0):.2%}")
        info_lines.append(f"Generated: {self.generated_contract_result.get('generated_at', 'Unknown')}")
        info_lines.append(f"Deployment Ready: {'Yes' if self.generated_contract_result.get('deployment_ready', False) else 'No'}")
        info_lines.append("")
        
        # Deployment Parameters
        deploy_params = self.generated_contract_result.get('deployment_parameters', {})
        if deploy_params:
            info_lines.append("DEPLOYMENT PARAMETERS:")
            constructor_params = deploy_params.get('constructor_params', {})
            for param, value in constructor_params.items():
                info_lines.append(f"  {param}: {value}")
            info_lines.append(f"Gas Limit: {deploy_params.get('gas_limit', 'Unknown'):,}")
            info_lines.append(f"Gas Price: {deploy_params.get('gas_price', 'Unknown'):,} wei")
            info_lines.append("")
        
        # Gas Estimation
        gas_info = self.generated_contract_result.get('gas_estimation', {})
        if gas_info:
            info_lines.append("GAS COST ESTIMATES:")
            info_lines.append(f"Deployment: ~{gas_info.get('deployment', 0):,} gas")
            info_lines.append(f"Function Calls: ~{gas_info.get('function_call', 0):,} gas")
            info_lines.append(f"Storage Operations: {gas_info.get('storage_write', 0):,} gas (write), {gas_info.get('storage_read', 0):,} gas (read)")
            info_lines.append("")
        
        # Security Information
        validation = self.generated_contract_result.get('validation_results', {})
        security = validation.get('security_analysis', {})
        if security:
            info_lines.append("SECURITY ANALYSIS:")
            info_lines.append(f"Security Score: {security.get('score', 0):.2%}")
            info_lines.append(f"Security Status: {'Secure' if security.get('secure', False) else 'Review Required'}")
            if security.get('issues'):
                info_lines.append("Security Issues:")
                for issue in security['issues']:
                    info_lines.append(f"  - {issue}")
            info_lines.append("")
        
        # Deployment Steps
        info_lines.append("DEPLOYMENT STEPS:")
        info_lines.append("1. Review the generated contract code thoroughly")
        info_lines.append("2. Test the contract on a testnet (Goerli, Sepolia, etc.)")
        info_lines.append("3. Verify all constructor parameters are correct")
        info_lines.append("4. Ensure sufficient gas limit for deployment")
        info_lines.append("5. Deploy using Remix, Hardhat, or Truffle")
        info_lines.append("6. Verify the contract on Etherscan after deployment")
        info_lines.append("")
        
        # Contract Code (truncated)
        contract_code = self.generated_contract_result.get('contract_code', '')
        if contract_code:
            info_lines.append("CONTRACT CODE PREVIEW:")
            info_lines.append("-" * 50)
            preview = contract_code[:2000]
            if len(contract_code) > 2000:
                preview += "\n\n... (truncated) ..."
            info_lines.append(preview)
            info_lines.append("-" * 50)
        
        return "\n".join(info_lines)
    
    def _save_deployment_package(self):
        """Save complete deployment package"""
        
        if not self.generated_contract_result:
            messagebox.showerror("Error", "No contract to save")
            return
        
        # Ask user where to save
        folder_path = filedialog.askdirectory(title="Select folder to save deployment package")
        if not folder_path:
            return
        
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            package_folder = os.path.join(folder_path, f"contract_deployment_{timestamp}")
            os.makedirs(package_folder, exist_ok=True)
            
            # Save contract code
            contract_code = self.generated_contract_result.get('contract_code', '')
            if contract_code:
                with open(os.path.join(package_folder, "contract.sol"), 'w', encoding='utf-8') as f:
                    f.write(contract_code)
            
            # Save deployment parameters
            deploy_params = self.generated_contract_result.get('deployment_parameters', {})
            if deploy_params:
                with open(os.path.join(package_folder, "deployment_parameters.json"), 'w', encoding='utf-8') as f:
                    json.dump(deploy_params, f, indent=2)
            
            # Save full generation results
            with open(os.path.join(package_folder, "generation_results.json"), 'w', encoding='utf-8') as f:
                # Remove knowledge graph object for JSON serialization
                results_copy = dict(self.generated_contract_result)
                if 'knowledge_graph' in results_copy:
                    del results_copy['knowledge_graph']
                json.dump(results_copy, f, indent=2)
            
            # Save deployment information
            deploy_info = self._generate_deployment_info()
            with open(os.path.join(package_folder, "deployment_guide.txt"), 'w', encoding='utf-8') as f:
                f.write(deploy_info)
            
            # Save README
            readme_content = f"""# Smart Contract Deployment Package
            
Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Contract Type: {self.generated_contract_result.get('contract_type', 'Unknown')}
Accuracy Score: {self.generated_contract_result.get('accuracy_score', 0):.2%}

## Files Included:

- contract.sol: The generated smart contract code
- deployment_parameters.json: Constructor parameters and deployment settings
- generation_results.json: Complete analysis and validation results
- deployment_guide.txt: Comprehensive deployment instructions

## Next Steps:

1. Review all files carefully
2. Test on a testnet first
3. Deploy using your preferred tool (Remix, Hardhat, Truffle)
4. Verify on block explorer after deployment

## Important:

This contract was automatically generated. Please review thoroughly before deployment to mainnet.
"""
            
            with open(os.path.join(package_folder, "README.md"), 'w', encoding='utf-8') as f:
                f.write(readme_content)
            
            messagebox.showinfo("Success", f"Deployment package saved to:\n{package_folder}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save deployment package: {str(e)}")


if __name__ == "__main__":
    app = MainWindow()
    app.run()