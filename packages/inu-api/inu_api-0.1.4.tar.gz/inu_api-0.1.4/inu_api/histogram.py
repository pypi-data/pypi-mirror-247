from inu_api.base_stream import BaseStream
from inu_api.base_frame import BaseFrame
from InuStreamsPyth import *
# from InuStreamsPyth import HistogramF, HistogramS, InuError, Point2D, VectorHistogramROI


class HistogramROI:
    """!  Histogram ROI.

    Role: Represents Histogram data and ROI.

    """
    topLeft: Point2D = None
    bottomRight: Point2D = None
    histograms: VectorHistogramROI = None
    accumulator: int = 0;


class HistogramFrame(BaseFrame):
    """!  Histogram frame.

    Role: Represents collection of Histogram data that is provided by Histogram.

    """

    def __init__(self, frame: HistogramF):
        self.histogramFrame = frame
        BaseFrame.__init__(self, frame)
        """! The Imu Frame class initializer.
            @param frame  The HistogramFrame  from InuStreamsPyth.
            @return  An instance of the HistogramFrame initialized with the specified InuStreamsPyth.HistogramF  object.
        """

    # @brief    InuStreamsPyth.HistogramF.
    #
    histogramFrame = None

    @property
    def histograms(self) -> VectorHistogramROI:
        # @brief    All histograms roi
        #
        # @return all histograms roi as VectorHistogramROI
        return self.histogramFrame.Histograms


class HistogramStream(BaseStream):
    """! Interface for Histogram service.

    Role: Controls Histogram streaming service and provides general or Histogram frames.
           Histogram frames are provided only if the connected device supports Histogram HW components.
           The caller application should be familiar with provided frames and should know how to interpret them.

    Responsibilities:
          1. Derives BaseStream class
          2. Knows how to acquire one depth image frame (pull)
          3. Knows how to provide a continuous stream of histogram frames (push)
    """

    # @brief    InuStreamsPyth.HistogramS.
    #
    stream = None

    def __init__(self, stream: HistogramS):
        """! The Histogram stream class initializer.
            @param stream  The InuStreamsPyth.HistogramStream.
            @return  An instance of the Imu stream initialized with the specified InuStreamsPyth.HistogramS object.
        """
        BaseStream.__init__(self, stream)
        self.stream = stream

    def init(self) -> None:
        # @brief    Service initialization.
        #
        # Hall be invoked once before starting frames acquisition.
        self.stream.Init()

    def callback_func(self, stream: HistogramS, frame: HistogramF, error: InuError) -> None:
        # @brief    Prototype of callback function which is used by the Register method.
        #
        # This function is invoked any time a frame is ready, or if an error occurs. The parameters of this function
        # are: Caller stream object, received Histogram frame and result code.
        if error is None:
            print('Undefined error in Histogram stream')
        elif error.code != EErrorCode.OK:
            print('Histogram CallBack callback Error = {} {}'.format(error.code, error.description))
        else:
            self.callback(HistogramStream(stream), HistogramFrame(frame), error)

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
    def frame(self) -> HistogramFrame:
        # @brief   Retrieves new frame (pull)
        #
        # This method returns when a new frame is ready (blocking) or if an input timeout has elapsed.
        # It shall be called only after a start() was invoked but before any invocation of a stop() is invoked.
        # @return  The returned stereo frame.
        return HistogramFrame(self.stream.GetFrame())
