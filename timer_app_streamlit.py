import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import time

# Sample data (replace with your own if needed)
data = [
    {"Name": "Venatus", "Interval": 600, "Last Time": "02:31 AM"},
    {"Name": "Viorent", "Interval": 600, "Last Time": "02:32 AM"},
    {"Name": "Ego", "Interval": 1260, "Last Time": "04:32 PM"},
    {"Name": "Aranco", "Interval": 1440, "Last Time": "04:36 PM"},
    {"Name": "Livera", "Interval": 1440, "Last Time": "04:36 PM"},
    {"Name": "Undomiel", "Interval": 1440, "Last Time": "04:36 PM"},
    {"Name": "Amentis", "Interval": 1740, "Last Time": "04:42 PM"},
    {"Name": "General Aqulucus", "Interval": 1920, "Last Time": "04:47 PM"},
    {"Name": "Baron Braudmore", "Interval": 1920, "Last Time": "04:37 PM"},
    {"Name": "Gareth", "Interval": 2100, "Last Time": "04:39 PM"},
    {"Name": "Shuliar", "Interval": 2100, "Last Time": "04:39 PM"},
    {"Name": "Larba", "Interval": 2100, "Last Time": "04:55 PM"},
    {"Name": "Catena", "Interval": 2100, "Last Time": "05:12 PM"},
    {"Name": "Lady Dalia", "Interval": 2280, "Last Time": "04:58 AM"},
    {"Name": "FRIOX", "Interval": 1440, "Last Time": "05:00 AM"},
    {"Name": "Titore", "Interval": 2220, "Last Time": "04:36 PM"},
    {"Name": "Duplican", "Interval": 2880, "Last Time": "04:36 PM"},
    {"Name": "Wannitas", "Interval": 2880, "Last Time": "04:36 PM"},
    {"Name": "Metus", "Interval": 2880, "Last Time": "04:46 PM"},
    {"Name": "Asta", "Interval": 2880, "Last Time": "04:46 PM"},
    {"Name": "Ordo", "Interval": 3720, "Last Time": "04:59 PM"},
    {"Name": "Secreta", "Interval": 3720, "Last Time": "05:07 AM"},
    {"Name": "Supore", "Interval": 3720, "Last Time": "05:15 PM"},
]

# Convert to DataFrame
df = pd.DataFrame(data)

st.set_page_config(page_title="Timer App", layout="wide")
st.title("⏳ Infinite Cycle Timer Dashboard (Live Updating)")

placeholder = st.empty()

def color_countdown(val):
    try:
        parts = val.split(":")
        minutes = int(parts[0]) * 60 + int(parts[1])
        seconds = minutes * 60 + int(parts[2]) if len(parts) == 3 else minutes
    except:
        return val

    if seconds < 300:  # < 5 min
        return f"<span style='color:red; font-weight:bold;'>{val}</span>"
    elif seconds < 900:  # < 15 min
        return f"<span style='color:orange;'>{val}</span>"
    else:
        return f"<span style='color:green;'>{val}</span>"

while True:
    now = datetime.now()
    next_times = []
    target_dates = []
    countdowns = []

    for i, row in df.iterrows():
        last_time = datetime.strptime(row["Last Time"], "%I:%M %p").replace(
            year=now.year, month=now.month, day=now.day
        )
        interval = timedelta(minutes=row["Interval"])
        next_time = last_time + interval

        while next_time <= now:
            next_time += interval

        countdown = next_time - now
        countdown_str = str(countdown).split(".")[0]

        next_times.append(next_time.strftime("%I:%M %p"))
        target_dates.append(next_time.strftime("%Y-%m-%d %I:%M:%S %p"))
        countdowns.append(color_countdown(countdown_str))

    df["Countdown"] = countdowns
    df["Next Time"] = next_times
    df["Target Date"] = target_dates

    with placeholder.container():
        st.markdown(
            df.to_html(escape=False, index=False),
            unsafe_allow_html=True
        )

    time.sleep(1)
