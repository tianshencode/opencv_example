import cv2
import sys


def get_tracker(tracker_name):
    """获取跟踪器"""

    # 初始化跟踪器
    if tracker_name == 'BOOSTING':
        tracker = cv2.legacy.TrackerBoosting_create()  # 创建一个BOOSTING跟踪器
    elif tracker_name == 'MIL':
        tracker = cv2.TrackerMIL_create()  # 创建MIL跟踪器
    elif tracker_name == 'KCF':
        tracker = cv2.TrackerKCF_create()  # 创建KCF跟踪器
    elif tracker_name == 'TLD':
        tracker = cv2.legacy.TrackerTLD_create()  # 创建TLD跟踪器，抗遮挡效果最佳
    elif tracker_name == 'MEDIANFLOW':
        tracker = cv2.legacy.TrackerMedianFlow_create()  # 创建MEDIANFLOW跟踪器
    elif tracker_name == 'GOTURN':
        tracker = cv2.TrackerGOTURN_create()  # 创建GOTURN跟踪器
    elif tracker_name == 'MOSSE':
        tracker = cv2.legacy.TrackerMOSSE_create()  # 创建MOSSE跟踪器，跟踪速度最快
    elif tracker_name == "CSRT":
        tracker = cv2.TrackerCSRT_create()  # 创建CSRT跟踪器
    else:
        tracker = None

    return tracker


if __name__ == '__main__':


    # 读取视频
    # video = cv2.VideoCapture('xiaoyan.mp4')
    video = cv2.VideoCapture('http://192.168.0.107:81/stream')  # 创建一个摄像头对象

    # 如果视频没有打开
    if not video.isOpened():
        print('Could not open video')
        sys.exit()  # 退出程序

    # 获取视频的第一帧
    ok, frame = video.read()

    if not ok:
        print('Cannot read video file')
        sys.exit()

    # 初始化边框
    # bbox = (287, 23, 86, 320)  # 表示x,y,w,h

    bbox = cv2.selectROI(frame, False)  # 选择一个边框
    print(bbox)

    tracker_name = 'KCF'
    tracker = get_tracker(tracker_name)  # 创建一个跟踪器

    # 初始化跟踪器
    ok = tracker.init(frame, bbox)  # 用第一帧的图像和边框初始化跟踪器，参数

    while True:  # 循环读取视频帧
        # 读取下一帧
        ok, frame = video.read()
        # 设置帧的大小
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
            cv2.putText(frame, 'Tracking failure detected', (100, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)

        # 显示帧速率
        cv2.putText(frame, f'FPS: {str(int(fps))}', (100, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)

        # 在帧上显示跟踪类型
        cv2.putText(frame, tracker_name, (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50, 170, 50), 2)

        # 显示图像
        cv2.imshow('Tracking', frame)

        # 按q键退出
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
