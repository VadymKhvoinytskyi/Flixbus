from main import get_cities_from_str, get_dates

#TODO: ran tests by pytest instead
def test_dates_string_interpretation():
    assert get_dates('04.05.2024 - 05.05.2024') == ['04.05.2024', '05.05.2024']
    assert get_dates('04.05.2024 -05.05.2024') == ['04.05.2024', '05.05.2024']
    assert get_dates('04.05.2024- 05.05.2024') == ['04.05.2024', '05.05.2024']
    assert get_dates('04.05.2024-05.05.2024') == ['04.05.2024', '05.05.2024']
    assert get_dates('04.05.2024 - 03.05.2024') == []
    assert get_dates('05.05.2024') == ['05.05.2024']

    print('test_dates_string_interpretation ran successfully')

def test_cities_string_interpretation():
    assert get_cities_from_str() == ["Duesseldorf", "Moenchengladbach", "Cologne", "Aachen"]
    assert get_cities_from_str('') == ["Duesseldorf", "Moenchengladbach", "Cologne", "Aachen"]
    assert get_cities_from_str('Kyiv, Chernihiv, Sumy') == ['Kyiv', 'Chernihiv', 'Sumy']
    assert get_cities_from_str('Kyiv, Chernihiv,Sumy') == ['Kyiv', 'Chernihiv', 'Sumy']
    assert get_cities_from_str('Kyiv,Chernihiv, Sumy') == ['Kyiv', 'Chernihiv', 'Sumy']
    assert get_cities_from_str('Kyiv,Chernihiv,Sumy') == ['Kyiv', 'Chernihiv', 'Sumy']

    print('test_cities_string_interpretation ran successfully')


test_dates_string_interpretation()
test_cities_string_interpretation()