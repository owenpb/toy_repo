import random
from matplotlib import pyplot as plt

# Input the rule number, length of initial condition, and the number of timesteps
rule_number = 235
length = 100
time = 100

# Create list of neighborhood tuples in lexicographical order. There are nine possible neighborhoods.
neighborhoods = [(0,0), (0,1), (0, 2), (1, 0), (1, 1), (1,2), (2,0), (2,1), (2,2)]

def initialize(length):

    """
    For a specified length, a list containing random states (which can be 0, 1, or 2) is generated. Error raised if the input
    length is negative or not an integer.
    """

    if not isinstance(length, int) or length < 0:
        raise ValueError("Length must be a positive integer")
    return [random.randint(0,2) for _ in range(length)]


def lookup(rule_number):

    """
    Convert rule number (in base 10) to ternary and pad with zeros if it has fewer than 9 digits. Order should be reversed.
    Since 3^9 = 19683, the possible rule numbers are 0, 1, 2, 3, ... , 19682. In ternary the rule number has at most 9
    digits. Works by repeatedly finding the quotient and remainder after dividing by 3, with the remainder corresponding
    to one of the digits 0,1,2, which is then added to a string.
    """

    if not isinstance(rule_number, int) or rule_number < 0 or rule_number > 19682:
        raise ValueError("rule_number must be an integer between 0 and 19682 (inclusive)")

    digits = '012'
    n = rule_number
    ternary = ''

    while n!=0:
        n, i = divmod(n,3) # gives quotient and remainder after dividing by 3
        ternary = ternary + digits[i]

    if len(ternary) != 9:
        padding = 9 - len(ternary)
        ternary = ternary + '0'*padding

    return dict(zip(neighborhoods, map(int, ternary)))


initial_condition = initialize(length)
lookup_table = lookup(rule_number)

class ECA(object):
    '''
    ECA: Elementary cellular automata
    '''
    def __init__(self, rule_number, initial_condition):
        '''
        For the given rule number, create lookup table, set initial condition, initialize spacetime field.
        '''

        for i in initial_condition:
            if i not in [0,1,2]:
                raise ValueError("The initial condition must be a list containing 0's, 1's and 2's only")

        self.lookup_table = lookup(rule_number)
        self.initial = initial_condition
        self.spacetime = [initial_condition]
        self.current_config = initial_condition.copy()
        self._length = len(initial_condition)

    def evolve(self, time_steps):
        '''
        Evolves the cellular automata for a specified number of timesteps.
        '''
        if time_steps < 0:
            raise ValueError("Number of timesteps must be a non-negative integer")
        try:
            time_steps = int(time_steps)
        except ValueError:
            raise ValueError("Number of timesteps must be a non-negative integer")

        for _ in range(time_steps):
            new_config = []
            for i in range(self._length):

                neighborhood = (self.current_config[(i-1)%length], self.current_config[i]) # apply periodic boundary condition
                new_config.append(self.lookup_table[neighborhood])

            self.current_config = new_config
            self.spacetime.append(new_config)

# Evolve the CA for 'time' timesteps, with rule number and initial condition as previously specified
config = ECA(rule_number, initial_condition)
config.evolve(time)
field = config.spacetime

# Plot the spacetime field diagram. 0=white, 1=light, 2=darkest
plt.figure(figsize=(12,12))
plt.imshow(field, cmap=plt.cm.Reds, interpolation='nearest')

plt.savefig('3_state_CA_ouput.jpg')

plt.show()
