from __future__ import annotations
import os
from pathlib import Path
from typing import List, Dict, Any
import requests
from pydub import AudioSegment
from tqdm import tqdm


def synth_ssml_to_mp3_segments(
    segments: List[Dict[str, Any]],
    output_dir: str,
    voice_id: str = None
) -> List[str]:
    """
    Convert SSML segments to MP3 files using ElevenLabs API.

    Args:
        segments: List of dicts with 'filename' and 'ssml' keys
        output_dir: Directory to save MP3 files
        voice_id: ElevenLabs voice ID

    Returns:
        List of paths to generated MP3 files
    """
    # Python Concept: Default parameter values
    if voice_id is None:
        voice_id = os.environ.get("ELEVEN_LABS_VOICE_ID", "21m00Tcm4TlvDq8ikWAM")

    # Python Concept: Environment variables for API keys
    api_key = os.environ.get("ELEVEN_LABS_API_KEY")
    if not api_key:
        raise RuntimeError("ELEVEN_LABS_API_KEY environment variable not set")

    # Python Concept: Path handling with pathlib (modern Python approach)
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)  # Create directory if it doesn't exist

    # Python Concept: List to store results
    generated_files = []

    # Python Concept: tqdm for progress bars
    for segment in tqdm(segments, desc="Generating audio segments"):
        filename = segment["filename"]
        ssml_content = segment["ssml"]

        # Python Concept: String formatting with f-strings
        file_path = output_path / filename

        try:
            # Python Concept: API call using requests
            mp3_data = _call_elevenlabs_api(ssml_content, voice_id, api_key)

            # Python Concept: File I/O - writing binary data
            with open(file_path, "wb") as f:
                f.write(mp3_data)

            generated_files.append(str(file_path))
            print(f"Success: Generated {filename}")

        except Exception as e:
            # Python Concept: Exception handling with specific error messages
            print(f"Error: Failed to generate {filename}: {e}")
            # Continue with other segments rather than stopping
            continue

    return generated_files


def _call_elevenlabs_api(ssml: str, voice_id: str, api_key: str) -> bytes:
    """
    Private function to call ElevenLabs API.

    Python Concept: Private functions start with underscore (_)
    """
    # ElevenLabs API endpoint
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"

    # Python Concept: Dictionary for HTTP headers
    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": api_key
    }

    # Python Concept: Dictionary for JSON payload
    data = {
        "text": ssml,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.5
        }
    }

    # Python Concept: HTTP POST request with error handling
    response = requests.post(url, json=data, headers=headers, timeout=60)

    # Python Concept: HTTP status code checking
    if response.status_code != 200:
        raise RuntimeError(f"ElevenLabs API error {response.status_code}: {response.text}")

    return response.content


def join_segments_to_podcast(segment_paths: List[str], output_file: str) -> str:
    """
    Join multiple MP3 segments into a single podcast file.

    Args:
        segment_paths: List of paths to MP3 segment files
        output_file: Path for final joined MP3 file

    Returns:
        Path to the final podcast file
    """
    if not segment_paths:
        raise ValueError("No segment paths provided")

    # Python Concept: Path handling for output directory
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Python Concept: Initialize with first segment
    combined_audio = AudioSegment.from_mp3(segment_paths[0])

    # Python Concept: Iterate through remaining segments
    for segment_path in tqdm(segment_paths[1:], desc="Joining segments"):
        try:
            # Python Concept: Audio manipulation with pydub
            segment = AudioSegment.from_mp3(segment_path)

            # Python Concept: Adding pause between segments (300ms)
            pause = AudioSegment.silent(duration=300)
            combined_audio = combined_audio + pause + segment

        except Exception as e:
            print(f"Warning: Could not load segment {segment_path}: {e}")
            continue

    # Python Concept: Export final audio file
    combined_audio.export(output_file, format="mp3")
    print(f"Success: Podcast saved: {output_file}")

    return output_file


# Python Concept: Script execution guard
if __name__ == "__main__":
    # This code only runs if the script is executed directly
    print("TTS module loaded successfully!")
    print("This module provides functions for:")
    print("- synth_ssml_to_mp3_segments(): Convert SSML to MP3 files")
    print("- join_segments_to_podcast(): Join MP3 segments into final podcast")