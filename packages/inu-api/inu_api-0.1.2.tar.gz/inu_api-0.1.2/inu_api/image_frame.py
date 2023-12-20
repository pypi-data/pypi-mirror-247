from inu_api.base_frame import BaseFrame
from inu_api.InuStreamsPyth import *


class ImageFrame(BaseFrame):
    """!  Image frame.

    Role: Represents  an image that is  provided  by InuDev streams

    Responsibilities:
          1. Image attributes: format, scale, width, height and number of bytes per pixel.
          2. Knows how to manage the image buffer.
    """

    def __init__(self, frame: ImageF):
        self.imageFrame = frame
        BaseFrame.__init__(self, frame)
        """! The Image Frame class initializer.
            @param frame  The ImageF  from InuStreamsPyth.
            @return  An instance of the Image initialized with the specified InuStreamsPyth.ImageF  object.
        """

    # @brief    InuStreamsPyth.ImageF.
    #
    imageFrame = None

    @property
    def width(self) -> int:
        # @brief    The Image width.
        return self.imageFrame.Width

    @width.setter
    def width(self, value: int) -> None:
        # @brief    Image width setter.
        #
        # @param[in]   value	    New Image width.
        self.imageFrame.Width = value

    @property
    def height(self) -> int:
        # @brief    The image height.
        return self.imageFrame.Height

    @height.setter
    def height(self, value: int) -> None:
        # @brief    Image height setter.
        #
        # @param[in]   value	 The new Image height.
        self.imageFrame.Height = value

    @property
    def cropped_image_width(self) -> int:
        # @brief    The width of image that is cropped by depth engine, is relevant when the image padding is requested.
        #           cropped_image_width <=  Width.
        return self.imageFrame.CroppedImageWidth

    @cropped_image_width.setter
    def cropped_image_width(self, value: int) -> None:
        # @brief    The Image Cropped Image Width setter.
        #
        # @param[in]   value	    The new Image CroppedImageWidth.
        self.imageFrame.CroppedImageWidth = value

    @property
    def cropped_image_height(self) -> int:
        # @brief    The height of image  that is cropped by depth engine, is relevant when the image padding is
        #           requested cropped_image_height <=  Height.
        return self.imageFrame.CroppedImageHeight

    @cropped_image_height.setter
    def cropped_image_height(self, value: int) -> None:
        # @brief    The Image Cropped Image Width setter.
        #
        # @param[in]   value	    The new Image CroppedImageWidth.
        self.imageFrame.CroppedImageWidth = value

    @property
    def cropped_image_top_left_w(self) -> int:
        # @brief    The width of image that is cropped by depth engine, is relevant when the image padding is
        #           requested. CroppedImageWidth <=  Width.
        return self.imageFrame.CroppedImageTopLeftW

    @cropped_image_top_left_w.setter
    def cropped_image_top_left_w(self, value: int) -> None:
        # @brief    The Image Cropped ImageTop Left W setter.
        #
        # @param[in]   value	    The new Image CroppedImageTopLeftW.
        self.imageFrame.CroppedImageTopLeftW = value

    @property
    def cropped_image_top_left_h(self) -> int:
        # @brief    The top left height offset of cropped image, is relevant when the image padding is requested.
        #           CroppedImageTopLeftH >= 0.
        return self.imageFrame.CroppedImageTopLeftH

    @cropped_image_top_left_h.setter
    def cropped_image_top_left_h(self, value: int) -> None:
        # @brief    The Image Cropped Image Top Left H setter.
        #
        # @param[in]   value	    The new Image CroppedImageTopLeftH.
        self.imageFrame.CroppedImageTopLeftH = value

    @property
    def format(self) -> int:
        # @brief    The Image format getter.
        return self.imageFrame.Format

    @format.setter
    def format(self, value: int) -> None:
        # @brief    Image format setter.
        #
        # @param[in]   value	    New Image format.
        self.imageFrame.Format = value

    @property
    def bytes_per_pixel(self) -> int:
        # @brief    The number of bytes that are used to represent each pixel.
        return self.imageFrame.BytesPerPixel

    @property
    def time_stamp(self) -> int:
        # @brief    The frame acquisition time in nanoseconds relates to host's system clock.
        #           It should be used for frames synchronization.
        return self.frame.Timestamp

    @property
    def frame_index(self) -> int:
        # @brief    The frame acquisition unique index, should be used for synchronization.
        return self.frame.FrameIndex

    @property
    def chunk_index(self) -> int:
        # @brief    The index of a chunk inside a frame, should be used for synchronization.
        return self.frame.ChunkIndex

    @property
    def valid(self) -> bool:
        # @brief   Indicates if this frame is valid data or not.
        return self.frame.Valid

    @property
    def score(self) -> int:
        # @brief   The confidence of current frame. Range is from SCORE_MIN up to SCORE_MAX.
        return self.frame.Score

    @property
    def service_time_stamp(self) -> int:
        # @brief   The  time stamp which is set when frame is received from USB (used for statistics and analysis).
        return self.frame.ServiceTimestamp

    @property
    def stream_time_stamp(self) -> int:
        # @brief   The time stamp which is set when frame is received from InuService (used for statistics and
        # analysis).
        return self.frame.StreamTimestamp

    @property
    def calibration_temperature(self) -> int:
        # @brief   Calibration temperature which was applied while this frame was acquired.
        # std::numeric_limits<int32_t>::max() if it is not valid.
        return self.frame.CalibrationTemperature

    @property
    def was_recorded(self) -> bool:
        # @brief  Indicated if the trame was recorded by InuService or doesn't.
        return self.frame.WasRecorded

    @property
    def active_projector(self) -> int:
        # @brief  The active projector received by FW for this frame: 0 - default(Pattern), 1 - Flood projector.
        return self.frame.ActiveProjector

    @property
    def projector_level(self) -> int:
        # @brief  The projector level received by FW for this frame.
        return self.frame.mProjectorLevel

    @property
    def projector_type(self) -> int:
        # @brief  The projector type by FW for this frame.
        return self.frame.mProjectorType
