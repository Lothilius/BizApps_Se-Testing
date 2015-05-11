__author__ = 'Lothilius'

import numpy as np
import random
import string


# Create random string values
def id_generator(size=6, chars=string.ascii_uppercase):
    return ''.join(random.choice(chars) for _ in range(size))


# Create random number
def id_generator(size=6, chars=string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


# Create array
