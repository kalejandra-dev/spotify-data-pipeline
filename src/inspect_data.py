import json
import glob
from pathlib import Path

def inspect_spotify_data(raw_data_path: str):
    # Locate all JSON files in the raw directory
    json_files = glob.glob(f"{raw_data_path}/*.json")
    
    if not json_files:
        print("No JSON files found in data/raw/")
        return

    for file_path in json_files:
        filename = Path(file_path).name
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        print(f"\n--- File: {filename} ---")
        
        if isinstance(data, list):
            print(f"Total records: {len(data)}")
            if len(data) > 0:
                first_record = data[0]
                print("Schema (Fields and Data Types):")
                for key, value in first_record.items():
                    print(f"  - {key}: {type(value).__name__}")
        else:
            print(f"Unexpected data structure: {type(data).__name__}")

if __name__ == "__main__":
    inspect_spotify_data("data/raw")
