import argparse
import os
import json
import random
from pathlib import Path


def process_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
        return {
            "context": data["rewritten_chunk"],
            "response": data["original_chunk"]
        }

def main(input_directory, output_directory):
    # Create output directory if it doesn't exist
    os.makedirs(output_directory, exist_ok=True)

    # Define the output files
    train_file = os.path.join(output_directory, 'train.jsonl')
    validation_file = os.path.join(output_directory, 'validation.jsonl')
    template_file = os.path.join(output_directory, 'template.json')

    # Read all files from the input directory
    file_paths = list(Path(input_directory).glob('*.json'))

    # Shuffle the file paths for random split
    random.shuffle(file_paths)

    # Split into training and validation (9:1 ratio)
    split_index = int(len(file_paths) * 0.9)
    train_paths = file_paths[:split_index]
    validation_paths = file_paths[split_index:]

    # Write JSON Lines to train.jsonl
    with open(train_file, 'w', encoding='utf-8') as train_f:
        for path in train_paths:
            entry = process_file(path)
            train_f.write(json.dumps(entry, ensure_ascii=False) + '\n')

    # Write JSON Lines to validation.jsonl
    with open(validation_file, 'w', encoding='utf-8') as validation_f:
        for path in validation_paths:
            entry = process_file(path)
            validation_f.write(json.dumps(entry, ensure_ascii=False) + '\n')

    # Create the template.json file
    template_content = {
        "prompt": "Rewrite the paragraph in 'Wait But Why' style: use a conversational, humorous tone with in-depth explanations and analogies. Use pop culture references and pose questions to the reader. Use creative formatting like lists or subheadings.\n\n### Input:\n{context}\n\n### Response:",
        "completion": "{response}"
    }

    with open(template_file, 'w', encoding='utf-8') as template_f:
        json.dump(template_content, template_f, indent=4)

    print(f'Training and validation files have been created in {output_directory}.')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Prepare dataset for model fine-tuning")
    parser.add_argument('--input_dir', type=str, required=True, help="Directory containing the input JSON files")
    parser.add_argument('--output_dir', type=str, required=True, help="Directory to save the output files")

    args = parser.parse_args()

    main(args.input_dir, args.output_dir)
