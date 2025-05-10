import re
import json
import os
import sys

def convert_markdown_to_json(input_path, output_path):
    """Convert Markdown file with video links to structured JSON format"""
    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            markdown_text = f.read()

        # Initialize the result dictionary
        result = {}
        current_category = None

        # Split the markdown into lines
        lines = markdown_text.split('\n')

        # Regular expressions for matching
        category_pattern = re.compile(r'^#\s*(?:Category:\s*)?(.+)$')
        video_pattern = re.compile(r'^\s*-\s*\[(.*?)\]\((https?://(?:www\.)?(?:youtube\.com|youtu\.be)/[^\s)]+)\)')

        for line in lines:
            # Check for category
            category_match = category_pattern.match(line)
            if category_match:
                current_category = category_match.group(1).strip()
                if current_category not in result:
                    result[current_category] = []
                continue

            # Check for video link
            video_match = video_pattern.match(line)
            if video_match and current_category is not None:
                title = video_match.group(1).strip()
                url = video_match.group(2).strip()

                video_entry = {
                    "title": title,
                    "url": url,
                    "watched": False  # Default to unwatched
                }

                result[current_category].append(video_entry)

        # Write JSON output
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)

        print(f"Successfully converted {input_path} to {output_path}")

    except FileNotFoundError:
        print(f"Error: Input file '{input_path}' not found")
        sys.exit(1)
    except Exception as e:
        print(f"Error processing file: {e}")
        sys.exit(1)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python md_to_json.py <input_markdown_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    if not os.path.isfile(input_file):
        print(f"Error: '{input_file}' is not a valid file")
        sys.exit(1)

    output_file = 'videos.json'  # Fixed output filename as requested
    convert_markdown_to_json(input_file, output_file)
