def getcowlist(cows, limit):
    dicty = cows
    rev_dict = {v:k for k,v in dicty.items()}
    keys = list(rev_dict.keys())
    keys.sort(reverse=True)
    total = []
    while len(keys) > 0:
        inner = []
        sumy = 0
        used = []
        for key in keys: 
            if sumy + key < limit:
                inner.append(rev_dict[key])
                used.append(key)
                sumy+=key
        total.append(inner)
        for k in used:
            keys.remove(k)
    return total

cows = dicty = {'Belle': 2, 'Betsy': 5, 'Bessy': 8}
limit = 10
print(getcowlist(cows, limit))
