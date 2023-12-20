from inu_api.base_stream import BaseStream
from inu_api.depth_properties import DepthProperties, CroppingROI
from inu_api.image_frame import ImageFrame
from inu_api.InuStreamsPyth import *  # DepthS.EOutputFormat
from inu_api.common import *

from enum import IntEnum


class DepthStream(BaseStream, DepthProperties, CroppingROI):
    """! Interface for Depth service.

    Role: Controls depth images streaming service and provides depth image frames.

    Responsibilities:
          1. Derives BaseStream class
          2. Knows how to acquire one depth image frame (pull)
          3. Knows how to provide a continuous stream of depth image frames (push)
    """

    # @brief    Define Depth Stream's Output formats
    #
    class EOutputFormat(IntEnum):
        # Provides ImageFrame with EImageFormat::Depth
        Default = DepthS.EOutputFormat.Default
        # Provides ImageFrame with EImageFormat::eDepth or EImageFormat::eDisparity  as streamed by Inuitive's chip,
        #   no additional processing on Host
        Raw = DepthS.EOutputFormat.Raw
        # Provides ImageFrame with EImageFormat::BGRA
        BGRA = DepthS.EOutputFormat.BGRA
        # Provides ImageFrame with EImageFormat::RGBA
        RGBA = DepthS.EOutputFormat.RGBA
        # Provides ImageFrame with EImageFormat::Depth
        Depth = DepthS.EOutputFormat.Depth
        # Provides ImageFrame with EImageFormat::RGB
        RGB = DepthS.EOutputFormat.RGB

    # @brief    Define Depth Stream's Post Processing methods
    #
    class EPostProcessing(IntEnum):
        # No algorithm is running
        NoneProcessing = DepthS.EPostProcessing.NoneProcessing
        # Register Depth to specific channel
        Registered = DepthS.EPostProcessing.Registration
        # Remove/Fill Holes
        Blob = DepthS.EPostProcessing.Blob
        # Apply TemporalFilter to depth data
        Temporal = DepthS.EPostProcessing.Temporal
        # Remove Outliers/Blobs by size
        OutlierRemove = DepthS.EPostProcessing.OutlierRemove
        # Fill Holes by radius
        HoleFill = DepthS.EPostProcessing.HoleFill
        # Static Temporal filter
        StaticTemporal = DepthS.EPostProcessing.StaticTemporal
        # Defatult, defined by host
        DefaultPP = DepthS.EPostProcessing.DefaultPP

    # @brief    InuStreamsPyth.DepthStream.
    #
    stream = None

    def __init__(self, stream: DepthS):
        """! The Depth stream class initializer.
            @param stream  The InuStreamsPyth.DepthS.
            @return  An instance of the Depth stream initialized with the specified InuStreamsPyth.DepthS object.
        """
        BaseStream.__init__(self, stream)
        DepthProperties.__init__(self, stream)
        CroppingROI.__init__(self, stream)
        self.stream = stream

    def init(self, form: EOutputFormat = EOutputFormat.Default,
             processing: EPostProcessing = EPostProcessing.NoneProcessing,
             reg_channel_id: int = BaseStream.DEFAULT_CHANNEL_ID) -> None:
        # @brief    Service initialization.
        #
        # Hall be invoked once before starting frames acquisition.
        # @param  format            The Output format that should be invoked.
        # @param  processing        The PostProcessing algorithms that should be invoked.
        # @param  regChannelID      The Register Channel ID - in the case of  RegisteredImage only
        self.stream.Init(DepthS.EOutputFormat(form), DepthS.EPostProcessing(processing), reg_channel_id)

    def callback_func(self, stream: DepthS, frame: ImageF, error: InuError) -> None:
        # @brief    Prototype of callback function which is used by the Register method.
        #
        # This function is invoked any time a frame is ready, or if an error occurs. The parameters of this function
        # are: Caller stream object, received depth frame and result code.
        if error is None:
            print('Undefined error in Depth stream')
        elif error.code != EErrorCode.OK:
            print('Depth CallBack callback Error = {} {}'.format(error.code, error.description))
        else:
            print(" ******************** {} ************************ ".format(frame.FrameIndex))
            self.callback(DepthStream(stream), ImageFrame(frame), error)

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
        fr = self.stream.GetFrame()
        print(" Depth.frame {} Depth.frame ".format(fr.FrameIndex))
        return ImageFrame(fr)

    @property
    def default_post_processing_mode(self) -> int:
        # @brief default_post_processing_mode
        #
        # Detailed description:        Get current PostProcessingModeDefault.
        #                              It's possible to use this function before or without starting the stream.
        # @return                      Return the default PostProcessingMode
        return self.stream.DefaultPostProcessingMode()

    def mipi_on(self, on: bool) -> None:
        # @brief    start/stop Mipi
        #
        # Shall be invoked once after a call to on = True in order to start transmitting frames over Mipi.
        # Shall be invoked once after a call to on = False in order to stop transmitting frames over Mipi.
        # This functionality is applicable only when complex graph with mipi connectors are in used.
        # If several streams should be transmitted over mipi then the order of activation should be:
        # "Start / Stop" all streams then "startMipi" of all streams
        if on:
            self.stream.startMipi()
        else:
            self.stream.stopMipi()
    mipi_on = property(None, mipi_on)
