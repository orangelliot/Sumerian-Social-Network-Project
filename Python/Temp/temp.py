for n in range(10):
    if n%7 != 0:
        print(n, (n**3-n)/7)

for a in range(10):
    for b in range(10):
        if (a**4-b**4)%5 == 0:
            print(a, a/5, b, b/5)