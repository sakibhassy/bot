import requests
import time
import random
import math

API_KEY = "bd6f3409a32b27d0c2a48127f6baa7fe"
API_URL = "https://smmgen.com/api/v2"

SERVICE_TT_VIEWS = "16272"
SERVICE_IG_VIEWS = "16143"

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json",
    "Content-Type": "application/x-www-form-urlencoded"
}

def place_views(link, service_id, quantity):
    data = {
        "key": API_KEY,
        "action": "add",
        "service": service_id,
        "link": link,
        "quantity": quantity
    }
    r = requests.post(API_URL, data=data, headers=HEADERS, timeout=30)
    print("Views:", r.json())

def run_views():
    platform = input("Platform (1=TikTok, 2=Instagram): ").strip()
    service = SERVICE_TT_VIEWS if platform == "1" else SERVICE_IG_VIEWS

    link = input("Video URL: ").strip()
    total_views = int(input("Total Views Target: "))
    min_v, max_v = map(int, input("Views per run (min-max): ").split("-"))
    delay = int(input("Delay between runs (minutes): ")) * 60

    sent = 0
    while sent < total_views:
        views = min(random.randint(min_v, max_v), total_views - sent)
        print(f"Sending {views} views | Progress {sent + views}/{total_views}")
        place_views(link, service, views)
        sent += views
        if sent < total_views:
            time.sleep(delay)

    print("Views target completed.")

if __name__ == "__main__":
    run_views()
