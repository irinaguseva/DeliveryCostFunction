import pytest
from delivery import calculate_delivery_cost


class TestDeliveryCost:

    @pytest.mark.parametrize("distance,expected", [
        (1, 400),  # 50 (distance) + 100 (small) = 150 -> min 400
        (2, 400),  # 50 + 100 = 150 -> 400
        (5, 400),  # 100 + 100 = 200 -> 400
        (10, 400),  # 100 + 100 = 200 -> 400
        (15, 400),  # 200 + 100 = 300 -> 400
        (30, 400),  # 200 + 100 = 300 -> 400
        (31, 400),  # 300 + 100 = 400 -> 400
    ])
    def test_base_distance_cases(self, distance, expected):
        assert calculate_delivery_cost(distance) == expected

    def test_large_sized(self):
        assert calculate_delivery_cost(10, small_sized=False) == 400  # 100 + 200 = 300 -> 400
        assert calculate_delivery_cost(31, small_sized=False) == 500  # 300 + 200 = 500

    def test_fragile(self):
        assert calculate_delivery_cost(10, fragile=True) == 500  # 100 + 100 + 300 = 500
        assert calculate_delivery_cost(2, fragile=True) == 450  # 50 + 100 + 300 = 450

    def test_fragile_long_distance(self):
        assert calculate_delivery_cost(31, fragile=True) == "Unable to deliver fragile items at such a long distance"

    @pytest.mark.parametrize("workload,expected", [
        ("normal", 500),  # (100 + 100 + 300)*1.0 = 500
        ("increased", 600),  # (100 + 100 + 300)*1.2 = 600
        ("high", 700),  # (100 + 100 + 300)*1.4 = 700
        ("very_high", 800),  # (100 + 100 + 300)*1.6 = 800
    ])
    def test_workload_coefficients(self, workload, expected):
        assert calculate_delivery_cost(10, fragile=True, workload=workload) == expected

    def test_invalid_workload(self):
        assert calculate_delivery_cost(10, workload="invalid") == "Invalid workload provided"

    def test_negative_distance(self):
        with pytest.raises(ValueError):
            calculate_delivery_cost(-1)

    def test_combined_parameters(self):
        # (200 + 200 + 300)*1.4 = 980
        assert calculate_delivery_cost(15, small_sized=False, fragile=True, workload="high") == 980

    def test_minimal_cost(self):
        assert calculate_delivery_cost(1, small_sized=True, fragile=False) == 400
        assert calculate_delivery_cost(31, small_sized=True, fragile=False) == 400
