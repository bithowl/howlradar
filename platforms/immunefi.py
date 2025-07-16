import requests

def fetch_immunefi():
    out = []
    url = 'https://immunefi.com/bounty-programs/'
    resp = requests.get(url)
    programs = resp.json().get('programs', [])
    for p in programs:
        minb = p.get('min_bounty', 0)
        maxb = p.get('max_bounty', 0)
        out.append({
            'platform':'Immunefi',
            'name': p.get('name', ''),
            'url': p.get('url', ''),
            'bounty_min': minb,
            'bounty_max': maxb,
            'attack_types': [],
            'category': '',
            'scope': '',
            'description': p.get('description', '')
        })
    return out
