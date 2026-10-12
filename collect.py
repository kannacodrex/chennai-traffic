import os, csv, json, datetime, urllib.request

ROADS = [
    ("Anna Salai", 13.0590, 80.2570),
    ("OMR", 12.9010, 80.2279),
    ("GST Road", 12.9229, 80.1275),
    ("Poonamallee High Rd", 13.0735, 80.2235),
    ("ECR", 12.9490, 80.2590),
]

KEY = os.environ["TOMTOM_KEY"]
IST = datetime.timezone(datetime.timedelta(hours=5, minutes=30))
now = datetime.datetime.now(IST)

rows = []
for name, lat, lon in ROADS:
    url = ("https://api.tomtom.com/traffic/services/4/flowSegmentData/absolute/10/json"
           f"?point={lat},{lon}&key={KEY}")
    try:
        with urllib.request.urlopen(url, timeout=20) as r:
            d = json.load(r)["flowSegmentData"]
        rows.append([now.strftime("%Y-%m-%d %H:%M"), now.strftime("%a"), name,
                     d["currentSpeed"], d["freeFlowSpeed"],
                     d["currentTravelTime"], d["freeFlowTravelTime"]])
    except Exception as e:
        print("Failed for", name, type(e).__name__)

os.makedirs("data", exist_ok=True)
path = "data/readings.csv"
new = not os.path.exists(path)
with open(path, "a", newline="") as f:
    w = csv.writer(f)
    if new:
        w.writerow(["time_ist", "day", "road", "speed_now", "speed_free",
                    "travel_secs_now", "travel_secs_free"])
    w.writerows(rows)
print("Saved", len(rows), "readings")
