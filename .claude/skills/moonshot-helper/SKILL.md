---
name: moonshot-helper
description: |
  Use this skill when the user needs to use the Moonshot AI (Kimi) API for document analysis,
  text extraction, chat completion, or any AI-powered processing tasks.
  This skill provides a unified interface to the Kimi API for analyzing documents, images,
  spreadsheets, presentations, code files, and text content.
  Make sure to use this skill whenever the user mentions:
  - Analyzing documents with Kimi/Moonshot
  - Extracting text or data from files
  - Using Kimi API for chat or completion
  - Processing PDFs, Word docs, Excel, PowerPoint with AI
  - OCR or document understanding
  - Code analysis with Kimi
  - Any task requiring Moonshot AI API integration
compatibility: |
  Requires: openai package or requests library
  Environment variable: MOONSHOT_API_KEY
---

# Moonshot Helper Skill

This skill provides a unified Python client for the Moonshot AI (Kimi) API, supporting document analysis, chat completion, and various AI-powered processing tasks.

## Quick Start

### Environment Setup

```bash
export MOONSHOT_API_KEY="your-api-key-here"
```

### Basic Usage

```python
from scripts.moonshot_client import MoonshotClient

# Initialize client
client = MoonshotClient()

# Analyze a file (document, image, spreadsheet, code, etc.)
result = client.analyze_file(
    file_path="/path/to/document.pdf",
    prompt="Extract all text content and summarize the key points"
)

print(result)
```

### Chat Completion

```python
# Simple chat completion
response = client.chat(
    messages=[
        {"role": "user", "content": "Hello, how are you?"}
    ]
)

# Multi-turn conversation
response = client.chat(
    messages=[
        {"role": "system", "content": "You are a helpful assistant"},
        {"role": "user", "content": "Explain quantum computing"}
    ],
    temperature=0.7
)
```

### Batch File Analysis

```python
# Analyze multiple files with the same prompt
results = client.analyze_files(
    file_paths=["doc1.pdf", "doc2.docx", "image.png"],
    prompt="Extract all dates and names mentioned",
    output_file="results.json"  # Optional: save to file
)
```

## API Reference

### MoonshotClient

Main client for Kimi API interactions.

#### Constructor

```python
client = MoonshotClient(
    api_key=None,           # Uses MOONSHOT_API_KEY env var if not provided
    base_url="https://api.moonshot.cn/v1",
    model="kimi-k2.5",      # Default model for chat
    max_tokens=4000,
    temperature=0.3
)
```

#### Methods

**analyze_file(file_path, prompt, **kwargs)**
- Analyze a single file with a text prompt
- Supports documents, images, spreadsheets, code files, etc.
- Returns: Analysis text from the model

**analyze_files(file_paths, prompt, output_file=None, **kwargs)**
- Batch analyze multiple files with the same prompt
- Returns: List of results

**chat(messages, model=None, **kwargs)**
- Send chat completion request
- Returns: Response text

**extract_structured_data(file_path, schema, **kwargs)**
- Extract structured data according to a schema
- Returns: Parsed JSON object

## Supported File Types

Kimi API supports a wide range of file formats including:

- **Documents**: .pdf, .doc, .docx, .txt, .md, .epub, .mobi, .html, .json, .log
- **Spreadsheets**: .xls, .xlsx, .csv
- **Presentations**: .ppt, .pptx
- **Images**: .jpeg, .jpg, .png, .gif, .bmp, .webp, .svg, .tiff, .ico, etc.
- **Code files**: .py, .js, .java, .cpp, .c, .cs, .go, .php, .jsp, .css, .ts, .tsx, etc.
- **Config files**: .yaml, .yml, .ini, .conf

## Examples

### Document Analysis

```python
# Analyze a PDF document
result = client.analyze_file(
    file_path="report.pdf",
    prompt="Extract all tables and summarize the findings"
)

# Extract specific information
result = client.analyze_file(
    file_path="contract.docx",
    prompt="Extract: 1) Parties involved, 2) Contract dates, 3) Key terms"
)
```

### Image Analysis

```python
# OCR and text extraction
result = client.analyze_file(
    file_path="screenshot.png",
    prompt="Extract all visible text, preserving the layout"
)

# Medical report analysis
result = client.analyze_file(
    file_path="lab_report.jpg",
    prompt="""Extract all medical data:
    - Patient information
    - Test results with units and reference ranges
    - Flag abnormal values
    Format as a structured table."""
)
```

### Spreadsheet Analysis

```python
# Analyze Excel data
result = client.analyze_file(
    file_path="sales_data.xlsx",
    prompt="Summarize the sales trends and identify top-performing products"
)

# CSV data extraction
result = client.analyze_file(
    file_path="data.csv",
    prompt="List all unique values in the 'Category' column"
)
```

### Code Analysis

```python
# Analyze code files
result = client.analyze_file(
    file_path="script.py",
    prompt="Explain what this code does and identify any potential issues"
)

# Multiple code files
results = client.analyze_files(
    file_paths=["main.py", "utils.py", "config.yaml"],
    prompt="Summarize the architecture and dependencies"
)
```

### Structured Data Extraction

```python
schema = {
    "invoice_number": "发票号码",
    "date": "日期",
    "items": [
        {"name": "项目名称", "quantity": "数量", "price": "单价"}
    ],
    "total": "总金额"
}

data = client.extract_structured_data(
    file_path="invoice.pdf",
    schema=schema,
    document_type="invoice"
)
```

## Configuration Options

```python
client = MoonshotClient(
    api_key="your-key",              # API key
    model="kimi-k2.5",               # Model selection
    max_tokens=8000,                 # Response length limit
    temperature=0.3,                 # Creativity (0-2)
    use_openai_sdk=True              # Use OpenAI SDK or requests
)
```

### Model Options

- `kimi-k2.5` - Latest general-purpose model (recommended)
- `moonshot-v1-8k` - Standard chat model
- `moonshot-v1-32k` - Long context model
- `moonshot-v1-8k-vision-preview` - Vision model

> **Note for image recognition:** `kimi-k2.6` only supports `temperature=1`. When using other models for image tasks, `temperature=0.1-0.3` is recommended for factual extraction.

## Error Handling

```python
from scripts.moonshot_client import MoonshotAPIError, FileProcessingError

try:
    result = client.analyze_file("document.pdf", "Extract text")
except MoonshotAPIError as e:
    print(f"API error: {e}")
except FileProcessingError as e:
    print(f"File error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

## Best Practices

1. **Use specific prompts** - Clearly state what you want extracted or analyzed
2. **Temperature setting** - Use 0.1-0.3 for factual extraction, 0.7+ for creative tasks
3. **Max tokens** - Set higher for long documents (up to 8000)
4. **System prompts** - Set context with system prompts for better results
5. **Batch processing** - Use `analyze_files()` for multiple related files
