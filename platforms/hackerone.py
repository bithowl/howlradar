import requests, feedparser, re

def fetch_hackerone():
    out = []
    feed = feedparser.parse('https://hackerone.com/blog.rss')
    for e in feed.entries:
        if 'launch' not in e.title.lower():
            continue
        m = re.search(r'(\$[\d,]+)(?:–\$([\d,]+))?', e.summary or '')
        minb = int(m.group(1).replace('$','').replace(',','')) if m else 0
        maxb = int(m.group(2).replace(',','')) if m and m.group(2) else minb
        out.append({
            'platform':'HackerOne',
            'name': e.title,
            'url': e.link,
            'bounty_min': minb,
            'bounty_max': maxb,
            'attack_types': [], 
            'category':'', 
            'scope':'', 
            'description':''
        })
    return out
