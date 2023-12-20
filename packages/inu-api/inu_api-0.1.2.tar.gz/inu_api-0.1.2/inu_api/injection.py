from inu_api.common import *
from inu_api.shared import EStreamType
from inu_api.InuStreamsPyth import InjectionS, InuSensor

import numpy as np


class InjectionStream:
    """! Interface for Injection Input  service.

    Role: Controls input injection streaming frames service.

    Responsibilities:
          1. Knows how to inject input frame buffer
    """
    # @brief    InuStreamsPyth.InjectionS.
    #
    stream = None

    # @brief    InuStreamsPyth.InuSensor.
    #
    sensor = None

    def __init__(self, stream: InjectionS, sensor: InuSensor):
        """! The Injection stream class initializer.
            @param stream  The InuStreamsPyth.InjectionStream.
            @param sensor  The InuStreamsPyth.InuSensor.
            @return  An instance of the Injection stream initialized with the specified InuStreamsPyth.InjectionStream and InuStreamsPyth.InuSensor objects.
        """
        self.stream = stream
        self.sensor = sensor

    def init(self, bufferSize: int = 0) -> None:
        # @brief    Service initialization.
        #
        # @param  bufferSize    Frame  Data buffer size used in memory pool build.
        # @return InuError    Operation status which indicates on success or failure.
        if bufferSize == 0:
            self.stream.Init()
        else:
            self.stream.Init(bufferSize)

    def terminate(self) -> None:
        # @brief    Service termination.
        #
        # Shall be invoked when the service is no longer in use and after frames acquisition has stopped.
        self.stream.Terminate()

    def start(self) -> None:
        # @brief    Start acquisition of frames.
        #
        # Shall be invoked only after the service is successfully initialized and before any request
        # for new frame (push or pull).
        self.stream.Start()

    def inject_2_stream(self, stream_type: EStreamType, frame_path: str):  # -> ImageFr or StereoFr or :
        #   FeaturesTrackingFr
        # @brief InjectTrackingImage2TrackingStream
        #
        # Inject Tracking Image Frame file to Stereo stream @param streamType - EStreamType currently support
        #   EStreamType.Depth, EStreamType.Stereo, EStreamType.Tracking and EStreamType.FeaturesTracking @param
        #   framePath - Image Frame path @return result frame as ImageFrame or StereoFrame or FeaturesTrackingFrame
        if stream_type == EStreamType.Depth:
            frame = ImageF()
            self.sensor.InjectStereoImage2DepthStream(frame_path, frame)
            return ImageFrame(frame)
        elif stream_type == EStreamType.Stereo:
            frame = StereoF()
            self.sensor.InjectStereoImage2DepthStream(frame_path, frame)
            return StereoFrame(frame)
        elif stream_type == EStreamType.Tracking:
            frame = ImageF()
            self.sensor.InjectTrackingImage2TrackingStream(frame_path, frame)
            return ImageFrame(frame)
        elif stream_type == EStreamType.FeaturesTracking:
            frame = FeaturesTracking()
            self.sensor.InjectTrackingImage2FeaturesTrackingStream(frame_path, frame)
            return FeaturesTrackingFrame(frame)
        return None

    def inject_2_stream(self, stream_type: EStreamType, width: int, height: int, bytes_per_pixel: int, data: np.array):
        #   ->ImageFr or StereoFr or FeaturesTrackingFr
        # @brief Inject frame data to Stram
        #
        # @param streamType - EStreamType currently support EStreamType.Depth, EStreamType.Stereo,
        #   EStreamType.Tracking and EStreamType.FeaturesTracking @param width - frame width @param height - frame
        #   height @param bytesPerPixel - bytes per pixel @param data - poiner to data buffer @return result frame as
        #   ImageFrame or StereoFrame or FeaturesTrackingFrame
        if stream_type == EStreamType.Depth:
            frame = ImageF()
            self.sensor.InjectStereoImage2DepthStream(width, height, bytes_per_pixel, data, frame)
            return ImageFrame(frame)
        elif stream_type == EStreamType.Stereo:
            frame = StereoF()
            self.sensor.InjectStereoImage2StereoStream(width, height, bytes_per_pixel, data, frame)
            return StereoFrame(frame)
        elif stream_type == EStreamType.Tracking:
            frame = ImageF()
            self.sensor.InjectTrackingImage2TrackingStream(width, height, bytes_per_pixel, data, frame)
            return ImageFrame(frame)
        elif stream_type == EStreamType.FeaturesTracking:
            frame = FeaturesTrackingF()
            self.sensor.InjectTrackingImage2FeaturesTrackingStream(width, height, bytes_per_pixel, data, frame)
            return FeaturesTrackingFrame(frame)
        return None
