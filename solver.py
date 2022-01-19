#!/usr/bin/env python3
"""
Methods for determining optimal play of https://www.powerlanguage.co.uk/wordle/

Terminology:
* The "answer" is the word that the player is trying to determine
* A "guess" is a word submitted as a candidate for the answer. A "guess-letter" is a letter in a guess.
* A "response" is a set of evaluations of the states (see below) of letters in a guess
* States:
** A guess-letter is correct if it is in the same position in the guess as in the answer.
** A guess-letter is present if it is present in the answer, but not in the same position.
** A guess-letter is absent if it is not in the answer.
** Note that these are in decreasing order of binding. For instance, for the guess "spine" and answer "apple", the second guess-letter (P) is Correct, not Present (even though there is also a P in the 3rd position of the answer)
* All ordinals are human-readable text are 1-indexed
"""
from collections import defaultdict
from enum import Enum, auto
from heapq import heappush, nlargest, nsmallest

# If I were being really strict about organization, `State` should probably live in a separate module.
from data import ALLOWED_GUESSES, WORD_LIST, State
from progress_bar import progressbar

def main():
  guesses_heap = []
  for guess in progressbar(ALLOWED_GUESSES):
    cost = findCostOfPartitioning(determinePartitionSizes(guess, WORD_LIST))
    heappush(guesses_heap, (cost, guess))
  print('Best guesses:')
  for cost_and_guess in nsmallest(5, guesses_heap, key=lambda tup: tup[0]):
    print(cost_and_guess)
  print()
  print('Worst guesses:')
  for cost_and_guess in nlargest(5, guesses_heap, key=lambda tup: tup[0]):
    print(cost_and_guess)


def findCostOfPartitioning(partitions):
  """
  A good partition is one with a low sum-of-squares-of-size. This is because we want to maximize the probability that the answer
  is in a partition with low size - the lower the size of the partition, the fewer words you have to choose from on the next round.

  The probability that the target word is in a given partition is proportional to the size of the partition.

  We evaluate the "cost" of a partitioning (rather than a score) so that it is proportional to the size of a partition.
  Otherwise, score evaluation (as (1/size(partition) * (size(partition)/(size(wordList))))) would be a constant.

  Cost(partioning) = Sum(Cost(partition) * P(target word is in partition))
                   = Sum(Size(partition) * size(partition)/size(word_list))
                   = Sum(Size(partition)^2 * 1/size(word_list))
                   = k * Sum(Size(partition)^2)

  For normalization, we divide by the maximal-possible-cost - when all words are in a single partition (i.e. when a guess provided no information).
  We divide by this sum-of-squares so that the maximal cost is 1.

  This approach relies on the fact that "sum of squares is less than square of sums" - https://math.stackexchange.com/a/439226/145654
  """
  numWords = sum(partitions.values())
  upperBound = numWords**2 # Sum of Squares if all candidates are in a single partition
  unnormalizedCost = sum([val**2 for val in partitions.values()])
  return float(unnormalizedCost)/upperBound

def determinePartitionSizes(wordGuess, wordList):
  """
  Determine the sizes of the partitions that guessing `word` divides `wordList` into based on the possible responses.

  The wordList will be split into (3^5=)243 partitions, since there are 3 states for each of the 5 letters in the guess
  (correct, present, and absent). Assuming that each word in the wordList is equally likely to be the answer, the best
  guess should be the one that splits the partitions most evenly, since that is most likely to give the most information.
  (TODO: elaborate on this in blog post - consider binary search, larger probability that target is in larger section)
  """

  # `partitionSizes` will be a map from `sequence of states` to `number of words in wordList that match those states
  partitionSizes = defaultdict(int)

  for word in wordList:
    states = [State.UNKNOWN]*len(word)
    for idx, letter in enumerate(word):
      # Intentionally no checking for same length - assuming wordList is well-formed, for speed
      if wordGuess[idx] == letter:
        states[idx] = State.CORRECT
        continue
      if letter in wordGuess: # But - because we `continue` above - implicitly, wordGuess[idx] != letter
        states[idx] = State.PRESENT
        continue
      states[idx] = State.ABSENT
    partitionSizes[tuple(states)]+=1 # thank you, `defaultdict`!

  assert (sum(partitionSizes.values()) == len(wordList))

  return partitionSizes

if __name__ == '__main__':
  main()
