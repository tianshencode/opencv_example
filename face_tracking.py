import cv2
import sys
from object_tracking import get_tracker

if __name__ == '__main__':
    # 窗口大小
    win_size = (640, 480)
    # 创建摄像头窗口，窗口大小为640x480
    cv2.namedWindow('camera', cv2.WINDOW_NORMAL)
    # cv2.resizeWindow('camera', win_size[0], win_size[1])#
    # 创建摄像头对象
    cap = cv2.VideoCapture('http://192.168.0.107:81/stream')
    # 创建人脸分类器
    face_detector = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')

    # 如果视频没有打开
    if not cap.isOpened():
        print('Could not open video')
        sys.exit()  # 退出程序

    # 获取视频的第一帧
    ok, frame = cap.read()

    if not ok:
        print('Cannot read video file')
        sys.exit()

    tracker_name = 'KCF'
    tracker = get_tracker(tracker_name)  # 创建一个跟踪器

    # 图片灰度化，提高识别速度
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # 人脸检测，1.3和5分别为图片缩放比例和需要检测的有效点数，返回的是人脸坐标列表
    faces = face_detector.detectMultiScale(gray, 1.3, 5)

    # 初始化跟踪器
    ok = tracker.init(frame, faces[0])  # 用第一帧的图像和边框初始化跟踪器，参数

    while True:  # 循环读取视频帧
        # 读取下一帧
        ok, frame = cap.read()

        if not ok:  # 如果没有读取到帧
            print('Cannot read video file')
            break

        timer = cv2.getTickCount()  # 获取时钟周期

        ok, bbox = tracker.update(frame)  # 跟踪器跟踪图像，返回跟踪器的状态和边框

        fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer)  # 计算帧速率，单位为帧/秒

        # 如果跟踪器跟踪到目标
        if ok:
            # 绘制边框
            (x, y, w, h) = [int(v) for v in bbox]
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        else:  # 如果没有跟踪到目标
            # 显示文字，用于提示
            cv2.putText(frame, 'Tracking failure detected', (100, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255),
                        2)

        # 显示帧速率
        cv2.putText(frame, f'FPS: {str(int(fps))}', (100, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)

        # 在帧上显示跟踪类型
        cv2.putText(frame, tracker_name, (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50, 170, 50), 2)

        # 显示图像
        cv2.imshow('Tracking', frame)

        # 按q键退出
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
