



# 输出
def jjj(pm):
    print( str(pm).center(50, "="))
    # print(pm.ljust(50,'*'))
    # print(pm.rjust(50,'*'))
    
def ppp(*oob):
    print(*oob)
    
    
#打印后后面加指定符号
def ppp_end(*argv):
    for item in argv[0]:
        print(item, end=argv[1])
    

def ppt(pm):
    print( ''.center(50, str(pm)))