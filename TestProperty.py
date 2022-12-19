'''
CS5001
Final project
Fall 2022
Chen Zhou

Test Property Class
'''


import unittest

from Property import Property

class testProperty(unittest.TestCase):

    def test_init_basic(self):
        property1 = Property("123-456-789", 1000000, "5252 CYPRESS ST VANCOUVER")
        self.assertEqual(property1.pid, "123-456-789")
        self.assertEqual(property1.value, 1000000)
        self.assertEqual(property1.address, "5252 CYPRESS ST VANCOUVER")

    def test_init_TypeError1(self):       
        with self.assertRaises(TypeError):
            Property("ABC-456-789", 1000000, "5252 CYPRESS ST VANCOUVER")

    def test_init_TypeError2(self):       
        with self.assertRaises(TypeError):
            Property("123-456-789", '1000000', "5252 CYPRESS ST VANCOUVER")

    def test_init_TypeError3(self):       
        with self.assertRaises(TypeError):
            Property("123-456-789", 1000000, 5252)

    def test_init_ValueError(self):       
        with self.assertRaises(ValueError):
            Property("123-456-789", -1000000, "5252 CYPRESS ST VANCOUVER")

    def test_str_basic(self):
        property_str_1 = Property("123-456-789", 1000000, "5252 CYPRESS ST VANCOUVER")
        self.assertEqual(property_str_1.__str__(), "The property 123-456-789 locating at 5252 CYPRESS ST VANCOUVER had an assessed value of 1000000.")

    def test_eq_basic(self):
        property_eq_1 = Property("123-456-789", 1000000, "5252 CYPRESS ST VANCOUVER")
        self.assertTrue(property_eq_1.__eq__(Property("013-947-435", 1000000, "4559 8TH AVE W VANCOUVER")))        

    def test_eq_TypeError(self):       
        with self.assertRaises(TypeError):
            property_eq_2 = Property("123-456-789", 1000000, "5252 CYPRESS ST VANCOUVER")
            self.assertTrue(property_eq_2.__eq__(1000000))

    def test_gt_basic(self):
        property_gt_1 = Property("123-456-789", 1000000, "5252 CYPRESS ST VANCOUVER")
        self.assertTrue(property_gt_1.__gt__(Property("013-947-435", 800000, "4559 8TH AVE W VANCOUVER")))        

    def test_gt_TypeError(self):       
        with self.assertRaises(TypeError):
            property_gt_2 = Property("123-456-789", 1000000, "5252 CYPRESS ST VANCOUVER")
            self.assertTrue(property_gt_2.__gt__(1000000))

def main():

     unittest.main(verbosity = 3)


if __name__ == "__main__":
    main()
