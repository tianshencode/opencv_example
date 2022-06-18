import cv2
from uart_cloud_platform import set_servo_angle
from dnn import detector_face
import time
import winsound
import multiprocessing

offset_threshold = 0.2  # 偏移量阈值，即人脸偏移量的绝对值超过该阈值，则控制舵机角度，否则不控制

last_btm_servo_angle = 90  # 上一次控制的底盘舵机角度
last_top_servo_angle = 90  # 上一次控制的顶部舵机角度

btm_kp = 2  # 底盘舵机的P值(PID算法中的P，即比例)，即控制舵机角度的系数，越大，控制的越灵敏
top_kp = 5


def face_filter(faces):
    """
    过滤人脸。
    如果检测到多张人脸，则返回最大的人脸。
    如果人脸太小，则抛弃

    :param faces: 人脸坐标列表
    :return: None或者过滤后的人脸坐标列表。如果没有人脸，或者人脸太小，则返回空列表
    """
    if len(faces) == 0:  # 没有检测到人脸
        return None

    # 只保留最大的一个人脸，也就是离摄像头最近的人脸
    max_face = max(faces, key=lambda x: x[2] * x[3])
    (x, y, w, h) = max_face

    if w < 10 or h < 10:  # 如果人脸太小，则抛弃
        return None

    return max_face


def calculate_offset(face, img_size):
    """
    计算人脸偏移量。\n
    偏移量是指人脸相对于图像的偏移量，即人脸相对于图像左上角的偏移量。\n
    偏移量的取值范围：[-1, 1]，其中-1表示左上角，1表示右下角。\n
    偏移量的计算方法是：\n
    x偏移量 = (人脸中心点的x / 图像宽度 - 0.5) * 2\n
    y偏移量 = (人脸中心点的y / 图像高度 - 0.5) * 2

    :param face: 人脸坐标
    :param img_size: 图像大小，格式为(宽, 高)
    :return: 偏移量
    """
    (x, y, w, h) = face

    # 人脸偏移量的归一化计算，即将坐标转换为[-1, 1]的范围。
    # 因为画面的分辨率可能不同，归一化后相当于按比例计算偏移量，
    # 以适应不同的分辨率，也方便后续的舵机角度计算
    x_offset = ((x + w / 2) / img_size[0] - 0.5) * 2  # -0.5是为了中心点是0，*2是为了偏移量是[-1, 1]
    y_offset = ((y + h / 2) / img_size[1] - 0.5) * 2

    return x_offset, y_offset


def btm_servo_control(x_offset):
    """
    根据人脸偏移量的x值来获取底部舵机角度。\n

    :param x_offset: x偏移量
    :return: 舵机角度
    """
    global offset_threshold
    global last_btm_servo_angle
    global btm_kp

    # print(abs(x_offset))
    # print(int(last_btm_servo_angle))
    if abs(x_offset) < offset_threshold:  # 如果偏移量太小，则不控制舵机角度。这是为了避免舵机角度的抖动
        return int(last_btm_servo_angle)
    # print(x_offset)
    # 计算舵机角度的增量。x_offset范围是[-1, 1]
    angle_increment = btm_kp * x_offset

    # print(angle_increment)

    # 计算舵机角度的最新的值
    new_btm_servo_angle = last_btm_servo_angle - angle_increment
    print(new_btm_servo_angle)

    # 添加边界控制，防止舵机角度超出范围，因为舵机角度的范围是[0, 180]
    if new_btm_servo_angle > 180:
        new_btm_servo_angle = 180
    elif new_btm_servo_angle < 0:
        new_btm_servo_angle = 0

    return new_btm_servo_angle


def top_servo_control(y_offset):
    """
    根据人脸偏移量的y值来获取顶部舵机角度。\n

    :param y_offset: y偏移量
    :return: 舵机角度
    """
    global offset_threshold
    global last_top_servo_angle
    global top_kp

    if abs(y_offset) < offset_threshold:  # 如果偏移量太小，则不控制舵机角度。这是为了避免舵机角度的抖动
        return last_top_servo_angle

    # 计算舵机角度的增量。y_offset范围是[-1, 1]
    angle_increment = top_kp * y_offset

    # 计算舵机角度的最新的值
    new_top_servo_angle = last_top_servo_angle + angle_increment

    # 添加边界控制，防止舵机角度超出范围，因为舵机角度的范围是[0, 180]
    if new_top_servo_angle > 180:
        new_top_servo_angle = 180
    elif new_top_servo_angle < 0:
        new_top_servo_angle = 0

    return int(new_top_servo_angle)


def play_music():
    winsound.PlaySound('where_are_you', winsound.SND_ASYNC)
    time.sleep(3)


face_cascade = cv2.CascadeClassifier('../data/haarcascade_frontalface_alt.xml')  # 加载人脸分类器

# 创建窗口，窗口名称为FaceDetect
cv2.namedWindow("FaceDetect", flags=cv2.WINDOW_AUTOSIZE)

# 摄像头IP地址
ip_camera_url = 'http://192.168.0.107:81/stream'
# 创建摄像头对象
cap = cv2.VideoCapture(ip_camera_url)
cap.set(cv2.CAP_PROP_BUFFERSIZE, 2)  # 设置缓存为1，减少摄像头延时


print('IP摄像头是否开启：{}'.format(cap.isOpened()))

while cap.isOpened():
    # 读取下一帧。因为缓存区设置为1，所以读取到的是最新的一帧
    ret, frame = cap.read()
    net = cv2.dnn.readNetFromCaffe("../data/deploy.prototxt", "../data/res10_300x300_ssd_iter_140000_fp16.caffemodel")
    faces = detector_face(net, frame)

    # 将图片转换为灰度图片，提高帧处理速度
    # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # 检测人脸
    # faces = face_cascade.detectMultiScale(gray, 1.1, 5)

    # 过滤人脸，取最大的一个人脸
    face = face_filter(faces)
    if face is not None:  # 如果有人脸
        # 获取人脸坐标
        (x, y, w, h) = face

        # 在图片上画出矩形框
        # cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

        img_height, img_width = frame.shape[:2]  # 获取图片的高和宽

        # 计算偏移量
        x_offset, y_offset = calculate_offset(face, (img_width, img_height))

        # 在图片中心画出十字
        cv2.line(frame, (img_width // 2, 0), (img_width // 2, img_height), (0, 0, 255), 2)
        cv2.line(frame, (0, img_height // 2), (img_width, img_height // 2), (0, 0, 255), 2)

        # 计算顶部和底部舵机要转的角度
        top_servo_angle = top_servo_control(y_offset)
        btm_servo_angle = btm_servo_control(x_offset)

        # 在图片上画出顶部舵机要转的角度
        # cv2.putText(frame, 'top_angle: {:.2f}'.format(top_servo_angle), (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
        # 在图片上画出底部舵机要转的角度
        # cv2.putText(frame, 'btm_angle: {:.2f}'.format(btm_servo_angle), (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)

        # 发送指令给舵机，控制舵机转动
        tmp_btm_servo_angle = int(btm_servo_angle)
        tmp_top_servo_angle = int(top_servo_angle)
        # if tmp_btm_servo_angle >= 120 or tmp_btm_servo_angle <= 50:
        #     p1 = multiprocessing.Process(target=play_music)
        #     p1.start()

        set_servo_angle(tmp_btm_servo_angle, tmp_top_servo_angle)

        # 更新舵机角度，下次循环使用
        last_top_servo_angle = top_servo_angle
        last_btm_servo_angle = btm_servo_angle

    # 显示图片
    cv2.imshow("FaceDetect", frame)
    # 50ms，每帧的延时
    # time.sleep(0.1)
    # 按q键退出
    if cv2.waitKey(1) & 0xFF == ord('q'):
        set_servo_angle(90, 90)
        break
    elif cv2.waitKey(1) & 0xFF == ord('r'):
        print('重置舵机角度')
        set_servo_angle(90, 90)

cap.release()  # 释放摄像头
cv2.destroyAllWindows()  # 删除所有窗口
