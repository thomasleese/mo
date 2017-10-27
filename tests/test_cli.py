from mo import cli


def test_parse_variables():
    variables = cli.parse_variables(['a=var', 'b=var', 'c=var=blah'])

    assert variables['a'] == 'var'
    assert variables['b'] == 'var'
    assert variables['c'] == 'var=blah'
