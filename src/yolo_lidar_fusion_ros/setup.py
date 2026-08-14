from setuptools import find_packages, setup

package_name = 'yolo_lidar_fusion_ros'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='seongjin1',
    maintainer_email='lee.seongjin@aist.go.jp',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
        'yolo_node = yolo_lidar_fusion_ros.yolo_node:main',
           ],
    },
)
