# Analyze Command

## Command Name
`analyze`

## Description
Run the Content Analyzer Agent to analyze article structure and generate insights.

## Usage
```bash
claude analyze --text <article-text>
claude analyze --text-file <path-to-file>
claude analyze --text-file <path> --output <json-file>
```

## Options
- `--text` - Article text as direct input
- `--text-file` - Path to text file containing article
- `--output` - Save analysis to JSON file (optional)

## Examples
```bash
# Analyze text directly
claude analyze --text "Your article content..."

# Analyze from file
claude analyze --text-file article.txt

# Analyze and save results
claude analyze --text-file article.txt --output analysis.json
```

## Agent Used
**Content Analyzer Agent** (`.claude/agents/content-analyzer.md`)

## Output
Analysis JSON containing:
- `word_count` - Total word count
- `estimated_reading_time` - Reading time in minutes
- `suggested_segments` - Recommended number of segments
- `content_preview` - First 200 characters
- `recommendation` - Suitability assessment