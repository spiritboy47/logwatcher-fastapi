# 🕵️‍♂️ Log Error Monitor

A lightweight **FastAPI** service that monitors log files for `ERROR` entries and sends summary emails every 10 minutes.

Ideal for tracking issues in microservices, NGINX logs, or any custom app logs — no need for heavy tools like ELK or Loki.

## 🚀 Features
- 🔍 Monitors `.log` files in specified directories
- 📧 Sends email notifications with the latest `ERROR` lines
- 🕒 Runs check every 10 minutes (configurable)
- 🐳 Dockerized for easy deployment
- ⚡ Built with Python 3.11 + FastAPI

## 📧 SMTP Setup
Update these values in app/mailer.py:
* SMTP_SERVER = "smtp.gmail.com"
* SMTP_PORT = 587
* SMTP_USERNAME = "your-email@gmail.com"
* SMTP_PASSWORD = "your-app-password"
* FROM_ADDRESS = "your-email@gmail.com"
Use an App Password for Gmail accounts.

## 🐳 Docker Setup
1. Build & Run the Container
* docker-compose up --build -d

2. Confirm it's Running
* docker logs -f logmonitor

## 🔄 How It Works
1. Every 10 minutes:
* Scans log files in configured directories
* Looks for new lines containing ERROR
* Caches the last sent timestamp for each file

2. If new ERROR entries are found:
* Sends a summary email listing each log file and its latest error line

## 🧪 Local Development (Without Docker)
1. Install Requirements
* python3 -m venv venv
* source venv/bin/activate
* pip install -r requirements.txt

2. Start the Server
* uvicorn app.main:app --reload --port 6000

## 🧹 Clean Up
To stop and remove containers:
* docker-compose down
