import os
import csv
import time
from datetime import datetime, timedelta, timezone
import requests
from dotenv import load_dotenv

load_dotenv()
ORS_API_KEY = os.getenv("ORS_API_KEY")
TWILIO_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_FROM = os.getenv("TWILIO_WHATSAPP_FROM")

ETA_BUFFER_MIN = 10  # safety cushion

def now_dubai():
    """Return current datetime in Dubai (UTC+4) as timezone-aware."""
    return datetime.now(timezone.utc) + timedelta(hours=4)

def read_csv(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def geocode(address):
    """Use ORS to turn address into (lat, lon)."""
    url = "https://api.openrouteservice.org/geocode/search"
    params = {"api_key": ORS_API_KEY, "text": address}
    r = requests.get(url, params=params, timeout=15)
    r.raise_for_status()
    data = r.json()
    feats = data.get("features", [])
    if not feats:
        raise ValueError(f"Address not found: {address}")
    lon, lat = feats[0]["geometry"]["coordinates"]
    return (lat, lon)

def ors_eta_minutes(origin_latlon, dest_latlon):
    """ORS routing (driving-car) ETA in minutes."""
    url = "https://openrouteservice.org/v2/directions/driving-car"
    params = {
        "api_key": ORS_API_KEY,
        "start": f"{origin_latlon[1]},{origin_latlon[0]}",  # lon,lat
        "end":   f"{dest_latlon[1]},{dest_latlon[0]}",
    }
    r = requests.get(url, params=params, timeout=20)
    r.raise_for_status()
    seconds = r.json()["features"][0]["properties"]["summary"]["duration"]
    return int(round(seconds / 60))

def send_whatsapp(to_number, body):
    """Send WhatsApp via Twilio Sandbox. 'to_number' must have joined the sandbox."""
    url = f"https://api.twilio.com/2010-04-01/Accounts/{TWILIO_SID}/Messages.json"
    data = {
        "From": TWILIO_FROM,                 # e.g. whatsapp:+14155238886
        "To": f"whatsapp:{to_number}",       # your joined phone number, e.g. +9715xxxxxxx
        "Body": body,
    }
    r = requests.post(url, data=data, auth=(TWILIO_SID, TWILIO_TOKEN), timeout=15)
    r.raise_for_status()

def minutes_until(future_dt, now_dt):
    return int((future_dt - now_dt).total_seconds() // 60)

def process():
    bookings = read_csv("bookings.csv")
    drivers  = read_csv("drivers.csv")
    drivers_by_id = {d["driver_id"]: d for d in drivers}

    today = now_dubai().date()
    processed = 0
    warnings = 0
    failures  = []

    for b in bookings:
        try:
            pickup_time = datetime.strptime(b["pickup_time"], "%H:%M").time()
            pickup_dt = datetime.combine(today, pickup_time, tzinfo=timezone.utc) + timedelta(hours=4)
            mins_ahead = minutes_until(pickup_dt, now_dubai())
            #if mins_ahead < 0:
            #   continue  # skip past pickups

            assigned = drivers_by_id.get(b["assigned_driver_id"])
            if not assigned:
                raise RuntimeError(f"No assigned driver for booking {b.get('booking_id')}")

            pickup_latlon = geocode(b["pickup_address"])
            driver_latlon = geocode(assigned["current_address"])
            eta_min       = ors_eta_minutes(driver_latlon, pickup_latlon)

            if eta_min + ETA_BUFFER_MIN > mins_ahead:
                # might be late → warn customer
                body = (
                    f"Hello {b['customer_name']}, quick update for your Desert Safari at {b['pickup_time']}:\n"
                    f"Traffic suggests a possible delay. We’re adjusting to minimize it.\n"
                    f"Current ETA: ~{eta_min} min. Thanks for your patience!"
                )
                send_whatsapp(b["customer_phone"], body)
                warnings += 1
            else:
                # on time → normal confirm
                body = (
                    f"Hello {b['customer_name']}, your Desert Safari pickup at {b['pickup_time']} is confirmed. 🚗🏜️\n"
                    f"Driver: {assigned['driver_name']} | ETA: ~{eta_min} min.\n"
                    f"Please be ready 10 minutes early."
                )
                send_whatsapp(b["customer_phone"], body)

            processed += 1
            time.sleep(0.4)

        except Exception as e:
            failures.append((b.get("booking_id"), str(e)))

    # simple console summary
    print("Pickup ETA summary")
    print(f"- Processed: {processed}")
    print(f"- Potential delays: {warnings}")
    print(f"- Failures: {len(failures)}")
    if failures:
        for bid, err in failures:
            print(f"  • {bid}: {err}")

def main():
    # quick env sanity
    need = ["ORS_API_KEY", "TWILIO_ACCOUNT_SID", "TWILIO_AUTH_TOKEN", "TWILIO_WHATSAPP_FROM"]
    missing = [k for k in need if not os.getenv(k)]
    if missing:
        print("Missing in .env:", ", ".join(missing))
    process()
    print("Done.")

if __name__ == "__main__":
    main()
