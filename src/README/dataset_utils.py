import json
import argparse
import os
import random

def validate_dataset(file_path):
    print(f"Validating dataset schema: {file_path}")
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Dataset path {file_path} does not exist.")
    
    with open(file_path, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            raise ValueError(f"Dataset must be valid JSON: {e}")
            
    if not isinstance(data, list):
        raise ValueError("Dataset must be a List of dictionaries.")
        
    for idx, row in enumerate(data):
        if not isinstance(row, dict):
            raise ValueError(f"Row {idx} is not a dictionary.")
        if "text" not in row:
            raise ValueError(f"Row {idx} is missing the 'text' key.")
        if not row["text"] or not str(row["text"]).strip():
            raise ValueError(f"Row {idx} has an empty 'text' field.")
            
    print(f"Dataset schema validated successfully. Total records: {len(data)}")
    return data

def sample_dataset(data, output_path, max_samples=2000):
    if len(data) <= max_samples:
        print(f"Dataset has {len(data)} records. No need to sample down to {max_samples}.")
        return

    print(f"Sampling {max_samples} random records out of {len(data)}...")
    sampled_data = random.sample(data, max_samples)
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(sampled_data, f, indent=4)
        
    print(f"Sample dataset cleanly outputted to: {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Dataset Validation and Sampling Toolkit")
    parser.add_argument("--input", type=str, default="data/cooking_finetune.json", help="Path to input full dataset JSON")
    parser.add_argument("--sample", action="store_true", help="Generate a sample dataset instead of just validating")
    parser.add_argument("--sample_size", type=int, default=2000, help="Number of records to sample (defaults to 2000)")
    
    args = parser.parse_args()
    
    data = validate_dataset(args.input)
    
    if args.sample:
        output_name = args.input.replace(".json", "_sample.json")
        sample_dataset(data, output_name, args.sample_size)
