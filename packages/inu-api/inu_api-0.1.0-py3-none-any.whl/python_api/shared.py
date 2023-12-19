from enum import IntEnum


class EStreamType(IntEnum):
    Depth = 1
    Stereo = 2
    GeneralCamera = 4
    Imu = 8
    FeaturesTracking = 16
    Histogram = 32
    Slam = 64
    Tracking = 128
    UserDefine = 256
    CnnApp = 512
    PointCloud = 1024
    Injection = 2048
    Cnn = 4096
