class ArithOps:
    """
    A class that performs basic mathematical calculations.

    Methods:
        add(num1, num2): Add two numbers and return their sum.
        sub(num1, num2): Subtract two numbers and return their difference.
        mul(num1, num2): Multiply two numbers and return their product.
        div(num1, num2): Divide two numbers and return their quotient.
    """
    def add(self, num1, num2):
        """
        Add two numbers and return their sum.

        Parameters:
            num1 (int): The first number to be added.
            num2 (int): The second number to be added.

        Returns:
            int: The sum of the two numbers.
        """
        return num1 + num2

    def sub(self, num1, num2):
        """
        Subtract two numbers and return their difference.

        Parameters:
            num1 (int): The first number to be subtracted.
            num2 (int): The second number to be subtracted.

        Returns:
            int: The difference of the two numbers.
        """
        return num1 - num2

    def mul(self, num1, num2):
        """
        Multiply two numbers and return their product.

        Parameters:
            num1 (int): The first number to be multiplied.
            num2 (int): The second number to be multiplied.

        Returns:
            int: The product of the two numbers.
        """
        return num1 * num2

    def div(self, num1, num2):
        """
        Divide two numbers and return their quotient.

        Parameters:
            num1 (int): The dividend.
            num2 (int): The divisor.

        Returns:
            float: The quotient of the two numbers.
        """
        if num2 != 0:
            return num1 / num2
        else:
            raise ValueError("Cannot divide by zero.")