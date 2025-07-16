# HowlRadar

**A command-line bug bounty program notifier that fetches new bounty programs from multiple platforms and sends notifications via Terminal, Discord, Telegram, or Email.**

---

## Features

- Fetches latest bounty programs from multiple platforms:
  - HackerOne
  - Bugcrowd
  - Immunefi
  - YesWeHack
  - Integriti
- Filter programs by bounty amount, attack types, categories, and platforms
- Supports notifications via:
  - Terminal output
  - Discord webhook
  - Telegram bot
  - Email (SMTP)
- Option to get only new programs (avoid repeats)
- Export results to JSON or CSV
- Easy CLI usage and installation via pip from GitHub

---

## Installation

Install directly from GitHub using pip:

```bash
pip install git+https://github.com/yourusername/howlradar.git
Usage:
Run howlradar command with options:

howlradar --notify=terminal,discord --min=100 --types=XSS,RCE --new-only --verbose

Options:
Option	Description
--notify	Comma separated notification methods: terminal, discord, telegram, email, or all
--platforms	Comma separated platform names (hackerone, bugcrowd, immunefi, yeswehack, integriti)
--min	Minimum bounty amount (default 0)
--max	Maximum bounty amount (optional)
--types	Comma separated attack types (e.g., XSS,RCE,SQLi). If not specified, returns all types
--category	Comma separated categories (e.g., web, api, mobile)
--new-only	Show only new programs that have not been notified before
--export	Export results to json or csv file
--verbose	Show detailed info including scope and description
