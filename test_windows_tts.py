#!/usr/bin/env python3
"""
Test Windows-compatible TTS functionality
"""

from dotenv import load_dotenv
import os
from tts_windows import synth_ssml_to_mp3_segments, join_segments_to_podcast

load_dotenv()

def test_windows_tts():
    """Test the Windows-compatible TTS pipeline."""

    print("=== Testing Windows-Compatible TTS ===")

    # Test segments (simplified for testing)
    test_segments = [
        {
            "filename": "test-seg-001.mp3",
            "ssml": "<speak>This is a test of the Windows compatible TTS system.</speak>"
        },
        {
            "filename": "test-seg-002.mp3",
            "ssml": "<speak>If you can hear this, the system is working correctly.</speak>"
        }
    ]

    print(f"API Key present: {'ELEVEN_LABS_API_KEY' in os.environ}")
    print(f"Voice ID: {os.environ.get('ELEVEN_LABS_VOICE_ID', 'default')}")

    try:
        print("\n1. Testing segment generation...")
        paths = synth_ssml_to_mp3_segments(
            test_segments,
            "audio/test_segments",
            voice_id=os.environ.get("ELEVEN_LABS_VOICE_ID")
        )

        print(f"Generated {len(paths)} segments:")
        for path in paths:
            print(f"  - {path}")

        print("\n2. Testing audio joining...")
        final_file = join_segments_to_podcast(paths, "audio/test_podcast.mp3")
        print(f"Final podcast: {final_file}")

        print("\n✅ Windows TTS test completed successfully!")
        print("🌐 Your web app should now work without errors.")

    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        print("💡 Check your .env file and internet connection.")

if __name__ == "__main__":
    test_windows_tts()