from agent.agent import answer

def test_weather_known_city():
    result = answer("Weather in Paris?")
    assert result is not None
    assert isinstance(result, str)
    assert result == "Mild and cloudy."

def test_weather_known_city_extending_prompt():
    result = answer("Summarize today's weather in Paris in 3 words.")
    assert result is not None
    assert isinstance(result, str)
    assert result == "Mild and cloudy."

def test_temp_multiple_known_cities():
    result = answer("Weather in Paris and London?")
    assert result is not None
    assert isinstance(result, dict)
    assert "Paris" in result and "London" in result
    assert result == {'Paris': 'Mild and cloudy.', 'London': 'Cool and rainy.'}

def test_weather_unknown_city():
    result = answer("Weather in Gotham?")
    assert result is not None
    assert isinstance(result, str)
    assert "default" in result.lower() or "unavailable" in result.lower()
    assert result == "Weather data unavailable. Default for Dhaka: Hot and humid."

def test_temp_known_and_unknown_cities():
    result = answer("Weather in Paris and Mumbai?")
    assert result is not None
    assert isinstance(result, str)
    assert result == "Mild and cloudy."
