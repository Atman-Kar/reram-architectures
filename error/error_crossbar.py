class WrongConductanceMatrixError(Exception):
    '''
    If the conductance matrix to be updated is of wrong dimensions provided by the user
    '''

    def __init__(self, expected_dimensions):
        self.message = f"Wrong Conductance Matrix Dimensions. Expected dimensions of {expected_dimensions}."
        super().__init__(self.message)


class InvalidInputVoltageError(Exception):
    '''
    The Input Voltage at a given time is binary - either 0/1
    '''

    def __init__(self):
        self.message = f"Invalid Input Voltage Values. Expected values are : 0/1"
        super().__init__(self.message)


class WrongInputVoltageDimensionError(Exception):
    '''
    The Input Voltage is of the wrong length for this block
    '''

    def __init__(self, expected_length):
        self.message = f"The Input Voltage is of the wrong length for this block. Expected length of {expected_length}."
        super().__init__(self.message)


class WrongShiftRegisterSetDimension(Exception):
    '''
    Input Value to be set is of wrong dimesion for this block 
    '''

    def __init__(self, expected_length):
        self.message = f"The Input Values is of the wrong length for this block. Expected length of {expected_length}."
        super().__init__(self.message)
