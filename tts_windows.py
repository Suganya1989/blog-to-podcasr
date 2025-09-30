from __future__ import annotations
import os
import io
from pathlib import Path
from typing import List, Dict, Any
import requests
from tqdm import tqdm


def synth_ssml_to_mp3_segments(
    segments: List[Dict[str, Any]],
    output_dir: str,
    voice_id: str = None
) -> List[str]:
    """
    Windows-compatible version: Convert SSML segments to MP3 files using ElevenLabs API.
    This version avoids pydub/ffmpeg dependencies for basic functionality.
    """
    if voice_id is None:
        voice_id = os.environ.get("ELEVEN_LABS_VOICE_ID", "21m00Tcm4TlvDq8ikWAM")

    api_key = os.environ.get("ELEVEN_LABS_API_KEY")
    if not api_key:
        raise RuntimeError("ELEVEN_LABS_API_KEY environment variable not set")

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    generated_files = []

    for segment in tqdm(segments, desc="Generating audio segments"):
        filename = segment["filename"]
        ssml_content = segment["ssml"]
        file_path = output_path / filename

        try:
            mp3_data = _call_elevenlabs_api(ssml_content, voice_id, api_key)

            with open(file_path, "wb") as f:
                f.write(mp3_data)

            generated_files.append(str(file_path))
            print(f"Success: Generated {filename}")

        except Exception as e:
            print(f"Error: Failed to generate {filename}: {e}")
            continue

    return generated_files


def _call_elevenlabs_api(ssml: str, voice_id: str, api_key: str) -> bytes:
    """Call ElevenLabs API to convert SSML to MP3."""
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"

    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": api_key
    }

    data = {
        "text": ssml,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.5
        }
    }

    response = requests.post(url, json=data, headers=headers, timeout=60)

    if response.status_code != 200:
        raise RuntimeError(f"ElevenLabs API error {response.status_code}: {response.text}")

    return response.content


def join_segments_to_podcast_simple(segment_paths: List[str], output_file: str) -> str:
    """
    Simple Windows-compatible version: Join MP3 segments without pydub.
    This creates a basic concatenated file - not as sophisticated as pydub but works.
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

    print(f"Success: Basic podcast saved: {output_file}")
    print("Note: For professional audio joining, install ffmpeg and use the full tts.py module")

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


if __name__ == "__main__":
    print("Windows-compatible TTS module loaded!")
    print("This version works without ffmpeg for basic functionality.")
    print("For professional audio joining, install ffmpeg.")