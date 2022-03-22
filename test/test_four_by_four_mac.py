import unittest
from basic_blocks.mvm_four_bit import mvm_four_by_four
from error.error_crossbar import *


class TestFourByFourMAC(unittest.TestCase):
    '''
    Test some multiplier structures
    '''

    def test_multiply_and_accumulate_operation_four_by_four(self):
        '''
        Test the multiplication:

            | 11    13| | 3 | = | 150 |
            | 2      6| | 9 | = |  60 |

        Remember, the matrix above is stored as its transpose in the ReRAM crossbar 
        '''
        mat = mvm_four_by_four()
        mat.set_conductance_matrix([[11, 2],
                                    [13, 6]])
        input_v = [3, 9]

        mat.crossbar_multiply(input_v=input_v)

        expected_matrix = [150, 60]
        self.assertEqual(mat.get_shift_reg_values(), expected_matrix)


if __name__ == "__main__":
    unittest.main()
