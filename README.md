# Personalized Conference Ticket Generator

## Overview

A FastAPI-powered service for generating personalized conference tickets with dynamic image manipulation using Pillow.

## Features

- 🎫 Generate custom tickets for multiple conferences
- 🖼️ Dynamic image personalization


## Prerequisites

- Python 3.8+
- FastAPI
- Uvicorn
- Pillow


## Installation

1. Clone the repository:
```bash
git clone https://github.com/MogboPython/conference_tickets_server.git
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Configuration

Customize service and ticket configurations in `service_configs.py`:
- Define service-specific ticket templates
- Set custom fonts, colors, and text placements

## Running the Server

```bash
uvicorn main:app --reload
```

## Endpoint Usage

Generate a ticket:
```
GET /api/{service}/generate-ticket?first_name=John&last_name=Doe
```

## Project Structure

```
ticket-generator/
│
├── main.py           # FastAPI server
├── schema.py         # Configuration schemas
├── ticket_generator.py  # Ticket generation logic
├── static/           # Ticket templates and fonts
│   ├── ysf-2022/
│   └── nexlds-ife/
└── requirements.txt
```
