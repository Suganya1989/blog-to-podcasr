---
description: Run complete blog-to-podcast pipeline with automatic orchestration
argument-hint: <url>
allowed-tools: Task(*)
---

Run the complete blog-to-podcast conversion pipeline for URL: $ARGUMENTS

Execute all agents in sequence automatically without user intervention:

**Agent Flow:**
1. **Web Scraper Agent** - Extract content from URL (handle PDFs, web pages)
2. **Content Analyzer Agent** - Analyze structure and generate insights
3. **SSML Specialist Agent** - Generate podcast script with SSML markup
4. **Audio Producer Agent** - Create MP3 segments and final podcast

**Configuration:**
- Voice: alloy (OpenAI TTS)
- Provider: OpenAI
- Output directory: audio/

**Tasks:**
1. Use Task tool to launch Web Scraper Agent to extract content from the URL
2. Save extracted content to `extracted_content.json`
3. Use Task tool to launch Content Analyzer Agent on the extracted content
4. Save analysis to `analysis.json`
5. Use Task tool to launch SSML Specialist Agent to generate podcast plan
6. Save podcast plan to `podcast_plan.json`
7. Use Task tool to launch Audio Producer Agent to generate audio files
8. Save segments to `audio/segments/` and final podcast to `audio/podcast.mp3`

**Output:**
Display execution log showing:
- Each agent's status (success/failure)
- Files created
- Final podcast location and duration
- Any errors encountered

All intermediate files should be saved for debugging and reuse.