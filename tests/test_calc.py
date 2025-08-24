from agent.agent import answer

def test_calc_simple_addition():
    result = answer("What is 2 + 3?")
    assert result is not None
    assert isinstance(result, float)
    assert result == 5.0

def test_calc_invalid_input():
    result = answer("What is foo + bar")
    assert result is None

def test_calc_simple_subtraction():
    result = answer("What is 10 - 4?")
    assert result is not None
    assert isinstance(result, float)
    assert result == 6.0

def test_calc_simple_multiplication():
    result = answer("What is 7 * 6?")
    assert result is not None
    assert isinstance(result, float)
    assert result == 42.0

def test_calc_simple_division():
    result = answer("What is 8 / 2?")
    assert result is not None
    assert isinstance(result, float)
    assert result == 4.0

def test_calc_zero_by_int_division():
    result = answer("What is 0 / 1?")
    assert result is not None
    assert isinstance(result, float)
    assert result == 0.0

def test_calc_int_by_zero_division():
    result = answer("What is 8 / 0?")
    assert result is None

def test_calc_int_by_zero_division():
    result = answer("What is 0 / 0?")
    assert result is None

def test_calc_int_by_float_division():
    result = answer("What is 3 / 1.5?")
    assert result is not None
    assert isinstance(result, float)
    assert result == 2.0

def test_calc_word_plus():
    result = answer("What is 3 plus 1.5?")
    assert result is not None
    assert isinstance(result, float)
    assert result == 4.5

def test_calc_percentage():
    result = answer("What is 12.5% of 243?")
    assert result is not None
    assert isinstance(result, float)
    assert result == 30.375
