from difflib import SequenceMatcher

def get_sim_metric(s1, s2):
    ssl = len(s1)
    if ssl < len(s2):
        best = 0
        for i in range(len(s2) - ssl):
            segsim = SequenceMatcher(None, s1, s2[i:i+ssl]).ratio()
            if segsim > best:
                best = segsim
        return best
    return SequenceMatcher(None, s1, s2).ratio()