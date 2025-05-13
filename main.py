'''
This code will try to guess the sequence provided by the user. It will do so
by using information theory, and trying guesses that maximized the expected
information value, until the correct solution is found.

The game is structured so that the sequence is made by digits
from 0 to 9.
'''

from itertools import product
from math import floor, log2
from random import choice, shuffle
from time import time


def get_hints(guess, solution):
    # Return the hints for the given guess and solution.
    # hints[0]: how many in correct place
    # hints[1]: how many in wrong place

    hints = [0, 0]

    # Multiple runs
    # First run: count hints[0]. The vector remaining stores the indices
    # where no match is found, which are then parsed when counting hints[2].
    remaining = []
    for i in range(len(solution)):  # cycle through all elements
        if guess[i] == solution[i]:
            # correct digit in the correct place found
            hints[0] += 1
        else:
            remaining.append(i)

    # Second run: count hints[1], among the remaining elements.
    remaining_solution = remaining
    for i in remaining:
        for j in remaining_solution:
            if (i != j) and (guess[i] == solution[j]):
                hints[1] += 1
                # remove matching index and break, so that it is not counted
                # multiple times
                # filter!(x->x≠j,remaining_solution)
                remaining_solution.remove(j)
                break

    return hints


def init_possibilities(N):
    # All the possible guesses:
    # Define using Cartesian product
    possibilities = [list(p) for p in product(range(10), repeat=N)]
    return possibilities


def init_possible_hints(N):
    # Define possible hints:
    # The sum of hints[0] and hints[1] should always be <= N
    possible_hints = []
    for k in range((N + 1)**2):
        if ((k % (N + 1)) + floor(k / (N + 1))) <= N:
            possible_hints.append([floor(k / (N + 1)), k % (N + 1)])
    return possible_hints


def main():
    solution = [
        int(digit) for digit in input("Please, insert the secret sequence: ")
    ]
    N = len(solution)

    possibilities = init_possibilities(N)
    possible_hints = init_possible_hints(N)

    unsolved = True
    attempts = 0
    while unsolved:
        time_spent = time()
        # Preallocate list for expected information
        Np = len(possibilities)
        if attempts >= 1:
            expected_information = [0 for _ in range(Np)]

            # compute expected information
            for i in range(Np):
                for j in range(len(possible_hints)):
                    p = 0.0
                    for k in range(Np):
                        if possible_hints[j] == get_hints(
                                possibilities[k], possibilities[i]):
                            p += 1

                    if p > 0:
                        expected_information[i] += -p / Np * log2(p / Np)

            guess = choice([
                possibilities[i] for i in range(Np)
                if expected_information[i] == max(expected_information)
            ])

        else:
            # Try to take as many different elements as possible
            guess = [i % 10 for i in range(max(N, 10))]
            shuffle(guess)
            guess = guess[0:N]

        hints = get_hints(guess, solution)

        attempts += 1  # increase number of attempts
        time_spent = round((time() - time_spent) * 100) / 100  # compute time
        if hints == [N, 0]:
            print("\nAttempt " + str(attempts) + ": it took me " +
                  str(time_spent) + " seconds.")
            print("I found the solution:")
            print(guess)
            unsolved = False
        else:
            print("\nAttempt " + str(attempts) + ": it took me " +
                  str(time_spent) + " seconds.")
            print("I chose the following guess:")
            print(guess)
            print("and I got the following hints:")
            print(hints)

        possibilities = [
            possibilities[i] for i in range(Np)
            if get_hints(guess, possibilities[i]) == hints
        ]


if __name__ == "__main__":

    main()
