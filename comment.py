import requests
import time
import random
import math

# ================== CONFIG ==================

API_KEY = "bd6f3409a32b27d0c2a48127f6baa7fe"
API_URL = "https://smmgen.com/api/v2"

# ===== TIKTOK SERVICES =====
SERVICE_ID_TT_COMMENTS = "16217"

# ===== INSTAGRAM SERVICES =====
SERVICE_ID_IG_COMMENTS = "16178"

MIN_COMMENTS_PER_RUN = 10
MAX_COMMENTS_PER_RUN = 20

COMMENT_LIST = [
    "Nice video!",
    "Amazing!",
    "Love this!",
    "Great post",
    "So good",
    "Keep it up",
    "Wow 🔥",
    "Perfect!",
    "Very nice",
    "Awesome content"
]

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json",
    "Content-Type": "application/x-www-form-urlencoded"
}

# ================== FUNCTIONS ==================

def place_comment_order(link, service_id, comments):
    if not service_id:
        return

    data = {
        "key": API_KEY,
        "action": "add",
        "service": service_id,
        "link": link,
        "comments": "\n".join(comments),
        "quantity": len(comments)
    }

    try:
        r = requests.post(API_URL, data=data, headers=HEADERS, timeout=30)
        res = r.json()
        if "order" in res:
            print(f"Comments sent | Order ID: {res['order']}")
        else:
            print("Comment failed | Response:", res)
    except Exception as e:
        print("Comment error:", e)


def countdown(seconds, sent, total):
    while seconds > 0:
        h = seconds // 3600
        m = (seconds % 3600) // 60
        print(f"Next run in {h}h {m}m | Comments: {sent}/{total}", end="\r")
        time.sleep(1)
        seconds -= 1
    print()

# ================== MAIN ==================

def run_bot():
    print("Select platform:")
    print("1 - TikTok")
    print("2 - Instagram")

    choice = input("Enter choice: ").strip()

    if choice == "1":
        service_comments = SERVICE_ID_TT_COMMENTS
        print("TikTok comment bot selected")
    elif choice == "2":
        service_comments = SERVICE_ID_IG_COMMENTS
        print("Instagram comment bot selected")
    else:
        print("Invalid choice.")
        return

    link = input("Enter post/video URL: ").strip()

    # TOTAL COMMENTS
    total_comments_input = input("Enter total comments: ").strip()
    try:
        if "-" in total_comments_input:
            a, b = map(int, total_comments_input.split("-"))
            total_comments_target = random.randint(a, b)
        else:
            total_comments_target = int(total_comments_input)
    except:
        print("Invalid input.")
        return

    # COMMENTS PER RUN
    per_run_input = input("Enter comments per run: ").strip()
    try:
        if "-" in per_run_input:
            min_c, max_c = map(int, per_run_input.split("-"))
        else:
            min_c = max_c = int(per_run_input)
    except:
        print("Invalid input.")
        return

    # DELAY
    print("Select delay unit:")
    print("1 - Minutes")
    print("2 - Hours")
    unit = input("Choice: ").strip()
    delay_input = input("Enter delay: ").strip()

    try:
        if "-" in delay_input:
            d1, d2 = map(float, delay_input.split("-"))
            base = random.uniform(d1, d2)
        else:
            base = float(delay_input)

        delay_seconds = int(base * (3600 if unit == "2" else 60))
    except:
        print("Invalid delay.")
        return

    sent = 0
    print("\nComment bot started...\n")

    while sent < total_comments_target:
        count = min(random.randint(min_c, max_c), total_comments_target - sent)
        comments = random.choices(COMMENT_LIST, k=count)

        print(f"RUN → Sending {count} comments | Progress: {sent+count}/{total_comments_target}")
        place_comment_order(link, service_comments, comments)
        sent += count

        if sent >= total_comments_target:
            break

        countdown(delay_seconds, sent, total_comments_target)

    print("\nTarget reached. Comment bot stopped.")

if __name__ == "__main__":
    run_bot()
