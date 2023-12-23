import asyncio



#设置超时断开时要触发的函数
async def timeout_handler():
    print('这里时超时断开的函数')


#从客户端接受消息
async def accept_to_mess(addr,reader,writer):
    try:
        while True:
            # 接受客户端消息,循环接受数据, 设置超时断开3秒
            data = await asyncio.wait_for(reader.read(1024*1000), timeout=3.0) 
            # data = await reader.read(1024)  # 从客户端读取数据(不会断开)
            if not data:
                break
            
            message = data.decode('utf-8')
            print(f"从客户端{addr} 接受到消息：{message}")

            # 发送消息给客户端
            response = "22222222222222222222222222222222222"
            writer.write(response.encode())
            await writer.drain() #确保数据完整发送
            #关闭连接
            # writer.close()
            # await writer.wait_closed()
            
            
    except asyncio.TimeoutError:
        print(f"与 {addr} 的连接已超时断开")
    except Exception as e:
        print(f"与 {addr} 的连接发生错误：{e}")
 
 
 
# 从客户端接受文件
async def accept_to_file(addr, reader, writer):
    try:
        while True:
            # 接受客户端消息,循环接受数据, 设置超时断开3秒
            data = await asyncio.wait_for(reader.read(1024*1000), timeout=3.0) 
            # data = await reader.read(1024)  # 从客户端读取数据(不会断开)
            if not data:
                print('文件接受完成')
                #发送信息给客户端
                # writer.write(b'this is server accept_success_file')  # 向客户端发送确认消息
                writer.write("success_to_client".encode('utf-8'))  # 向客户端发送确认消息
                await writer.drain()  # 确保数据完整发送
                break

            # 将接收到的数据以2进制形式追加末尾写入
            # with open('接受文件.txt', 'ab') as file:
            with open('万剑归宗.mp4', 'ab') as file:
                file.write(data)  
                file.flush
                
    except asyncio.TimeoutError:
        print(f"与 {addr} 的连接已超时断开")
        await timeout_handler() #超时断开时触发的函数
    except Exception as e:
        print(f"与 {addr} 的连接发生错误：{e}")




'''
协程是一种轻量级的并发编程方式，它可以在单个线程内实现多个任务之间的切换和调度。协程允许在代码中定义可中断的点，可以暂停执行、
保存当前状态，然后在需要的时候恢复执行。这种能力使得协程在处理并发任务时更加高效。与线程相比，协程的主要区别在于调度和切换的方式。
线程是由操作系统进行调度的，它们在不同的时间片之间切换，而协程则由程序员手动控制调度和切换。由于没有线程切换的开销，
协程可以更加高效地利用计算资源，并且不会面临线程之间的竞争条件和锁问题。另外，协程通常具有更小的内存占用，因为它们不需要独立的堆栈空间。
相比之下，每个线程都需要独立的堆栈空间。

总结来说，协程是一种更加轻量级和高效的并发编程方式，它通过手动控制调度和切换来实现任务之间的并发执行。
'''


'''
在这个示例中使用了asyncio.wait_for函数来设置接收数据的超时时间为10秒
。如果在10秒内没有接收到客户端的消息，将会触发asyncio.TimeoutError异常，然后断开连接
'''
async def handle_client(reader, writer):
    addr = writer.get_extra_info('peername')
    print(f"新客户端连接 {addr}")

    await accept_to_mess(addr,reader,writer)   #挂起协程
    # await accept_to_file(addr,reader,writer)  


    #应该是上面的代码出现问题后继续往下执行关闭连接
    print(f"与 {addr} 的连接已关闭")
    writer.close()
    await writer.wait_closed()



async def main():
    server = await asyncio.start_server(handle_client, '127.0.0.1', 8888)

    addr = server.sockets[0].getsockname()
    print(f'服务端启动，正在监听 {addr}')

    async with server:
        await server.serve_forever()

asyncio.run(main())
