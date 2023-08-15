# StockExcanger
backend for stock monitoring


### environment variables need to add into stockex/.env  all variables discribed in stockex/config.py

#### start macrotrends task
```
$ docker exec -it stock bash
#./manage.py shell
from stockouter.tasks import *
get_macrotrends_values()
#get_macrotrends_values.delay()
```
