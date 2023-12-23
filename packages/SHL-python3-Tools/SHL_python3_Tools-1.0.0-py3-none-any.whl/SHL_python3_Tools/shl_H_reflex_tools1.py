import importlib.util


"""
###########################类似反射#############################
"""


"""
################################################################

      说明  :  获取动态(import)模块
   所属目录 :  D:\SHL-DeskTop\MyWorkspase\WebProj\SHL_VUE_PROJ\myweb_backend_django\app_01\static\PYTHON_TOOLS_DIR
    文件名  :  shl_H_reflex_tools1.py
      日期  :  2023-10-25 14:10:55
      参数  :  字典形式参数
      应用  :  get_importModule(fileName=xxx,filePath=xxx) , 传入后的形式{'fileName':xxx,'filePath':xxx}
      
1.    /前面的部分为强制参数(位置不能变)
2.    *p  可传入多个参数
3.    **p   传入的参数为字典模式 , 
4.    *    单独一个没有参数名,没有参数名 ,可以传入多个参数 ,但是后面必须跟关键字参数
5.    xxx=10    关键字参数 ,由于传入的参数名称和函数里的名称一样,所以顺序可以变
################################################################
"""

# def  get_importModule(file_path):
def get_spec_module(**argv_dict):
    # 指定模块名称(理解为别名)
    module_name = argv_dict["fileName"]
    # 文件绝对路径
    fpath = argv_dict["filePath"]

    # 使用 importlib.util.spec_from_file_location 方法创建一个 module spec 对象
    spec = importlib.util.spec_from_file_location(module_name, fpath)

    # 使用 importlib.util.module_from_spec 方法创建一个新的模块对象
    module = importlib.util.module_from_spec(spec)

    # 使用 spec.loader.exec_module 方法执行模块代码
    # 现在，xxx.py 文件中的内容被导入到 module 对象中了
    spec.loader.exec_module(module)

    # 使用动态导入的模块
    # module.function_name  # 调用模块中的函数

    return  module
  


