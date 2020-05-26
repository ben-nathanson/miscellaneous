from random import randint
import sys
from typing import List


class PrimeNumberSolver:
    def _find_all_primes(self, upper: int) -> set:
        candidates: set = set()
        if upper <= 1:
            return candidates
        solution_space = range(2, upper + 1)
        candidates = set(solution_space)
        for candidate in solution_space:
            if not candidate in candidates:
                continue
            knockout: int = pow(candidate, 2)
            while knockout <= upper:
                candidates.discard(knockout)  # This is the most costly operation
                knockout = knockout + candidate
        return candidates

    def find_primes_in_range(self, start: int, end: int) -> dict:
        solutions: set = set()
        solutions = self._find_all_primes(upper=max(start, end))
        solutions_sorted = set(solutions)
        for number in solutions_sorted:
            if number <= min(start, end):
                solutions.remove(number)
        return solutions


class PrimeNumberSolverRegressionTester:
    def __init__(self):
        self.solver = PrimeNumberSolver()

    def test_all(self):
        self.test_correctness()
        self.test_boundary_values()
        self.test_fuzz()
        self.test_knockout_bug

    def assert_expected_result(self, expected: set, start: int, end: int):
        found: dict = self.solver.find_primes_in_range(start=start, end=end)
        assert (
            found == expected
        ), f"\nExpected: {expected}, \nFound:    {found}.\nstart={start}, end={end}"

    def test_correctness(self):
        self.assert_expected_result(
            expected={
                2,
                3,
                5,
                7,
                11,
                13,
                17,
                19,
                23,
                29,
                31,
                37,
                41,
                43,
                47,
                53,
                59,
                61,
                67,
            },
            start=1,
            end=67,
        )
        self.assert_expected_result(expected={2, 3}, start=1, end=3)

    def test_knockout_bug(self):
        """There was a logic operator bug in _find_all_primes 
        which prevented the removal of the last non-prime number
        from the sieve"""
        a = list(self.solver.find_primes_in_range(start=1024, end=0))
        expected = 1021
        found = a[-1]
        assert expected == found, f"Expected {expected}, Found {found}."

    def test_fuzz(self, upper_bound: int = 10000, trials: int = 10):
        for n in range(trials):
            self.solver.find_primes_in_range(
                start=randint(0, upper_bound), end=randint(0, upper_bound)
            )

    def test_boundary_values(self):
        self.assert_expected_result(expected=set(), start=0, end=1)
        self.assert_expected_result(expected=set(), start=1, end=1)
        self.assert_expected_result(expected=set(), start=-1, end=1)
        self.assert_expected_result(expected=set(), start=0, end=0)
        self.assert_expected_result(expected=set(), start=-1, end=0)
        self.assert_expected_result(expected=set(), start=-2, end=-1)


def verify_command_line_args(arguments: List[str]):
    if len(arguments) != 3:
        print("Insufficient arguments.")
        return False
    lower = arguments[1]
    upper = arguments[2]
    try:
        int(upper)
        int(lower)
    except ValueError:
        print("Not a number.")
        return False
    if lower > upper:
        print("Invalid range.")
        return False
    return True


if __name__ == "__main__":
    t = PrimeNumberSolverRegressionTester()
    t.test_all()
    p = PrimeNumberSolver()
    help_message: str = "Returns all primes within a given inclusive range.\nUsage: primes.py <start> <end>."
    arguments: List[str] = sys.argv
    if not verify_command_line_args(arguments=arguments):
        print(help_message)
        exit()
    else:
        lower: int = int(arguments[1])
        upper: int = int(arguments[2])
        p = PrimeNumberSolver()
        solutions: dict = p.find_primes_in_range(start=lower, end=upper)
        print(solutions)
