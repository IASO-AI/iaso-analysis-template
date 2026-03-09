#!/usr/bin/env python3
"""
Moonshot AI (Kimi) API Client

A unified client for the Moonshot AI API supporting document analysis,
chat completion, and various AI-powered processing tasks.
"""

import os
import base64
import json
import mimetypes
from pathlib import Path
from typing import List, Dict, Optional, Union, Any
from dataclasses import dataclass

# Try to import OpenAI SDK
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

import requests


# Default configuration
DEFAULT_BASE_URL = "https://api.moonshot.cn/v1"
DEFAULT_MODEL = "kimi-k2.5"
DEFAULT_MAX_TOKENS = 4000
DEFAULT_TEMPERATURE = 1.0  # Kimi k2.5 only supports temperature=1


class MoonshotAPIError(Exception):
    """Custom exception for Moonshot API errors"""
    def __init__(self, message: str, status_code: Optional[int] = None):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class FileProcessingError(Exception):
    """Custom exception for file processing errors"""
    pass


@dataclass
class AnalysisResult:
    """Data class for analysis results"""
    file: str
    analysis: str
    success: bool
    error: Optional[str] = None


class MoonshotClient:
    """
    Unified client for Moonshot AI API

    Supports document analysis, chat completion, and AI-powered processing.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: str = DEFAULT_BASE_URL,
        model: str = DEFAULT_MODEL,
        max_tokens: int = DEFAULT_MAX_TOKENS,
        temperature: float = DEFAULT_TEMPERATURE,
        use_openai_sdk: bool = True
    ):
        """
        Initialize Moonshot client

        Args:
            api_key: API key (or set MOONSHOT_API_KEY env var)
            base_url: API base URL
            model: Default model for tasks
            max_tokens: Maximum tokens in response
            temperature: Sampling temperature (0-2)
            use_openai_sdk: Whether to use OpenAI SDK if available
        """
        self.api_key = api_key or os.environ.get("MOONSHOT_API_KEY")
        if not self.api_key:
            raise MoonshotAPIError(
                "API key required. Set MOONSHOT_API_KEY env var or pass api_key parameter."
            )

        self.base_url = base_url
        self.model = model
        self.max_tokens = max_tokens
        self.temperature = temperature

        # Initialize OpenAI client if requested and available
        self._use_openai_sdk = use_openai_sdk and OPENAI_AVAILABLE
        self._openai_client = None

        if self._use_openai_sdk:
            self._openai_client = OpenAI(
                api_key=self.api_key,
                base_url=self.base_url
            )

    def _is_image_file(self, file_path: str) -> bool:
        """Check if file is an image"""
        ext = Path(file_path).suffix.lower()
        image_exts = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.svg', '.tiff', '.tif', '.ico'}
        return ext in image_exts

    def _encode_image(self, file_path: str) -> tuple:
        """
        Encode image file to base64

        Returns:
            Tuple of (base64_data, mime_type)
        """
        if not os.path.exists(file_path):
            raise FileProcessingError(f"File not found: {file_path}")

        # Read file
        with open(file_path, "rb") as f:
            file_data = f.read()

        # Encode to base64
        base64_data = base64.b64encode(file_data).decode("utf-8")

        # Detect MIME type
        mime_type, _ = mimetypes.guess_type(file_path)
        if not mime_type:
            ext = Path(file_path).suffix.lower()
            mime_map = {
                '.jpg': 'image/jpeg',
                '.jpeg': 'image/jpeg',
                '.png': 'image/png',
                '.gif': 'image/gif',
                '.bmp': 'image/bmp',
                '.webp': 'image/webp',
                '.svg': 'image/svg+xml',
                '.tiff': 'image/tiff',
                '.tif': 'image/tiff',
                '.ico': 'image/x-icon',
            }
            mime_type = mime_map.get(ext, 'image/jpeg')

        return base64_data, mime_type

    def _prepare_image_content(self, file_path: str) -> dict:
        """Prepare image content for API request"""
        base64_data, mime_type = self._encode_image(file_path)

        return {
            "type": "image_url",
            "image_url": {
                "url": f"data:{mime_type};base64,{base64_data}"
            }
        }

    def _upload_file(self, file_path: str) -> str:
        """
        Upload a file to Moonshot API and return file_id

        Args:
            file_path: Path to the file

        Returns:
            file_id for use in API requests
        """
        if not os.path.exists(file_path):
            raise FileProcessingError(f"File not found: {file_path}")

        # Use requests to upload file
        headers = {
            "Authorization": f"Bearer {self.api_key}"
        }

        with open(file_path, "rb") as f:
            files = {"file": (os.path.basename(file_path), f)}
            response = requests.post(
                f"{self.base_url}/files",
                headers=headers,
                files=files,
                timeout=120
            )

        if response.status_code != 200:
            raise MoonshotAPIError(
                f"File upload failed: {response.text}",
                status_code=response.status_code
            )

        result = response.json()
        return result.get("id")

    def _get_file_content(self, file_id: str) -> str:
        """Get file content from uploaded file"""
        headers = {
            "Authorization": f"Bearer {self.api_key}"
        }

        response = requests.get(
            f"{self.base_url}/files/{file_id}/content",
            headers=headers,
            timeout=120
        )

        if response.status_code != 200:
            raise MoonshotAPIError(
                f"Failed to get file content: {response.text}",
                status_code=response.status_code
            )

        return response.json().get("content", "")

    def _make_api_request(
        self,
        messages: List[Dict],
        model: Optional[str] = None,
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None
    ) -> str:
        """Make API request using OpenAI SDK or requests"""

        if self._use_openai_sdk:
            response = self._openai_client.chat.completions.create(
                model=model or self.model,
                messages=messages,
                max_tokens=max_tokens or self.max_tokens,
                temperature=temperature or self.temperature
            )
            return response.choices[0].message.content
        else:
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}"
            }

            payload = {
                "model": model or self.model,
                "messages": messages,
                "max_tokens": max_tokens or self.max_tokens,
                "temperature": temperature or self.temperature
            }

            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=payload,
                timeout=120
            )

            if response.status_code == 200:
                result = response.json()
                return result["choices"][0]["message"]["content"]
            else:
                raise MoonshotAPIError(
                    f"API request failed: {response.text}",
                    status_code=response.status_code
                )

    def analyze_file(
        self,
        file_path: str,
        prompt: str,
        system_prompt: Optional[str] = None,
        model: Optional[str] = None,
        **kwargs
    ) -> str:
        """
        Analyze a file with a text prompt

        Args:
            file_path: Path to the file to analyze
            prompt: Analysis prompt/question
            system_prompt: Optional system prompt
            model: Model to use
            **kwargs: Additional parameters (max_tokens, temperature)

        Returns:
            Analysis result as string
        """
        # Check if file is an image
        if self._is_image_file(file_path):
            # For images, use base64 encoding
            return self._analyze_image_file(
                file_path, prompt, system_prompt, model, **kwargs
            )
        else:
            # For documents, use file upload API
            return self._analyze_document_file(
                file_path, prompt, system_prompt, model, **kwargs
            )

    def _analyze_image_file(
        self,
        file_path: str,
        prompt: str,
        system_prompt: Optional[str] = None,
        model: Optional[str] = None,
        **kwargs
    ) -> str:
        """Analyze an image file using base64 encoding"""
        messages = []

        if system_prompt:
            messages.append({
                "role": "system",
                "content": system_prompt
            })

        # Add image and prompt as user message
        image_content = self._prepare_image_content(file_path)
        messages.append({
            "role": "user",
            "content": [
                image_content,
                {"type": "text", "text": prompt}
            ]
        })

        return self._make_api_request(
            messages=messages,
            model=model,
            max_tokens=kwargs.get('max_tokens'),
            temperature=kwargs.get('temperature')
        )

    def _analyze_document_file(
        self,
        file_path: str,
        prompt: str,
        system_prompt: Optional[str] = None,
        model: Optional[str] = None,
        **kwargs
    ) -> str:
        """Analyze a document file using file upload API"""
        # Upload file first
        file_id = self._upload_file(file_path)

        messages = []

        if system_prompt:
            messages.append({
                "role": "system",
                "content": system_prompt
            })

        # Add file reference and prompt
        messages.append({
            "role": "user",
            "content": prompt  # File content will be automatically included
        })

        # For file-based analysis, we need to use a different approach
        # Kimi API supports file_id in the content, but this varies by API version
        # Let's use the file content approach
        file_content = self._get_file_content(file_id)

        # Replace the last message with combined content
        messages[-1] = {
            "role": "user",
            "content": f"Document content:\n{file_content}\n\n{prompt}"
        }

        return self._make_api_request(
            messages=messages,
            model=model,
            max_tokens=kwargs.get('max_tokens'),
            temperature=kwargs.get('temperature')
        )

    def analyze_files(
        self,
        file_paths: List[str],
        prompt: str,
        system_prompt: Optional[str] = None,
        model: Optional[str] = None,
        output_file: Optional[str] = None,
        **kwargs
    ) -> List[AnalysisResult]:
        """
        Analyze multiple files with the same prompt

        Args:
            file_paths: List of file paths
            prompt: Analysis prompt
            system_prompt: Optional system prompt
            model: Model to use
            output_file: Optional file to save results (JSON format)
            **kwargs: Additional parameters

        Returns:
            List of AnalysisResult objects
        """
        results = []

        for i, file_path in enumerate(file_paths):
            print(f"Analyzing {i+1}/{len(file_paths)}: {file_path}")

            try:
                analysis = self.analyze_file(
                    file_path=file_path,
                    prompt=prompt,
                    system_prompt=system_prompt,
                    model=model,
                    **kwargs
                )
                results.append(AnalysisResult(
                    file=file_path,
                    analysis=analysis,
                    success=True
                ))
            except Exception as e:
                results.append(AnalysisResult(
                    file=file_path,
                    analysis="",
                    success=False,
                    error=str(e)
                ))

        # Save to file if requested
        if output_file:
            output_data = {
                "results": [
                    {
                        "file": r.file,
                        "analysis": r.analysis,
                        "success": r.success,
                        "error": r.error
                    }
                    for r in results
                ]
            }
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(output_data, f, ensure_ascii=False, indent=2)
            print(f"Results saved to: {output_file}")

        return results

    def chat(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None,
        **kwargs
    ) -> str:
        """
        Send a chat completion request

        Args:
            messages: List of message dicts with 'role' and 'content'
            model: Model to use
            max_tokens: Max tokens in response
            temperature: Sampling temperature
            **kwargs: Additional parameters

        Returns:
            Response text
        """
        return self._make_api_request(
            messages=messages,
            model=model,
            max_tokens=max_tokens,
            temperature=temperature
        )

    def extract_structured_data(
        self,
        file_path: str,
        schema: Dict[str, Any],
        document_type: str = "document",
        model: Optional[str] = None,
        **kwargs
    ) -> Dict:
        """
        Extract structured data from a file

        Args:
            file_path: Path to the file
            schema: Dictionary describing expected data structure
            document_type: Type of document for context
            model: Model to use
            **kwargs: Additional parameters

        Returns:
            Dictionary with extracted data
        """
        schema_json = json.dumps(schema, ensure_ascii=False, indent=2)

        prompt = f"""Please analyze this {document_type} and extract structured data.

Extract the data according to this schema:
```json
{schema_json}
```

Return ONLY a valid JSON object matching the schema structure. Do not include any explanatory text before or after the JSON."""

        system_prompt = "You are a data extraction specialist. Always return valid JSON."

        result = self.analyze_file(
            file_path=file_path,
            prompt=prompt,
            system_prompt=system_prompt,
            model=model,
            **kwargs
        )

        # Try to parse JSON from the result
        try:
            # Find JSON in the response
            json_start = result.find("{")
            json_end = result.rfind("}")
            if json_start != -1 and json_end != -1:
                json_str = result[json_start:json_end + 1]
                return json.loads(json_str)
            else:
                return {"error": "No JSON found in response", "raw_response": result}
        except json.JSONDecodeError as e:
            return {"error": f"JSON parse error: {str(e)}", "raw_response": result}


def create_client(**kwargs) -> MoonshotClient:
    """
    Factory function to create a MoonshotClient

    Args:
        **kwargs: Arguments for MoonshotClient

    Returns:
        Configured MoonshotClient instance
    """
    return MoonshotClient(**kwargs)
