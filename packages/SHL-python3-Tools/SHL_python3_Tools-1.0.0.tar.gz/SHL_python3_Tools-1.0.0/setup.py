from distutils.core import  setup


packages = ['SHL_python3_Tools']# 唯一的包名，自己取名
setup(name='SHL_python3_Tools',
	version='1.0.0',
	author='SHL',
    packages=packages, 
    package_dir={'requests': 'requests'},)



