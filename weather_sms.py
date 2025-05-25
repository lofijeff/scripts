import requests
import feedparser
from datetime import datetime, date
from base64 import b64encode

LAT = 63.8258  # Umeå
LON = 20.2630

TO_NUMBER = "XXX"
FROM_NAME = "Morsning"
USERNAME = "XXX"
PASSWORD = "XXX"

def get_weather():
    url = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={LAT}&longitude={LON}"
        f"&hourly=temperature_2m,precipitation_probability,precipitation"
        f"&timezone=auto"
    )
    res = requests.get(url, timeout=10)
    res.raise_for_status()
    data = res.json()

    times = data['hourly']['time']
    temps = data['hourly']['temperature_2m']
    prec_probs = data['hourly']['precipitation_probability']
    prec_amounts = data['hourly']['precipitation']

    wanted_hours = ['08:00', '12:00', '16:00', '20:00']
    today = date.today().isoformat()
    result = {}

    for idx, t in enumerate(times):
        if t.startswith(today):
            hour = t[11:16]
            if hour in wanted_hours:
                result[hour] = {
                    "temp": temps[idx],
                    "precip_prob": prec_probs[idx],
                    "precip_amt": prec_amounts[idx]
                }

    message = ""
    for hour in wanted_hours:
        if hour in result:
            temp = result[hour]["temp"]
            prob = result[hour]["precip_prob"]
            amt = result[hour]["precip_amt"]
            line = f"{hour}: {temp:.1f}°C"
            if prob > 20 or amt > 0.1:
                line += f" ({amt:.1f}mm)"
            message += line + "\n"
        else:
            message += f"{hour}: ingen data\n"
    return message.strip()

def get_news_summary():
    feed = feedparser.parse("https://www.svt.se/nyheter/rss.xml")
    headlines = [entry["title"] for entry in feed["entries"][:2]]
    summary = "Nyheter:\n" + "\n".join(f"- {h}" for h in headlines)
    return summary

def send_sms(message):
    auth = b64encode(f"{USERNAME}:{PASSWORD}".encode()).decode()
    headers = {"Authorization": f"Basic {auth}"}
    data = {
        "from": FROM_NAME,
        "to": TO_NUMBER,
        "message": message
    }
    response = requests.post("https://api.46elks.com/a1/SMS", data=data, headers=headers)
    return response.status_code, response.text

if __name__ == "__main__":
    weather = get_weather()
    news = get_news_summary()
    full_message = weather + "\n\n" + news

    if len(full_message) > 160:
        full_message = full_message[:157] + "..."
    status, response = send_sms(full_message)
    if status == 200:
        print("SMS skickat!")
    else:
        print("Fel vid SMS-sändning:", response)

