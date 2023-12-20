from inu_api.base_stream import BaseStream
from inu_api.depth_properties import DepthProperties, CroppingROI
from inu_api.image_frame import ImageFrame
from inu_api.InuStreamsPyth import *

from enum import IntEnum


class ImageStream(BaseStream, DepthProperties, CroppingROI):
    """! Interface for Image service.

    Role: Controls depth images streaming service and provides image frames.

    Responsibilities:
          1. Derives BaseStream class
          2. Knows how to acquire one depth image frame (pull)
          3. Knows how to provide a continuous stream of depth image frames (push)
    """

    # @brief    Define Depth Stream's Output formats
    #
    class EOutputFormat(IntEnum):
        # Provides CImageFrames with ImageFormat::BGRA, on Android ImageFormat::RGBA
        Default = ImageS.EOutputFormat.Default
        # Provides CImageFrames as streamed by Inuitive chip, no additional processing on Host
        Raw = ImageS.EOutputFormat.Raw
        # Provides CImageFrames of ImageFormat::BGRA format
        BGRA = ImageS.EOutputFormat.BGRA
        # Provides CImageFrames of ImageFormat::RGBA format
        RGBA = ImageS.EOutputFormat.RGBA
        # Provides CImageFrame of ImageFormat::BGR format
        BGR = ImageS.EOutputFormat.BGR

    # @brief    Define Depth Stream's Post Processing methods
    #
    class EPostProcessing(IntEnum):
        # No algorithm is running
        NoneProcessing = 0
        # Projection of image on depth, format is similar to eDefault
        Registered = ImageS.EPostProcessing.Registered
        # Undistorted image, format is similar to eDefault
        Undistorted = ImageS.EPostProcessing.Undistorted
        # GammaCorrected image, format is similar to eDefault
        GammaCorrect = ImageS.EPostProcessing.GammaCorrect

    # @brief    InuStreamsPyth.ImageS.
    #
    stream = None

    def __init__(self, stream: ImageS):
        BaseStream.__init__(self, stream)
        DepthProperties.__init__(self, stream)
        self.stream = stream
        """! The Depth stream class initializer.
            @param stream  The InuStreamsPyth.ImageS.
            @return  An instance of the Image stream initialized with the specified InuStreamsPyth.ImageS object.
        """

    def init(self, form: EOutputFormat = EOutputFormat.Default,
             processing: EPostProcessing = EPostProcessing.NoneProcessing,
             reg_channel_id: int = BaseStream.DEFAULT_CHANNEL_ID) -> None:
        # @brief    Service initialization.
        #
        # Hall be invoked once before starting frames acquisition.
        # @param  format            The Output format that should be invoked.
        # @param  processing        The PostProcessing algorithms that should be invoked.
        # @param  regChannelID      The Register Channel ID - in the case of  RegisteredImage only
        self.stream.Init(ImageS.EOutputFormat(form), ImageS.EPostProcessing(processing), reg_channel_id)

    def callback_func(self, stream: ImageS, frame: ImageF, error: InuError) -> None:
        # @brief    Prototype of callback function which is used by the Register method.
        #
        # This function is invoked any time a frame is ready, or if an error occurs. The parameters of this function
        # are: Caller stream object, received depth frame and result code.
        if error is None:
            print('Undefined error in Image stream')
        elif error.code != EErrorCode.OK:
            print('Image CallBack callback Error = {} {}'.format(error.code, error.description))
        else:
            self.callback(ImageStream(stream), ImageFrame(frame), error)

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
    def frame(self) -> ImageFrame:
        # @brief   Retrieves new frame (pull)
        #
        # This method returns when a new frame is ready (blocking) or if an input timeout has elapsed.
        # It shall be called only after a start() was invoked but before any invocation of a stop() is invoked.
        # @return  The returned depth frame (Z-buffer).
        return ImageFrame(self.stream.GetFrame())
