from inu_api.common import *
from inu_api.base_stream import BaseStream
from inu_api.base_frame import BaseFrame
from InuStreamsPyth import *

from enum import IntEnum


class ImuFrame(BaseFrame):
    """!  Imu frame.

    Role: Represents collection of IMU data that is provided by IMU device.

    """

    # @brief    Represents the type of the sensor which ImuData refer to.
    #
    class EType(IntEnum):
        Accelerometer = ImuF.EImuType.Accelerometer
        Gyroscope = ImuF.EImuType.Gyroscope
        Magnetometer = ImuF.EImuType.Magnetometer
        NumOfImuTypes = ImuF.EImuType.NumOfImuTypes

    # @brief    InuStreamsPyth.ImuFrame.
    #
    imuFrame = None

    def __init__(self, frame: ImuF):
        self.imuFrame = frame
        BaseFrame.__init__(self, frame)
        """! The Imu Frame class initializer.
            @param frame  The ImuFrame  from InuStreamsPyth.
            @return  An instance of the ImuFr initialized with the specified InuStreamsPyth.ImuFrame  object.
        """

    @property
    def sensors_data(self) -> MapImuTypePoint3D:
        # @brief     Represents collection of IMU data that is provided by IMU device.
        #
        # @return collection of IMU data.
        return self.imuFrame.SensorsData

    def get_sensor_data(self, imu_type: EType) -> Point3DFloat:
        # @brief     Represents collection of IMU data that is provided by IMU device.
        #
        # @param imu_type  type of the sensor which CImuData refer to
        # @return 3D float point
        return self.imuFrame.GetSensorData(imu_type)

    @property
    def sub_index_frame(self) -> int:
        # @brief     Index of the same IMU type, i.e. continuous index of all IMU frames of the same type.
        #
        # @return Index of the same IMU type.
        return self.imuFrame.SubIndexFrame

    @property
    def temperature(self) -> float:
        # @brief     Current temperature of IMU in Celsius deg. std::numeric_limits<float>::max() if temperature is
        #   not available
        #
        # @return Current temperature of IMU in Celsius deg
        return self.imuFrame.Temperature


class ImuStream(BaseStream):
    """! Interface for Imu service.

    Role: Controls IMU streaming service and provides general or IMU frames.
          IMU frames are provided only if the connected device supports IMU HW components.
          The caller application should be familiar with provided frames and should know how to interpret them.

    Responsibilities:
          1. Derives BaseStream class
          2. Knows how to acquire one imu image frame (pull)
          3. Knows how to provide a continuous stream of imu frames (push)
    """

    # @brief    InuStreamsPyth.ImuS.
    #
    stream = None

    def __init__(self, stream: ImuS):
        """! The Imu stream class initializer.
            @param stream  The InuStreamsPyth.ImuS.
            @return  An instance of the Imu stream initialized with the specified InuStreamsPyth.ImuS object.
        """
        BaseStream.__init__(self, stream)
        self.stream = stream

    def init(self) -> None:
        # @brief    Service initialization.
        #
        # Hall be invoked once before starting frames acquisition.
        self.stream.Init()

    def callback_func(self, stream: ImuS, frame: ImuF, error: InuError) -> None:
        # @brief    Prototype of callback function which is used by the Register method.
        #
        # This function is invoked any time a frame is ready, or if an error occurs. The parameters of this function
        # are: Caller stream object, received Imu frame and result code.
        if error is None:
            print('Undefined error in Imu stream')
        elif error.code != EErrorCode.OK:
            print('Imu CallBack callback Error = {} {}'.format(error.code, error.description))
        else:
            self.callback(ImuStream(stream), ImuFrame(frame), error)

    def register(self, callback) -> None:
        # @brief    Registration/De registration for receiving stream frames (push)
        #
        # The provided callback function is called when a new frame is ready (non-blocking).
        # It shall be called only after a start() was invoked but before any invocation of a stop() is invoked.
        # @param  callback    The Callback function which is invoked when a new frame is ready.
        #                     Send nullptr to unregister for receiving frames.
        self.callback = callback;
        self.baseStream.Register(self.callback_func)
    register = property(None, register)

    @property
    def frame(self) -> ImuFrame:
        # @brief   Retrieves new frame (pull)
        #
        # This method returns when a new frame is ready (blocking) or if an input timeout has elapsed.
        # It shall be called only after a start() was invoked but before any invocation of a stop() is invoked.
        # @return  The returned stereo frame.
        return ImuFrame(self.stream.GetFrame())

    @property
    def temperature(self) -> float:
        # @brief      Get the IMU sensor temperature
        #
        # @return returns the temperature in Celsius .
        return self.stream.Temperature

    @property
    def imu_params(self) -> MapImuTypePoint3D:
        # @brief  Get IMU params
        #
        # @Detailed description:        IMU params that are currently used
        return self.stream.ImuParams

    @imu_params.setter
    def imu_params(self, value: MapImuTypePoint3D) -> None:
        # @brief    temporal_filter_params setter
        #
        # @Detailed description:    Set new IMU params.
        #
        # @param[in]   value	    new IMU params
        self.ImuParams.imu_params = value
