# Blog-to-Podcast: AI-Powered Agentic Workflow

Convert any blog post or article into a professional podcast using an AI-powered multi-agent system. This project uses Claude Code's agentic architecture to orchestrate web scraping, content analysis, SSML generation, and audio production.

## 🎯 Overview

Give it a URL, get a podcast. The system automatically:
- 📄 Extracts content from blogs and PDFs
- 🔍 Analyzes structure and generates insights
- 🎙️ Creates host-style scripts with SSML markup
- 🔊 Produces professional MP3 audio files

## 🏗️ Architecture

This project uses **4 specialized AI agents** working in sequence:

```
URL Input → [Agent 1] → [Agent 2] → [Agent 3] → [Agent 4] → Podcast MP3
```

### Agent Workflow

#### 1. **Web Scraper Agent** 🌐
**Role:** Extract clean content from any URL

**Capabilities:**
- Handles web pages and PDF documents
- Uses `trafilatura` for article extraction
- Falls back to `BeautifulSoup` for HTML parsing
- Supports PDF extraction with `PyPDF2`

**Output:** `extracted_content.json`
```json
{
  "url": "https://...",
  "character_count": 20247,
  "word_count": 3087,
  "full_text": "..."
}
```

---

#### 2. **Content Analyzer Agent** 🔍
**Role:** Analyze content structure for podcast optimization

**Capabilities:**
- Identifies main topics and key themes
- Calculates optimal podcast duration (150-170 WPM)
- Suggests segment breakpoints (2-4 min each)
- Recommends tone and pacing

**Output:** `analysis.json`
```json
{
  "word_count": 3087,
  "estimated_podcast_duration": "18-21 minutes",
  "suggested_segments": 6,
  "content_summary": "...",
  "key_topics": ["topic1", "topic2", ...],
  "suitability_for_podcast": "assessment"
}
```

---

#### 3. **SSML Specialist Agent** 📝
**Role:** Generate podcast script with Speech Synthesis Markup Language

**Capabilities:**
- Converts text to podcast-friendly narration
- Adds SSML markup for natural speech
- Uses `<break time="300ms"/>` for pauses
- Applies `<emphasis level="moderate">` for key terms
- Creates 3-8 standalone segments

**Output:** `podcast_plan.json`
```json
{
  "title": "Episode Title",
  "hook": "Opening hook (1-2 sentences)",
  "sections": ["Section 1", "Section 2", ...],
  "cta": "Call to action",
  "segments": [
    {
      "filename": "seg-001.mp3",
      "ssml": "<speak>...</speak>"
    }
  ]
}
```

**SSML Features:**
- ✅ English (India-neutral) tone
- ✅ 150-170 WPM pacing
- ✅ Natural pauses and emphasis
- ✅ Valid XML structure
- ✅ TTS-optimized formatting

---

#### 4. **Audio Producer Agent** 🎵
**Role:** Generate MP3 audio from SSML scripts

**Capabilities:**
- Converts SSML to plain text for OpenAI TTS
- Calls OpenAI TTS API (model: `tts-1`, voice: `alloy`)
- Generates individual segment MP3 files
- Joins segments into final podcast
- Uses `pydub` for audio manipulation

**Output:**
```
audio/
├── segments/
│   ├── seg-001.mp3
│   ├── seg-002.mp3
│   └── ...
└── podcast.mp3  (Final combined podcast)
```

---

## 🚀 Quick Start

### Prerequisites
```bash
pip install openai trafilatura beautifulsoup4 requests pypdf2 pydub
```

### Usage

#### Option 1: Full Pipeline (Recommended)
Run the complete workflow with a single command:

```bash
/pipeline https://your-blog-url.com
```

**What it does:**
1. Scrapes content from URL
2. Analyzes structure
3. Generates SSML script
4. Produces MP3 audio

**Example:**
```bash
/pipeline https://blog.example.com/ai-trends-2024
```

---

#### Option 2: Run Agents Individually

**Step 1: Scrape Content**
```bash
/scrape https://blog.example.com/article
```
Output: `extracted_content.json`

**Step 2: Analyze Content**
```bash
/analyze @extracted_content.json
```
Output: `analysis.json`

**Step 3: Generate SSML Script**
```bash
/ssml @extracted_content.json
```
Output: `podcast_plan.json`

**Step 4: Produce Audio**
```bash
/audio @podcast_plan.json --voice alloy
```
Output: `audio/podcast.mp3`

---

## 📁 Project Structure

```
blog-to-podcast/
├── .claude/
│   ├── agents/              # Agent definitions
│   │   ├── web-scraper.md
│   │   ├── content-analyzer.md
│   │   ├── ssml-specialist.md
│   │   └── audio-producer.md
│   └── commands/            # Slash commands
│       ├── pipeline.md      # Full workflow
│       ├── scrape.md
│       ├── analyze.md
│       ├── ssml.md
│       └── audio.md
├── audio/                   # Generated audio files
│   ├── segments/
│   └── podcast.mp3
├── extracted_content.json   # Scraped content
├── analysis.json           # Content analysis
├── podcast_plan.json       # SSML script
├── scrape.py              # Web scraping utilities
├── cli.py                 # Command-line interface
└── requirements.txt       # Python dependencies
```

---

## 🎛️ Configuration

### Voice Options

**OpenAI TTS Voices:**
- `alloy` (default) - Neutral, clear
- `echo` - Male, clear
- `fable` - British accent
- `onyx` - Deep male
- `nova` - Female, warm
- `shimmer` - Female, bright

**Change voice:**
```bash
/audio @podcast_plan.json --voice nova
```

### SSML Customization

Edit `CLAUDE.md` to customize:
- Pacing (default: 150-170 WPM)
- Tone (default: English India-neutral)
- Break timing (default: 300ms)
- Emphasis levels

---

## 🔧 How It Works

### Agent Orchestration

The `/pipeline` command uses Claude Code's **Task tool** to launch agents:

```markdown
1. Task(Web Scraper Agent) → Extract content
2. Save to extracted_content.json
3. Task(Content Analyzer Agent) → Analyze content
4. Save to analysis.json
5. Task(SSML Specialist Agent) → Generate script
6. Save to podcast_plan.json
7. Task(Audio Producer Agent) → Produce audio
8. Save to audio/podcast.mp3
```

**Key Features:**
- ✅ Fully autonomous execution
- ✅ No user intervention required
- ✅ Intermediate files saved for debugging
- ✅ Error handling and recovery
- ✅ Execution logs with status tracking

---

## 📊 Example Output

**Input URL:**
```
https://rm.coe.int/european-prison-rules-978-92-871-5982-3/16806ab9af
```

**Pipeline Execution:**
```
✅ Agent 1: Web Scraper
   - Extracted: 20,529 characters (3,087 words)
   - Output: extracted_content.json

✅ Agent 2: Content Analyzer
   - Duration: 18-21 minutes
   - Segments: 6 recommended
   - Output: analysis.json

✅ Agent 3: SSML Specialist
   - Generated: 6 SSML segments
   - Title: "Transforming Justice..."
   - Output: podcast_plan.json

✅ Agent 4: Audio Producer
   - Generated: 6 MP3 segments
   - Final: audio/podcast.mp3 (14.5 MB, ~10.5 min)
   - Voice: alloy (OpenAI TTS)
```

---

## 🛠️ Advanced Usage

### Custom Agent Behavior

Agents are defined in `.claude/agents/*.md` files. Modify them to:
- Change extraction strategies
- Adjust analysis criteria
- Customize SSML patterns
- Configure audio settings

### Command Customization

Commands are in `.claude/commands/*.md`. Each uses:
```yaml
---
description: Command description
argument-hint: <url>
allowed-tools: Task(*)
---
```

### Error Handling

Each agent handles specific errors:
- **Web Scraper:** Network timeouts, PDF decoding
- **Content Analyzer:** Invalid content format
- **SSML Specialist:** XML validation
- **Audio Producer:** API rate limits, file I/O

---

## 📝 SSML Format

### Example Segment
```xml
<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis">
  <p>Welcome to the podcast.<break time="300ms"/></p>
  <p>Today we explore <emphasis level="moderate">AI trends</emphasis>.</p>
  <p>Let's dive in.<break time="500ms"/></p>
</speak>
```

### Markup Reference
- `<p>` - Paragraph (natural pause)
- `<break time="300ms"/>` - Short pause
- `<break time="500ms"/>` - Section transition
- `<emphasis level="moderate">` - Emphasized term
- `<prosody rate="95%">` - Slightly slower (for quotes)

---

## 🔌 API Requirements

### OpenAI API
Set your API key:
```bash
export OPENAI_API_KEY='your-api-key-here'
```

Or create `.env`:
```
OPENAI_API_KEY=your-api-key-here
```

---

## 🤝 Contributing

This is an agentic architecture project. To add features:

1. **Create new agent:** Add `.claude/agents/your-agent.md`
2. **Create command:** Add `.claude/commands/your-command.md`
3. **Update pipeline:** Modify `pipeline.md` to include new agent

---

## 📄 License

MIT License - See LICENSE file for details

---

## 🎉 Credits

Built with:
- [Claude Code](https://claude.ai/claude-code) - AI development environment
- [OpenAI TTS](https://platform.openai.com/docs/guides/text-to-speech) - Text-to-speech API
- [Trafilatura](https://trafilatura.readthedocs.io/) - Web scraping
- [PyPDF2](https://pypdf2.readthedocs.io/) - PDF extraction
- [pydub](https://github.com/jiaaro/pydub) - Audio processing

---

**Made with ❤️ using AI agents**
