import sys

# venv 내 ultralytics 사용
sys.path.insert(
    0,
    "/home/seongjin1/ros2_ws/src/yolo_lidar_fusion/venv/lib/python3.10/site-packages"
)

# ROS2
import rclpy
from rclpy.node import Node

# 검출 결과 Publish용
from std_msgs.msg import String

# LiDAR PointCloud 수신용
from sensor_msgs.msg import PointCloud2
from sensor_msgs_py import point_cloud2

# 수학 계산
import math

# 카메라 처리
import cv2

# YOLOv8
from ultralytics import YOLO


class YoloNode(Node):

    def __init__(self):

        # ROS2 노드 생성
        super().__init__('yolo_node')

        # 객체 검출 결과 Publish
        self.publisher_ = self.create_publisher(
            String,
            '/detections',
            10
        )

        # 최신 PointCloud 저장
        self.latest_cloud = None

        # 최근 거리 저장
        self.latest_distance = -1.0

        # Velodyne PointCloud 구독
        self.lidar_sub = self.create_subscription(
            PointCloud2,
            '/velodyne_points',
            self.lidar_callback,
            10
        )

        # FLIR 카메라 연결
        self.cap = cv2.VideoCapture(
            0,
            cv2.CAP_V4L2
        )

        # 카메라 해상도
        self.cap.set(
            cv2.CAP_PROP_FRAME_WIDTH,
            640
        )

        self.cap.set(
            cv2.CAP_PROP_FRAME_HEIGHT,
            480
        )

        # YOLO 모델
        self.model = YOLO(
            '/home/seongjin1/ros2_ws/src/yolo_lidar_fusion/models/yolov8n.pt'
        )

        # 5Hz
        self.timer = self.create_timer(
            0.2,
            self.timer_callback
        )

        self.get_logger().info(
            'YOLO Detection Node Started'
        )

    # LiDAR 데이터 수신
    def lidar_callback(self, msg):

        self.latest_cloud = msg

        min_distance = 9999.0

        try:

            points = point_cloud2.read_points(
                msg,
                field_names=("x", "y", "z"),
                skip_nans=True
            )

            for point in points:

                x, y, z = point

                distance = math.sqrt(
                    x * x +
                    y * y +
                    z * z
                )

                if 0.3 < distance < min_distance:

                    min_distance = distance

            if min_distance < 9999.0:

                self.latest_distance = min_distance

        except Exception as e:

            self.get_logger().error(
                str(e)
            )

    # YOLO 추론
    def timer_callback(self):

        ret, frame = self.cap.read()

        if not ret:

            self.get_logger().warning(
                'camera read failed'
            )

            return

        results = self.model(frame)

        annotated_frame = results[0].plot()

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

        lidar_status = (
            'LiDAR OK'
            if self.latest_cloud is not None
            else 'LiDAR NOT RECEIVED'
        )

        distance_text = (
            f'{self.latest_distance:.2f} m'
            if self.latest_distance > 0
            else 'N/A'
        )

        cv2.putText(
            annotated_frame,
            lidar_status,
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2
        )

        cv2.putText(
            annotated_frame,
            f'Distance: {distance_text}',
            (20, 80),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 255),
            2
        )

        cv2.imshow(
            'YOLO LiDAR Fusion',
            annotated_frame
        )

        cv2.waitKey(1)

        self.get_logger().info(
            f'detected: {msg.data} | {lidar_status}'
        )


def main(args=None):

    rclpy.init(args=args)

    node = YoloNode()

    rclpy.spin(node)

    cv2.destroyAllWindows()

    node.destroy_node()

    rclpy.shutdown()


if __name__ == '__main__':
    main()
