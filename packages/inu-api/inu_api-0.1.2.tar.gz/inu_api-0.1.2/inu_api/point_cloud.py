from inu_api.base_stream import BaseStream
from inu_api.base_frame import BaseFrame
from inu_api.InuStreamsPyth import *


class PointCloudFrame(BaseFrame):
    """!  PointCloud frame.

    Role: Represents  an PointCloud Frame that is  provided  by InuDev PointCloud stream

    Responsibilities:
          1. Frame attributes: Format, Confidence,  NumOfPoints  and number of bytes per pixel.
          2. Knows how to manage the  buffer.

    """

    def __init__(self, frame: PointCloudF):
        self.pointCloudFrame = frame
        BaseFrame.__init__(self, frame)
        """! The PointCloudFrame Frame class initializer.
            @param frame  The PointCloudFrame  from InuStreamsPyth.
            @return  An instance of the ImuFr initialized with the specified InuStreamsPyth.PointCloudF  object.
        """

    # @brief    InuStreamsPyth.PointCloudFrame.
    #
    pointCloudFrame = None


class PointCloudStream(BaseStream):
    """! Interface for PointCloud service.

    Role: Controls PointCloud streaming service and provides general or PointCloud frames.
          IMU frames are provided only if the connected device supports PointCloud HW components.
          The caller application should be familiar with provided frames and should know how to interpret them.

    Responsibilities:
          1. Derives BaseStream class
          2. Knows how to acquire one PointCloud image frame (pull)
          3. Knows how to provide a continuous stream of PointCloud frames (push)
    """

    # @brief    InuStreamsPyth.PointCloudS.
    #
    stream = None

    def __init__(self, stream: PointCloudS):
        """! The Imu stream class initializer.
            @param stream  The InuStreamsPyth.ImuS.
            @return  An instance of the PointCloud stream initialized with the specified
            InuStreamsPyth.PointCloudS object.
        """
        BaseStream.__init__(self, stream)
        self.stream = stream

    def init(self) -> None:
        # @brief    Service initialization.
        #
        # Hall be invoked once before starting frames acquisition.
        self.stream.Init()

    def callback_func(self, stream: PointCloudS, frame: PointCloudF, error: InuError) -> None:
        # @brief    Prototype of callback function which is used by the Register method.
        #
        # This function is invoked any time a frame is ready, or if an error occurs. The parameters of this function
        # are: Caller stream object, received PointCloud frame and result code.
        if error is None:
            print('Undefined error in Imu stream')
        elif error.code != EErrorCode.OK:
            print('Imu CallBack callback Error = {} {}'.format(error.code, error.description))
        else:
            self.callback(PointCloudStream(stream), PointCloudFrame(frame), error)

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
    def frame(self) -> PointCloudFrame:
        # @brief   Retrieves new frame (pull)
        #
        # This method returns when a new frame is ready (blocking) or if an input timeout has elapsed.
        # It shall be called only after a start() was invoked but before any invocation of a stop() is invoked.
        # @return  The returned stereo frame.
        return PointCloudFrame(self.stream.GetFrame())
