# Alexej Antropov - Personal Website

## Overview
A simple static personal website for Alexej Antropov. Content is written in Markdown (`content.md`) and converted to HTML (`index.html`) using a Python build script (`build.py`).

## Project Architecture
- `content.md` - Source content in Markdown
- `build.py` - Python 3 script (standard library only) that converts content.md to index.html
- `index.html` - Generated HTML output (do not edit directly)
- `server.py` - Simple Python HTTP server for local development on port 5000
- `setup.sh` - Git hooks configuration

## Workflow
- **Build**: Run `python build.py` to regenerate index.html from content.md
- **Serve**: `python server.py` serves the site on port 5000

## Deployment
- Static deployment serving index.html from the project root
