# SSML Command

## Command Name
`ssml`

## Description
Run the SSML Specialist Agent to convert article text into podcast script with SSML markup.

## Usage
```bash
claude ssml --text <article-text>
claude ssml --text-file <path-to-file>
claude ssml --text-file <path> --output <json-file>
```

## Options
- `--text` - Article text as direct input
- `--text-file` - Path to text file containing article
- `--output` - Save podcast plan to JSON file (optional)

## Examples
```bash
# Generate SSML from text
claude ssml --text "Your article content..."

# Generate from file
claude ssml --text-file article.txt

# Generate and save podcast plan
claude ssml --text-file article.txt --output podcast.json
```

## Agent Used
**SSML Specialist Agent** (`.claude/agents/ssml-specialist.md`)

This agent internally uses the Content Analyzer Agent first.

## Output
Podcast plan JSON containing:
- `title` - Podcast episode title
- `hook` - Opening hook (1-2 sentences)
- `sections` - Array of section summaries
- `cta` - Call-to-action
- `segments` - Array of SSML segments with:
  - `filename` - Segment filename (e.g., "seg-001.mp3")
  - `ssml` - SSML markup ready for TTS