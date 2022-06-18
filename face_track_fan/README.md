人脸识别使用dnn神经网络，可以识别侧脸和抗遮挡：<br>
cv2.dnn.readNetFromCaffe("data/deploy.prototxt", "data/res10_300x300_ssd_iter_140000_fp16.caffemodel")<br>
也可以用这个：<br>
cv2.dnn.readNetFromTensorflow("data/opencv_face_detector_uint8.pb", "data/opencv_face_detector.pbtxt")