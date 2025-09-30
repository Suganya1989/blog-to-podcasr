from __future__ import annotations
import os, json
from anthropic import Anthropic

SYSTEM_PROMPT = """You are a senior audio producer who converts articles into podcast scripts with SSML.
Follow the CLAUDE.md rules strictly and return only JSON as specified."""

def blog_to_podcast_json(article_text: str) -> dict:
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError("ANTHROPIC_API_KEY not set")
    client = Anthropic(api_key=api_key)

    user_prompt = f"""Convert the following article/text into a podcast per CLAUDE.md requirements.

Return ONLY valid JSON with this exact structure:
{{
"title": "string",
"hook": "1-2 sentences",
"sections": ["...", "..."],
"cta": "one sentence",
"segments": [
{{"filename": "seg-001.mp3", "ssml": "<speak>...</speak>"}},
{{"filename": "seg-002.mp3", "ssml": "<speak>...</speak>"}}
]
}}

Split the content into 3-8 segments. Each segment should be valid standalone SSML with <speak> root.
Use short sentences, ~150-170 wpm pacing, add <break time="300ms"/> for pauses.

ARTICLE START
{article_text[:120000]}
ARTICLE END
"""

    resp = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=4000,
        temperature=0.4,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_prompt}],
    )

    content = "".join([blk.text for blk in resp.content if hasattr(blk, "text")])
    # Try to locate JSON (in case model adds stray text)
    start = content.find("{")
    end = content.rfind("}")
    if start == -1 or end == -1:
        raise ValueError("Claude did not return JSON")
    data = json.loads(content[start:end+1])
    # minimal sanity checks
    assert "segments" in data and isinstance(data["segments"], list) and data["segments"], "no segments returned"
    return data
