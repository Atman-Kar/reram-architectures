import unittest
from basic_blocks.mvm_two_bit import mvm_two_by_two
from error.error_mvm_two_by_two import *


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
