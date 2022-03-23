import operator
from typing import List
from error.error_crossbar import *
from basic_blocks.mvm_two_bit import mvm_two_by_two


class mvm_four_by_four():
    '''
    Multiply two 4-bit numbers by making use of 2 bit 2x2 crossbar
    '''

    def __init__(self):

        # Define two 2x2 matrix crossbars
        self.mat_arr = [mvm_two_by_two() for _ in range(4)]
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

        msb_conductance_matrix = [[(matrix[0][0] >> 2) & 3, (matrix[0][1] >> 2) & 3],
                                  [(matrix[1][0] >> 2) & 3, (matrix[1][1] >> 2) & 3]]

        lsb_conductance_matrix = [[matrix[0][0] & 3, matrix[0][1] & 3],
                                  [matrix[1][0] & 3, matrix[1][1] & 3]]

        # Set the conductance matrix for the 2x2 crossbar - Core 0 and 1
        self.mat_arr[0].set_conductance_matrix(msb_conductance_matrix)
        self.mat_arr[1].set_conductance_matrix(msb_conductance_matrix)

        # Set the conductance matrix for the 2x2 crossbar - Core 2 and 3
        self.mat_arr[2].set_conductance_matrix(lsb_conductance_matrix)
        self.mat_arr[3].set_conductance_matrix(lsb_conductance_matrix)

    def set_shift_register(self, values: List[int]):
        '''
        Set the Value of the Output Shift register
        '''

        if len(values) != 2:
            raise WrongShiftRegisterSetDimension(
                expected_length=2
            )

        self.shift_reg_output = values

    def leftshift_shift_reg(self, shifts=1):
        '''
        Bitshift the shift register to the left 
        Default shifts by one
        '''

        shift_reg_val = self.get_shift_reg_values()
        shift_reg_val = [(i << shifts) for i in shift_reg_val]
        self.set_shift_register(shift_reg_val)

    def clear_shift_reg(self):
        '''
        Clear the shift reg - back to [0, 0]
        '''

        self.shift_reg_output = [0, 0]

    def crossbar_multiply(self, input_v):
        '''
        Crossbar Multiplication
        '''
        bit_pos_0 = [int((input_v[0] & (1 << 0)) > 0),
                     int((input_v[1] & (1 << 0)) > 0)]
        bit_pos_1 = [int((input_v[0] & (1 << 1)) > 0),
                     int((input_v[1] & (1 << 1)) > 0)]
        bit_pos_2 = [int((input_v[0] & (1 << 2)) > 0),
                     int((input_v[1] & (1 << 2)) > 0)]
        bit_pos_3 = [int((input_v[0] & (1 << 3)) > 0),
                     int((input_v[1] & (1 << 3)) > 0)]

        # Core 0 - MSB G and LSB V
        self.mat_arr[0].crossbar_multiply(bit_pos_1)
        self.mat_arr[0].leftshift_shift_reg()
        self.mat_arr[0].crossbar_multiply(bit_pos_0)

        # Core 1 - MSB G and MSB V
        self.mat_arr[1].crossbar_multiply(bit_pos_3)
        self.mat_arr[1].leftshift_shift_reg()
        self.mat_arr[1].crossbar_multiply(bit_pos_2)

        # Core 2 - LSB G and LSB V
        self.mat_arr[2].crossbar_multiply(bit_pos_1)
        self.mat_arr[2].leftshift_shift_reg()
        self.mat_arr[2].crossbar_multiply(bit_pos_0)

        # Core 3 - LSB G and MSB V
        self.mat_arr[3].crossbar_multiply(bit_pos_3)
        self.mat_arr[3].leftshift_shift_reg()
        self.mat_arr[3].crossbar_multiply(bit_pos_2)

        # Cores ready, shift and add
        # MSB/MSB - 4 left shifts
        # MSB/LSB + LSB/MSB - 2 left shifts
        # LSB/LSB - No shifts

        self.mat_arr[0].leftshift_shift_reg(2)  # Core 0
        self.mat_arr[1].leftshift_shift_reg(4)  # Core 1
        self.mat_arr[2].leftshift_shift_reg(0)  # Core 2
        self.mat_arr[3].leftshift_shift_reg(2)  # Core 3

        self.set_shift_register(
            [sum(it) for it in zip(self.mat_arr[0].get_shift_reg_values(),
                                   self.mat_arr[1].get_shift_reg_values(),
                                   self.mat_arr[2].get_shift_reg_values(),
                                   self.mat_arr[3].get_shift_reg_values())]
        )

        return [self.mat_arr[0].get_shift_reg_values(),
                self.mat_arr[1].get_shift_reg_values(),
                self.mat_arr[2].get_shift_reg_values(),
                self.mat_arr[3].get_shift_reg_values()]
