# fluent-critic
Business Insider PitchBot

Scrapes up to **25 headlines** from [Business Insider](https://www.businessinsider.com) and uses **OpenAI** to generate **5 snarky, satirical parody alternatives**.

## Requirements

- Python 3.10+
- An [OpenAI API key](https://platform.openai.com/api-keys)

## Quick Start

```bash
# 1. Clone the repo (if you haven't already)
git clone https://github.com/guycole/fluent-critic.git
cd fluent-critic

# 2. Run the setup script – creates a virtualenv and installs dependencies
chmod +x setup.sh
./setup.sh

# 3. Configure your OpenAI API key
cp .env.example .env
# Edit .env and replace the placeholder with your real key

# 4. Activate the virtualenv and run the bot
source .venv/bin/activate
python src/main.py
```

## Project Structure

```
fluent-critic/
├── src/
│   ├── main.py        # CLI entry point
│   ├── scraper.py     # Fetches headlines from businessinsider.com
│   └── generator.py   # Calls OpenAI to produce parody headlines
├── requirements.txt   # Python dependencies
├── setup.sh           # virtualenv + dependency installation script
├── .env.example       # Template for your .env file
└── README.md
```

## Dependencies

| Package | Purpose |
|---------|---------|
| `requests` | HTTP requests to Business Insider |
| `beautifulsoup4` | HTML parsing |
| `openai` | OpenAI API client |
| `python-dotenv` | Loads `OPENAI_API_KEY` from `.env` |
