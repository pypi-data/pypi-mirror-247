class Calculator:
    def __init__(self):
        """
        Initializes a new Calculator object with an initial memory value of 0.
        """

        self.memory = 0

    def add(self, num):
        """
        Adds the given number to the memory.

        Parameters:
        - num (float): The number to be added to the memory.
        """

        self.memory += num
        return self.memory

    def subtract(self, num):
        """
        Subtracts the given number from the memory.

        Parameters:
        - num (float): The number to be subtracted from the memory.
        """

        self.memory -= num
        return self.memory

    def multiply(self, num):
        """
        Multiplies the memory by the given number.

        Parameters:
        - num (float): The number to multiply the memory by.
        """

        self.memory *= num
        return self.memory

    def divide(self, num):
        """
        Divides the memory by the given number.

        Parameters:
        - num (float): The number to divide the memory by.
        """

        self.memory /= num
        return self.memory

    def floor_divide(self, num):
        """
        Performs floor division on the memory by the given number.

        Parameters:
        - num (float): The number to perform floor division on the memory by.
        """

        self.memory //= num
        return self.memory

    def root(self, n):
        """
        Calculates the n-th root of the memory.

        Parameters:
        - n (float): The degree of the root to be calculated.
        """

        self.memory **= 1 / n
        return self.memory

    def reset_memory(self):
        """
        Resets the memory value to 0.
        """

        self.memory = 0
        return self.memory
