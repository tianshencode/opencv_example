import socket
import time
import struct


def set_servo_angle(bottom_angle, top_angle):
    """
    设置舵机角度到给定的值

    :param bottom_angle: 底部舵机角度
    :param top_angle: 顶部舵机角度
    """
    print(f"'底部舵机角度':{bottom_angle}, '顶部舵机角度':{top_angle}")
    # 判断参数bottom_angle是否空白，包括换行符回车符


    # 作为TCP服务端
    # try:
    #     s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 建立TCP连接
    #
    #     port = 5000  # 端口号
    #     ip = '192.168.0.105'  # IP地址，这个是我的电脑的IP地址，可以自己改
    #     s.bind((ip, port))  # 绑定端口号
    #     s.listen(1)  # 监听连接，最大连接数为1
    #     s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    #
    #     print('waiting for connection...')
    #
    #     # while True:
    #     conn, addr = s.accept()  # 接受连接，返回连接对象和远程地址
    #     print('connected from:', addr)
    #
    #     byte_raw = f'<{bottom_angle}><{top_angle}>'
    #     # byte_raw = b''.join(map(lambda x: bytes([x]), byte_raw))
    #     byte_raw = bytes(byte_raw, encoding='utf-8')
    #     print(f"byte_raw: {byte_raw}")
    #     # time.sleep(2)
    #     lenss = conn.send(byte_raw)  # 发送数据，注意要使用bytes格式，不能使用str格式，否则会报错。
    #     print(f"发送字节流长度: {lenss}")
    #     # conn.send('\r\n')  # 发送\r\n，表示结束
    # except:
    #     if s:  # 如果s已经创建，则关闭
    #         s.close()

    # 作为TCP客户端
    HOST = '192.168.0.101'  # 服务器的主机名或IP地址
    PORT = 5000  # 连接的端口
    BUFFER_SIZE = 1024  # 缓冲区大小的作用是为了接收的数据不会太大，如果数据太大，会导致内存不足
    ADDR = (HOST, PORT)  # 地址

    tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 创建一个socket对象，AF_INET表示IPv4，SOCK_STREAM表示TCP
    tcp_client.connect(ADDR)  # 连接服务器
    byte_raw = f'<{bottom_angle}><{top_angle}>'
    byte_raw = bytes(byte_raw, encoding='utf-8')
    tcp_client.send(byte_raw)  # 发送数据
    tcp_client.close()  # 关闭连接

def pack_bin_data(bottom_angle, top_angle):
    """
    h: unsigned short bit=2
    b: unsigned char (byte): bit =1
    """

    bin_data = struct.pack(">iiB",
                           int(bottom_angle),  # 顶部舵机的角度
                           int(top_angle),  # 底部舵机的角度
                           0x0A)  # 结束符 '\n = 0x0A

    return bin_data

if __name__ == '__main__':
    set_servo_angle(180, 90)
    i = 0
    # while True:
    #     i += 1
    #     data = i * 10
    #     print(data)
    #     # 测试角度
    #     set_servo_angle(data, 20)
    #     # 每隔1s发送一次数据
    #     time.sleep(1)
    #     # 三元运算符，如果data大于0，则取data，否则取0
    #     data = data if data > 0 else 0

