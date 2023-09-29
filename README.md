# StockExcanger
backend for stock monitoring

[![CodeQL](https://github.com/Aioramu/StockExcanger/actions/workflows/codeql.yml/badge.svg?branch=unittests&event=check_run)](https://github.com/Aioramu/StockExcanger/actions/workflows/codeql.yml)
### environment variables need to add into stockex/.env  all variables discribed in stockex/config.py and managment folder

#### start macrotrends task
```
$ docker exec -it stock bash
#./manage.py shell
from stockouter.tasks import *
get_macrotrends_values()
#get_macrotrends_values.delay()
```
