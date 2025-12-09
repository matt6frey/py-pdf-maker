# Markdown to PDF Converter - Docker

A Docker container that converts Markdown files to professionally styled PDFs using Python, markdown2, and WeasyPrint.

## Quick Start

### Build the Docker Image

```bash
docker build -t md2pdf .
```

### Basic Usage

Convert a markdown file to PDF:

```bash
docker run --rm \
  -v $(pwd)/input:/input \
  -v $(pwd)/output:/output \
  md2pdf /input/document.md /output/document.pdf
```

### With Custom Title

```bash
docker run --rm \
  -v $(pwd)/input:/input \
  -v $(pwd)/output:/output \
  md2pdf /input/document.md /output/document.pdf --title "My Custom Title"
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

## Setup

1. Create input and output directories:
   ```bash
   mkdir -p input output
   ```

2. Place your markdown files in the `input` directory:
   ```bash
   cp your-document.md input/
   ```

3. Build the Docker image:
   ```bash
   docker build -t md2pdf .
   ```

4. Run the converter:
   ```bash
   docker run --rm \
     -v $(pwd)/input:/input \
     -v $(pwd)/output:/output \
     md2pdf /input/your-document.md /output/your-document.pdf
   ```

## Usage Examples

### Example 1: Single File Conversion

```bash
# Put your markdown in the input folder
echo "# Hello World" > input/test.md
echo "This is a test document." >> input/test.md

# Convert to PDF
docker run --rm \
  -v $(pwd)/input:/input \
  -v $(pwd)/output:/output \
  md2pdf /input/test.md /output/test.pdf

# Check the output
ls -lh output/test.pdf
```

### Example 2: Batch Conversion Script

Create a shell script `convert-all.sh`:

```bash
#!/bin/bash

# Convert all markdown files in input directory
for file in input/*.md; do
    filename=$(basename "$file" .md)
    echo "Converting $filename..."
    docker run --rm \
      -v $(pwd)/input:/input \
      -v $(pwd)/output:/output \
      md2pdf "/input/${filename}.md" "/output/${filename}.pdf"
done

echo "All conversions complete!"
```

Make it executable and run:
```bash
chmod +x convert-all.sh
./convert-all.sh
```

### Example 3: Custom Styling

The default styles are embedded in `convert.py`. To customize:

1. Edit `convert.py` and modify the CSS in the `<style>` section
2. Rebuild the Docker image:
   ```bash
   docker build -t md2pdf .
   ```
3. Run conversions with your custom styles

## Features

- **Professional Styling**: Clean, readable PDFs with proper typography
- **Code Syntax Highlighting**: Formatted code blocks with syntax support
- **Tables**: Properly styled tables with alternating row colors
- **Headers & Footers**: Automatic page numbers and document title
- **Page Breaks**: Smart page break handling for better readability
- **Responsive Tables**: Tables that fit the page width

## Supported Markdown Features

- Headers (H1-H6)
- Bold and italic text
- Code blocks (with language specification)
- Inline code
- Tables
- Lists (ordered and unordered)
- Blockquotes
- Horizontal rules
- Links

## Customization

### Change Color Scheme

Edit the CSS variables in `convert.py`:

```python
h1 {
    color: #1a5490;  # Change this to your preferred color
    ...
}
```

### Change Font

Modify the font-family in the body style:

```python
body {
    font-family: 'Helvetica', 'Arial', sans-serif;  # Change fonts here
    ...
}
```

### Change Page Size

Modify the @page rule:

```python
@page {
    size: A4;  # Options: A4, Letter, Legal, etc.
    margin: 2cm 1.5cm;  # Adjust margins
}
```

## Troubleshooting

### Permission Issues

If you get permission errors with output files:

```bash
# On Linux/Mac, ensure proper permissions
chmod -R 777 output/

# Or run with user mapping
docker run --rm \
  -v $(pwd)/input:/input \
  -v $(pwd)/output:/output \
  -u $(id -u):$(id -g) \
  md2pdf /input/document.md /output/document.pdf
```

### Windows Paths

On Windows (PowerShell):

```powershell
docker run --rm `
  -v ${PWD}/input:/input `
  -v ${PWD}/output:/output `
  md2pdf /input/document.md /output/document.pdf
```

On Windows (Command Prompt):

```cmd
docker run --rm ^
  -v %cd%/input:/input ^
  -v %cd%/output:/output ^
  md2pdf /input/document.md /output/document.pdf
```

### File Not Found

Ensure your input file path is relative to the `/input` mount point:

```bash
# Correct
docker run ... md2pdf /input/doc.md /output/doc.pdf

# Incorrect
docker run ... md2pdf input/doc.md output/doc.pdf
```

## Docker Compose (Optional)

Create `docker-compose.yml` for easier usage:

```yaml
version: '3.8'

services:
  md2pdf:
    build: .
    volumes:
      - ./input:/input
      - ./output:/output
    command: /input/document.md /output/document.pdf
```

Usage:
```bash
docker-compose run --rm md2pdf /input/document.md /output/document.pdf
```

## Technical Details

### Dependencies

- **Python 3.12**: Base runtime
- **markdown2**: Markdown parsing with extras
- **WeasyPrint**: HTML to PDF conversion
- **System libraries**: Cairo, Pango, HarfBuzz for text rendering

### Image Size

Approximate image size: ~300-400MB (includes all system dependencies)

### Performance

Typical conversion speed:
- Small documents (<10 pages): <1 second
- Medium documents (10-50 pages): 1-3 seconds
- Large documents (50+ pages): 3-10 seconds

## License

This tool uses the following open-source libraries:
- markdown2 (MIT License)
- WeasyPrint (BSD License)

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review the examples provided
3. Check WeasyPrint documentation: https://weasyprint.org/

## Version History

- **1.0.0**: Initial release with core functionality
  - Markdown to PDF conversion
  - Professional styling
  - Docker containerization
  - Volume mount support
