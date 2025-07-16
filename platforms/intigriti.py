import requests
from bs4 import BeautifulSoup

def fetch_intigriti():
    out = []
    url = 'https://app.intigriti.com/researcher/dashboard'
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, 'html.parser')
    programs = soup.select('div.program-card')
    for p in programs:
        name = p.select_one('h3').text.strip()
        link = p.select_one('a')['href']
        bounty_text = p.select_one('span.bounty').text if p.select_one('span.bounty') else ''
        minb, maxb = 0, 0
        import re
        m = re.search(r'\$([\d,]+)', bounty_text)
        if m:
            minb = int(m.group(1).replace(',', ''))
            maxb = minb
        out.append({
            'platform':'Intigriti',
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
