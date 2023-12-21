def r():
    with open('BAI01.INP', 'r') as i, open('BAI01.OUT', 'w') as o:
        s = list(map(lambda x: float(x.replace(',', '.')), i.readline().strip().split()))
        o.write(f"{len(s)}\n{max(s)}\n{s.count(max(s))}\n")