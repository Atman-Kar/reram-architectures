import unittest
from basic_blocks.mvm_two_bit import mvm_two_by_two
from error.error_mvm_two_by_two import *


class TestTwoByTwoMVMMethods(unittest.TestCase):
    '''
    Test the 2x2 MVM Class 
    '''

    def test_init_shift_reg(self):

        mat = mvm_two_by_two()
        mat.step_clock()
        self.assertEqual(mat.get_shift_reg_values(), [0, 0])

    def test_step_clock(self):

        mat1 = mvm_two_by_two()
        mat2 = mvm_two_by_two()
        instance_list = [mat1, mat2]
        for instance in instance_list:
            instance.step_clock()
        self.assertEqual(mat1.clock, 1)
        self.assertEqual(mat2.clock, 1)

    def test_get_conductance_matrix(self):
        mat = mvm_two_by_two()
        matrix = mat.get_conductance_matrix()
        expected_matrix = [[0, 0],
                           [0, 0]]
        self.assertEqual(matrix, expected_matrix)

    def test_update_conductance_matrix(self):
        mat = mvm_two_by_two()
        mat.set_conductance_matrix([[1, 1], [3, 3]])
        expected_matrix = [[1, 1],
                           [3, 3]]
        matrix = mat.get_conductance_matrix()
        self.assertEqual(matrix, expected_matrix)

    def test_conductance_matrix_exception_error(self):
        mat = mvm_two_by_two()
        with self.assertRaises(WrongConductanceMatrixError):
            mat.set_conductance_matrix([0])

    def test_invalid_input_voltage_vector_value(self):
        mat = mvm_two_by_two()
        with self.assertRaises(InvalidInputVoltageError):
            mat.crossbar_multiply([12, 0])

    def test_wrong_input_voltage_dimension(self):
        mat = mvm_two_by_two()
        with self.assertRaises(WrongInputVoltageDimensionError):
            mat.crossbar_multiply([0, 1, 1, 0, 1])

    def test_wrong_input_shift_reg_dimension(self):
        mat = mvm_two_by_two()
        with self.assertRaises(WrongShiftRegisterSetDimension):
            mat.set_shift_register([3, 2, 1, 1, 1, 4, 5, 6])

    def test_set_shift_register(self):
        mat = mvm_two_by_two()
        mat.set_shift_register([7, 4])
        self.assertEqual(mat.get_shift_reg_values(), [7, 4])

    def test_single_bit_crossbar_multiplier(self):
        mat = mvm_two_by_two()
        mat.set_conductance_matrix([[1, 2],
                                    [3, 2]])
        input_v = [1,
                   0]
        mat.crossbar_multiply(input_v=input_v)
        output_current_vector = mat.get_shift_reg_values()
        self.assertEqual(output_current_vector, [1, 2])

    def test_left_bitshift_shift_reg(self):
        mat = mvm_two_by_two()
        mat.set_shift_register([3, 2])
        mat.leftshift_shift_reg()
        shift_reg_out = mat.get_shift_reg_values()
        self.assertEqual(shift_reg_out, [6, 4])


class TestTwoByTwoMAC(unittest.TestCase):
    '''
    Test some multiplier structures
    '''

    def test_multiply_and_accumulate_operation(self):
        '''
        Test the multiplication:

            | 1    2| | 3 | = | 7 |
            | 3    1| | 2 | = | 11|

        Remember, the matrix above is stored as its transpose in the ReRAM crossbar 
        '''
        mat = mvm_two_by_two()
        mat.set_conductance_matrix([[1, 3],
                                    [2, 1]])

        # Start multiplication - MSB first
        input_v = [1,
                   1]
        mat.crossbar_multiply(input_v=input_v)
        mat.step_clock()

        # Shift the shift reg to the left once
        mat.leftshift_shift_reg()

        # Now add the LSB crossbar product
        input_v = [1,
                   0]
        mat.crossbar_multiply(input_v=input_v)
        mat.step_clock()

        expected_vector_output = [7,
                                  11]

        test_vector_output = mat.get_shift_reg_values()
        self.assertEqual(test_vector_output, expected_vector_output)


if __name__ == "__main__":
    unittest.main()
