from urllib.parse import parse_qs



'''
#解析编码格式
argv_dict['request'] = request
argv_dict['code'] = 'utf-8'
'''
def analysis_coding(argv_dict):
    decoded_params =argv_dict['request'].body.decode(argv_dict['code'])  # 将字节字符串解码为 'utf-8' 字符串
    dict_oob = parse_qs(decoded_params)  # 解析参数
    return dict_oob


## 将字节序列( b'Hello World')转换为字符串str('Hello World')
def byteChar_conver_str(*pm):
     char_bytes = pm[0]
     if type(char_bytes) == bytes:
        # 将字节序列转换为字符串
        # val = my_string_bytes.decode('utf-8')# 将字节序列转换为字符串
        val = char_bytes.decode()# 将字节序列转换为字符串
        return val
     return char_bytes