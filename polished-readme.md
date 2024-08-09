# wbw_finetune

This Python project is designed to preprocess and rewrite articles crawled from https://waitbutwhy.com/. It prepares the data for fine-tuning language models by cleaning the original content and rewriting it in various styles.

## Features

- Cleans up boilerplate text (promotions, subscriptions, etc.) from original files
- Validates article URLs to ensure they match the expected format
- Chunks articles to respect the max input length of the target model (e.g., LLaMA 3 8B)
- Rewrites article chunks using the Claude API in one of three styles:
  - Study Notes
  - K-12 Student Essay Draft
  - English Learner Writing Exercise
- Maintains consistent rewriting style across all chunks of the same article
- Provides options for cleaning only, rewriting only, or both operations

## Requirements

- Python 3.7+
- `anthropic` library (for Claude API access)
- `argparse` library (for command-line argument parsing)
- Valid Claude API key (set as an environment variable or in the script)

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/wbw_finetune.git
   cd wbw_finetune
   ```

2. Install the required dependencies:
   ```
   pip install anthropic argparse
   ```

3. Set up your Claude API key:
   ```
   export ANTHROPIC_API_KEY=your_api_key_here
   ```

## Usage

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

## Process

1. **Cleaning**: 
   - Removes boilerplate text and irrelevant content from the original articles
   - Validates URLs to ensure they match the expected format (e.g., "https://waitbutwhy.com/YYYY/MM/article-name.html")
   - Saves cleaned content to the specified cleaned directory

2. **Rewriting**:
   - Loads cleaned articles from the cleaned directory
   - Splits articles into chunks that fit within the model's max input length
   - Selects a rewriting style (Study Notes, K-12 Essay, or English Learner) for each article
   - Sends each chunk to the Claude API for rewriting in the selected style
   - Combines rewritten chunks and saves the result to the specified rewritten directory

## Configuration

You can adjust the following parameters in the script:

- `MAX_CHUNK_SIZE`: Maximum size of each chunk sent to Claude (default: 12000 characters)
- `MAX_TOKENS_TO_SAMPLE`: Maximum number of tokens for Claude to generate (default: 2000 tokens)

## Contributing

Contributions to improve the script or extend its functionality are welcome. Please feel free to submit pull requests or open issues for any bugs or feature requests.

## License

[Specify your license here, e.g., MIT, GPL, etc.]

## Disclaimer

This script is for educational and research purposes only. Ensure you have the right to use and process the content from Wait But Why before running this script. Respect the website's terms of service and any applicable copyright laws.
