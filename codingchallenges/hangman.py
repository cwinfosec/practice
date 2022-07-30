#!/usr/bin/env python3

import sys
import random

####################
#
# Hangman
#
# Rules:
# 1. choose a secret word from a list - done
# 2. have input to check letter of word - done
# 3. if we have a match, fill in all matches
# 4. if we don't match, fill in hangman - done
# 5. if we win - print win message - done
# 6. if we lose - print lose message + restart - done

def get_words(wordlist):
        """ Get a random word from the wordlist """

        with open(wordlist, "r") as f:
                lines = f.readlines()
                word = random.choice(lines)
        return word

def get_output(word, guess_stack):
        """ Display hidden length of word + correct guesses """
        word = word.strip('\n')
        for letter in word:
                if letter in guess_stack:
                        print(f"{letter} ", end="")
                else:
                        print("_ ", end="")
        print("\n")

def tracker(word, guesses):
        print("---------------------------------")
        x = print(f"Guesses: {guesses} | Remaining: {(len(word) - 1) - guesses}\n")
        return x

def main(word):
        """ Main function """

        letter_stack = []
        guess_stack = []

        guesses = 1
        correct = 0

        guess = ""

        for letter in word:
                if '\n' in letter:
                        break
                else:
                        letter_stack.append(letter)

        while guesses <= (len(word) - 1):
                get_output(word, guess_stack)
                guess = input("Guess a letter: ")

                if "hint" in guess:
                        print(f"The first letter is: {word[0]}")

                elif len(guess) != 1:
                        print("Guess only one letter at a time.")
                        break

                if guess in letter_stack:
                        guess_stack.append(guess)
                        correct += word.count(guess)

                if not guess in word:
                        guess_stack.append(guess)
                        guesses += 1

                if correct == (len(word) - 1):
                        get_output(word, guess_stack)
                        print(f"Win! The word was: {word}")
                        sys.exit()

                elif (len(word) - 1 - guesses) == 0:
                        print(f"Failed! The word was: {word}")
                        break

                tracker(word, guesses)


if __name__ in "__main__":
        wordlist = sys.argv[1]
        word = get_words(wordlist)
        main(word)