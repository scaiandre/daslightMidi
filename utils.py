import random


def select_different_random_value(array, currentvalue):
    """Selects a random value from the given array differing from passed."""
    if not array:  # Check if the array is empty
        return None  # Or raise an error or another appropriate response
    while True:
        nextvalue = random.choice(array)
        if nextvalue != currentvalue:
            return nextvalue


def select_random_value(array):
    """Selects a random value from the given array."""
    if not array:  # Check if the array is empty
        return None  # Or raise an error or another appropriate response
    return random.choice(array)