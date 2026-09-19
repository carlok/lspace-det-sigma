import re, time, snappy
from khoca import InteractiveCalculator
KQ = InteractiveCalculator(1, (0, 1), 0)
K2 = InteractiveCalculator(2, (0, 1), 0)

def s_of(KH, pd):
    _, mess = KH(pd, print_messages=True)
    i = mess.index('Reduced Homology:')
    j = mess.index('Unreduced Homology:')
    red = mess[i:j]
    inf = next(k for k, m in enumerate(red) if 'infinity' in m)
    terms = re.findall(r't\^(-?\d+)q\^(-?\d+)', red[inf + 1])
    assert len(terms) == 1 and terms[0][0] == '0', red
    return int(terms[0][1])

def invariants(link):
    pd = link.PD_code()
    pd = [list(map(int, c)) for c in pd]
    h = link.knot_floer_homology()
    return dict(tau=h['tau'], epsilon=h['epsilon'], fibered=h['fibered'], genus=h['seifert_genus'],
                sQ=s_of(KQ, pd), sF2=s_of(K2, pd))
