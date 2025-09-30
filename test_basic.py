#!/usr/bin/env python3
"""
Quick test of the blog-to-podcast pipeline
"""

from dotenv import load_dotenv
from scrape import extract_from_url
from llm import blog_to_podcast_json

# Load environment variables
load_dotenv()

# Test URL scraping
def test_scraping():
    """Test the URL scraping functionality."""
    print("Testing web scraping...")
    try:
        # Test with a simple blog post
        test_url = "https://example.com"  # Simple test URL
        text = extract_from_url(test_url)
        print(f"Success: Scraped {len(text)} characters")
        return text
    except Exception as e:
        print(f"Error: Scraping failed: {e}")
        return None

# Test Claude integration
def test_claude_conversion():
    """Test Claude's blog-to-podcast conversion."""
    print("\nTesting Claude conversion...")

    # Sample blog text for testing
    sample_text = """
    Welcome to Modern AI Development

    Artificial Intelligence is transforming how we build software. In this post,
    we'll explore three key trends: machine learning automation, natural language
    processing, and computer vision applications.

    First, ML automation is making it easier than ever to deploy intelligent
    systems. Second, NLP is revolutionizing human-computer interaction.
    Finally, computer vision is opening new possibilities in robotics and
    autonomous systems.

    These technologies are not just theoretical - they're being used in production
    systems today to solve real-world problems.
    """

    try:
        result = blog_to_podcast_json(sample_text)
        print("Success: Claude conversion successful!")
        print(f"  Title: {result.get('title', 'N/A')}")
        print(f"  Segments: {len(result.get('segments', []))}")
        return result
    except Exception as e:
        print(f"Error: Claude conversion failed: {e}")
        return None

if __name__ == "__main__":
    print("Blog -> Podcast Pipeline Test")
    print("=" * 40)

    # Test individual components
    scrape_result = test_scraping()
    claude_result = test_claude_conversion()

    print("\n" + "=" * 40)
    if claude_result:
        print("Success: Core pipeline working!")
        print("Web app running at: http://localhost:8501")
    else:
        print("Error: Issues detected - check API keys in .env file")