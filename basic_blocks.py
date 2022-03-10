'''
Author : Atman Kar
Guide: Abhijit Pethe

This file contains all the basic building blocks to create more complex architectures. 
'''

from error_messages import *


class mvm_two_by_two ():
    '''
    A two by two matrix vector multiplier (MVM). 

    Inputs to a matrix multiplier are:

    - A global clock
    - Input voltage (0 mV for logic 0, 100 mV for logic 1), one bit per cycle
    - Conductance Matrix Values (4 values, as 2x2 mat)
    - Crossbar current output values
    - Shift register output 
    '''

    clock = 0

    def __init__(self):
        '''
        Defining class variables for the required input data
        '''
        self.shift_reg_output = 0
        self.conductance_matrix = [[0, 0],
                                   [0, 0]]

    def get_shift_reg_value(self):
        '''
        Get the current value stored in the shift register
        '''
        return self.shift_reg_output

    def get_conductance_matrix(self):
        '''
        Get the current value stored in the conductance matrix ReRAMs
        '''
        return self.conductance_matrix

    def update_conductance_matrix(self, matrix):
        '''
        Update the conductance matrix output

        TODO: Check the number of bits of conductance matrix
        '''

        expected_dimensions = (2, 2)  # (Rows , Columns)
        if (len(matrix) != expected_dimensions[0]) or (len(matrix) != expected_dimensions[1]):
            # Raise an exception if the user enters the wrong matrix dimensions

            raise WrongConductanceMatrixError(
                expected_dimensions=expected_dimensions
            )

        # If assert passes, update!
        self.conductance_matrix = matrix

    def crossbar_multiply(self, input_v):
        '''
        Multiply G with V (MVM)

        TODO: Have to take account into clock cycles taken
        '''

        for v in input_v:
            if v != 0 or v != 1:
                raise InvalidInputVoltageError()

        if len(v) != 2:
            raise WrongInputVoltageDimensionError(
                expected_length=2
            )

        # Output Currents - On Application of voltages through the crossbar
        I1 = (input_v[0]*self.conductance_matrix[0][0]) + \
            (input_v[1]*self.conductance_matrix[1][0])
        I2 = (input_v[0]*self.conductance_matrix[0][1]) + \
            (input_v[1]*self.conductance_matrix[1][1])

        output_current_vector = [I1, I2]

        return output_current_vector

    def step_clock(cls):
        cls.clock += 1
        cls.clock %= 2

        return cls.clock
