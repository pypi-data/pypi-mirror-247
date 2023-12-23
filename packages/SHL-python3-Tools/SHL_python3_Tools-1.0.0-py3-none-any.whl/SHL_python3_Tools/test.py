from django.conf import settings  # 导入Django的设置模块
from redis import Redis, RedisError  # 导入redis库

import redis
r = redis.StrictRedis(host='10.142.0.103', port=6379, db=9)
r.set(':foo', '{bar:a}')
r.get(':foo')
print(r.get(':foo'))





# # 创建Redis连接
# redis_conn = Redis(
#     host='10.142.0.103',
#     port=6397,
#     db=1,
# )

#         # 'BACKEND': 'django_redis.cache.RedisCache',
#         # 'LOCATION': 'redis://10.142.0.103:6379/0',  # Redis服务器的连接地址和端口号
#         # 'OPTIONS': {
#         #     'CLIENT_CLASS': 'django_redis.client.DefaultClient',
#         # }

# # 使用RedisTemplate进行数据存储
# redis_conn.set('my_key', 'my_value')

# # 使用RedisTemplate进行数据检索
# my_data = redis_conn.get('my_key')

# # 打印检索到的数据
# print(my_data)