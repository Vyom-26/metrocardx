import unittest
from metrocard import calculate_recharge

class TestRecharge(unittest.TestCase):
    def test_basic_topup(self):
        self.assertEqual(calculate_recharge(5.00, 10.00, 0.0), 15.00)

    def test_bonus(self):
        self.assertEqual(calculate_recharge(0.0, 10.00, 0.10), 11.00)

    def test_negative_topup(self):
        with self.assertRaises(ValueError):
            calculate_recharge(5.0, -1.0, 0.0)

if __name__ == '__main__':
    unittest.main()
