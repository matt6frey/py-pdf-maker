#!/bin/bash

# Batch Markdown to PDF Converter
# Converts all .md files in the input directory to PDFs in the output directory

set -e

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Create directories if they don't exist
mkdir -p input output

# Check if Docker image exists
if ! docker images | grep -q "md2pdf"; then
    echo -e "${YELLOW}Docker image 'md2pdf' not found. Building...${NC}"
    docker build -t md2pdf .
fi

# Count markdown files
md_count=$(find input -maxdepth 1 -name "*.md" 2>/dev/null | wc -l)

if [ "$md_count" -eq 0 ]; then
    echo -e "${RED}No markdown files found in 'input/' directory${NC}"
    echo "Please place .md files in the 'input/' directory and try again."
    exit 1
fi

echo -e "${GREEN}Found $md_count markdown file(s) to convert${NC}"
echo ""

# Counter for successful conversions
success_count=0
fail_count=0

# Convert each markdown file
for file in input/*.md; do
    if [ -f "$file" ]; then
        filename=$(basename "$file" .md)
        echo -e "${YELLOW}Converting: ${filename}.md${NC}"
        
        if docker run --rm \
            -v "$(pwd)/input:/input" \
            -v "$(pwd)/output:/output" \
            md2pdf "/input/${filename}.md" "/output/${filename}.pdf" 2>&1; then
            success_count=$((success_count + 1))
        else
            echo -e "${RED}Failed to convert: ${filename}.md${NC}"
            fail_count=$((fail_count + 1))
        fi
        echo ""
    fi
done

# Summary
echo "================================================"
echo -e "${GREEN}Conversion Summary:${NC}"
echo -e "  Total files:    $md_count"
echo -e "  ${GREEN}Successful:     $success_count${NC}"
if [ "$fail_count" -gt 0 ]; then
    echo -e "  ${RED}Failed:         $fail_count${NC}"
fi
echo "================================================"

if [ "$success_count" -gt 0 ]; then
    echo -e "${GREEN}✓ PDFs saved to 'output/' directory${NC}"
fi
