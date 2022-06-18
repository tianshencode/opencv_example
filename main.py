import cv2
import numpy as np

if __name__ == '__main__':
    # 窗口大小
    win_size = (640, 480)
    # 创建摄像头窗口，窗口大小为640x480
    cv2.namedWindow('camera')
    # cv2.resizeWindow('camera', win_size[0], win_size[1])
    # 创建摄像头对象
    cap = cv2.VideoCapture('http://192.168.0.107:81/stream')
    # 创建人脸分类器
    face_detector = cv2.CascadeClassifier('./data/haarcascade_frontalface_alt.xml')
    # 头像训练集
    # face_recognizer = cv2.face.LBPHFaceRecognizer_create()
    # face_recognizer.read('trainer/trainer.yml')

    # 显示摄像头视频
    while True:
        # 读取摄像头
        ret, frame = cap.read()
        # 图片灰度化，提高识别速度
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # 人脸检测，1.3和5分别为图片缩放比例和需要检测的有效点数，返回的是人脸坐标列表
        faces = face_detector.detectMultiScale(gray, 1.3, 5)
        # 循环遍历人脸坐标列表
        for (x, y, w, h) in faces:
            # 画出矩形框
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        # 判断人脸移动方向
        if len(faces) > 0:
            # 获取当前摄像头中人脸的坐标
            x, y, w, h = faces[0]
            # 判断人脸是否移动到了摄像头右侧
            if x > frame.shape[1] / 2 - w / 2:
                # 计算人脸移动的幅度百分比
                move_percent = (x - frame.shape[1] / 2 + w / 2) / (frame.shape[1] / 2) * 100
                print('move left: %.2f%%' % move_percent)
            else:
                # 如果移动到了摄像头左侧，则摄像头向右移动
                move_percent = (frame.shape[1] / 2 - x - w / 2) / (frame.shape[1] / 2) * 100
                print('move right: %.2f%%' % move_percent)
        # 显示图片
        cv2.imshow('camera', frame)
        # 按键盘q退出
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    # 释放摄像头
    cap.release()
    # 删除窗口
    cv2.destroyAllWindows()

