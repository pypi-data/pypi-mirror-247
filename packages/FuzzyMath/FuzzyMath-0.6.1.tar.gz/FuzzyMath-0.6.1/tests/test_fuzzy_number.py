import math
from decimal import Decimal, InvalidOperation

import pytest
from conftest import assert_equal_decimals

from FuzzyMath.class_factories import FuzzyNumberFactory, IntervalFactory
from FuzzyMath.class_fuzzy_number import FuzzyNumber
from FuzzyMath.class_memberships import PossibilisticMembership


def test_creation_errors():
    with pytest.raises(TypeError, match="must be a list"):
        FuzzyNumber(1, [])

    with pytest.raises(TypeError, match="must be a list"):
        FuzzyNumber([], 1)

    with pytest.raises(ValueError, match="Lists `alphas` and `alpha_cuts` must be of same length."):
        FuzzyNumber([1, 2, 3], [1, 2])

    with pytest.raises(ValueError, match="`alpha` must be from range"):
        FuzzyNumber([0, 0.5, 1, 1.1], [None] * 4)

    with pytest.raises(InvalidOperation, match="Cannot convert alpha value `a`"):
        FuzzyNumber([0, 0.5, 1, "a"], [None] * 4)

    with pytest.raises(ValueError, match="Values in `alphas` are not unique"):
        FuzzyNumber([0, 0.5, 1, 0.5], [None] * 4)

    with pytest.raises(ValueError, match="`alphas` must contain both 0 and 1 alpha value"):
        FuzzyNumber([0, 0.5, 0.9], [None] * 3)

    with pytest.raises(ValueError, match="`alphas` must contain both 0 and 1 alpha value"):
        FuzzyNumber([0.1, 0.5, 1], [None] * 3)

    with pytest.raises(TypeError, match="All elements of `alpha_cuts` must be Interval"):
        FuzzyNumber([0, 1], [IntervalFactory.two_values(0, 1), 5])

    with pytest.raises(ValueError, match="Interval on lower alpha level has to contain the higher level alpha cuts"):
        FuzzyNumber([0, 1], [IntervalFactory.two_values(0, 1), IntervalFactory.two_values(2, 2)])


def test_alphas(fn_a: FuzzyNumber, fn_e: FuzzyNumber):
    assert fn_a.alpha_levels == [Decimal(0), Decimal(1)]
    assert fn_e.alpha_levels == [Decimal(0), Decimal("0.2"), Decimal("0.4"), Decimal("0.6"), Decimal("0.8"), Decimal(1)]


def test_alpha_cuts(fn_a: FuzzyNumber):
    intervals = [IntervalFactory.infimum_supremum(1, 3), IntervalFactory.infimum_supremum(2, 2)]

    assert intervals == fn_a.alpha_cuts


def test_get_alpha_cut(fn_a: FuzzyNumber):
    assert fn_a.get_alpha_cut(0) == IntervalFactory.two_values(1, 3)
    assert fn_a.get_alpha_cut(0.25) == IntervalFactory.two_values(1.25, 2.75)
    assert fn_a.get_alpha_cut(0.5) == IntervalFactory.two_values(1.5, 2.5)
    assert fn_a.get_alpha_cut(0.75) == IntervalFactory.two_values(1.75, 2.25)
    assert fn_a.get_alpha_cut(1) == IntervalFactory.two_values(2, 2)


def test_contain(fn_a: FuzzyNumber):
    assert 2 in fn_a
    assert 1 in fn_a
    assert 1.1 in fn_a
    assert 2.9 in fn_a
    assert 3 in fn_a
    assert IntervalFactory.infimum_supremum(2.9, 3.1) in fn_a
    assert FuzzyNumberFactory.crisp_number(3) in fn_a
    assert (0.999 in fn_a) is False
    assert (3.001 in fn_a) is False

    with pytest.raises(TypeError, match="Cannot test if object of type"):
        "a" in fn_a


def test_get_alpha_cut_values():
    assert FuzzyNumber.get_alpha_cut_values(6) == [
        Decimal("0"),
        Decimal("0.2"),
        Decimal("0.4"),
        Decimal("0.6"),
        Decimal("0.8"),
        Decimal("1"),
    ]
    assert FuzzyNumber.get_alpha_cut_values(2) == [Decimal("0"), Decimal("1")]
    assert FuzzyNumber.get_alpha_cut_values(11) == [
        Decimal("0"),
        Decimal("0.1"),
        Decimal("0.2"),
        Decimal("0.3"),
        Decimal("0.4"),
        Decimal("0.5"),
        Decimal("0.6"),
        Decimal("0.7"),
        Decimal("0.8"),
        Decimal("0.9"),
        Decimal("1"),
    ]

    with pytest.raises(ValueError, match="`number_of_cuts` has to be integer and higher than 1"):
        FuzzyNumber.get_alpha_cut_values("str")

    with pytest.raises(ValueError, match="`number_of_cuts` has to be integer and higher than 1"):
        FuzzyNumber.get_alpha_cut_values(5.0)

    with pytest.raises(ValueError, match="`number_of_cuts` has to be integer and higher than 1"):
        FuzzyNumber.get_alpha_cut_values(1)


def test_add(fn_a: FuzzyNumber, fn_b: FuzzyNumber, fn_c: FuzzyNumber):
    assert fn_a + 1 == FuzzyNumberFactory.triangular(2, 3, 4)

    assert 1 + fn_a == FuzzyNumberFactory.triangular(2, 3, 4)

    assert fn_a + fn_b == FuzzyNumberFactory.triangular(3, 5, 7)

    assert fn_b + fn_a == FuzzyNumberFactory.triangular(3, 5, 7)

    assert fn_a + fn_c == FuzzyNumberFactory.triangular(0, 2, 4)


def test_sub(fn_a: FuzzyNumber, fn_b: FuzzyNumber, fn_c: FuzzyNumber):
    assert fn_a - 1 == FuzzyNumberFactory.triangular(0, 1, 2)

    assert 1 - fn_a == FuzzyNumberFactory.triangular(-2, -1, 0)

    assert fn_a - fn_b == FuzzyNumberFactory.triangular(-3, -1, 1)

    assert fn_b - fn_a == FuzzyNumberFactory.triangular(-1, 1, 3)

    assert fn_a - fn_c == FuzzyNumberFactory.triangular(0, 2, 4)


def test_truediv(fn_a: FuzzyNumber, fn_b: FuzzyNumber, fn_c: FuzzyNumber):
    assert fn_a / 2 == FuzzyNumberFactory.triangular(0.5, 1, 1.5)

    with pytest.raises(ArithmeticError, match="Cannot divide by 0"):
        fn_a / 0

    assert fn_a / fn_b == FuzzyNumberFactory.triangular(
        fn_a.min / fn_b.max, fn_a.kernel.min / fn_b.kernel.min, fn_a.max / fn_b.min
    )

    assert 5 / fn_a == FuzzyNumberFactory.triangular(5 / fn_a.max, 5 / fn_a.kernel.min, 5 / fn_a.min)


def test_pow(fn_a: FuzzyNumber):
    power = 2

    assert pow(fn_a, power) == FuzzyNumberFactory.triangular(1**power, 2**power, 3**power)


def test_function():
    fn = FuzzyNumberFactory.triangular(-math.pi / 2, 0, math.pi / 2, 11)

    with pytest.raises(ValueError, match="`function` must be either"):
        fn.apply_function(5)

    fn_cos = fn.apply_function(math.cos)

    diff = 0.00000001

    assert fn_cos.min == pytest.approx(-0, diff)
    assert fn_cos.max == pytest.approx(1, diff)
    assert fn_cos.kernel_min == pytest.approx(1, diff)

    fn_sin = fn.apply_function(math.sin)

    assert fn_sin.min == pytest.approx(-1, diff)
    assert fn_sin.max == pytest.approx(1, diff)
    assert fn_sin.kernel_min == pytest.approx(0, diff)


def test_comparisons(fn_a: FuzzyNumber, fn_b: FuzzyNumber, fn_c: FuzzyNumber):
    assert (fn_a == fn_b) is False
    assert fn_a == FuzzyNumberFactory.triangular(1, 2, 3)

    assert fn_c < fn_b
    assert (fn_c > fn_b) is False

    assert fn_c < 2
    assert (fn_c < -2) is False
    assert fn_c > -5
    assert (fn_c > 5) is False

    with pytest.raises(TypeError):
        fn_a > "test"


def test_complex_comparisons_1(quantize_precision):
    fn_a = FuzzyNumberFactory.triangular("2", "3", "5")
    fn_b = FuzzyNumberFactory.triangular("1.5", "4", "4.8")

    assert_equal_decimals(fn_a.possibility_exceedance(fn_b), "0.7777777777777777", quantize_precision)

    assert_equal_decimals(fn_a.necessity_exceedance(fn_b), "0.4285714285714289", quantize_precision)

    assert_equal_decimals(fn_a.possibility_strict_exceedance(fn_b), "0.357142857142857", quantize_precision)

    assert_equal_decimals(fn_a.necessity_strict_exceedance(fn_b), "0.0", quantize_precision)

    assert_equal_decimals(fn_a.possibility_undervaluation(fn_b), "1.0", quantize_precision)

    assert_equal_decimals(fn_a.necessity_undervaluation(fn_b), "0.6428571428571429", quantize_precision)

    assert_equal_decimals(fn_a.possibility_strict_undervaluation(fn_b), "0.5714285714285711", quantize_precision)

    assert_equal_decimals(fn_a.necessity_strict_undervaluation(fn_b), "0.22222222222222235", quantize_precision)

    comparison = fn_a.exceedance(fn_b)

    assert isinstance(comparison, PossibilisticMembership)

    assert_equal_decimals(comparison.possibility, "0.7777777777777777", quantize_precision)
    assert_equal_decimals(comparison.necessity, "0.4285714285714289", quantize_precision)

    comparison = fn_a.strict_exceedance(fn_b)

    assert isinstance(comparison, PossibilisticMembership)

    assert_equal_decimals(comparison.possibility, "0.357142857142857", quantize_precision)
    assert_equal_decimals(comparison.necessity, "0.0", quantize_precision)

    comparison = fn_a.undervaluation(fn_b)

    assert isinstance(comparison, PossibilisticMembership)

    assert_equal_decimals(comparison.possibility, "1.0", quantize_precision)
    assert_equal_decimals(comparison.necessity, "0.6428571428571429", quantize_precision)

    comparison = fn_a.strict_undervaluation(fn_b)

    assert isinstance(comparison, PossibilisticMembership)

    assert_equal_decimals(comparison.possibility, "0.5714285714285711", quantize_precision)
    assert_equal_decimals(comparison.necessity, "0.22222222222222235", quantize_precision)


def test_complex_comparisons_2(quantize_precision):
    fn_a = FuzzyNumberFactory.triangular("1.7", "2.7", "2.8")
    fn_b = FuzzyNumberFactory.triangular("0", "1.8", "2.2")

    assert_equal_decimals(fn_a.possibility_exceedance(fn_b), "1.0", quantize_precision)

    assert_equal_decimals(fn_a.necessity_exceedance(fn_b), "0.9642857142857143", quantize_precision)

    assert_equal_decimals(fn_a.possibility_strict_exceedance(fn_b), "1.0", quantize_precision)

    assert_equal_decimals(fn_a.necessity_strict_exceedance(fn_b), "0.642857142857143", quantize_precision)

    assert_equal_decimals(fn_a.possibility_undervaluation(fn_b), "0.35714285714285726", quantize_precision)

    assert_equal_decimals(fn_a.necessity_undervaluation(fn_b), "0.0", quantize_precision)

    assert_equal_decimals(fn_a.possibility_strict_undervaluation(fn_b), "0.03571428571428574", quantize_precision)

    assert_equal_decimals(fn_a.necessity_strict_undervaluation(fn_b), "0.0", quantize_precision)

    comparison = fn_a.exceedance(fn_b)

    assert isinstance(comparison, PossibilisticMembership)
    assert_equal_decimals(comparison.possibility, "1.0", quantize_precision)
    assert_equal_decimals(comparison.necessity, "0.9642857142857143", quantize_precision)

    comparison = fn_a.strict_exceedance(fn_b)

    assert isinstance(comparison, PossibilisticMembership)

    assert_equal_decimals(comparison.possibility, "1.0", quantize_precision)
    assert_equal_decimals(comparison.necessity, "0.642857142857143", quantize_precision)

    comparison = fn_a.undervaluation(fn_b)

    assert isinstance(comparison, PossibilisticMembership)

    assert_equal_decimals(comparison.possibility, "0.35714285714285726", quantize_precision)
    assert_equal_decimals(comparison.necessity, "0.0", quantize_precision)

    comparison = fn_a.strict_undervaluation(fn_b)

    assert isinstance(comparison, PossibilisticMembership)

    assert_equal_decimals(comparison.possibility, "0.03571428571428574", quantize_precision)
    assert_equal_decimals(comparison.necessity, "0.0", quantize_precision)


def test_hash(fn_a: FuzzyNumber):
    assert hash(fn_a)

    assert isinstance(hash(fn_a), int)


def test_repr(fn_a: FuzzyNumber):
    assert isinstance(fn_a.__repr__(), str)


def test_str(fn_a: FuzzyNumber):
    assert isinstance(fn_a.__str__(), str)


def test_membership(fn_a: FuzzyNumber, fn_d: FuzzyNumber, fn_e: FuzzyNumber, quantize_precision):
    assert fn_a.membership(0) == Decimal(0)
    assert fn_a.membership(0.999) == Decimal(0)
    assert fn_a.membership(3.001) == Decimal(0)
    assert fn_a.membership(99) == Decimal(0)

    assert fn_a.membership(2) == Decimal(1)

    assert fn_a.membership(1.5) == Decimal("0.5")
    assert fn_a.membership(2.5) == Decimal("0.5")

    assert fn_a.membership(1.25) == Decimal("0.25")
    assert fn_a.membership(1.75) == Decimal("0.75")

    assert fn_a.membership(2.25) == Decimal("0.75")
    assert fn_a.membership(2.75) == Decimal("0.25")

    assert fn_d.membership(2.5) == Decimal("1")
    assert fn_d.membership(2) == Decimal("1")
    assert fn_d.membership(3) == Decimal("1")
    assert fn_d.membership(1) == Decimal("0")
    assert fn_d.membership(4) == Decimal("0")

    assert_equal_decimals(fn_e.membership(1.5).membership, "0.5", quantize_precision)
    assert_equal_decimals(fn_e.membership(2.5).membership, "0.5", quantize_precision)


def test_wrong_operations(fn_a: FuzzyNumber):
    with pytest.raises(TypeError):
        fn_a + "a"

    with pytest.raises(TypeError):
        fn_a - "a"

    with pytest.raises(TypeError):
        fn_a / "a"

    with pytest.raises(TypeError):
        fn_a * "a"
