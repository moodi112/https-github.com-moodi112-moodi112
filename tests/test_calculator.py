"""
Unit tests for calculator module.
"""

import pytest
from src.calculator import add, subtract, multiply, divide, power


class TestCalculator:
    """Test suite for calculator functions."""

    def test_add(self):
        """Test addition."""
        assert add(2, 3) == 5
        assert add(-1, 1) == 0
        assert add(0, 0) == 0

    def test_subtract(self):
        """Test subtraction."""
        assert subtract(5, 3) == 2
        assert subtract(0, 5) == -5
        assert subtract(-1, -1) == 0

    def test_multiply(self):
        """Test multiplication."""
        assert multiply(3, 4) == 12
        assert multiply(-2, 3) == -6
        assert multiply(0, 100) == 0

    def test_divide(self):
        """Test division."""
        assert divide(10, 2) == 5
        assert divide(9, 3) == 3
        assert divide(-8, 2) == -4

    def test_divide_by_zero(self):
        """Test division by zero raises error."""
        with pytest.raises(ValueError, match="Cannot divide by zero"):
            divide(10, 0)

    def test_power(self):
        """Test exponentiation."""
        assert power(2, 3) == 8
        assert power(5, 0) == 1
        assert power(10, 2) == 100


class TestEdgeCases:
    """Test edge cases and special values."""

    def test_large_numbers(self):
        """Test with large numbers."""
        result = add(1000000, 2000000)
        assert result == 3000000

    def test_floating_point(self):
        """Test with floating point numbers."""
        assert abs(add(0.1, 0.2) - 0.3) < 1e-10
        assert abs(divide(1, 3) - 0.3333333333333333) < 1e-10

    def test_negative_numbers(self):
        """Test with negative numbers."""
        assert multiply(-5, -5) == 25
        assert power(-2, 2) == 4
