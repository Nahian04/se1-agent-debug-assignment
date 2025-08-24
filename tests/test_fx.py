from agent.agent import answer

def test_fx_simple_conversion():
    result = answer("Convert 10 USD to EUR")
    assert result is not None
    assert isinstance(result, float)
    assert result == 9.1

def test_fx_nested_conversion():
    result = answer("Convert the average of 10 and 20 USD into EUR.")
    assert result is not None
    assert isinstance(result, float)
    assert result == 13.65

def test_fx_same_currency_conversion():
    result = answer("Convert the average of 10 USD into USD.")
    assert result is not None
    assert isinstance(result, float)
    assert result == 10.0

def test_fx_invalid_currency():
    result = answer("Convert 10 XYZ to ABC")
    assert result is None

def test_fx_known_to_unknown_currency():
    result = answer("Convert 10 USD to ABC")
    assert result is None

def test_fx_unknown_to_unknown_currency():
    result = answer("Convert 10 XYZ to ABC")
    assert result is None
