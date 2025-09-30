from __future__ import annotations
import os
import re
from pathlib import Path
from typing import List, Dict, Any
from openai import OpenAI
from tqdm import tqdm


def synth_ssml_to_mp3_segments(
    segments: List[Dict[str, Any]],
    output_dir: str,
    voice_name: str = "alloy"
) -> List[str]:
    """
    Convert SSML segments to MP3 files using OpenAI TTS API.

    Args:
        segments: List of dicts with 'filename' and 'ssml' keys
        output_dir: Directory to save MP3 files
        voice_name: OpenAI voice (alloy, echo, fable, onyx, nova, shimmer)

    Returns:
        List of generated file paths
    """
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY environment variable not set")

    client = OpenAI(api_key=api_key)

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    generated_files = []

    for segment in tqdm(segments, desc="Generating audio segments with OpenAI TTS"):
        filename = segment["filename"]
        ssml_content = segment["ssml"]
        file_path = output_path / filename

        try:
            # Convert SSML to plain text (OpenAI doesn't support SSML)
            text = _ssml_to_text(ssml_content)

            # Call OpenAI TTS API
            response = client.audio.speech.create(
                model="tts-1-hd",  # Use HD model for better quality
                voice=voice_name,
                input=text,
                response_format="mp3"
            )

            # Save to file
            response.stream_to_file(file_path)

            generated_files.append(str(file_path))
            print(f"Success: Generated {filename}")

        except Exception as e:
            print(f"Error: Failed to generate {filename}: {e}")
            continue

    return generated_files


def _ssml_to_text(ssml: str) -> str:
    """
    Convert SSML to plain text by removing XML tags.
    OpenAI TTS doesn't support SSML, but handles text naturally.
    """
    # Remove XML declaration
    text = re.sub(r'<\?xml[^>]*\?>', '', ssml)

    # Remove speak tag
    text = re.sub(r'<speak[^>]*>', '', text)
    text = re.sub(r'</speak>', '', text)

    # Remove break tags (pauses)
    text = re.sub(r'<break[^>]*/?>', ' ', text)

    # Remove emphasis tags but keep content
    text = re.sub(r'<emphasis[^>]*>', '', text)
    text = re.sub(r'</emphasis>', '', text)

    # Remove paragraph tags but keep content
    text = re.sub(r'<p>', '', text)
    text = re.sub(r'</p>', '\n', text)

    # Remove any other XML tags
    text = re.sub(r'<[^>]+>', '', text)

    # Clean up extra whitespace
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()

    return text


def join_segments_to_podcast_simple(segment_paths: List[str], output_file: str) -> str:
    """
    Simple Windows-compatible version: Join MP3 segments without pydub.
    This creates a basic concatenated file.
    """
    if not segment_paths:
        raise ValueError("No segment paths provided")

    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    print(f"Joining {len(segment_paths)} segments...")

    # Simple binary concatenation (works for MP3s in many cases)
    with open(output_file, "wb") as outfile:
        for i, segment_path in enumerate(segment_paths):
            try:
                with open(segment_path, "rb") as infile:
                    outfile.write(infile.read())
                print(f"Added segment {i+1}/{len(segment_paths)}")
            except Exception as e:
                print(f"Warning: Could not read segment {segment_path}: {e}")

    print(f"Success: Podcast saved: {output_file}")
    print("Note: For professional audio joining with pauses, install ffmpeg and pydub")

    return output_file


def join_segments_to_podcast(segment_paths: List[str], output_file: str) -> str:
    """
    Main function that tries advanced joining first, falls back to simple method.
    """
    try:
        # Try to import pydub for professional audio joining
        from pydub import AudioSegment
        return _join_with_pydub(segment_paths, output_file)
    except ImportError:
        print("pydub not available, using simple joining method...")
        return join_segments_to_podcast_simple(segment_paths, output_file)
    except Exception as e:
        print(f"pydub failed ({e}), using simple joining method...")
        return join_segments_to_podcast_simple(segment_paths, output_file)


def _join_with_pydub(segment_paths: List[str], output_file: str) -> str:
    """Use pydub for professional audio joining with proper timing."""
    from pydub import AudioSegment

    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    combined_audio = AudioSegment.from_mp3(segment_paths[0])

    for segment_path in tqdm(segment_paths[1:], desc="Joining segments"):
        try:
            segment = AudioSegment.from_mp3(segment_path)
            pause = AudioSegment.silent(duration=300)  # 300ms pause
            combined_audio = combined_audio + pause + segment
        except Exception as e:
            print(f"Warning: Could not load segment {segment_path}: {e}")
            continue

    combined_audio.export(output_file, format="mp3")
    print(f"Success: Professional podcast saved: {output_file}")

    return output_file


# Available OpenAI voices
AVAILABLE_VOICES = {
    "alloy": "Neutral, balanced voice",
    "echo": "Male voice",
    "fable": "British male voice",
    "onyx": "Deep male voice",
    "nova": "Female voice",
    "shimmer": "Soft female voice"
}


if __name__ == "__main__":
    print("OpenAI TTS module loaded!")
    print("\nAvailable voices:")
    for voice, description in AVAILABLE_VOICES.items():
        print(f"  - {voice}: {description}")
    print("\nCost: ~$15 per 1M characters (tts-1-hd model)")
    print("No SSML needed - OpenAI handles natural pacing automatically!")