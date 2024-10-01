import random
import string

class Generator:

    @staticmethod
    def random_char():
        char_list = string.ascii_lowercase + string.digits
        random_char = ''.join(random.choice(char_list) for _ in range(1))
        return random_char

    @staticmethod
    def random_number(min, max):
        random_number = random.randint(min, max)
        return random_number

    @staticmethod
    def biased_boolean(probability):
        return random.random() < probability