#!/usr/bin/env python3

"""
As a comparison point for my initial solver (implemented in solver.py),
I wanted to implement a smaller, simpler, and more human-understandable
approach for selecting guesses - simply pick two words that, between them,
contain the 10 most-common letters in the corpus. Using those for the first
two guesses will give a good cross-section of information, from which a human
(or another algorithmic process) should be able to guess the actual answer
fairly quickly.
"""

from collections import Counter
from itertools import product

from data import WORD_LIST, ALLOWED_GUESSES
from progress_bar import progressbar

def main():
  letter_counts = Counter()
  for word in WORD_LIST:
    for letter in word:
      letter_counts[letter]+=1
  ten_most_common_letters = [tup[0] for tup in letter_counts.most_common(10)]

  # A small optimization - before checking the (guess1, guess2) pair for if they _exactly_ match
  # the 10 most-common letters, we first trim to only the guesses that are composed of those letters.
  #
  # Since the next step is going to be O(n^2) on those guesses, this should result in a pretty significant speed-up
  # (The first time I ran the naïve version that checks the full product for exact 10-letter matches, it
  # would have taken several minutes to complete)
  #
  # (This still doesn't filter out guesses that have repeated letters, but that's probably not a big deal -
  # we can explore that if the product-checking is still infeasibly slow)
  guess_subset = [guess for guess in ALLOWED_GUESSES if all([guess_letter in ten_most_common_letters for guess_letter in guess])]
  print(f'Guess subset has size {len(guess_subset)} - a {(100*float(len(ALLOWED_GUESSES)-len(guess_subset))/len(ALLOWED_GUESSES)):.2f}% improvement on the full ALLOWED_GUESSES')

  target_string = sorted(''.join(ten_most_common_letters))
  results = []
  for guess_pair in progressbar(product(guess_subset, repeat=2), count=len(guess_subset)**2):
    if sorted((guess_pair[0]+guess_pair[1])) == target_string:
      results.append(guess_pair)
  for result in results:
    print(result)
    # /2 since `(a,b)` and `(b,a)` will be counted.
    # Could maybe fix that (and optimize!) by splitting guess_subset in half and taking the product of the halves.
  print(f' There are {len(results)/2} pairs')


if __name__ == '__main__':
  main()