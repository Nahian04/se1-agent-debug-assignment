from agent.agent import answer

def test_temp_known_city():
    result = answer("Temperature in Dhaka?")
    assert result is not None
    assert isinstance(result, str)
    assert result == '31°C'

def test_temp_known_cities():
    result = answer("What is the temperature in Paris and London?")
    assert result is not None
    assert isinstance(result, dict)
    assert result == {'Paris': '18°C', 'London': '17.0°C'}

def test_temp_known_and_unknown_cities():
    result = answer("Temperature in Paris and Mumbai?")
    assert result is not None
    assert isinstance(result, str)
    assert result == '18°C'

def test_temp_nested_cities_and_number():
    result = answer("Add 10 to the average temperature in Paris and London right now.")
    assert result is not None
    assert isinstance(result, str)
    assert result == '28.0°C'

def test_temp_unknown_city():
    result = answer("Temperature in Atlantis?")
    assert result is not None
    assert isinstance(result, str)
    assert result == "Temperature data unavailable. Default for Dhaka: 31°C"

def test_calc_nested_calc_and_average_temperature():
    result = answer("Add 10 and multiply by 2 and multiply by 4 and then divide by 2 to the average temperature in dhaka and London.")
    assert result is not None
    assert isinstance(result, str)
    assert result == "136.0°C"

