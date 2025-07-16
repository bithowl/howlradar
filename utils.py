import os, json

def load_cache(f):
    if os.path.exists(f):
        with open(f, 'r') as file:
            return set(json.load(file))
    return set()

def save_cache(f, cache_set):
    with open(f, 'w') as file:
        json.dump(list(cache_set), file)
