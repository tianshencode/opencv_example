## 人脸追踪小风扇
项目采用：<br>
树莓派pico + esp32cam + ESP-01S + opencv<br>
将采集到的视频（esp32cam加入WiFi），通过WiFi传输到PC，交给OpenCV进行人脸识别，获取风扇转动方向<br>
将PC作为TCP客户端与作为TCP服务端的树莓派pico（通过ESP-01S加入WiFi）通信，然后将方向命令发送到pico<br>
pico驱动风扇转向
<br>
### 注意：
树莓派pico作为TCP服务端的好处是可以随时快速响应，如果将其作为TCP客户端，则pico每次通信完后都要用AT指令重连服务端，<br>
大大增加延迟，不能做的实时响应。当然，如果pico与pc是通过串口通信，就没有前面的延迟问题了

<br>
人脸识别使用dnn神经网络，可以识别侧脸和抗遮挡：<br>
cv2.dnn.readNetFromCaffe("data/deploy.prototxt", "data/res10_300x300_ssd_iter_140000_fp16.caffemodel")<br>
也可以用这个：<br>
cv2.dnn.readNetFromTensorflow("data/opencv_face_detector_uint8.pb", "data/opencv_face_detector.pbtxt")