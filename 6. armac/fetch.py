import requests

def fetch():
    url = "http://localhost/timelapse/NVDA?tier=1h&ticker=NVDA"
    resp = requests.get(url)
    return resp.text
