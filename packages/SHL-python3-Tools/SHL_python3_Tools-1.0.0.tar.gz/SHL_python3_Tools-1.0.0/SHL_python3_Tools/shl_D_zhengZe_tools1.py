import re




'''
################################################################

      说明  :  正则
   所属目录 :  D:\SHL-DeskTop\MyWorkspase\WebProj\myweb_backend_django\app_01\static\PYTHON_TOOLS_DIR
      文件名  :  shl_D_zhengZe_tools1.py
        日期  :  2023-10-26 11:01:34
      参数  :  
      应用  :  

################################################################
'''


   
'''
################################################################

      说明  : 完全匹配, 如果匹配返回对象,否则返回空
   所属目录 :  D:\SHL-DeskTop\MyWorkspase\WebProj\myweb_backend_django\app_01\static\PYTHON_TOOLS_DIR
      文件名  :  shl_D_zhengZe_tools1.py
        日期  :  2023-10-26 14:58:01
      参数  :  字符串

################################################################
'''

#完全匹配
def matching_regular(text , match_str = r".*shl_\w+_\w+_tools\d+.py"):
    # 定义待匹配的字符串
    # text = "shl_example_string_tools123"

    # 使用 re 模块进行匹配
    match = re.match(match_str, text)
    # match = re.match(match_str, text)

    # 判断是否匹配成功
    # if match:
    #    print("字符串匹配成功！")
    #    return True
    # else:
    #    print("字符串不符合规则！")
    #    return False
   
    return match #不匹配应该返回空
   
   
   
   
'''
################################################################

      说明  : 包含(模糊)匹配, 如果匹配返回对象,否则返回空
   所属目录 :  D:\SHL-DeskTop\MyWorkspase\WebProj\myweb_backend_django\app_01\static\PYTHON_TOOLS_DIR
      文件名  :  shl_D_zhengZe_tools1.py
        日期  :  2023-10-26 14:58:01
      参数  :  字符串

################################################################
'''
#包含(模糊)匹配
# match_str = r"shl_\w+_\w+_tools\d+.py"
#匹配包含
def search_regular(text, match_str=r"shl_\w+_\w+_tools\d+.py" ):
    # 定义待匹配的字符串
    # text = "shl_example_string_tools123"

    # 使用 re 模块进行匹配
    match = re.search(match_str, text)
    # match = re.match(match_toolsRegular, text)
    
    return match  #不匹配应该返回空



'''
################################################################

      说明  :  返回匹配后的字符串,否则返回空
   所属目录 :  D:\SHL-DeskTop\MyWorkspase\WebProj\myweb_backend_django\app_01\static\PYTHON_TOOLS_DIR
      文件名  :  shl_D_zhengZe_tools1.py
        日期  :  2023-10-26 14:57:43
      参数  :  默认参数为工具开始查找

################################################################
'''
def get_search_regular_text(text , arr_match=[r"shl_\w+_\w+_tools\d+.py"]):
   match = None
   for item in arr_match:
      match = re.search(item,text)
      if match:
        return match.group() #返回内容

   return
          
    


   
