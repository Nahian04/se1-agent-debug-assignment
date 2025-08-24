from agent.agent import answer

def test_kb_existing_query():
    result = answer("Who is Ada Lovelace?")
    assert result is not None
    assert isinstance(result, str)
    assert result == "Ada Lovelace was a 19th-century mathematician regarded as an early computing pioneer for her work on Charles Babbage's Analytical Engine."

def test_kb_existing_query_case_insensitive():
    result = answer("Who is aDa LOVElace?")
    assert result is not None
    assert isinstance(result, str)
    assert result == "Ada Lovelace was a 19th-century mathematician regarded as an early computing pioneer for her work on Charles Babbage's Analytical Engine."

def test_kb_existing_query_typo():
    result = answer("Who is aDa LOVlace?")
    assert result is not None
    assert isinstance(result, str)
    assert result == "No entry found."

def test_kb_existing_query_partial_name():
    result = answer("Who is lace?")
    assert result is not None
    assert isinstance(result, str)
    assert result == "No entry found."

def test_kb_unknown_query():
    result = answer("Who is Foo Bar?")
    assert result is not None
    assert isinstance(result, str)
    assert result == "No entry found."
