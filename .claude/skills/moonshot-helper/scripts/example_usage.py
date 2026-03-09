#!/usr/bin/env python3
"""
Example usage of moonshot-helper skill

This script demonstrates common use cases for the MoonshotClient.
"""

import os
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.moonshot_client import MoonshotClient, create_client


def example_file_analysis():
    """Example: Analyze a file (document, image, spreadsheet, etc.)"""
    print("Example 1: File Analysis")
    print("-" * 50)

    # Initialize client
    client = create_client()

    # Analyze a file
    result = client.analyze_file(
        file_path="/path/to/document.pdf",
        prompt="Extract all text content and summarize the key points",
        system_prompt="You are a document analysis expert"
    )

    print(result)


def example_chat_completion():
    """Example: Chat completion"""
    print("\nExample 2: Chat Completion")
    print("-" * 50)

    client = create_client()

    # Simple chat
    response = client.chat(
        messages=[
            {"role": "system", "content": "You are a helpful assistant"},
            {"role": "user", "content": "Explain quantum computing in simple terms"}
        ],
        temperature=0.7
    )

    print(response)


def example_batch_analysis():
    """Example: Batch analyze multiple files"""
    print("\nExample 3: Batch File Analysis")
    print("-" * 50)

    client = create_client()

    # Analyze multiple files
    results = client.analyze_files(
        file_paths=["doc1.pdf", "doc2.docx", "image.png"],
        prompt="Extract all dates and names mentioned",
        system_prompt="You are a data extraction specialist",
        output_file="results.json"
    )

    for r in results:
        print(f"{r.file}: {'Success' if r.success else 'Failed'}")


def example_structured_extraction():
    """Example: Extract structured data"""
    print("\nExample 4: Structured Data Extraction")
    print("-" * 50)

    client = create_client()

    # Define schema
    schema = {
        "invoice_number": "发票号码",
        "date": "日期",
        "items": [
            {"name": "项目名称", "quantity": "数量", "price": "单价"}
        ],
        "total": "总金额"
    }

    # Extract data
    data = client.extract_structured_data(
        file_path="invoice.pdf",
        schema=schema,
        document_type="invoice"
    )

    import json
    print(json.dumps(data, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    print("Moonshot Helper - Example Usage")
    print("=" * 50)
    print()
    print("This file contains example usage patterns.")
    print("Uncomment the example you want to run.")
    print()

    # Uncomment the example you want to run:
    # example_file_analysis()
    # example_chat_completion()
    # example_batch_analysis()
    # example_structured_extraction()
