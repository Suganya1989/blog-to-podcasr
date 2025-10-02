# Audio Command

## Command Name
`audio`

## Description
Run the Audio Producer Agent to generate MP3 files from a podcast plan JSON.

## Usage
```bash
claude audio --podcast-file <podcast.json>
claude audio --podcast-file <podcast.json> --voice <voice-name>
claude audio --podcast-file <podcast.json> --provider elevenlabs
```

## Options
- `--podcast-file` - Path to podcast plan JSON file (required)
- `--voice` - Voice name/ID (default: "alloy")
  - OpenAI: alloy, echo, fable, onyx, nova, shimmer
  - ElevenLabs: your voice ID
- `--provider` - TTS provider (default: "openai")
  - Options: openai, elevenlabs

## Examples
```bash
# Generate audio with default voice
claude audio --podcast-file podcast.json

# Use specific OpenAI voice
claude audio --podcast-file podcast.json --voice nova

# Use ElevenLabs
claude audio --podcast-file podcast.json --provider elevenlabs --voice "21m00Tcm4TlvDq8ikWAM"
```

## Agent Used
**Audio Producer Agent** (`.claude/agents/audio-producer.md`)

## Output
- Individual MP3 segments in `audio/segments/`
- Final joined podcast at `audio/podcast.mp3`
- Segment count and file paths
- TTS provider used