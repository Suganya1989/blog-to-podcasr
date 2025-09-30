# Project: AI Blog → Podcast

## Goal

Given a blog URL or pasted text, produce:

1. a concise outline (title, hook, 3–5 sections, CTA)
2. a **host-style** script with **SSML** suitable for TTS
3. keep pacing ~150–170 wpm, short sentences, small pauses `<break time="300ms"/>`.

## Voice and SSML

- Default English (India-neutral) tone unless asked otherwise.
- Mark emphasized terms with `<emphasis level="moderate">` where useful.
- Split long content into 3–8 segments. Each segment should be **valid standalone SSML** with its own `<speak>` root.
- Do **not** include audio tags; we synthesize externally.

## Output format (JSON)

Return only valid JSON with keys:
{
"title": "string",
"hook": "1-2 sentences",
"sections": ["...", "..."],
"cta": "one sentence",
"segments": [
{"filename": "seg-001.mp3", "ssml": "<speak>...</speak>"},
{"filename": "seg-002.mp3", "ssml": "<speak>...</speak>"}
]
}

## Example segment SSML

<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis">
  <p>Welcome to our show.<break time="300ms"/></p>
  <p>Today we explore …</p>
</speak>

## Style

Friendly host, clear signposting between sections, avoid overlong paragraphs.
