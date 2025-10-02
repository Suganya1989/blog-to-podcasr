#!/usr/bin/env python3
"""
Intelligent Claude AI CLI - Self-modifying agentic system
Interprets natural language commands, generates missing code/agents, and executes tasks.

Usage: python claude_ai.py "convert this blog to podcast: https://example.com"
"""
from __future__ import annotations
import os
import sys
import json
from pathlib import Path
from anthropic import Anthropic
from agents import PodcastOrchestrator
from dotenv import load_dotenv

load_dotenv()


class ClaudeAI:
    """Intelligent CLI that can interpret commands and generate missing components."""

    def __init__(self):
        self.client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
        self.orchestrator = PodcastOrchestrator()
        self.agents_dir = Path(".claude/agents")
        self.commands_dir = Path(".claude/commands")

    def interpret_command(self, user_input: str) -> dict:
        """Use Claude to interpret the user's natural language command."""

        system_prompt = """You are an intelligent CLI interpreter for a blog-to-podcast system.

Your job is to interpret user commands and determine:
1. What they want to do
2. What parameters are needed
3. Whether any new agents or code need to be created

Available commands:
- pipeline: Full blog-to-podcast conversion
- scrape: Extract content from URL
- analyze: Analyze content structure
- ssml: Generate podcast script
- audio: Produce audio files

Available agents:
- WebScraperAgent
- ContentAnalyzerAgent
- SSMLSpecialistAgent
- AudioProducerAgent
- PodcastOrchestrator

Return ONLY valid JSON with this structure:
{
    "intent": "pipeline|scrape|analyze|ssml|audio|custom",
    "parameters": {
        "url": "...",
        "text": "...",
        "voice": "alloy",
        "provider": "openai"
    },
    "needs_generation": false,
    "generation_request": ""
}"""

        response = self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1000,
            system=system_prompt,
            messages=[{
                "role": "user",
                "content": f"Interpret this command: {user_input}"
            }]
        )

        content = response.content[0].text
        # Extract JSON
        start = content.find("{")
        end = content.rfind("}") + 1
        return json.loads(content[start:end])

    def generate_missing_component(self, request: str):
        """Use Claude to generate missing agents or code."""

        system_prompt = """You are a code generation AI that creates Python agents and code.
Generate clean, production-ready code based on the user's request.
Follow the existing agent patterns in the codebase."""

        response = self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=3000,
            system=system_prompt,
            messages=[{
                "role": "user",
                "content": f"Generate code for: {request}"
            }]
        )

        return response.content[0].text

    def execute_pipeline(self, url: str = None, text: str = None, voice: str = "alloy", provider: str = "openai"):
        """Execute the full blog-to-podcast pipeline."""

        print("[PIPELINE] Starting Intelligent Blog-to-Podcast Pipeline")
        print("=" * 60)

        use_openai = provider == "openai"

        if url:
            print(f"[SOURCE] URL: {url}")
            print(f"[VOICE] {voice} ({provider})")
            print()

            result = self.orchestrator.from_url(url, voice, use_openai=use_openai)
        elif text:
            print(f"[SOURCE] Text input ({len(text)} chars)")
            print(f"[VOICE] {voice} ({provider})")
            print()

            result = self.orchestrator.from_text(text, voice, use_openai=use_openai)
        else:
            print("[ERROR] Need either URL or text")
            return False

        # Display execution log
        print("\n[AGENTS] Execution Log:")
        print("-" * 60)
        for log_entry in result["execution_log"]:
            icon = "[+]" if log_entry["success"] else "[-]"
            print(f"{icon} {log_entry['agent']}: {log_entry['step']}")
            if log_entry.get("error"):
                print(f"    [!] Error: {log_entry['error']}")

        if result["success"]:
            print("\n" + "=" * 60)
            print("[SUCCESS] Podcast created!")
            print("=" * 60)

            data = result["data"]
            plan = data.get("podcast_plan", data.get("podcast_plan"))

            print(f"\n[DETAILS] Podcast Information:")
            print(f"   Title: {plan.get('title', 'N/A')}")
            print(f"   Segments: {len(plan.get('segments', []))}")
            print(f"   Audio: {data['audio']['final_podcast']}")
            print(f"   Provider: {data['audio']['tts_provider']}")

            return True
        else:
            print(f"\n[ERROR] Pipeline Failed: {result.get('error')}")
            return False

    def run(self, user_input: str):
        """Main entry point - interprets and executes user commands."""

        try:
            # Interpret the command
            print("[*] Interpreting your command...")
            interpretation = self.interpret_command(user_input)

            print(f"[+] Intent: {interpretation['intent']}")

            # Check if we need to generate something
            if interpretation.get("needs_generation"):
                print(f"[>] Generating: {interpretation['generation_request']}")
                code = self.generate_missing_component(interpretation['generation_request'])
                print("[+] Code generated!")
                print(code)
                return

            # Execute the command
            params = interpretation.get("parameters", {})

            if interpretation["intent"] == "pipeline":
                return self.execute_pipeline(
                    url=params.get("url"),
                    text=params.get("text"),
                    voice=params.get("voice", "alloy"),
                    provider=params.get("provider", "openai")
                )
            else:
                print(f"[!] Command '{interpretation['intent']}' not yet implemented")
                return False

        except Exception as e:
            print(f"[ERROR] {e}")
            import traceback
            traceback.print_exc()
            return False


def main():
    if len(sys.argv) < 2:
        print("""
Claude AI - Intelligent Blog-to-Podcast CLI

Usage:
    python claude_ai.py "your command in natural language"

Examples:
    python claude_ai.py "convert this blog to podcast: https://example.com/article"
    python claude_ai.py "make a podcast from this URL using nova voice: https://blog.com"
    python claude_ai.py "create a podcast with the following text: AI is transforming..."
    python claude_ai.py "convert https://example.com to audio with shimmer voice"

The AI will:
* Understand your natural language command
* Generate any missing agents or code
* Execute the blog-to-podcast conversion automatically
* Show you the execution log from all agents
        """)
        sys.exit(1)

    # Join all arguments as the command
    user_command = " ".join(sys.argv[1:])

    # Create and run the AI
    ai = ClaudeAI()
    success = ai.run(user_command)

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()