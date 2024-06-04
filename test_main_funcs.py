from main import get_dates

def test_get_dates():
    # test  previously problematic dates
    assert get_dates('07.06.2024 - 20.06.2024') == [('' if i >= 10 else '0') + str(i) + '.06.2024' for i in range(7,21)]
    assert get_dates('05.06.2024 - 20.06.2024') == [('' if i >= 10 else '0') + str(i) + '.06.2024' for i in range(5,21)]

    # test month transition
    assert get_dates('30.05.2024 - 01.06.2024') == ['30.05.2024', '31.05.2024', '01.06.2024']
    assert get_dates('30.04.2024 - 01.05.2024') == ['30.04.2024', '01.05.2024']

    # test year transition
    assert get_dates('28.12.2024 - 03.01.2025') == ['28.12.2024', '29.12.2024', '30.12.2024', '31.12.2024', '01.01.2025', '02.01.2025', '03.01.2025']

    # TODO: test leap years