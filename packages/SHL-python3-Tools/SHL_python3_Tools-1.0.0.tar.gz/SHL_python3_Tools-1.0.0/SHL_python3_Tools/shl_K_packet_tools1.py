

#数据包
class creat_data_pack:
    def __init__(self, data):
        self.data = str(data).encode('utf-8') #单位是字节
        self.len = len(data)
        #存字节数量, 使用int.to_bytes方法将数据大小转换为4个字节序列,big为大端
        #这行代码不需要进行UTF-8转换，因为它是将整数转换为字节序列，而不涉及字符串或文本数据。
        self.header = int.to_bytes(self.len, length=4, byteorder='big')

    def add_data(self, add_data):
        self.data += str(add_data).encode('utf-8')#单位是字节
        self.len = len(self.data)
        #存字节数量, 使用int.to_bytes方法将数据大小转换为4个字节序列,big为大端
        #这行代码不需要进行UTF-8转换，因为它是将整数转换为字节序列，而不涉及字符串或文本数据。 
        self.header = int.to_bytes(self.len, length=4, byteorder='big')
        
    #获取完整包内容
    def get_pack(self):
        return self.header + self.data
    
    #读取4个字节头部信息
    def read_header(self):
        header = self.get_pack()[:4]  # 读取前4个字节作为头部信息
        return int.from_bytes(header, byteorder='big')  # 将前4个字节按照大端序解析为整数
    
    def read_content(self):
        content = self.get_pack()[4:].decode('utf-8') 
        return content
            


pk = creat_data_pack('这里是内容')
pk.add_data('内容')
print('头部信息(总内容大小):',pk.read_header(),'字节')
print('内容:',pk.read_content())

