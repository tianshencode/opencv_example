import socket as s


HOST = '192.168.0.104'  # 服务器的主机名或IP地址
PORT = 5000        # 连接的端口
BUFFER_SIZE = 1024  # 缓冲区大小的作用是为了接收的数据不会太大，如果数据太大，会导致内存不足
ADDR = (HOST, PORT) # 地址

tcp_client = s.socket(s.AF_INET, s.SOCK_STREAM) # 创建一个socket对象，AF_INET表示IPv4，SOCK_STREAM表示TCP
tcp_client.connect(ADDR) # 连接服务器

# 等待输入，并发送数据
while True:
    data = input('> ')
    if not data:
        break
    tcp_client.send(data.encode('utf-8'))  # 发送数据，注意要使用bytes格式，不能使用str格式，否则会报错
