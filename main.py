import argparse, os
from dotenv import load_dotenv
from platforms.hackerone import fetch_hackerone
from platforms.bugcrowd import fetch_bugcrowd
from platforms.immunefi import fetch_immunefi
from platforms.yeswehack import fetch_yeswehack
from platforms.integriti import fetch_intigriti
from filter import apply_filters
from utils import load_cache, save_cache
from notify.discord import send_discord
from notify.telegram import send_telegram
from notify.emailer import send_email

load_dotenv()
CACHE_FILE = 'cache.json'
cache = load_cache(CACHE_FILE)

def get_notify_methods(args):
    if args.notify:
        methods = args.notify.split(',')
    elif os.getenv("NOTIFY"):
        methods = os.getenv("NOTIFY").split(',')
    else:
        methods = ['terminal']
    if 'all' in methods:
        return ['terminal', 'discord', 'email', 'telegram']
    return methods

def notify(methods, msg):
    if 'terminal' in methods:
        print(msg + '\n' + '-'*40)
    if 'discord' in methods and os.getenv("DISCORD_WEBHOOK"):
        send_discord(msg)
    if 'telegram' in methods and os.getenv("TELEGRAM_BOT_TOKEN"):
        send_telegram(msg)
    if 'email' in methods and os.getenv("EMAIL_USER"):
        send_email("New Bug Bounty Program", msg)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--notify')
    parser.add_argument('--platforms')
    parser.add_argument('--min', type=int, default=0)
    parser.add_argument('--max', type=int, default=None)
    parser.add_argument('--types')
    parser.add_argument('--category')
    parser.add_argument('--new-only', action='store_true')
    parser.add_argument('--export')
    parser.add_argument('--verbose', action='store_true')
    args = parser.parse_args()

    methods = get_notify_methods(args)
    attack_types = args.types.split(',') if args.types else []
    categories = args.category.split(',') if args.category else []
    wanted_platforms = args.platforms.split(',') if args.platforms else []

    fetchers = []
    if not wanted_platforms or 'hackerone' in wanted_platforms:
        fetchers.append(fetch_hackerone)
    if not wanted_platforms or 'bugcrowd' in wanted_platforms:
        fetchers.append(fetch_bugcrowd)
    if not wanted_platforms or 'immunefi' in wanted_platforms:
        fetchers.append(fetch_immunefi)
    if not wanted_platforms or 'yeswehack' in wanted_platforms:
        fetchers.append(fetch_yeswehack)
    if not wanted_platforms or 'intigriti' in wanted_platforms:
        fetchers.append(fetch_integriti)

    programs = []
    for fetch in fetchers:
        try:
            programs.extend(fetch())
        except Exception as e:
            print(f"Error fetching from {fetch.__name__}: {e}")

    filtered = apply_filters(programs, args.min, args.max, attack_types, categories)

    new_items = []
    for prog in filtered:
        uid = prog['platform'] + '::' + prog['url']
        if args.new_only and uid in cache:
            continue
        new_items.append(prog)
        cache.add(uid)

        msg = f"{prog['name']} ({prog['platform']})\n{prog['url']}\nBounty: ${prog['bounty_min']}-{prog.get('bounty_max','?')}\nCategory: {prog.get('category','')}\nAttacks: {','.join(prog.get('attack_types', []))}\n"
        if args.verbose:
            msg += f"Scope:\n{prog.get('scope','')}\nDescription:\n{prog.get('description','')}\n"
        notify(methods, msg)

    save_cache(CACHE_FILE, cache)

    if args.export and new_items:
        import csv, json
        if args.export == 'json':
            with open('export.json', 'w') as f:
                json.dump(new_items, f, indent=2)
        elif args.export == 'csv':
            keys = new_items[0].keys()
            with open('export.csv', 'w', newline='') as f:
                import csv
                dict_writer = csv.DictWriter(f, keys)
                dict_writer.writeheader()
                dict_writer.writerows(new_items)

if __name__ == "__main__":
    main()
