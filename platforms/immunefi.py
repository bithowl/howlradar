import requests

def fetch():
    url = 'https://immunefi.com/api/bug-bounty-programs/'
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json"
    }
    try:
        res = requests.get(url, headers=headers, timeout=10)
        res.raise_for_status()  # Raises HTTPError if not 2xx
        if 'application/json' not in res.headers.get('Content-Type', ''):
            print("⚠️ Immunefi returned non-JSON response.")
            print(res.text[:200])  # print a sample
            return []
        data = res.json()
        programs = []
        for item in data.get('programs', []):
            programs.append({
                'name': item.get('name'),
                'platform': 'immunefi',
                'url': 'https://immunefi.com' + item.get('url', ''),
                'bounty_min': item.get('min_reward', 0),
                'bounty_max': item.get('max_reward', 0),
                'category': 'web3',
                'attack_types': item.get('attack_types', []),
                'scope': item.get('scope', ''),
                'description': item.get('description', '')
            })
        return programs
    except requests.RequestException as e:
        print(f"🛑 HTTP error fetching Immunefi: {e}")
    except ValueError as e:
        print(f"🛑 JSON decode error from Immunefi: {e}")
    return []
