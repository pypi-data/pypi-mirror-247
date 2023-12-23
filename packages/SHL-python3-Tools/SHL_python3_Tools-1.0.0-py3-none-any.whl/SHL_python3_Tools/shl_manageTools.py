import os
import sys
'''===========================配置临时环境变量============================'''

current_file_directory = os.path.dirname(os.path.realpath(__file__))
if not current_file_directory in sys.path:
    print('当前工具模块目录 :' ,current_file_directory) #查看工作目录
    sys.path.append(current_file_directory) #添加到临时环境变量
    
root_proj_dir = os.getcwd()
if not root_proj_dir in sys.path:
    print('工作目录(项目根目录) :' ,root_proj_dir) #查看工作目录
    sys.path.append(root_proj_dir) #添加到临时环境变量
    
'''======================================================================'''

from shl_F_prints_tools1 import *
from shl_H_reflex_tools1 import get_spec_module
from shl_G_io_tools1 import get_confFileContent,get_allFilePath,get_recursion_filePath
from shl_D_zhengZe_tools1 import get_search_regular_text,search_regular,matching_regular



# from shl_G_io_tools1 import get_confFileContent #配置文件读取

# conf_dist = get_confFileContent()
# print(conf_dist['read_allfile_path'])

'''
管理所有tools工具
应用: mng.get_instance()
'''
class mng:
    
    modules = None #类变量(理解为静态,在python里类也是对象)
    def shl_module(module_name): 
       return mng.get_instance(module_name)
        
    #静态方法 , 单例模式
    def get_instance(module_name):

        if mng.modules:
            # jjj('已经有对象')
            return mng.modules[module_name]
        else:
            # jjj('没有对象')
            
            conf_dist = get_confFileContent()
            # print('-------', conf_dist)
            #获取所有子级文件路径,默认从当前文件开始,可指定路径
            
            new_arr = [ get_recursion_filePath(dir_path =list(item.values())[0]) for item in conf_dist['read_allfile_path'] if list(item.values())[0]]
            
            #并集 (合并显示元素,但是重复的元素只显示一个)
            # arr = list(set(new_arr[0]) | set(new_arr[1])) #转换为list
            arr = set(new_arr[0]) | set(new_arr[1])
            
            # [print(i) for i in arr]

            mthArr = [ item["match_str"]   for item in conf_dist['read_allfile_path']     if item["match_str"] ]
            
            # [print(i) for i in mthArr]
            
            tmp_dict = {get_search_regular_text(val,arr_match=mthArr).split('_')[2]: val    for val in arr      if get_search_regular_text(val,arr_match=mthArr)  }       
            
            # [print(k,v) for k,v in tmp_dict.items()]
            
            #按照文件路径获取所有模块的spec
            mng.modules  =  { k : get_spec_module(fileName=k,filePath=v) for k,v in tmp_dict.items() }
                        
            # [print(i) for i in mng.modules]

            return mng.modules[module_name]
        
            
            
#装饰器 , 查看参数
def view_parameters(func):
    def wrapper(*args, **kwargs):
        request = args[0]
        mng.shl_module('prints').jjj('######接受前端数据######')
        print("参数类型-------", request.content_type)
        print('查看接受的头部信息-------', request.headers)
        mng.shl_module('prints').jjj('')
        print('')
        
        
        result = func(*args, **kwargs)  # 调用原始函数，传递参数
        print('')
        
        mng.shl_module('prints').jjj('######发送后端数据######')
        response = result
        print('查看反馈的头部信息-------', response.headers)
        print("参数类型-------", response['Content-Type'])
        mng.shl_module('prints').jjj('')
        return result  # 返回原始函数的返回值
    return wrapper



#装饰器 ,除了post以外过滤其他请求
def check_post(func):
    def wrapper(*args, **kwargs):
        request = args[0]
        if request.method == "POST":
            print("Before function execution")
            result = func(*args, **kwargs)  # 调用原始函数，传递参数
            print("After function execution")
        return result  # 返回原始函数的返回值
    return wrapper


