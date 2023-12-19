class BaseFrame:
    def __init__(self, frame):
        self.frame = frame
        """! The Base Frame class initializer.
            @param frame  The one of frames from InuStreamsPyth.
            @return  An instance of the BaseFrame initialized with the specified InuStreamsPyth.frame  object.
        """

    frame = None

    SCORE_MIN = 0
    SCORE_MAX = 100

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
