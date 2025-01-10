import json
import os
import time
import anthropic
import argparse
from urllib.parse import urlparse
from clean_content import clean_article_content
from split_content import split_content_by_paragraph
from get_prompt import get_prompt, select_style
from ratelimit import limits, sleep_and_retry
from config.settings import (
    CLAUDE_API_KEY,
    MODEL_NAME,
    MAX_TOKENS_TO_SAMPLE,
    CALLS,
    RATE_LIMIT
)

client = anthropic.Anthropic(
    api_key=CLAUDE_API_KEY,
)


@sleep_and_retry
@limits(calls=CALLS, period=RATE_LIMIT)
def rewrite_with_claude(content, style):
    try:
        message = client.messages.create(
            model="claude-3-5-sonnet-20240620",
            max_tokens=MAX_TOKENS_TO_SAMPLE,
            messages=[
                {"role": "user", "content": get_prompt(content, style)}
            ]
        )
        # Assuming the response is in the first TextBlock
        return message.content[0].text
    except Exception as e:
        print(f"Error in API call: {str(e)}")
        return None


def rewrite_cleaned_articles(input_directory, output_directory):
    os.makedirs(output_directory, exist_ok=True)
    
    for root, dirs, files in os.walk(input_directory):
        for file in files:
            if file.endswith('.json'):
                input_path = os.path.join(root, file)
                with open(input_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                url = data.get('url')
                cleaned_article = data.get('cleaned_article')
                
                if cleaned_article:
                    style = select_style()
                    chunks = split_content_by_paragraph(cleaned_article, MAX_CHUNK_SIZE)

                    for i, chunk in enumerate(chunks):
                        rewritten_chunk = rewrite_with_claude(chunk, style)
                        if rewritten_chunk:
                            output_filename = f"{file.replace('.json', '')}_rewritten_chunk_{i+1}.json"
                            output_path = os.path.join(output_directory, output_filename)
                            with open(output_path, 'w', encoding='utf-8') as f:
                                json.dump({
                                    "url": url,
                                    "style": style, 
                                    "original_chunk": chunk,
                                    "rewritten_chunk": rewritten_chunk
                                }, f, ensure_ascii=False, indent=2)
                            print(f"Processed and saved: {output_path}")
                        else:
                            print(f"Failed to rewrite chunk {i+1} of {input_path}")
                        time.sleep(1)  # Basic rate limiting
                else:
                    print(f"No 'cleaned_article' field found in: {input_path}")


def is_valid_url(url):
    parsed_url = urlparse(url)
    path_parts = parsed_url.path.strip('/').split('/')
    
    if len(path_parts) >= 3:
        if path_parts[0].isdigit() and path_parts[1].isdigit():
            if path_parts[-1].endswith('.html'):
                return True
    return False


def clean_and_save_articles(input_directory, output_directory):
    os.makedirs(output_directory, exist_ok=True)
    
    for root, dirs, files in os.walk(input_directory):
        for file in files:
            if file.endswith('.json'):
                input_path = os.path.join(root, file)
                with open(input_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                url = data.get('url')
                article = data.get('article')
                
                if url and article and is_valid_url(url):
                    cleaned_article = clean_article_content(article)
                    
                    url_parts = urlparse(url).path.strip('/').split('/')
                    output_filename = f"{url_parts[-3]}_{url_parts[-2]}_{url_parts[-1].replace('.html', '')}.json"
                    output_path = os.path.join(output_directory, output_filename)
                    
                    with open(output_path, 'w', encoding='utf-8') as f:
                        json.dump({
                            "url": url,
                            "cleaned_article": cleaned_article
                        }, f, ensure_ascii=False, indent=2)
                    print(f"Cleaned and saved: {output_path}")
                else:
                    print(f"Skipped (invalid URL or no article): {input_path}")


def parse_args():
    parser = argparse.ArgumentParser(description="Process and rewrite articles using Claude API")
    parser.add_argument("input_dir", help="Directory containing original JSON files")
    parser.add_argument("cleaned_dir", help="Directory to save cleaned JSON files")
    parser.add_argument("output_dir", help="Directory to save rewritten JSON files")
    parser.add_argument("--clean-only", action="store_true", help="Only clean articles without rewriting")
    parser.add_argument("--rewrite-only", action="store_true", help="Only rewrite previously cleaned articles")
    
    args = parser.parse_args()
    return args


def main():
    args = parse_args()

    if not args.clean_only and not args.rewrite_only:
        print("Cleaning articles...")
        clean_and_save_articles(args.input_dir, args.cleaned_dir)
        print("Rewriting articles...")
        rewrite_cleaned_articles(args.cleaned_dir, args.output_dir)
    elif args.clean_only:
        print("Cleaning articles...")
        clean_and_save_articles(args.input_dir, args.cleaned_dir)
    elif args.rewrite_only:
        print("Rewriting articles...")
        rewrite_cleaned_articles(args.cleaned_dir, args.output_dir)
    
    print("Process completed.")


if __name__ == "__main__":
    main()
