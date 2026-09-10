YOLO-LiDAR Fusion

RGBカメラとLiDAR（Velodyne VLP-16）を組み合わせた物体検出・距離情報取得システムの開発・検証。

YOLOによる物体検出結果とVLP-16の3次元点群情報を連携し、検出対象に対するLiDARベースの距離情報を取得する。

使用機器
LiDAR：Velodyne VLP-16
RGB Camera：320 × 240
PC
開発環境
Ubuntu 22.04
ROS 2 Humble
RViz2
Python
OpenCV
YOLO（Ultralytics）
System Overview
RGB Camera
    ↓
YOLO Object Detection
    ↓
Bounding Box
    ↓
LiDAR Point Cloud（VLP-16）
    ↓
Sensor Fusion
    ↓
Distance Information

<img width="1978" height="788" alt="image" src="https://github.com/user-attachments/assets/3c2e14f4-6550-4561-8377-5b8717575543" />

現在の実装
 VLP-16による3D Point Cloud取得
 RViz2によるPoint Cloud可視化
 RGB Camera画像取得
 YOLOによる複数物体検出
 YOLOとLiDAR Point Cloudの連携
 LiDARを用いた距離情報の取得
 検出物体に対する距離情報の表示
今後の課題
複数物体それぞれの距離情報の取得・表示
Camera-LiDAR Calibrationの改善
3次元位置座標（X, Y, Z）の物体別取得
低視認環境における検出性能の評価

特に「3D位置座標（X,Y,Z）取得」を現在の実装完了として書くのは一旦やめた方がいい。
画像を見る限り、現状でGitHubに堂々と成果として書けるのは 「YOLO複数物体検出 ＋ VLP-16 Point Cloud連携 ＋ LiDAR距離情報取得・表示」。


