#!usr/bin/env python3

"""
Method for generating examples for blog post on blog.scubbo.org
"""
from itertools import product, islice

from data import ALLOWED_GUESSES, WORD_LIST, State

def examples():
  # Chosen arbitrarily as having "nice" letters :P

  # Lack of repeated letters means building conditions is easier - we don't have to worry about the
  # contradictory case where one condition says "<letter> is in word" and another condition says
  # "<letter> is not in word". That is - all 125 possible partitions are valid.
  guess_word = 'pints'
  partitions = product([State.ABSENT, State.PRESENT, State.CORRECT], repeat=5)
  for partition in partitions:
    conditions = _build_conditions(partition, guess_word)
    words = islice((word for word in ALLOWED_GUESSES if all([condition(word) for condition in conditions])), 10)
    print(f'{[s.name for s in partition]}: {list(words)}')

def _build_conditions(partition, guess_word):
  conditions = []
  for idx, state in enumerate(partition):
    conditions.append(_build_condition(state, idx, guess_word))
  return conditions

def _build_condition(state, idx, guess_word):
  if state == State.ABSENT:
    return lambda x: guess_word[idx] not in x
  if state == State.PRESENT:
    return lambda x: guess_word[idx] in x and x[idx] != guess_word[idx]
  if state == State.CORRECT:
    return lambda x: x[idx] == guess_word[idx]