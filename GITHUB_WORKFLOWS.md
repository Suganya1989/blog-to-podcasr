# GitHub Workflows with Claude Integration

This repository includes automated GitHub Actions workflows that use Claude agents to convert blogs to podcasts.

## 🔧 Setup

### 1. Add GitHub Secrets

Go to your repo → Settings → Secrets and variables → Actions

Add these secrets:
- `ANTHROPIC_API_KEY` - Your Anthropic API key
- `OPENAI_API_KEY` - Your OpenAI API key

### 2. Enable GitHub Actions

Make sure GitHub Actions are enabled in your repository settings.

## 🚀 Available Workflows

### 1. **Blog to Podcast Conversion** (`blog-to-podcast.yml`)

Converts a blog URL to a podcast using Claude agents.

**Trigger Methods:**

#### A. Manual Trigger
1. Go to Actions → "Blog to Podcast Conversion"
2. Click "Run workflow"
3. Enter blog URL and voice
4. Download podcast from artifacts

#### B. GitHub Issue
1. Create an issue with label `podcast`
2. Include the blog URL in the issue body
3. Workflow runs automatically
4. Bot comments with download link

**Example Issue:**
```markdown
Title: Convert AI Blog to Podcast
Labels: podcast

Please convert this blog:
https://blog.example.com/ai-future

Thanks!
```

---

### 2. **Claude Agent Trigger** (`claude-agent-trigger.yml`)

Execute any Claude command via issue comments.

**Usage:**
```
/claude convert this blog to podcast: https://example.com using voice nova
/claude make a podcast from https://blog.com with shimmer voice
```

**How it works:**
1. Comment `/claude <command>` on any issue
2. Workflow parses the natural language command
3. Claude AI interprets and executes
4. Results uploaded as artifacts
5. Bot replies with link

---

### 3. **Claude PR Review** (`pr-agent-review.yml`)

Automatic code review by Claude on every pull request.

**Triggers:** Automatically on PR open/update

**What it does:**
- Analyzes code diff
- Reviews for bugs, security, best practices
- Posts detailed review as PR comment
- Provides constructive feedback

**Example Review:**
```markdown
# Claude Code Review

## Code Quality: ⭐⭐⭐⭐

## Issues Found:
1. Missing error handling in line 45
2. Potential SQL injection risk in query builder

## Suggestions:
- Add input validation
- Use parameterized queries

## Security: ✅ No critical issues
```

---

### 4. **Scheduled Podcast** (`scheduled-podcast.yml`)

Generate podcasts automatically on a schedule.

**Schedule:** Daily at 9 AM UTC

**Setup:**
1. Create `podcast_sources.txt` with blog URLs (one per line)
2. Workflow reads first URL each day
3. Generates podcast
4. Creates GitHub release with MP3

**Manual trigger:** Actions → "Scheduled Podcast Generation" → Run workflow

---

## 📋 Workflow Examples

### Example 1: Convert Blog via Manual Workflow

```yaml
# Triggered manually
Inputs:
  blog_url: https://anthropic.com/news/claude-3-5-sonnet
  voice: nova

Result:
  ✅ Podcast generated
  📦 Available in artifacts
  🎵 Voice: nova
```

### Example 2: Issue-based Conversion

```markdown
# Create this issue:
Title: Podcast Request - AI Safety
Labels: podcast
Body:
Please convert: https://example.com/ai-safety-blog
```

Bot responds:
```markdown
✅ Podcast created successfully!

🎧 Download from the Actions artifacts
Voice: alloy
```

### Example 3: Comment Command

```markdown
# Comment on any issue:
/claude convert https://blog.example.com to podcast with echo voice
```

Bot responds:
```markdown
✅ Claude AI executed successfully!

Command: `convert https://blog.example.com to podcast with echo voice`

📦 Results available in Actions artifacts
```

---

## 🔐 Security Notes

1. **API Keys:** Never commit API keys - use GitHub Secrets
2. **Public Repos:** Be aware artifacts are visible to repo collaborators
3. **Rate Limits:** Workflows respect API rate limits
4. **Costs:** OpenAI TTS costs ~$15 per 1M characters

---

## 🎯 Advanced Usage

### Custom Agent Workflows

Create your own workflow using Claude agents:

```yaml
name: Custom Agent Task

on:
  workflow_dispatch:
    inputs:
      task:
        description: 'Task for Claude'
        required: true

jobs:
  execute:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Run Claude Agent
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
        run: |
          python claude_ai.py "${{ inputs.task }}"
```

### Webhook Integration

Trigger workflows via webhooks:

```bash
curl -X POST \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer $GITHUB_TOKEN" \
  https://api.github.com/repos/OWNER/REPO/actions/workflows/blog-to-podcast.yml/dispatches \
  -d '{"ref":"main","inputs":{"blog_url":"https://example.com","voice":"nova"}}'
```

---

## 📊 Monitoring

View workflow runs:
1. Go to "Actions" tab
2. Select workflow
3. View logs and artifacts
4. Download generated podcasts

---

## 🐛 Troubleshooting

### Workflow fails with "No module named 'anthropic'"
- Check `requirements.txt` is committed
- Verify dependencies install step runs

### No artifacts generated
- Check workflow logs for errors
- Verify API keys are set correctly
- Ensure `audio/` directory is created

### Claude returns errors
- Verify `ANTHROPIC_API_KEY` secret is set
- Check API key has sufficient credits
- Review Claude API quotas

---

## 🎓 Learn More

- [GitHub Actions Docs](https://docs.github.com/en/actions)
- [Anthropic API](https://docs.anthropic.com/)
- [OpenAI TTS](https://platform.openai.com/docs/guides/text-to-speech)

---

## 💡 Ideas for Extension

1. **Slack Integration:** Post podcasts to Slack channel
2. **RSS Feed:** Auto-generate from RSS feeds
3. **Multi-language:** Support multiple TTS languages
4. **Quality Checks:** Automated testing of generated audio
5. **CDN Upload:** Auto-upload to S3/CDN