#!/usr/bin/env python3
"""Non-destructive check for public GameDay ladder accessibility and format."""
import re
from urllib.parse import urlsplit
from urllib.robotparser import RobotFileParser
import requests
from bs4 import BeautifulSoup

URL = "https://websites.mygameday.app/comp_info.cgi?a=LADDER&c=0-12901-208419-662896-27305228&pool=1"
UA = "MelbourneBaseballClubPublicStatsChecker/1.0 (GitHub Actions; periodic, limited requests)"
TIMEOUT = 20


def main():
    domain = urlsplit(URL).netloc
    robots_url = f"https://{domain}/robots.txt"
    try:
        rr = requests.get(robots_url, headers={"User-Agent": UA}, timeout=TIMEOUT)
        print(f"robots.txt status: {rr.status_code}")
        if rr.ok:
            rp = RobotFileParser()
            rp.parse(rr.text.splitlines())
            if not rp.can_fetch(UA, URL):
                print("SCRAPING_DISABLED: robots.txt disallows the supplied URL")
                return
        elif rr.status_code in (401, 403):
            print("SCRAPING_DISABLED: robots.txt access restricted")
            return
    except requests.RequestException as exc:
        print(f"robots check unavailable ({type(exc).__name__}), no collection attempted")
        return

    try:
        response = requests.get(URL, headers={"User-Agent": UA, "Accept": "text/html"}, timeout=TIMEOUT)
        print(f"ladder status: {response.status_code}")
        response.raise_for_status()
        if len(response.content) > 3_000_000:
            print("ERROR: oversized HTML")
            return
        soup = BeautifulSoup(response.text, "html.parser")
        title = soup.title.get_text(" ", strip=True) if soup.title else "(no title)"
        print("page title:", title[:200])
        print("HTML size:", len(response.content))
        tables = soup.find_all("table")
        print("number of tables:", len(tables))
        for i, table in enumerate(tables[:10]):
            header = [x.get_text(" ", strip=True) for x in table.select("tr")[:1] for x in x.find_all(["td", "th"])]
            print(f"table {i}: rows={len(table.select('tr'))}, header={header[:15]}")
        text = soup.get_text(" ", strip=True)
        print("mentions Melbourne:", bool(re.search(r"\bMelbourne\b", text, re.I)))
        print("mentions Premier:", "premier" in text.lower())
        print("mentions Victoria:", "victoria" in text.lower())
        print("links to match centre:", len(soup.select('a[href*="round_info.cgi"]')))
        print("links to player statistics:", len(soup.select('a[href*="rpt_stats.cgi"],a[href*="player_info.cgi"]')))
        print("PROBE_COMPLETED (does not update published statistics)")
    except requests.RequestException as exc:
        print("FETCH_FAILED:", type(exc).__name__, str(exc)[:220])


if __name__ == "__main__":
    main()
