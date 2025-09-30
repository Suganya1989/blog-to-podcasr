"""
Simulated agent orchestration system for blog-to-podcast conversion.
Each function represents a specialized agent with specific responsibilities.
"""
from __future__ import annotations
import os
from typing import Dict, List, Any
from scrape import extract_from_url
from llm import blog_to_podcast_json


class AgentResult:
    """Result from an agent execution."""
    def __init__(self, success: bool, data: Any = None, error: str = None, agent_name: str = ""):
        self.success = success
        self.data = data
        self.error = error
        self.agent_name = agent_name

    def __repr__(self):
        return f"AgentResult(agent={self.agent_name}, success={self.success})"


class WebScraperAgent:
    """Specialized agent for web content extraction."""

    @staticmethod
    def execute(url: str) -> AgentResult:
        """Extract clean content from a blog URL."""
        try:
            content = extract_from_url(url)
            return AgentResult(
                success=True,
                data={"content": content, "source": url, "length": len(content)},
                agent_name="WebScraper"
            )
        except Exception as e:
            return AgentResult(
                success=False,
                error=str(e),
                agent_name="WebScraper"
            )


class ContentAnalyzerAgent:
    """Specialized agent for content analysis."""

    @staticmethod
    def execute(content: str) -> AgentResult:
        """Analyze content structure and extract insights."""
        try:
            # Basic analysis
            words = content.split()
            word_count = len(words)

            # Estimate reading time
            reading_time_minutes = word_count / 200  # Average reading speed

            # Suggested segments based on length
            suggested_segments = max(3, min(8, word_count // 300))

            analysis = {
                "word_count": word_count,
                "estimated_reading_time": f"{reading_time_minutes:.1f} minutes",
                "suggested_segments": suggested_segments,
                "content_preview": content[:200] + "..." if len(content) > 200 else content,
                "recommendation": "Content is suitable for podcast conversion"
            }

            return AgentResult(
                success=True,
                data=analysis,
                agent_name="ContentAnalyzer"
            )
        except Exception as e:
            return AgentResult(
                success=False,
                error=str(e),
                agent_name="ContentAnalyzer"
            )


class SSMLSpecialistAgent:
    """Specialized agent for SSML generation."""

    @staticmethod
    def execute(content: str, analysis: Dict) -> AgentResult:
        """Convert content to SSML segments using Claude."""
        try:
            # Use Claude to generate structured podcast plan with SSML
            podcast_data = blog_to_podcast_json(content)

            # Validate SSML structure
            if not podcast_data.get("segments"):
                raise ValueError("No SSML segments generated")

            return AgentResult(
                success=True,
                data=podcast_data,
                agent_name="SSMLSpecialist"
            )
        except Exception as e:
            return AgentResult(
                success=False,
                error=str(e),
                agent_name="SSMLSpecialist"
            )


class AudioProducerAgent:
    """Specialized agent for audio generation."""

    @staticmethod
    def execute(segments: List[Dict], out_dir: str, final_mp3: str, voice_id: str,
                use_openai: bool = False) -> AgentResult:
        """Generate audio segments and join into final podcast."""
        try:
            if use_openai:
                from tts_openai import synth_ssml_to_mp3_segments, join_segments_to_podcast
                # For OpenAI, voice_id is actually a voice name (alloy, echo, etc.)
                paths = synth_ssml_to_mp3_segments(segments, out_dir, voice_name=voice_id)
            else:
                from tts_windows import synth_ssml_to_mp3_segments, join_segments_to_podcast
                # For ElevenLabs, use voice_id
                paths = synth_ssml_to_mp3_segments(segments, out_dir, voice_id=voice_id)

            if not paths:
                raise ValueError("No audio segments were generated")

            # Join into final podcast
            final_path = join_segments_to_podcast(paths, final_mp3)

            return AgentResult(
                success=True,
                data={
                    "segment_count": len(paths),
                    "segment_paths": paths,
                    "final_podcast": final_path,
                    "tts_provider": "OpenAI" if use_openai else "ElevenLabs"
                },
                agent_name="AudioProducer"
            )
        except Exception as e:
            return AgentResult(
                success=False,
                error=str(e),
                agent_name="AudioProducer"
            )


class PodcastOrchestrator:
    """Main orchestrator that coordinates all agents."""

    def __init__(self):
        self.execution_log = []

    def log_step(self, step: str, result: AgentResult):
        """Log agent execution steps."""
        self.execution_log.append({
            "step": step,
            "agent": result.agent_name,
            "success": result.success,
            "error": result.error
        })

    def from_url(self, url: str, voice_id: str, out_dir: str = "audio/segments",
                 final_mp3: str = "audio/podcast.mp3", use_openai: bool = False) -> Dict[str, Any]:
        """
        Orchestrate complete blog-to-podcast pipeline from URL.

        Returns:
            Dict with keys: success, data, execution_log, error
        """
        self.execution_log = []

        # Step 1: Web Scraper Agent
        scraper_result = WebScraperAgent.execute(url)
        self.log_step("Extract content from URL", scraper_result)
        if not scraper_result.success:
            return {
                "success": False,
                "error": f"Web scraping failed: {scraper_result.error}",
                "execution_log": self.execution_log
            }

        content = scraper_result.data["content"]

        # Step 2: Content Analyzer Agent
        analyzer_result = ContentAnalyzerAgent.execute(content)
        self.log_step("Analyze content structure", analyzer_result)
        if not analyzer_result.success:
            return {
                "success": False,
                "error": f"Content analysis failed: {analyzer_result.error}",
                "execution_log": self.execution_log
            }

        # Step 3: SSML Specialist Agent
        ssml_result = SSMLSpecialistAgent.execute(content, analyzer_result.data)
        self.log_step("Generate SSML segments", ssml_result)
        if not ssml_result.success:
            return {
                "success": False,
                "error": f"SSML generation failed: {ssml_result.error}",
                "execution_log": self.execution_log
            }

        podcast_plan = ssml_result.data

        # Step 4: Audio Producer Agent
        audio_result = AudioProducerAgent.execute(
            podcast_plan["segments"],
            out_dir,
            final_mp3,
            voice_id,
            use_openai=use_openai
        )
        self.log_step("Generate and join audio", audio_result)
        if not audio_result.success:
            return {
                "success": False,
                "error": f"Audio production failed: {audio_result.error}",
                "execution_log": self.execution_log
            }

        # Success - return all data
        return {
            "success": True,
            "data": {
                "scraper": scraper_result.data,
                "analysis": analyzer_result.data,
                "podcast_plan": podcast_plan,
                "audio": audio_result.data
            },
            "execution_log": self.execution_log
        }

    def from_text(self, text: str, voice_id: str, out_dir: str = "audio/segments",
                  final_mp3: str = "audio/podcast.mp3", use_openai: bool = False) -> Dict[str, Any]:
        """
        Orchestrate complete blog-to-podcast pipeline from text.

        Returns:
            Dict with keys: success, data, execution_log, error
        """
        self.execution_log = []

        # Skip web scraper, start with content analyzer
        analyzer_result = ContentAnalyzerAgent.execute(text)
        self.log_step("Analyze content structure", analyzer_result)
        if not analyzer_result.success:
            return {
                "success": False,
                "error": f"Content analysis failed: {analyzer_result.error}",
                "execution_log": self.execution_log
            }

        # SSML Specialist Agent
        ssml_result = SSMLSpecialistAgent.execute(text, analyzer_result.data)
        self.log_step("Generate SSML segments", ssml_result)
        if not ssml_result.success:
            return {
                "success": False,
                "error": f"SSML generation failed: {ssml_result.error}",
                "execution_log": self.execution_log
            }

        podcast_plan = ssml_result.data

        # Audio Producer Agent
        audio_result = AudioProducerAgent.execute(
            podcast_plan["segments"],
            out_dir,
            final_mp3,
            voice_id,
            use_openai=use_openai
        )
        self.log_step("Generate and join audio", audio_result)
        if not audio_result.success:
            return {
                "success": False,
                "error": f"Audio production failed: {audio_result.error}",
                "execution_log": self.execution_log
            }

        return {
            "success": True,
            "data": {
                "analysis": analyzer_result.data,
                "podcast_plan": podcast_plan,
                "audio": audio_result.data
            },
            "execution_log": self.execution_log
        }