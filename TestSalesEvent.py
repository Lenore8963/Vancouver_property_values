'''
CS5001
Final project
Fall 2022
Chen Zhou

Test SalesEvent Class
'''


import unittest

from SalesEvent import SalesEvent

class testSalesEvent(unittest.TestCase):

    def test_init_basic(self):
        sales1 = SalesEvent('019-084-358', [['09-02-2016', 330000], ['17-05-2016', 450000]], 450000)
        self.assertEqual(sales1.pid, '019-084-358')
        self.assertEqual(sales1.sales_record, [['09-02-2016', 330000], ['17-05-2016', 450000]])
        self.assertEqual(sales1.value, 450000)

    def test_init_TypeError1(self):       
        with self.assertRaises(TypeError):
            SalesEvent("ABC-456-789", [['09-02-2016', 330000], ['17-05-2016', 450000]], 450000)

    def test_init_TypeError2(self):       
        with self.assertRaises(TypeError):
            SalesEvent("123-456-789", '1000000', 450000)

    def test_init_TypeError3(self):       
        with self.assertRaises(TypeError):
            SalesEvent("123-456-789", [['09-02-2016', 330000], ['17-05-2016', 450000]], "450000")

    def test_init_ValueError(self):       
        with self.assertRaises(ValueError):
            SalesEvent("123-456-789", [['09-02-2016', 330000], ['17-05-2016', 450000]], -450000)

    def test_number_of_sales_basic(self):
        sales_number_of_sales_1 = SalesEvent('019-084-358', [['09-02-2016', 330000], ['17-05-2016', 450000]], 450000)
        self.assertEqual(sales_number_of_sales_1.number_of_sales(), 2)

    def test_str_basic(self):
        sales_str_1 = SalesEvent('019-084-358', [['09-02-2016', 330000], ['17-05-2016', 450000]], 450000)
        self.assertEqual(sales_str_1.__str__(), "The property 019-084-358 had 2 transactions in 2016, its latest price is 450000.")

    def test_eq_basic(self):
        sales_eq_1 = SalesEvent('019-084-358', [['09-02-2016', 330000], ['17-05-2016', 450000]], 450000)
        self.assertTrue(sales_eq_1.__eq__(SalesEvent("013-947-435", ['23-02-2016', 450000], 450000)))        

    def test_eq_TypeError(self):       
        with self.assertRaises(TypeError):
            sales_eq_2 = SalesEvent('019-084-358', [['09-02-2016', 330000], ['17-05-2016', 450000]], 450000)
            self.assertTrue(sales_eq_2.__eq__(450000))

    def test_gt_basic(self):
        sales_gt_1 = SalesEvent('019-084-358', [['09-02-2016', 330000], ['17-05-2016', 450000]], 450000)
        self.assertTrue(sales_gt_1.__gt__(SalesEvent("013-947-435", ['23-02-2016', 300000], 300000)))        

    def test_gt_TypeError(self):       
        with self.assertRaises(TypeError):
            sales_gt_2 = SalesEvent("013-947-435", ['23-02-2016', 300000], 300000)
            self.assertTrue(sales_gt_2.__gt__(200000))

def main():

     unittest.main(verbosity = 3)


if __name__ == "__main__":
    main()
