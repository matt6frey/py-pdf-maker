#!/usr/bin/env python3
"""
Markdown to PDF Converter
Converts markdown files to professionally styled PDFs.

Usage:
  python convert.py <input_file.md> <output_file.pdf> [--title "Custom Title"]
"""

import sys
import argparse
from pathlib import Path
import markdown2
from weasyprint import HTML

def convert_markdown_to_pdf(input_path, output_path, title=None):
    """
    Convert a markdown file to PDF with professional styling.
    
    Args:
        input_path: Path to input markdown file
        output_path: Path to output PDF file
        title: Optional custom title for the document
    """
    # Read the markdown file
    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            md_content = f.read()
    except FileNotFoundError:
        print(f"Error: Input file '{input_path}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading input file: {e}")
        sys.exit(1)
    
    # Extract title from markdown if not provided
    if title is None:
        lines = md_content.split('\n')
        for line in lines:
            if line.startswith('# '):
                title = line[2:].strip()
                break
        if title is None:
            title = Path(input_path).stem
    
    # Convert markdown to HTML
    html_content = markdown2.markdown(
        md_content,
        extras=['tables', 'fenced-code-blocks', 'header-ids', 'code-friendly']
    )
    
    # Create full HTML document with styling
    full_html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{title}</title>
    <style>
        @page {{
            size: A4;
            margin: 2cm 1.5cm;
            @top-center {{
                content: "{title}";
                font-size: 9pt;
                color: #666;
            }}
            @bottom-center {{
                content: "Page " counter(page) " of " counter(pages);
                font-size: 9pt;
                color: #666;
            }}
        }}
        
        body {{
            font-family: 'Helvetica', 'Arial', sans-serif;
            font-size: 10pt;
            line-height: 1.6;
            color: #333;
        }}
        
        h1 {{
            color: #1a5490;
            font-size: 24pt;
            margin-top: 0;
            margin-bottom: 20pt;
            padding-bottom: 10pt;
            border-bottom: 3px solid #1a5490;
            page-break-after: avoid;
        }}
        
        h2 {{
            color: #2c5aa0;
            font-size: 18pt;
            margin-top: 24pt;
            margin-bottom: 12pt;
            page-break-after: avoid;
        }}
        
        h3 {{
            color: #3d6bb3;
            font-size: 14pt;
            margin-top: 18pt;
            margin-bottom: 10pt;
            page-break-after: avoid;
        }}
        
        h4 {{
            color: #4d7bc3;
            font-size: 12pt;
            margin-top: 14pt;
            margin-bottom: 8pt;
            page-break-after: avoid;
        }}
        
        p {{
            margin-bottom: 8pt;
            text-align: justify;
        }}
        
        code {{
            background-color: #f4f4f4;
            border: 1px solid #ddd;
            border-radius: 3px;
            padding: 2px 6px;
            font-family: 'Courier New', monospace;
            font-size: 9pt;
            color: #d14;
        }}
        
        pre {{
            background-color: #f8f8f8;
            border: 1px solid #ccc;
            border-left: 4px solid #1a5490;
            border-radius: 4px;
            padding: 12px;
            overflow-x: auto;
            margin: 12pt 0;
            page-break-inside: avoid;
        }}
        
        pre code {{
            background-color: transparent;
            border: none;
            padding: 0;
            color: #333;
        }}
        
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 12pt 0;
            page-break-inside: avoid;
            font-size: 9pt;
        }}
        
        th {{
            background-color: #1a5490;
            color: white;
            padding: 8px;
            text-align: left;
            font-weight: bold;
        }}
        
        td {{
            border: 1px solid #ddd;
            padding: 8px;
        }}
        
        tr:nth-child(even) {{
            background-color: #f9f9f9;
        }}
        
        strong {{
            color: #1a5490;
            font-weight: bold;
        }}
        
        em {{
            font-style: italic;
        }}
        
        ul, ol {{
            margin: 8pt 0;
            padding-left: 24pt;
        }}
        
        li {{
            margin-bottom: 4pt;
        }}
        
        hr {{
            border: none;
            border-top: 2px solid #e0e0e0;
            margin: 24pt 0;
        }}
        
        a {{
            color: #1a5490;
            text-decoration: none;
        }}
        
        a:hover {{
            text-decoration: underline;
        }}
        
        blockquote {{
            border-left: 4px solid #1a5490;
            padding-left: 16px;
            margin: 12pt 0;
            color: #666;
            font-style: italic;
        }}
        
        img {{
            max-width: 100%;
            height: auto;
        }}
    </style>
</head>
<body>
    {html_content}
</body>
</html>
"""
    
    # Generate PDF
    try:
        HTML(string=full_html).write_pdf(output_path)
        print(f"✓ Successfully converted '{input_path}' to '{output_path}'")
    except Exception as e:
        print(f"Error generating PDF: {e}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(
        description='Convert Markdown files to professionally styled PDFs',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic conversion
  python convert.py input.md output.pdf
  
  # With custom title
  python convert.py input.md output.pdf --title "My Document"
  
  # Using Docker with volume mounts
  docker run -v $(pwd)/input:/input -v $(pwd)/output:/output \\
    md2pdf /input/document.md /output/document.pdf
        """
    )
    
    parser.add_argument('input', help='Input markdown file path')
    parser.add_argument('output', help='Output PDF file path')
    parser.add_argument('--title', help='Custom document title (defaults to first H1 or filename)')
    
    args = parser.parse_args()
    
    # Validate input file exists
    if not Path(args.input).exists():
        print(f"Error: Input file '{args.input}' does not exist.")
        sys.exit(1)
    
    # Create output directory if it doesn't exist
    output_dir = Path(args.output).parent
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Convert the file
    convert_markdown_to_pdf(args.input, args.output, args.title)

if __name__ == '__main__':
    main()
