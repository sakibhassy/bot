import requests
import time
import random

API_KEY = "bd6f3409a32b27d0c2a48127f6baa7fe"
API_URL = "https://smmgen.com/api/v2"

SERVICE_TT_LIKES = "15995"
SERVICE_IG_LIKES = "16267"

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json",
    "Content-Type": "application/x-www-form-urlencoded"
}

MIN_LIKES = 10
MAX_LIKES = 13

def place_likes(link, service_id, quantity):
    data = {
        "key": API_KEY,
        "action": "add",
        "service": service_id,
        "link": link,
        "quantity": quantity
    }
    r = requests.post(API_URL, data=data, headers=HEADERS, timeout=30)
    print("Likes:", r.json())

def run_likes():
    platform = input("Platform (1=TikTok, 2=Instagram): ").strip()
    service = SERVICE_TT_LIKES if platform == "1" else SERVICE_IG_LIKES

    link = input("Video URL: ").strip()
    total_likes = int(input("Total Likes Target: "))
    delay = int(input("Delay between runs (minutes): ")) * 60

    sent = 0
    while sent < total_likes:
        likes = min(random.randint(MIN_LIKES, MAX_LIKES), total_likes - sent)
        print(f"Sending {likes} likes | Progress {sent + likes}/{total_likes}")
        place_likes(link, service, likes)
        sent += likes
        if sent < total_likes:
            time.sleep(delay)

    print("Likes target completed.")

if __name__ == "__main__":
    run_likes()
