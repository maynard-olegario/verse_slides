# Verse Slides

## Summary
Given a list of biblical verses, generate uniform slides for each verse.  The generated slides can then be used in bible presentations.

## Details
1. The `verses.txt` file contains the citations to lookup
1. API requests are sent to biblegateway.com to retrieve the passage of the citation
1. API requests are then sent to Google to create slides in a [presentation file](https://docs.google.com/presentation/d/12XDv6JAdduXgoTneZdQ9tawfGouTPQLExTUEb3RUurU/).
   - **Note: this file will get overwritten every time the script is run.**
   - Manually make a copy of the file to avoid losing changes.

## Prerequisites
1. [Git](https://help.github.com/en/github/getting-started-with-github/set-up-git#setting-up-git)
1. [PyEnv](https://github.com/pyenv/pyenv#installation)
1. [Python 3.x+](https://www.python.org/downloads/)
1. [Enable Google Slides API](https://developers.google.com/slides/quickstart/python)
   - Download `credentials.json`
   - On the first run only, a browser window will open to authenticate your google user

## Installation
```
git clone https://github.com/maynard-olegario/verse_slides.git
pip install -r requirements.txt
```

## How to use
1. Add citations in the `verses.txt` file.  Enter the book name, then chapter, then verse, then version (defaults to NKJV if ommitted).  For example:
```
book 1:2-5 KJV
```
1. Run the python script
```
python ./main.py
```

## Misc
1. Additional slide [templates](https://www.slidescarnival.com/)