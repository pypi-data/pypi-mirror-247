import jwt
from shl_manageTools import mng

#秘钥
secret_key = r"密钥/\&*][^%$~}{)(#"
 
'''
################################################################

      说明  :  生成口令
   所属目录 :  D:\SHL-DeskTop\MyWorkspase\WebProj\myweb_backend_django\app_01\static\python_tools_dir
      文件名  :  shl_E_token_tools1.py
        日期  :  2023-10-30 11:16:47
      参数  :  数据 , 超时时间(分钟)
      应用  : 
            token = mng.shl_module("token").generate_token(data_box=data,token_timeout = 5 )
            或者
            token = mng.shl_module("token").generate_token(**{'data_box':data,'token_timeout' : 5 })
            
1.    /前面的部分为强制参数(位置不能变)
2.    *p  可传入多个参数
3.    **p   (字典展开)运算符,拷贝内容 , fun(key1=value1,key2=value2)
4.    *    (数组展开)运算符,拷贝内容,没有参数名 ,可以传入多个参数(类似js的展开...) ,但是后面必须跟关键字参数
5.    xxx=10    关键字参数 ,由于传入的参数名称和函数里的名称一样,所以顺序可以变
################################################################
'''
def generate_token(**token_dict):

    pm = {}
    pm['data_box'] = token_dict['data_box'] #数据
    
    tm = token_dict['token_timeout']
    
    #token超时时间(分钟) , 默认设置为60分钟
    exp_time =   tm if tm else 60 #分钟
    
    #超时时间(分钟)
    pm['data_box']['exp'] = mng.shl_module('date').get_guoQiShiJian(exp_time)  

    # 生成令牌
    token = jwt.encode(pm["data_box"], secret_key, algorithm="HS256")

    # 返回令牌
    return token



"""
#说明:  解析token为对象
   参数   de_token = mng.shl_module("token").analysis_token(convert_token)
"""
def analysis_token(token):
    try:
        # 解析令牌
        analysis_token = jwt.decode(token, secret_key, algorithms=["HS256"])
        # 返回解码后的令牌数据
        # return decoded_token.encode('utf-8')
        return analysis_token

    except jwt.ExpiredSignatureError:
        # 令牌已过期
        return {"message": "令牌已过期"}

    except jwt.InvalidTokenError:
        # 令牌无效
        return {"message": "令牌无效"}
