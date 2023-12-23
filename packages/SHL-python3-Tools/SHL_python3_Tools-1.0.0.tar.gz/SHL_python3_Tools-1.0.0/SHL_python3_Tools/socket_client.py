import asyncio


#构造数据包
def constructing_data_packets():
    data_packet = "头部信息".encode('utf-8') + "正文内容".encode('utf-8')
    packet_size = len(data_packet) #计算数据包的大小
    print(packet_size)
    # # 发送数据包
    # writer.write(data_packet)
    # await writer.drain()


'''
使用 await 挂起当前的协程，让其它协程继续执行，从而提高程序的并发性能。一旦被等待的操作完成，
被挂起的协程便会恢复执行。简单来说，await 可以让程序在等待某个事件完成时不阻塞，提高了程序的效率和性能。
'''
#给服务端发送消息
async def send_to_mess(writer):
    send_message = '11111111111111111111111111111111111'
    print(f'发送给服务端: {send_message!r}')
    writer.write(send_message.encode('utf-8'))
    await writer.drain()#确保数据完整发送


#发送文件(全部存放到内存)
async def send_to_file_all(writer):
    with open('E:/KuGou/我喜欢/111.txt', 'rb') as file:
        save_to_memory = file.read()  # 读取文件内容保存到内存中
        
    writer.write(save_to_memory)
    await writer.drain()  # 确保数据完整发送
    

#发送文件(每次存放上限为1024*1000字节)   
async def send_to_file(writer):
    with open('E:\迅雷下载\万剑归宗.mp4', 'rb') as file:
        while True:
            save_to_memory = file.read(1024*1000)  # 每次最多读取1024*1000字节的数据(应该是用游标来控制读取到哪里)
            if not save_to_memory:  # 如果读取完毕则跳出循环
                print('文件读取完成')
                break
            
            file.flush()
            writer.write(save_to_memory)#每次发送数据上限为1024*1000字节
            await writer.drain()  # 确保数据完整发送
            



#从服务端接收消息
async def accept_to_mess(reader,writer):
    try:
        # 接收数据部分
        while True:
            data = await reader.read(1024*1000)  # 循环接收数据
            if not data:
                break
            accept = data.decode('utf-8')
            print(f'从服务端接收: {accept!r}')
            
        
    except Exception as e:
        print(f"发生错误：{e}")
 
 
 

'''在这个示例中在发送完数据后使用了await writer.drain()来确保数据完整发送
。然后使用一个无限循环来持续接收来自服务端的响应，直到服务端关闭连接或其他条件满足后再断开连接。'''
async def main_fun():
    reader, writer = await asyncio.open_connection('127.0.0.1', 8888)

    #发送数据部分
    await send_to_mess(writer)
    # await send_to_file(writer) #发送文件
    
    #接受消息部分
    await accept_to_mess(reader,writer)


    print('关闭连接')
    writer.close()
    await writer.wait_closed()


asyncio.run(main_fun())
