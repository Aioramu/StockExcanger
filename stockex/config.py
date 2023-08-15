from decouple import config
charset = 'utf8mb4'

rabbit_user = config('rabbit_user')#креды рэббита,запущенного тут
rabbit_pass = config('rabbit_pass')
rabbit_host = config('rabbit_host')
