def unique_partitions(n):
    # Base case of recursion: zero is the sum of the empty list
    if n == 0:
        yield []
        return
        
    # Modify partitions of n-1 to form partitions of n
    for p in unique_partitions(n-1):
        yield [1] + p
        if p and (len(p) < 2 or p[1] > p[0]):
            yield [p[0] + 1] + p[1:]

for partition in unique_partitions(5):
    print(sorted(partition, reverse=False))


