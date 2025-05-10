# YouTube Video Organizer

Organizes YouTube videos into categories and provides a REST API for programmatic use.

## Project Setup

### Creating a Virtual Environment

```bash
# Create virtual environment

python -m venv myenv

# Activate environment

# Linux/macOS

source myenv/bin/activate

# Windows

venv\Scripts\activate
```

### Running the Converter

```bash
# Execute the conversion script with your markdown file
python md_to_json.py your_file.md
```

### Running the Application

```bash
# Run the FastAPI application
uvicorn main:app --reload
```
