# wbw-finetune-dataset-prep

This Python project is designed to preprocess and rewrite articles crawled from https://waitbutwhy.com/. It prepares the data for fine-tuning language models by cleaning the original content and rewriting it in various styles.

## Features

- Cleans up boilerplate text (promotions, subscriptions, etc.) from original files
- Chunks articles to respect the max input length of the target model
- Rewrites article chunks using the Claude API in one of three styles:
  - Study Notes
  - K-12 Student Essay Draft
  - English Learner Writing Exercise
- Provides options for cleaning only, rewriting only, or both operations
- Prepares fine-tuning datasets by:
  - Splitting data into training and validation sets
  - Creating prompt-completion pairs from original and rewritten content

## Requirements

- Python 3.7+
- `anthropic` library (for Claude API access)
- Valid Claude API key (set as an environment variable or in the script)

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/liyi5895/wbw-finetune-dataset-prep.git
   cd wbw-finetune-dataset-prep
   ```

2. Install the required dependencies:
   ```
   pip install anthropic
   ```

3. Set up your Claude API key:
   ```
   export ANTHROPIC_API_KEY=your_api_key_here
   ```

## Usage

### Article Processing

The main script is `main.py`. It can be run with the following options:

```bash
# To run both cleaning and rewriting:
python main.py /path/to/input /path/to/cleaned /path/to/rewritten

# To only clean articles:
python main.py /path/to/input /path/to/cleaned /path/to/rewritten --clean-only

# To only rewrite previously cleaned articles:
python main.py /path/to/input /path/to/cleaned /path/to/rewritten --rewrite-only
```

Replace `/path/to/input`, `/path/to/cleaned`, and `/path/to/rewritten` with the appropriate directories for your input files, cleaned output, and rewritten output respectively.

### Fine-tuning Dataset Preparation

After processing articles, use `prepare_finetune_data.py` to create the fine-tuning dataset:

```bash
python prepare_finetune_data.py /path/to/input_directory /path/to/output_directory
```


## Configuration

You can adjust the following parameters in the script:

- `MAX_CHUNK_SIZE`: Maximum size of each chunk sent to Claude
- `MAX_TOKENS_TO_SAMPLE`: Maximum number of tokens for Claude to generate


## Disclaimer

This script is for educational and research purposes only. Ensure you have the right to use and process the content from Wait But Why before running this script. Respect the website's terms of service and any applicable copyright laws.
