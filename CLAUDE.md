# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This project for researching data and generating analysis reports.

## Project Structure

```
./
├── reference/                  # Original reference documents directory
│   ├── data.xlsx               # Research data file
│   ├── presentation.pdf        # PDF presentation
│   └── ...                     # Other reference documents (subdirectories supported)
├── transformed/                # Parsed markdown resources directory
│   ├── data.png.md            # Single-page file → flat .md
│   ├── presentation.pdf.desc/ # Multi-page file → subdirectory
│   │   ├── page-1.md          # Page-by-page markdown
│   │   └── page-2.md
│   └── ...                     # One-to-one correspondence with reference structure
├── generated/                  # Generated derivative content directory
│   ├── chart_*.png             # Generated charts
│   ├── chart_*.png.desc.md     # Chart description document (required for non-text files)
│   └── ...                     # Other generated files
├── temp/                       # Temporary files directory
│   └── ...                     # Temporary scripts and files (subdirectories supported)
└── output/                     # Final output directory
    └── report.md               # Generated final report
```

**Directory Descriptions:**
- **reference/**: Stores original reference files (Excel, Word, PDF, images, etc.), supports subdirectories
- **transformed/**: Stores markdown parsing results of files in reference. Single-page files use flat naming `<filename>.<ext>.md`; multi-page files (PDF, DOCX, PPT, etc.) use subdirectory `<filename>.<ext>.desc/page-N.md`
- **generated/**: Stores generated charts and visualizations. Non-text files (images, etc.) must be accompanied by `.desc.md` description files that describe content only without analysis
- **temp/**: Stores temporary code scripts and other temporary files, subdirectories can be created inside
- **output/**: Stores the generated final report

## Key Skills

Prioritize using existing skills to complete tasks. Read the `.claude/skills` directory.

## Basic Workflow

1. **Environment Check**: Confirm that the `reference/` directory contains files
2. **Preprocessing**:
   * Check `transformed/` first: if a converted result already exists for a file, read it directly and skip re-conversion
   * For files that cannot be directly parsed (scanned PDFs, images, etc.), convert them to markdown in `transformed/` first, then read the content from `transformed/`
   * For image extraction, prioritize checking installed skills for AI-capable ones (e.g., `moonshot-helper`); check `.env` for API key configuration (`MOONSHOT_API_KEY`, etc.)
   * Convert non-plain-text files (images, etc.) from reference to markdown in `transformed/`
   * xlsx files do not need conversion
   * For PDF conversion, evaluate the internal structure; if images dominate, convert to images first and then use image recognition
   * For image recognition results saved to `transformed/xx.desc.md`:
     * File header must include the image's blur level (recognition result credibility) as `0-100%`
     * Watermarks should not be written to the desc file
   * For multi-page files (PDF, DOCX, PPT, etc.), each page converts to a separate markdown file under `transformed/<filename>.<ext>.desc/`:
     * Format: `transformed/<filename>.<ext>.desc/page-1.md`, `page-2.md`, ...
     * Single-page files keep the flat naming: `transformed/<filename>.<ext>.md`
3. **Analysis & Generation**: Generate reports to `output/` based on transformed content
4. **Chart Generation**: Use skills to generate charts to `generated/` and reference them in reports
5. **Quality Check**: Verify data accuracy
6. **Traceability**: Add text citation markers for all related reference information

## Formatting Requirements

* Add a half-width space between Chinese and English characters
* Add a half-width space between numbers and text
* Tables and report content must not use ellipsis to omit data
