import requests
import time
import random
import math

# ================== CONFIG ==================

API_KEY = "bd6f3409a32b27d0c2a48127f6baa7fe"
API_URL = "https://smmgen.com/api/v2"

# ===== TIKTOK SERVICES =====
SERVICE_ID_VIEWS = "16272"
SERVICE_ID_LIKES = "15995"
SERVICE_ID_COMMENTS = "00000000000"

# ===== INSTAGRAM SERVICES =====
SERVICE_ID_IG_VIEWS = "16143"
SERVICE_ID_IG_LIKES = "INSTAGRAM_LIKES_ID"
SERVICE_ID_IG_COMMENTS = ""  # comments disabled safely

# ===== RATIOS =====
MIN_LIKE_RATIO = 0.05
MAX_LIKE_RATIO = 0.07

IG_MIN_LIKE_RATIO = 0.03
IG_MAX_LIKE_RATIO = 0.04

MIN_LIKES_PER_RUN = 10
MAX_LIKES_PER_RUN = 13

MIN_COMMENTS = 2
MAX_COMMENTS = 25

COMMENT_LIST = [
    "This is amazing",
    "Love this!",
    "Great video",
    "Wow",
    "So good",
    "Keep it up"
]

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json",
    "Content-Type": "application/x-www-form-urlencoded"
}

# ================== FUNCTIONS ==================

def place_order(link, service_id, quantity=None, comments=None):
    if not service_id:
        return

    data = {
        "key": API_KEY,
        "action": "add",
        "service": service_id,
        "link": link
    }

    if comments is not None:
        data["comments"] = "\n".join(comments)
        data["quantity"] = len(comments)
        order_type = "Comments"
    else:
        data["quantity"] = quantity
        order_type = "Views" if quantity else "Likes"

    try:
        r = requests.post(API_URL, data=data, headers=HEADERS, timeout=30)
        r.raise_for_status()
        res = r.json()

        if "order" in res:
            print(f"{order_type} sent | Order ID: {res['order']}")
        else:
            print(f"{order_type} failed | Response:", res)

    except Exception as e:
        print(f"{order_type} request error:", e)


def countdown(seconds, views_sent, total_views):
    while seconds > 0:
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        print(
            f"Next run in {hours}h {minutes}m | Views sent: {views_sent}/{total_views}",
            end="\r"
        )
        time.sleep(1)
        seconds -= 1
    print()

# ================== MAIN ==================

def run_bot():
    print("Select platform:")
    print("1 - TikTok")
    print("2 - Instagram")

    choice = input("Enter choice (1 or 2): ").strip()

    if choice == "1":
        service_views = SERVICE_ID_VIEWS
        service_likes = SERVICE_ID_LIKES
        service_comments = SERVICE_ID_COMMENTS
        print("TikTok bot selected")
    elif choice == "2":
        service_views = SERVICE_ID_IG_VIEWS
        service_likes = SERVICE_ID_IG_LIKES
        service_comments = SERVICE_ID_IG_COMMENTS
        print("Instagram bot selected")
    else:
        print("Invalid choice.")
        return

    link = input("Enter video URL: ").strip()

    # ===== TOTAL VIEWS =====
    total_views_input = input("Enter total views: ").strip()
    try:
        if "-" in total_views_input:
            a, b = map(int, total_views_input.split("-"))
            total_views_target = random.randint(a, b)
        else:
            total_views_target = int(total_views_input)
    except:
        print("Invalid total views input.")
        return

    # ===== VIEWS PER ORDER =====
    views_per_order_input = input("Enter views per order: ").strip()
    try:
        if "-" in views_per_order_input:
            min_v, max_v = map(int, views_per_order_input.split("-"))
        else:
            min_v = max_v = int(views_per_order_input)
    except:
        print("Invalid views per order input.")
        return

    # ===== CYCLE DELAY =====
    print("Select cycle delay unit:")
    print("1 - Minutes")
    print("2 - Hours")
    unit_choice = input("Enter choice (1 or 2): ").strip()

    delay_input = input("Enter cycle delay: ").strip()

    try:
        if "-" in delay_input:
            d1, d2 = map(float, delay_input.split("-"))
            delay_value = random.uniform(d1, d2)
        else:
            delay_value = float(delay_input)

        if unit_choice == "2":
            cycle_delay_seconds = int(delay_value * 3600)
        else:
            cycle_delay_seconds = int(delay_value * 60)
    except:
        print("Invalid cycle delay input.")
        return

    avg_views = (min_v + max_v) / 2
    cycles = math.ceil(total_views_target / avg_views)
    total_time = cycles * cycle_delay_seconds

    print("\n===== ORDER ESTIMATION =====")
    print(f"Estimated views per order: {min_v}-{max_v}")
    print(f"Estimated cycles needed: {cycles}")
    print(f"Estimated time: {total_time // 3600}h {(total_time % 3600) // 60}m")
    print("===========================\n")

    total_views_sent = 0

    while total_views_sent < total_views_target:
        views = min(
            random.randint(min_v, max_v),
            total_views_target - total_views_sent
        )

        if choice == "2":
            raw_likes = int(views * random.uniform(IG_MIN_LIKE_RATIO, IG_MAX_LIKE_RATIO))
        else:
            raw_likes = int(views * random.uniform(MIN_LIKE_RATIO, MAX_LIKE_RATIO))

        likes = max(MIN_LIKES_PER_RUN, min(raw_likes, MAX_LIKES_PER_RUN))

        if choice == "2":
            comments_count = min(int((views / 1000) * 4), MAX_COMMENTS)
        else:
            comments_count = min(int(likes * random.uniform(0.10, 0.15)), MAX_COMMENTS)

        print(
            f"\nRUN → {views} views | {likes} likes | {comments_count} comments "
            f"| Progress: {total_views_sent + views}/{total_views_target}"
        )

        place_order(link, service_views, quantity=views)
        total_views_sent += views
        time.sleep(5)

        place_order(link, service_likes, quantity=likes)
        time.sleep(5)

        if comments_count > 0:
            comments = random.choices(COMMENT_LIST, k=comments_count)
            place_order(link, service_comments, comments=comments)

        if total_views_sent >= total_views_target:
            break

        countdown(cycle_delay_seconds, total_views_sent, total_views_target)

    print("\nTarget reached. Bot stopped.")

# ================== ENTRY ==================

if __name__ == "__main__":
    run_bot()
