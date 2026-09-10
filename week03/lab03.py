import random


def generate_mad_lib(adjective, noun, verb):
    """Return a short story containing the supplied words."""
    return f"The {adjective} {noun} {verb} through the park."


def guessing_game():
    """Run an interactive number-guessing game."""
    secret_number = random.randint(1, 100)

    while True:
        guess = int(input("Guess a number from 1 to 100: "))

        if guess < secret_number:
            print("Too low!")
        elif guess > secret_number:
            print("Too high!")
        else:
            print("Correct! You guessed the number.")
            break
