# Markdown to PDF Converter - Docker

A Docker container that converts Markdown files to styled PDFs using Python, markdown2, and WeasyPrint. This was built with Linux/Unix in mind, but I will update this in the future for ease of use on Windows too (See `Next Steps` section). Yes, the current styling is a bit ugly as well (also check `Next Steps`)

## Quick Start

### Build the Docker Image

```bash
docker compose up --build -d
```

### Basic Usage

Convert a markdown file to PDF:

```bash
./convert-all.sh
```

### With Custom Title

```bash
./convert-all.sh --title "My Custom Title"
```

## Directory Structure

```
.
├── Dockerfile          # Docker image definition
├── convert.py          # Python conversion script
├── README.md          # This file
├── input/             # Place your .md files here (create this)
└── output/            # PDFs will be generated here (create this)
```

## Next steps.

I will probably revisit this in the new year and make it a little more modular (_cough cough_ - update `convert.py`)

1. Modularize for clarity
2. Update `convert-all.sh` to look for `.html` extensions
3. Provide more details on running on Windows.
4. Beautify PDF output and provide additional themes/styles 
