#!/usr/bin/env python3
"""
Debug Claude response to understand what it's returning
"""

from dotenv import load_dotenv
import os
import json
from anthropic import Anthropic

load_dotenv()

def debug_claude_response():
    """Debug what Claude is actually returning."""

    SYSTEM_PROMPT = """You are a senior audio producer who converts articles into podcast scripts with SSML.
Follow the CLAUDE.md rules strictly and return only JSON as specified."""

    sample_text = """
    Welcome to Modern AI Development

    Artificial Intelligence is transforming how we build software. In this post,
    we'll explore three key trends: machine learning automation, natural language
    processing, and computer vision applications.
    """

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("Error: ANTHROPIC_API_KEY not set")
        return

    client = Anthropic(api_key=api_key)

    user_prompt = f"""Convert the following article/text into a podcast per CLAUDE.md.
Return only the JSON schema described there.

ARTICLE START
{sample_text}
ARTICLE END
"""

    print("Sending request to Claude...")
    resp = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=4000,
        temperature=0.4,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_prompt}],
    )

    content = "".join([blk.text for blk in resp.content if hasattr(blk, "text")])

    print("Raw Claude Response:")
    print("=" * 50)
    print(content)
    print("=" * 50)

    # Try to extract JSON
    start = content.find("{")
    end = content.rfind("}")
    if start == -1 or end == -1:
        print("Error: No JSON found in response")
        return

    json_str = content[start:end+1]
    print("\nExtracted JSON:")
    print(json_str)

    try:
        data = json.loads(json_str)
        print("\nParsed successfully!")
        print(f"Keys: {list(data.keys())}")
        if "segments" in data:
            print(f"Number of segments: {len(data.get('segments', []))}")
        else:
            print("Warning: No 'segments' key found")
    except json.JSONDecodeError as e:
        print(f"\nJSON parse error: {e}")

if __name__ == "__main__":
    debug_claude_response()