from stockex.celery import app
from .macrotrends import initiate_display

@app.task( time_limit=8000, soft_time_limit=7600)
def get_macrotrends_values():
    return initiate_display()
