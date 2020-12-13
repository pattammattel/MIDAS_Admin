from random import randrange, random

jan  = {
    'sequoia': randrange(10_000, 30_000),
    'vulcan':  randrange(10_000, 20_000),
    'quartz':  randrange( 5_000,  7_500),
    'zin':     randrange( 1_000,  1_500),
}
may = {
    'sequoia': randrange(10_000, 30_000),
    'vulcan':  randrange(10_000, 20_000),
    'quartz':  randrange( 5_000,  7_500),
    'sierra':  randrange(30_000, 50_000),
}


j = []

for key,value in jan.items():
    print(key,value)
    j.append(value)
print(j)





