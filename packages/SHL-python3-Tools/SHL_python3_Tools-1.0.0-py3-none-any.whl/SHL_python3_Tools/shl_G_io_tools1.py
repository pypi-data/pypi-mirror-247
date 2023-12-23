import os
import glob
import json

'''
################################################################

      说明  :  io相关模块(路径或提取文件)
   所属目录 :  D:\SHL-DeskTop\MyWorkspase\WebProj\myweb_backend_django\app_01\static\PYTHON_TOOLS_DIR
      文件名  :  shl_G_io_tools1.py
        日期  :  2023-10-26 11:03:22
      参数  :  
      应用  :  

################################################################
'''


#项目根路径(绝对路径)
def get_projRootPath():
    # 获取项目根目录
    projRootPath = os.getcwd()
    return projRootPath

#当前文件所在目录(绝对路径)
def get_currFilePath():
    # 获取当前文件所在的路径(绝对路径)
    currFilePath = os.path.dirname(os.path.abspath(__file__))
    print('当前文件-----------------',currFilePath)
    return currFilePath



#返回当前文件所在目录中所有文件路径(绝对路径)
def get_allFilePath():
    currFilePath = get_currFilePath()
    allFilePath =  glob.glob(os.path.join(currFilePath, '*.py'))
    return allFilePath

'''
#只返回文件名 , 参数为绝对路径
'''
def get_fileName(jueDuiLuJing):
    # 获取文件的路径
    # file_path = r'D:\Mywork_Code\web_proj\web_houDuan\myweb_backend_django\app_01\static\PYTHON_TOOLS_DIR\mngTools.py'
    # 获取文件名
    file_name = os.path.basename(jueDuiLuJing)
    get_fileNameAndExtension(jueDuiLuJing)
    return file_name

    
    
'''
#返回文件名和扩展名 , 参数为绝对路径
'''   
def get_fileNameAndExtension(jueDuiLuJing):
    # 获取文件名和扩展名
    file_name, file_extension = os.path.splitext(jueDuiLuJing)
    # 打印文件名
    return file_name, file_extension





'''
################################################################

      说明  :  默认从当前目录 或者  从指定目录递归查找所有文件(返回的是文件的精确路径
   所属目录 :  D:\Mywork_Code\web_proj\web_houDuan\myweb_backend_django\app_01\static\PYTHON_TOOLS_DIR
     文件名  :  shl_G_io_tools1.py
       日期  :  2023-10-28 19:36:43
      参数  :  
      应用  : 
                get_recursion_filePath()
                或者
                get_recursion_filePath(dir_path = r"""app_01\static\PYTHON_TOOLS_DIR""")
                或者
                get_recursion_filePath(r"""app_01\static\PYTHON_TOOLS_DIR""")

1.    /前面的部分为强制参数(位置不能变)
2.    *p  可传入多个参数
3.    **p   (字典展开)运算符 ,拷贝内容, fun(key1=value1,key2=value2)
4.    *    (数组展开)运算符,拷贝内容,没有参数名 ,可以传入多个参数(类似js的展开...) ,但是后面必须跟关键字参数
5.    xxx=10    默认关键字参数 ,由于传入的参数名称和函数里的名称一样,所以顺序可以变
################################################################
'''

# 默认从当前文件所在目录开始 递归获取所有文件路径(绝对路径)
def get_recursion_filePath(dir_path = os.path.dirname(os.path.abspath(__file__))):
    #内联函数
    def get_file_paths(directory):
        file_paths = []
        for root, dirs, files in os.walk(directory):
            for file in files:
                file_paths.append(os.path.join(root, file))
        return file_paths
    
    arr_filePaths = get_file_paths(dir_path)
    # [print(item) for item in arr_filePaths]
    return arr_filePaths
    


'''
################################################################

      说明  :  获取配置文件内容
   所属目录 :  D:\Mywork_Code\web_proj\web_houDuan\myweb_backend_django\app_01\static\PYTHON_TOOLS_DIR
     文件名  :  shl_G_io_tools1.py
       日期  :  2023-10-28 21:34:30
      参数  :  如果没有参数会执行默认参数
      应用  : 
             conf_dist = get_confFileContent()
             或者
             conf_dist = get_confFileContent(conf_file_path='xxx')

1.    /前面的部分为强制参数(位置不能变)
2.    *p  可传入多个参数
3.    **p   (字典展开)运算符 ,拷贝内容, fun(key1=value1,key2=value2)
4.    *    (数组展开)运算符,拷贝内容,没有参数名 ,可以传入多个参数(类似js的展开...) ,但是后面必须跟关键字参数
5.    xxx=10    默认关键字参数,参数可有可无  ,由于传入的参数名称和函数里的名称一样,所以顺序可以变
################################################################
'''
def get_confFileContent(conf_file_path=r"app_01\static\CONFIG_DIR\configuration_File.ini"):
    # 读取conf.ini文件内容
    with open(conf_file_path, "r") as f:
        conf_str = f.read()
    # 将JSON格式的内容解析为对象
    cfi = json.loads(conf_str)
    
    # print(cfi['read_allfile_path'][0]['toolsPath'])


    return cfi