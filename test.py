import unittest
from basic_blocks import mvm_two_by_two
from error_messages import *


class TestTwoByTwoMVM(unittest.TestCase):
    '''
    Test the 2x2 MVM Class 
    '''

    def test_init_shift_reg(self):

        mat = mvm_two_by_two()
        mat.step_clock()
        self.assertEqual(mat.get_shift_reg_value(), 0)

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
        mat.update_conductance_matrix([[1, 1], [3, 3]])
        expected_matrix = [[1, 1],
                           [3, 3]]
        matrix = mat.get_conductance_matrix()
        self.assertEqual(matrix, expected_matrix)

    def test_conductance_matrix_exception_error(self):
        mat = mvm_two_by_two()
        with self.assertRaises(WrongConductanceMatrixError):
            mat.update_conductance_matrix([0])


if __name__ == "__main__":
    unittest.main()
