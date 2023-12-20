from inu_api.base_stream import BaseStream
from inu_api.depth_properties import CroppingROI
from inu_api.base_frame import BaseFrame
# from InuStreamsPyth import FeaturesTrackingF, FeaturesTrackingS, InuError, FeaturesTrackingParsedData,\
#     FeaturesTrackingProcessedData
from inu_api.InuStreamsPyth import *

from enum import IntEnum


class FeaturesTrackingFrame(BaseFrame):
    """!  Features Tracking frame.

    Role: Represents Features Tracking frame.

    Responsibilities:
          1. Access to Features Tracking dats.
    """

    # @brief    Define FeaturesTracking Stream's Output types
    #
    class EOutputType(IntEnum):
        # Provides FeaturesTracking Frames with Parsed output type
        Default = FeaturesTrackingS.EOutputType.Parsed
        # Provides FeaturesTracking Frames with Raw output type
        Raw = FeaturesTrackingS.EOutputType.Raw
        # Provides FeaturesTracking Frames with Parsed output type
        Parsed = FeaturesTrackingS.EOutputType.Parsed
        # Provides FeaturesTracking Frames with Processed output type
        Processed = FeaturesTrackingS.EOutputType.Processed

    def __init__(self, frame: FeaturesTrackingF):
        self.frame = frame
        BaseFrame.__init__(self, frame)
        """! The Features Tracking Frame class initializer. @param frame  The FeaturesTrackingFrame  from 
        InuStreamsPyth. @return  An instance of the Features Tracking frame initialized with the specified 
        InuStreamsPyth.FeaturesTrackingF  object.
        """

    @property
    def data(self) -> FeaturesTrackingParsedData or FeaturesTrackingProcessedData:
        # @brief data getter
        #
        # @Detailed description:        Get ParsedData array
        # @return                       The ParsedData or ProcessedData array
        if self.output_type == Default or self.output_type == Parsed:
            return self.frame.ParsedData
        elif self.output_type == Processed:
            return self.frame.ProcessedData
        else:   # self.output_type == Raw:
            return None

    @property
    def image_width(self) -> int:
        # @brief Image Width getter
        #
        # @Detailed description:        Get Image Width
        # @return                       The Image Width
        return self.frame.ImageWidth

    @property
    def image_height(self) -> int:
        # @brief Image Height getter
        #
        # @Detailed description:        Get Image Height
        # @return                       The Image Height
        return self.frame.ImageHeight

    @property
    def output_type(self) -> EOutputType:
        # @brief Output Type getter
        #
        # @Detailed description:        Get Output Type
        # @return                       The Output Type
        return FeaturesTrackingStream.EOutputType(self.frame.OutputType)

    @property
    def key_point_number(self) -> int:
        # @brief Key Point Number getter
        #
        # @Detailed description:        Get Key Point Number
        # @return                       The Key Point Number
        return self.frame.KeyPointNumber

    @property
    def key_point_number_right(self) -> int:
        # @brief Key Point Number Right getter
        #
        # @Detailed description:        Get Key Point Right Number
        # @return                       The Key Point Right Number
        return self.frame.KeyPointNumberRight

    @property
    def key_point_number_left(self) -> int:
        # @brief Key Point Number Left getter
        #
        # @Detailed description:        Get Key Point Left Number
        # @return                       The Key Point Left Number
        return self.frame.KeyPointNumberLeft

    @property
    def descriptor(self):
        # @brief descriptor getter
        #
        # @Detailed description:        Get descriptor
        # @return                       The descriptor
        return self.frame.Descriptor

    @property
    def descriptor_size(self):
        # @brief descriptor size getter
        #
        # @Detailed description:        Get descriptor size
        # @return                       The descriptor size
        return self.frame.DescriptorSize


class FeaturesTrackingStream(BaseStream, CroppingROI):
    """! Interface for FeaturesTracking service.

    Role: Controls FeaturesTracking streaming service and provides Stereo FeaturesTracking frames.

    Responsibilities:
          1. Derives BaseStream class
          2. Knows how to acquire one stereo frame (pull)
          3. Knows how to provide a continuous stream of stereo frames (push)
    """

    def __init__(self, stream: FeaturesTrackingS):
        """! The FeaturesTracking stream class initializer.
            @param stream  The InuStreamsPyth.FeaturesTrackingS.
            @return  An instance of the FeaturesTracking stream initialized with the specified
            InuStreamsPyth.FeaturesTrackingS object.
        """
        BaseStream.__init__(self, stream)
        self.stream = stream

    def init(self, form: FeaturesTrackingFrame.EOutputType = FeaturesTrackingFrame.EOutputType.Default) -> None:
        # @brief    Service initialization.
        #
        # Hall be invoked once before starting frames acquisition.
        # @param  format            The Output type that should be invoked.
        self.stream.Init(FeaturesTrackingS.EOutputType(form))

    def callback_func(self, stream: FeaturesTrackingS, frame: FeaturesTrackingF, error: InuError) -> None:
        # @brief    Prototype of callback function which is used by the Register method.
        #
        # This function is invoked any time a frame is ready, or if an error occurs. The parameters of this function
        # are: Caller stream object, received depth frame and result code.
        if error is None:
            print('Undefined error in FeaturesTracking stream')
        elif error.code != EErrorCode.OK:
            print('FeaturesTracking CallBack callback Error = {} {}'.format(error.code, error.description))
        else:
            self.callback(FeaturesTrackingStream(stream), FeaturesTrackingFrame(frame), error)

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
    def frame(self) -> FeaturesTrackingFrame:
        # @brief   Retrieves new frame (pull)
        #
        # This method returns when a new frame is ready (blocking) or if an input timeout has elapsed.
        # It shall be called only after a start() was invoked but before any invocation of a stop() is invoked.
        # @return  The returned FeaturesTracking frame.
        return FeaturesTrackingFrame(self.stream.GetFrame())
