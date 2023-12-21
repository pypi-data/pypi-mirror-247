class Calculator:

    def __init__(self, memory = 0.0):
        self.memory = memory

    def reset_memory(self):
        self.memory = 0.0
        """
        Reset the calculator memory value to zero.
        
        """

    def Addition(self, *arg: float):
        self.memory += sum(arg)
        print(self.memory)
        """
        Numbers Addition.

        In this method variables (numbers) of arguments
        added to the current self.memory value: 0.0.

        arg: chosen number for addition.
        arg type: float.
        """

    def Subtraction(self, *arg: float):
        number = self.memory
        for i in arg:
            number -= i
        self.memory = number
        print(self.memory)
        """
        Numbers Subtraction.

        In this method variables (numbers) of arguments
        one by one subtracted from current self.memory value: 0.0.

        arg: chosen number for subraction.
        arg type: float.
        """
    
    def Multiplication(self, *arg: float):
        self.memory = 1.0
        for i in arg:
            self.memory *= i
        print(self.memory)
        """
        Numbers Multiplication.

        In this method self.memory value: 1.0 is multiplied
        by each variables (numbers) in arguments.

        arg: chosen number for multiplication.
        arg type: float.
        """
    
    def Division(self, *arg: float):
        self.memory = arg[0]
        for i in arg[1:]:
            if i == 0:
                raise ZeroDivisionError("Division by 0 is impossible")
            else:
                self.memory /= i
        print(self.memory)  
        """
        Numbers Division.

        In this method self.memory value: first argument.
        Self.memory is divided by each variables (numbers),
        started from second, in arguments.

        arg: chosen number for division.
        arg type: float.

        ZeroDivisionError: raise if division by zero is attemped.
        """     
    
    def Root(self, nth_root: float, number: float):
        if number > 0 and nth_root != 0:
            self.memory = number ** (1/nth_root)
        elif number < 0 and nth_root != 0:
            self.memory = ((-1 * number) ** (1/nth_root)) * -1
        else:
            raise ZeroDivisionError("There is no 0-th root operation")
        print(round((self.memory), 2))
        """
        Nth Root calculations.

        In this method:
        For positive number with nth_root not equal to 0,
        number exponent by 1/nth_root. 
        For negative number with nth_root not equal to 0,
        number multiplied by -1, exponent by 1/nth_root and
        multiplied by -1.
        For numbers with nth_root equal to 0,
        raise ZeroDivisionError: There is no 0-th root operation.

        nth_root: chosen number root number.
        number: chosen number for root opeartion.

        ZeroDivisionError: raise if nth_root is 0.
        """   

