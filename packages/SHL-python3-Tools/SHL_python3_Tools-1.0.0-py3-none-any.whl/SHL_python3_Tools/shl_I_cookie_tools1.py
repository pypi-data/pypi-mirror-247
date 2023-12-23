import importlib.util
from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse


"""
###########################cookie设置#############################
"""



'''
################################################################
      说明  :  设置cookie , 同时设置超时
   所属目录 :  D:\SHL-DeskTop\MyWorkspase\WebProj\SHL_VUE_PROJ\myweb_backend_django\app_01\static\PYTHON_TOOLS_DIR
    文件名  :  shl_H_reflex_tools1.py
      日期  :  2023-10-25 14:10:55
      参数  :  反馈对象(response)  , cookie键 ,cookie值 , 超时时间(秒)
      应用  :  
              response = mng.shl_module("cookie").set_cookie(response=response,cook_key= "shl_cook_key", cook_val= token, cook_timeout= 1)
              或者
              response = mng.shl_module("cookie").set_cookie(**{'response':response,'cook_key':"shl_cook_key", 'cook_val':token, 'cook_timeout':1})
      
      超时设置:max_age参数设置为60秒，表示这个cookie将在60秒后过期。当客户端收到这个响应后，浏览器会将cookie存储起来，然后在60秒后自动删除该cookie。
      注意，使用max_age参数设置超时时间会覆盖使用expires参数设置的过期日期。如果你想根据具体的日期时间设置超时时间，可以使用expires参数，并将时间按照RFC 1123日期字符串的格式传递给它。

################################################################
'''

def set_cookie(**pm):
        
        response = pm["response"]
        key = pm["cook_key"]
        val = pm["cook_val"]
        tmout = pm['cook_timeout'] 
        
        #cookie超时时间(秒) , 默认设置为60秒
        cookie_timeout =   tmout if tmout else 20
        
        ########################## 浏览器会自动清空超时的cookie###############################
        # response.set_cookie(key, val.encode('utf-8'),max_age=cookie_timeout)#有特殊符号时用
        response.set_cookie(key, val,max_age=cookie_timeout)#设置cookie,超时60秒
        
        return response 
  
  
  
'''
  ################################################################
  
        说明  :  读取前端发过来的cookie
     所属目录 :  D:\SHL-DeskTop\MyWorkspase\WebProj\myweb_backend_django\app_01\static\PYTHON_TOOLS_DIR
        文件名  :  shl_I_cookie_tools1.py
          日期  :  2023-10-27 11:55:32
        参数  :  字典形式参数
        应用  : 
             convert_token = mng.shl_module("cookie").read_cookie(req_res=req_res,cook_key="shl_cook_key")
               或者
             convert_token = mng.shl_module("cookie").read_cookie(**{'req_res':req_res,'cook_key':"shl_cook_key"})
              

  ################################################################
'''
def read_cookie(**pm ):
      req_res = pm["req_res"]
      key_name = pm["cook_key"]
      #读取内容
      cookie_value = req_res.COOKIES.get(key_name)
      return cookie_value 
