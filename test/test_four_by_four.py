import unittest
from basic_blocks.mvm_four_bit import mvm_four_by_four
from error.error_crossbar import *


class TestFourByFourMVMMethods(unittest.TestCase):

    def test_conductance_matrix_storage(self):
        mat = mvm_four_by_four()
        mat.set_conductance_matrix([[11, 13],
                                    [2, 3]])
        expected_matrix = [[11, 13],
                           [2, 3]]

        self.assertEqual(mat.get_conductance_matrix(), expected_matrix)

    def test_core_matrix_storage(self):
        mat = mvm_four_by_four()
        mat.set_conductance_matrix([[11, 2],
                                   [13, 6]])
        exp_core_msb = [[2, 0],
                        [3, 1]]
        exp_core_lsb = [[3, 2],
                        [1, 2]]

        self.assertEqual(mat.mat_arr[0].get_conductance_matrix(), exp_core_msb)
        self.assertEqual(mat.mat_arr[1].get_conductance_matrix(), exp_core_msb)
        self.assertEqual(mat.mat_arr[2].get_conductance_matrix(), exp_core_lsb)
        self.assertEqual(mat.mat_arr[3].get_conductance_matrix(), exp_core_lsb)
