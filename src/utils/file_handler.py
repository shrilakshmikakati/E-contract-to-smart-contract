
import os
import json
import pickle
from typing import Optional, Dict, Any, List
import pandas as pd
from pathlib import Path

class FileHandler:
    
    @staticmethod
    def read_text_file(file_path: str) -> str:
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except UnicodeDecodeError:
            with open(file_path, 'r', encoding='latin-1') as file:
                return file.read()
    
    @staticmethod
    def write_text_file(file_path: str, content: str) -> bool:
        try:
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(content)
            return True
        except Exception as e:
            print(f"Error writing file {file_path}: {e}")
            return False
    
    @staticmethod
    def read_json_file(file_path: str) -> Optional[Dict[str, Any]]:
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return json.load(file)
        except Exception as e:
            print(f"Error reading JSON file {file_path}: {e}")
            return None
    
    @staticmethod
    def write_json_file(file_path: str, data: Dict[str, Any]) -> bool:
        try:
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, 'w', encoding='utf-8') as file:
                json.dump(data, file, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error writing JSON file {file_path}: {e}")
            return False
    
    @staticmethod
    def read_pickle_file(file_path: str) -> Optional[Any]:
        try:
            with open(file_path, 'rb') as file:
                return pickle.load(file)
        except Exception as e:
            print(f"Error reading pickle file {file_path}: {e}")
            return None
    
    @staticmethod
    def write_pickle_file(file_path: str, data: Any) -> bool:
        try:
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, 'wb') as file:
                pickle.dump(data, file)
            return True
        except Exception as e:
            print(f"Error writing pickle file {file_path}: {e}")
            return False
    
    @staticmethod
    def read_solidity_file(file_path: str) -> Dict[str, Any]:
        try:
            content = FileHandler.read_text_file(file_path)
            
            pragma_line = None
            for line in content.split('\n'):
                if line.strip().startswith('pragma solidity'):
                    pragma_line = line.strip()
                    break
            
            return {
                'content': content,
                'pragma': pragma_line,
                'file_name': os.path.basename(file_path),
                'file_path': file_path
            }
        except Exception as e:
            print(f"Error reading Solidity file {file_path}: {e}")
            return {}
    
    @staticmethod
    def list_files_in_directory(directory: str, extensions: List[str] = None) -> List[str]:
        try:
            files = []
            for root, dirs, filenames in os.walk(directory):
                for filename in filenames:
                    if extensions is None or any(filename.lower().endswith(ext) for ext in extensions):
                        files.append(os.path.join(root, filename))
            return files
        except Exception as e:
            print(f"Error listing files in directory {directory}: {e}")
            return []
    
    @staticmethod
    def save_graph_data(file_path: str, graph_data: Dict[str, Any]) -> bool:
        try:
            base_path = os.path.splitext(file_path)[0]
            
            json_success = FileHandler.write_json_file(f"{base_path}.json", graph_data)
            
            pickle_success = FileHandler.write_pickle_file(f"{base_path}.pkl", graph_data)
            
            if 'entities' in graph_data and 'relations' in graph_data:
                entities_df = pd.DataFrame(graph_data['entities'])
                relations_df = pd.DataFrame(graph_data['relations'])
                
                entities_df.to_csv(f"{base_path}_entities.csv", index=False)
                relations_df.to_csv(f"{base_path}_relations.csv", index=False)
            
            return json_success and pickle_success
            
        except Exception as e:
            print(f"Error saving graph data {file_path}: {e}")
            return False
    
    @staticmethod
    def load_graph_data(file_path: str) -> Optional[Dict[str, Any]]:
        try:
            pickle_path = os.path.splitext(file_path)[0] + '.pkl'
            if os.path.exists(pickle_path):
                return FileHandler.read_pickle_file(pickle_path)
            
            json_path = os.path.splitext(file_path)[0] + '.json'
            if os.path.exists(json_path):
                return FileHandler.read_json_file(json_path)
            
            return None
            
        except Exception as e:
            print(f"Error loading graph data {file_path}: {e}")
            return None
    
    @staticmethod
    def validate_file_path(file_path: str, allowed_extensions: List[str] = None) -> bool:
        if not os.path.exists(file_path):
            return False
        
        if allowed_extensions:
            file_ext = os.path.splitext(file_path)[1].lower()
            return file_ext in allowed_extensions
        
        return True
    
    @staticmethod
    def get_file_info(file_path: str) -> Dict[str, Any]:
        try:
            stat = os.stat(file_path)
            return {
                'name': os.path.basename(file_path),
                'path': file_path,
                'size': stat.st_size,
                'extension': os.path.splitext(file_path)[1].lower(),
                'modified': stat.st_mtime,
                'exists': True
            }
        except Exception as e:
            return {
                'name': os.path.basename(file_path) if file_path else '',
                'path': file_path,
                'size': 0,
                'extension': '',
                'modified': 0,
                'exists': False,
                'error': str(e)
            }