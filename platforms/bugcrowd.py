import requests
from bs4 import BeautifulSoup

def fetch_bugcrowd():
    out = []
    url = 'https://www.bugcrowd.com/programs/'
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, 'html.parser')
    cards = soup.select('div.program-card')
    for c in cards:
        name = c.select_one('h3').text.strip()
        link = c.select_one('a.program-card-link')['href']
        bounty = c.select_one('p.bounty').text if c.select_one('p.bounty') else ''
        minb, maxb = 0, 0
        import re
        m = re.search(r'\$([\d,]+)', bounty)
        if m:
            minb = int(m.group(1).replace(',', ''))
            maxb = minb
        out.append({
            'platform':'Bugcrowd',
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
