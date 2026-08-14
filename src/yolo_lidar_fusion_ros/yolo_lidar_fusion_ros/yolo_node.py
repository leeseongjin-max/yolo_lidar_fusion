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

# 카메라 영상 처리
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

        # 최근 LiDAR 데이터 저장
        self.latest_cloud = None

        # Velodyne PointCloud 구독
        self.lidar_sub = self.create_subscription(
            PointCloud2,
        
