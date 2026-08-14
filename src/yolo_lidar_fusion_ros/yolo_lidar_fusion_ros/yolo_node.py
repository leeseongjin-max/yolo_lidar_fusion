import sys

sys.path.insert(
    0,
    "/home/seongjin1/ros2_ws/src/yolo_lidar_fusion/venv/lib/python3.10/site-packages"
)

# ROS2 기능 사용
import rclpy

# ROS2 노드 클래스
from rclpy.node import Node

# 문자열 토픽 사용
from std_msgs.msg import String

# OpenCV
import cv2

# YOLO 모델
from ultralytics import YOLO


class YoloNode(Node):

    def __init__(self):

        # 노드 이름
        super().__init__('yolo_node')

        # 검출 결과 발행 토픽
        self.publisher_ = self.create_publisher(
            String,
            '/detections',
            10
        )

        # 카메라 열기
        self.cap = cv2.VideoCapture(0)

        # YOLO 모델 로드
        self.model = YOLO(
            '/home/seongjin1/ros2_ws/src/yolo_lidar_fusion/models/yolov8n.pt'
        )

        # 1초마다 실행
        self.timer = self.create_timer(
            1.0,
            self.timer_callback
        )

        self.get_logger().info('YOLO Detection Node Started')

    def timer_callback(self):

        ret, frame = self.cap.read()

        if not ret:
            self.get_logger().warning('camera read failed')
            return

        results = self.model(frame)

        detected_names = []

        for result in results:

            for box in result.boxes:

                cls_id = int(box.cls[0])

                name = self.model.names[cls_id]

                detected_names.append(name)

        msg = String()

        if detected_names:
            msg.data = ', '.join(detected_names)
        else:
            msg.data = 'none'

        self.publisher_.publish(msg)

        self.get_logger().info(
            f'detected: {msg.data}'
        )


def main(args=None):

    rclpy.init(args=args)

    node = YoloNode()

    rclpy.spin(node)

    node.destroy_node()

    rclpy.shutdown()


if __name__ == '__main__':
    main()
