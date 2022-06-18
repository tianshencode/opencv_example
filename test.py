import cv2
import numpy as np

if __name__ == '__main__':
    # 加载图像
    img = cv2.imread('meinv.jpg')
    # 加载分类器，这里使用的是opencv的人脸分类器，参数为haar特征的xml文件，
    face_detector = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')
    # 这是一个多尺度检测，返回的是一个坐标列表
    faces = face_detector.detectMultiScale(img)
    print(faces)
    for (x, y, w, h) in faces:
        # 画出矩形框
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)

    # 显示图像
    cv2.imshow('img', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()