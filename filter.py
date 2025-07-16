def apply_filters(progs, min_b, max_b, types, cats):
    filtered = []
    for p in progs:
        if p['bounty_min'] < min_b:
            continue
        if max_b and p.get('bounty_max', 0) > max_b:
            continue
        if types:
            attack_types = [a.lower() for a in p.get('attack_types', [])]
            if not any(t.lower() in attack_types for t in types):
                continue
        if cats:
            category = p.get('category', '').lower()
            if category not in [c.lower() for c in cats]:
                continue
        filtered.append(p)
    return filtered
