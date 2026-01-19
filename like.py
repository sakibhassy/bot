import requests, time, random, math

API_KEY = "bd6f3409a32b27d0c2a48127f6baa7fe"
API_URL = "https://smmgen.com/api/v2"

SERVICE_TT_LIKES = "15995"
SERVICE_IG_LIKES = "16267"

HEADERS = {
    "User-Agent":"Mozilla/5.0",
    "Accept":"application/json",
    "Content-Type":"application/x-www-form-urlencoded"
}

def send_likes(link, service, qty):
    r = requests.post(API_URL, data={
        "key":API_KEY,
        "action":"add",
        "service":service,
        "link":link,
        "quantity":qty
    }, headers=HEADERS)
    print(r.json())

def run():
    platform = input("1-TikTok 2-Instagram: ").strip()
    service = SERVICE_TT_LIKES if platform=="1" else SERVICE_IG_LIKES

    link = input("URL: ").strip()
    total = int(input("Total likes: ").strip())

    per_input = input("Likes per order: ").strip()
    try:
        if "-" in per_input:
            min_v, max_v = map(int, per_input.split("-"))
        else:
            min_v = max_v = int(per_input)
    except:
        print("Invalid likes per order.")
        return

    print("Delay unit:")
    print("1 - Minutes")
    print("2 - Hours")
    unit = input("Choose (1 or 2): ").strip()
    delay_val = float(input("Delay value: ").strip())
    delay = int(delay_val * (3600 if unit=="2" else 60))

    avg = (min_v + max_v) / 2
    cycles = math.ceil(total / avg)
    total_time = cycles * delay

    print("\n===== ORDER ESTIMATION =====")
    print(f"Estimated likes per order: {min_v}-{max_v}")
    print(f"Estimated cycles needed: {cycles}")
    print(f"Estimated time: {total_time//3600}h {(total_time%3600)//60}m")
    print("===========================\n")

    sent = 0
    while sent < total:
        q = min(random.randint(min_v, max_v), total - sent)
        print(f"Sending {q} likes | Progress {sent+q}/{total}")
        send_likes(link, service, q)
        sent += q
        time.sleep(delay)

run()
