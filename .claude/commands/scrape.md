---
description: Extract clean content from a blog URL using the Web Scraper Agent
argument-hint: <url>
allowed-tools: Task(*)
---

Use the Task tool to launch the Web Scraper Agent (subagent_type: general-purpose) to extract content from URL: $ARGUMENTS

The agent should:
1. Detect if URL is a PDF and install pypdf or PyPDF2 if needed
2. For PDFs: download and extract text from all pages
3. For web pages: use trafilatura or BeautifulSoup to extract clean content
4. Return the extracted text, character count, and preview

After extraction, display the results and offer to save to a file or pass to the analyze command.