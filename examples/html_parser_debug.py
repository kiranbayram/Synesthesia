from html_parser import remove_html_markup

def test_output(output):
    return output.find('<') == -1

html_fail = '"<b>foo</b>"'
html_pass = "'<b>foo</b>'"

inputs = [[html_fail], [html_pass]]