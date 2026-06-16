import unittest
from baitap import calculate_energy_financials


class TestEnergyFinancials(unittest.TestCase):

    def test_case_no_discount(self):
        mock_devices = [
            {'id': 'M01', 'location': 'Shop A', 'old_index': 1000, 'new_index': 5000, 'status': 'Normal'}
        ]
        total_con, discount, final_cost = calculate_energy_financials(mock_devices)

        self.assertEqual(total_con, 4000)
        self.assertEqual(discount, 0)
        self.assertEqual(final_cost, 4000 * 3000)

    def test_case_with_discount(self):
        mock_devices = [
            {'id': 'M01', 'location': 'Shop A', 'old_index': 0, 'new_index': 60000, 'status': 'Normal'}
        ]
        total_con, discount, final_cost = calculate_energy_financials(mock_devices)

        expected_cost_before_discount = 60000 * 3000
        expected_discount = expected_cost_before_discount * 0.03
        expected_final_cost = expected_cost_before_discount - expected_discount

        self.assertEqual(total_con, 60000)
        self.assertEqual(discount, 3)
        self.assertEqual(final_cost, expected_final_cost)


if __name__ == '__main__':
    unittest.main()