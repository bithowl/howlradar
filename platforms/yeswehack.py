import requests
from bs4 import BeautifulSoup

def fetch_yeswehack():
    out = []
    url = 'https://www.yeswehack.com/programs'
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, 'html.parser')
    programs = soup.select('div.program-card')
    for p in programs:
        name = p.select_one('h3').text.strip()
        link = 'https://www.yeswehack.com' + p.select_one('a')['href']
        bounty = p.select_one('span.bounty').text if p.select_one('span.bounty') else ''
        minb, maxb = 0, 0
        import re
        m = re.search(r'\$([\d,]+)', bounty)
        if m:
            minb = int(m.group(1).replace(',', ''))
            maxb = minb
        out.append({
            'platform':'YesWeHack',
            'name': name,
            'url': link,
            'bounty_min': minb,
            'bounty_max': maxb,
            'attack_types': [],
            'category': '',
            'scope': '',
            'description': ''
        })
    return out
