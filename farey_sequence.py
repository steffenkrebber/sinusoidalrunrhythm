#!/usr/bin/env python3
# Python3 program to print
# Farey Sequence of given order

# code taken and adapted from: https://fr.acervolima.com/sequence-de-farey/
# under CCBY-SA - https://creativecommons.org/licenses/by/4.0/

# class for x/y (a term in farey sequence
class Term:

    # Constructor to initialize
    # x and y in x/y
    def __init__(self, x, y):
        self.x = x
        self.y = y

# GCD of a and b
def gcd(a, b):
    if b == 0:
        return a
    return gcd(b, a % b)

# Function to print
# Farey sequence of order n
def farey(n):

    # Create a vector to
    # store terms of output
    v = []

    # One by one find and store
    # all terms except 0/1 and n/n
    # which are known
    for i in range(1, n + 1):
        for j in range(i + 1, n + 1):

            # Checking whether i and j
            # are in lowest term
            if gcd(i, j) == 1:
                v.append(Term(i, j))

    # Sorting the term of sequence
    for i in range(len(v)):
        for j in range(i + 1, len(v)):
            if (v[i].x * v[j].y > v[j].x * v[i].y):
                v[i], v[j] = v[j], v[i]
    return v

# Driver Code
if __name__ == "__main__":
    n = 8
    sequence = farey(n)
    print(f"Farey sequence of order {n} (length: {len(sequence)}) is:")
    print("0/1", end = " ")
    for i in range(len(sequence)):
        print(f"{sequence[i].x}/{sequence[i].y}", end = " ")

    # explicitly printing last term
    print("1/1")
