from pages._common import render_monthly_page


def render(st_module):
    render_monthly_page(st_module, "data/activity_service/activity_service-all.csv", key_prefix="act")
