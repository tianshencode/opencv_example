import cv2
import numpy as np
# 添加一个边界，防止舵机角度超出范围，因为舵机角度的范围是[0, 180]


def show_detections(image, detections):
    h, w, c = image.shape
    for i in range(0, detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > 0.6:
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")
            text = "{:.2f}%".format(confidence * 100)
            y = startY - 10 if startY - 10 > 10 else startY + 10  # 三元运算符，类似于其他语言的?:
            cv2.rectangle(image, (startX, startY), (endX, endY), (0, 255, 0), 1)
            cv2.putText(image, text, (startX, y), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 255, 0), 2)
            # 画出人脸坐标
            # cv2.putText(image, str(startX) + "," + str(startY) + "," + str(endX) + "," + str(endY), (startX, startY), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 255, 0), 2)

    return image


def get_detections(image, detections):
    """
    获取人脸x,y,w,h

    :param image: 图片
    :param detections: 人脸检测网络
    :return: 人脸x,y,w,h
    """
    h, w, c = image.shape
    faces = []
    for i in range(0, detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > 0.6:
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")
            text = "{:.2f}%".format(confidence * 100)
            y = startY - 10 if startY - 10 > 10 else startY + 10  # 三元运算符，类似于其他语言的?:
            cv2.rectangle(image, (startX, startY), (endX, endY), (0, 255, 0), 2)
            cv2.putText(image, text, (startX, y), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 255, 0), 2)
            # 返回人脸x,y,w,h
            width = endX - startX
            height = endY - startY
            face = [startX, startY, width, height]

            faces.append(face)

    return np.array(faces)


def detect_img(net, image):
    # 其中的固定参数，我们在上面已经解释过了，固定就是如此
    blob = cv2.dnn.blobFromImage(image, 1.0, (300, 300), (104.0, 177.0, 123.0), False, False)  # 图片转化为blob
    net.setInput(blob)
    detections = net.forward()
    return show_detections(image, detections)


def detector_face(net, image):
    """
    人脸检测

    :param net: 人脸检测网络
    :param image: 图片
    :return: 人脸x,y,w,h
    """
    # 其中的固定参数，我们在上面已经解释过了，固定就是如此
    blob = cv2.dnn.blobFromImage(image, 1.0, (300, 300), (104.0, 177.0, 123.0), False, False)  # 图片转化为blob
    net.setInput(blob)
    detections = net.forward()

    return get_detections(image, detections)


def test_file(net, filepath):
    img = cv2.imread(filepath)
    showimg = detect_img(net, img)
    cv2.imshow("img", showimg)
    cv2.waitKey(0)


def test_camera(net):
    cap = cv2.VideoCapture('http://192.168.0.107:81/stream')
    while True:
        ret, img = cap.read()
        if not ret:
            break
        showimg = detect_img(net, img)
        cv2.imshow("img", showimg)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


def get_face(net):
    """
    获取人脸x,y,w,h

    :param net: 人脸检测网络
    :return: 人脸x,y,w,h
    """
    cap = cv2.VideoCapture('http://192.168.0.107:81/stream')
    while True:
        ret, img = cap.read()
        if not ret:
            break

        face = detector_face(net, img)
        print(face)
        cv2.imshow("img", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        # if face:  # 如果检测到人脸
        #     return face, img


if __name__ == "__main__":
    # 构造SSD网络模型。参数说明:prototxt表示定义模型结构的prototxt文件，model表示已经训练好的模型，
    net = cv2.dnn.readNetFromCaffe("data/deploy.prototxt", "data/res10_300x300_ssd_iter_140000_fp16.caffemodel")
    # net =cv2.dnn.readNetFromTensorflow("data/opencv_face_detector_uint8.pb", "data/opencv_face_detector.pbtxt")
    # file_path = 'data/380.png'
    # test_file(net, file_path)
    # test_camera(net)

    get_face(net)

    # face, img = get_face(net)


    # print(face)