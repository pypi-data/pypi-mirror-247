from inu_api.base_stream import BaseStream
from inu_api.depth_properties import CroppingROI
from inu_api.base_frame import BaseFrame
from inu_api.image_frame import ImageFrame
from InuStreamsPyth import *

from enum import IntEnum


class StereoFrame(BaseFrame):
    """!  Stereo Image frame.

    Role: Represents Stereo Image which comprises left and right sensor images.

    Responsibilities:
          1. Access to Left and Right frames separately
    """

    def __init__(self, frame: StereoF):
        self.frame = frame
        BaseFrame.__init__(self, frame)
        """! The Stereo Frame class initializer.
            @param frame  The StereoFrame  from InuStreamsPyth.
            @return  An instance of the Image initialized with the specified InuStreamsPyth.StereoFrame  object.
        """

    # @brief    InuStreamsPyth.StereoFrame.
    #
    frame = None
    # left_image = None
    # right_image = None

    @property
    def left_frame(self) -> ImageFrame:
        # @brief left getter
        #
        # @Detailed description:        Get left frame Image
        # @return                       The left frame Image
        # if self.left_image is None:
        #     self.left_image = ImageFr(self.frame.LeftFrame)
        # return self.left_image
        return ImageFrame(self.frame.LeftFrame)

    @property
    def right_frame(self) -> ImageFrame:
        # @brief left getter
        #
        # @Detailed description:        Get right frame Image
        # @return                       The right frame Image
        # if self.right_image is None:
        #     self.right_image = ImageFr(self.frame.RightFrame)
        # return self.right_image
        return ImageFrame(self.frame.RightFrame)


class StereoStream(BaseStream, CroppingROI):
    """! Interface for Stereo service.

    Role: Controls Stereo images streaming service and provides Stereo Image frames.

    Responsibilities:
          1. Derives BaseStream class
          2.  Knows how to acquire one stereo frame (pull)
          3. Knows how to provide a continuous stream of stereo frames (push)
    """

    # @brief    Define Stereo Stream's Output formats
    #
    class EOutputFormat(IntEnum):
        # Provides CImageFrames with ImageFormat::BGRA, on Android ImageFormat::RGBA
        Default = StereoS.EOutputFormat.Default
        # Provides ImageFrames as streamed by Inuitive chip, no additional processing on Host
        Raw = StereoS.EOutputFormat.Raw
        # Provides CImageFrames of ImageFormat::BGRA format
        BGRA = StereoS.EOutputFormat.BGRA
        # Provides CImageFrames of ImageFormat::RGBA format
        RGBA = StereoS.EOutputFormat.RGBA

    def __init__(self, stream: StereoS):
        """! The Stereo stream class initializer.
            @param stream  The InuStreamsPyth.StereoStream.
            @return  An instance of the Stereo stream initialized with the specified InuStreamsPyth.StereoStream object.
        """
        BaseStream.__init__(self, stream)
        self.stream = stream

    def init(self, form: EOutputFormat = EOutputFormat.Default) -> None:
        # @brief    Service initialization.
        #
        # Hall be invoked once before starting frames acquisition.
        # @param  format            The Output format that should be invoked.
        self.stream.Init(StereoS.EOutputFormat(form))

    def callback_func(self, stream: StereoS, frame: StereoF, error: InuError) -> None:
        # @brief    Prototype of callback function which is used by the Register method.
        #
        # This function is invoked any time a frame is ready, or if an error occurs. The parameters of this function
        # are: Caller stream object, received depth frame and result code.
        if error is None:
            print('Undefined error in Stereo stream')
        elif error.code != EErrorCode.OK:
            print('Stereo CallBack callback Error = {} {}'.format(error.code, error.description))
        else:
            self.callback(StereoStream(stream), StereoFrame(frame), error)

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
    def frame(self) -> StereoFrame:
        # @brief   Retrieves new frame (pull)
        #
        # This method returns when a new frame is ready (blocking) or if an input timeout has elapsed.
        # It shall be called only after a start() was invoked but before any invocation of a stop() is invoked.
        # @return  The returned stereo frame.
        return StereoFrame(self.stream.GetFrame())
