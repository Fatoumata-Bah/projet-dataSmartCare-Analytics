from pages._common import render_annual_page


def render(st_module):
    render_annual_page(st_module, "data/hr/hr-all.csv", key_prefix="hr")
