from stockex.celery import app
from .macrotrends import switch_page


@app.task(time_limit=8000, soft_time_limit=7600)
def get_macrotrends_values():
    return switch_page()
