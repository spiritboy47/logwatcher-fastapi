import os
import time
import json
import re
from datetime import datetime
from app.mailer import send_summary_email
from app.config import LOG_DIRS, RECIPIENTS, SEND_INTERVAL_SECONDS

# Cache file to store last sent timestamp per log file
CACHE_FILE = os.path.join(os.path.dirname(__file__), "cache.json")

# Regex to extract ISO 8601 timestamps
TIMESTAMP_REGEX = re.compile(r"(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d+([+-]\d{2}:\d{2})?)")

def parse_timestamp(line: str) -> datetime | None:
    match = TIMESTAMP_REGEX.search(line)
    if match:
        try:
            return datetime.fromisoformat(match.group(1))
        except ValueError:
            return None
    return None

def load_cache():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {}
    return {}

def save_cache(cache):
    try:
        with open(CACHE_FILE, "w") as f:
            json.dump(cache, f, indent=2)
        print(f"[DEBUG] Cache saved to {CACHE_FILE}")
    except Exception as e:
        print(f"[ERROR] Failed to save cache: {e}")

def start_monitoring():
    print("[INFO] Starting log monitor...")
    cache = load_cache()

    while True:
        for project, dir_path in LOG_DIRS.items():
            error_summary = {}

            if not os.path.exists(dir_path):
                print(f"[WARNING] Log directory does not exist: {dir_path}")
                continue

            for filename in os.listdir(dir_path):
                if not filename.endswith(".log"):
                    continue

                filepath = os.path.join(dir_path, filename)
                cache_key = f"{project}/{filename}"
                latest_ts = None
                latest_line = None

                try:
                    with open(filepath, "r") as f:
                        for line in f:
                            if "ERROR" not in line:
                                continue

                            ts = parse_timestamp(line)
                            if not ts:
                                continue

                            if not latest_ts or ts > latest_ts:
                                latest_ts = ts
                                latest_line = line.strip()

                    # Only consider if we found a new line
                    if latest_ts and latest_line:
                        prev_sent_ts_str = cache.get(cache_key)
                        prev_sent_ts = datetime.fromisoformat(prev_sent_ts_str) if prev_sent_ts_str else None

                        if not prev_sent_ts or latest_ts > prev_sent_ts:
                            error_summary[filename] = [latest_line]
                            cache[cache_key] = latest_ts.isoformat()

                except Exception as e:
                    print(f"[ERROR] Failed to read {filepath}: {e}")

            if error_summary:
                send_summary_email(project, error_summary, RECIPIENTS)

        save_cache(cache)
        print(f"[INFO] Monitoring paused for {SEND_INTERVAL_SECONDS} seconds...\n")
        time.sleep(SEND_INTERVAL_SECONDS)
