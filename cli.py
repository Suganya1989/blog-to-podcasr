#!/usr/bin/env python3
"""
CLI interface for blog-to-podcast agentic workflow.
Allows triggering individual agents or full pipeline via command line.

Usage: claude <command> [options]

Commands are defined in .claude/commands/*.md
Agents are defined in .claude/agents/*.md
"""
from __future__ import annotations
import argparse
import sys
import json
from pathlib import Path
from agents import (
    PodcastOrchestrator,
    WebScraperAgent,
    ContentAnalyzerAgent,
    SSMLSpecialistAgent,
    AudioProducerAgent
)


def run_web_scraper(url: str):
    """Run Web Scraper Agent standalone."""
    print(f"🌐 Running Web Scraper Agent on: {url}")
    result = WebScraperAgent.execute(url)

    if result.success:
        print(f"✅ Success! Extracted {result.data['length']} characters")
        print(f"Preview: {result.data['content'][:200]}...")
        return result.data
    else:
        print(f"❌ Failed: {result.error}")
        sys.exit(1)


def run_content_analyzer(text: str):
    """Run Content Analyzer Agent standalone."""
    print(f"🔍 Running Content Analyzer Agent...")
    result = ContentAnalyzerAgent.execute(text)

    if result.success:
        print(f"✅ Analysis Complete:")
        print(json.dumps(result.data, indent=2))
        return result.data
    else:
        print(f"❌ Failed: {result.error}")
        sys.exit(1)


def run_ssml_specialist(text: str, analysis: dict = None):
    """Run SSML Specialist Agent standalone."""
    print(f"📝 Running SSML Specialist Agent...")

    if analysis is None:
        # Run analyzer first
        analyzer_result = ContentAnalyzerAgent.execute(text)
        if not analyzer_result.success:
            print(f"❌ Analysis failed: {analyzer_result.error}")
            sys.exit(1)
        analysis = analyzer_result.data

    result = SSMLSpecialistAgent.execute(text, analysis)

    if result.success:
        print(f"✅ Generated {len(result.data['segments'])} SSML segments")
        print(f"Title: {result.data['title']}")
        return result.data
    else:
        print(f"❌ Failed: {result.error}")
        sys.exit(1)


def run_audio_producer(podcast_plan: dict, voice: str, use_openai: bool = True):
    """Run Audio Producer Agent standalone."""
    print(f"🎵 Running Audio Producer Agent...")
    print(f"Voice: {voice}")
    print(f"Provider: {'OpenAI' if use_openai else 'ElevenLabs'}")

    result = AudioProducerAgent.execute(
        podcast_plan["segments"],
        "audio/segments",
        "audio/podcast.mp3",
        voice,
        use_openai=use_openai
    )

    if result.success:
        print(f"✅ Audio Production Complete!")
        print(f"Segments: {result.data['segment_count']}")
        print(f"Final podcast: {result.data['final_podcast']}")
        return result.data
    else:
        print(f"❌ Failed: {result.error}")
        sys.exit(1)


def run_full_pipeline(url: str = None, text: str = None, voice: str = "alloy", use_openai: bool = True):
    """Run complete pipeline with orchestrator."""
    orchestrator = PodcastOrchestrator()

    print("🤖 Running Full Agentic Pipeline")
    print("=" * 50)

    if url:
        print(f"Source: {url}")
        result = orchestrator.from_url(url, voice, use_openai=use_openai)
    elif text:
        print(f"Source: Text input ({len(text)} chars)")
        result = orchestrator.from_text(text, voice, use_openai=use_openai)
    else:
        print("❌ Error: Must provide either --url or --text")
        sys.exit(1)

    # Display execution log
    print("\n📋 Execution Log:")
    for log_entry in result["execution_log"]:
        icon = "✅" if log_entry["success"] else "❌"
        print(f"{icon} {log_entry['agent']}: {log_entry['step']}")
        if log_entry.get("error"):
            print(f"   Error: {log_entry['error']}")

    if result["success"]:
        print("\n🎉 Pipeline Complete!")
        print(f"Final podcast: {result['data']['audio']['final_podcast']}")
        return result
    else:
        print(f"\n❌ Pipeline Failed: {result.get('error')}")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="Blog-to-Podcast Agentic CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run full pipeline from URL
  python cli.py pipeline --url https://blog.example.com/article

  # Run full pipeline from text file
  python cli.py pipeline --text-file article.txt --voice nova

  # Run individual agents
  python cli.py scrape --url https://blog.example.com/article
  python cli.py analyze --text "Your article text here"
  python cli.py ssml --text "Your article text here"
  python cli.py audio --podcast-file podcast.json --voice alloy

  # Use ElevenLabs instead of OpenAI
  python cli.py pipeline --url https://example.com --provider elevenlabs --voice "voice-id-here"
        """
    )

    subparsers = parser.add_subparsers(dest="command", help="Agent command")

    # Full pipeline command
    pipeline_parser = subparsers.add_parser("pipeline", help="Run complete pipeline")
    pipeline_parser.add_argument("--url", help="Blog URL to convert")
    pipeline_parser.add_argument("--text", help="Article text directly")
    pipeline_parser.add_argument("--text-file", help="Path to text file")
    pipeline_parser.add_argument("--voice", default="alloy", help="Voice name/ID")
    pipeline_parser.add_argument("--provider", choices=["openai", "elevenlabs"], default="openai")

    # Web scraper command
    scrape_parser = subparsers.add_parser("scrape", help="Run Web Scraper Agent")
    scrape_parser.add_argument("--url", required=True, help="Blog URL to scrape")
    scrape_parser.add_argument("--output", help="Save content to file")

    # Content analyzer command
    analyze_parser = subparsers.add_parser("analyze", help="Run Content Analyzer Agent")
    analyze_parser.add_argument("--text", help="Article text")
    analyze_parser.add_argument("--text-file", help="Path to text file")
    analyze_parser.add_argument("--output", help="Save analysis to JSON file")

    # SSML specialist command
    ssml_parser = subparsers.add_parser("ssml", help="Run SSML Specialist Agent")
    ssml_parser.add_argument("--text", help="Article text")
    ssml_parser.add_argument("--text-file", help="Path to text file")
    ssml_parser.add_argument("--output", help="Save podcast plan to JSON file")

    # Audio producer command
    audio_parser = subparsers.add_parser("audio", help="Run Audio Producer Agent")
    audio_parser.add_argument("--podcast-file", required=True, help="Path to podcast JSON file")
    audio_parser.add_argument("--voice", default="alloy", help="Voice name/ID")
    audio_parser.add_argument("--provider", choices=["openai", "elevenlabs"], default="openai")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    # Handle commands
    if args.command == "pipeline":
        text_input = None
        if args.text:
            text_input = args.text
        elif args.text_file:
            text_input = Path(args.text_file).read_text()

        use_openai = args.provider == "openai"
        run_full_pipeline(
            url=args.url,
            text=text_input,
            voice=args.voice,
            use_openai=use_openai
        )

    elif args.command == "scrape":
        data = run_web_scraper(args.url)
        if args.output:
            Path(args.output).write_text(data["content"])
            print(f"💾 Saved to {args.output}")

    elif args.command == "analyze":
        text_input = args.text or Path(args.text_file).read_text()
        data = run_content_analyzer(text_input)
        if args.output:
            Path(args.output).write_text(json.dumps(data, indent=2))
            print(f"💾 Saved to {args.output}")

    elif args.command == "ssml":
        text_input = args.text or Path(args.text_file).read_text()
        data = run_ssml_specialist(text_input)
        if args.output:
            Path(args.output).write_text(json.dumps(data, indent=2))
            print(f"💾 Saved to {args.output}")

    elif args.command == "audio":
        podcast_plan = json.loads(Path(args.podcast_file).read_text())
        use_openai = args.provider == "openai"
        run_audio_producer(podcast_plan, args.voice, use_openai=use_openai)


if __name__ == "__main__":
    main()