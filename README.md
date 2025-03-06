# Dalili

## Introduction

**DISCLAIMER**: This tool is still in the early stages of development.

A script that creates a Gmail calendar event to remind you if your location is scheduled for power interruption by Kenya Power.
To be [forewarned is to be forearmed](https://www.collinsdictionary.com/dictionary/english/forewarned-is-forearmed)!

## Developing

Using `venv`, create:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Installation

### Creating service.json for GMail Auth

### Setting up crontab

I recommend setting it to run once per week. They usually have the new schedule up every Thursday.

```bash
crontab -e
```

## Usage

After following the installation instructions above, you're good to go!

## Contributing
