'''
Author : Atman Kar
Guide: Abhijit Pethe

This file contains all the basic building blocks to create more complex architectures. 
'''

from typing import List
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
        self.shift_reg_output = [0, 0]
        self.conductance_matrix = [[0, 0],
                                   [0, 0]]

    def get_shift_reg_values(self):
        '''
        Get the current value stored in the shift register
        '''
        return self.shift_reg_output

    def get_conductance_matrix(self):
        '''
        Get the current value stored in the conductance matrix ReRAMs
        '''
        return self.conductance_matrix

    def set_conductance_matrix(self, matrix):
        '''
        Update the conductance matrix output

        TODO: Account for clock cycles?
        '''

        expected_dimensions = (2, 2)  # (Rows , Columns)
        if (len(matrix) != expected_dimensions[0]) or (len(matrix) != expected_dimensions[1]):
            # Raise an exception if the user enters the wrong matrix dimensions

            raise WrongConductanceMatrixError(
                expected_dimensions=expected_dimensions
            )

        # If assert passes, update!
        self.conductance_matrix = matrix

    def set_shift_register(self, values: List[int]):
        '''
        Set the Value of the Output Shift register
        '''

        if len(values) != 2:
            raise WrongShiftRegisterSetDimension(
                expected_length=2
            )

        self.shift_reg_output = values

    def crossbar_multiply(self, input_v: List[int]):
        '''
        Multiply G with V (MVM)

        TODO: Have to take account into clock cycles taken
        '''

        for v in input_v:
            if v not in [0, 1]:
                raise InvalidInputVoltageError()

        if len(input_v) != 2:
            raise WrongInputVoltageDimensionError(
                expected_length=2
            )

        # Output Currents - On Application of voltages through the crossbar
        I1 = (input_v[0]*self.conductance_matrix[0][0]) + \
            (input_v[1]*self.conductance_matrix[1][0])
        I2 = (input_v[0]*self.conductance_matrix[0][1]) + \
            (input_v[1]*self.conductance_matrix[1][1])

        output_current_vector = [I1, I2]

        self.set_shift_register(self.shift_reg_add(output_current_vector))

        return output_current_vector

    def leftshift_shift_reg(self):
        '''
        Bitshift the shift register to the left exactly once
        '''

        shift_reg_val = self.get_shift_reg_values()
        shift_reg_val = [(i << 1) for i in shift_reg_val]
        self.set_shift_register(shift_reg_val)

    def shift_reg_add(self, vals):

        return [self.shift_reg_output[0] + vals[0], self.shift_reg_output[1] + vals[1]]

    def step_clock(cls):
        '''
        Step da clock
        '''

        cls.clock += 1
        cls.clock %= 2

        return cls.clock
