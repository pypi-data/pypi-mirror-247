from django_redis import get_redis_connection
from shl_F_prints_tools1 import *
from shl_manageTools import *



class redis_class:
    redis_conn= None
      # #获取redis连接
    def get_instance():
      if not redis_class.redis_conn:
          # print('没有redis_conn')
          redis_class.redis_conn = get_redis_connection("default")
        
        # print('已经有redis_conn')
      return redis_class.redis_conn


#获取在redis的路径
def redis_key_tokenPath(**argv_dict):
  redisPath = f"API_login:user_account:{argv_dict['user_account']}:token"
  return redisPath


# 写入值
def set_keyVal(**pm):
    redis_conn = redis_class.get_instance()
    if pm['ex']:
      redis_conn.set(pm['key'], pm['val'],ex= int(pm['ex'])) #超时(秒)
      # redis_conn.set('user_account:aaa',{'user_account': 'aaa', 'exp': datetime.datetime(2023, 11, 3, 5, 32, 40)},ex= int(3600)) #超时(秒)
    else:
      redis_conn.set(pm['key'], pm['val'])


#读取值
def get_keyVal(**pm):
    redis_conn = redis_class.get_instance()
    # 获取存储的数据
    tmp_val = redis_conn.get(pm['key'])
    val =  mng.shl_module('coder').byteChar_conver_str(tmp_val)
    return val