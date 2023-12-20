from inu_api.common import *


class BaseStream:
    """! Common interface for all InuDev NUI streams.

    Role: Base class for all streams classes. It defines an interface that should be implemented by all derived classes.

    Responsibilities:
          1. Knows how to control the service (Init, Terminate, Start and Stop)
          2. Implements a state machine (more details in Reference Manual)
    """

    DEFAULT_CHANNEL_ID = 4294967295

    # @brief    The one of InuStreamsPyth streams.
    #
    baseStream = None

    # @brief    The Callback to one of InuStreamsPyth streams.
    #
    callback = None

    def __init__(self, stream):
        self.baseStream = stream
        """! The stream class initializer.
            @param stream  The one of InuStreamsPyth streams..
            @return  An instance of the stream initialized with the specified InuStreamsPyth stream object.
        """

    def start(self) -> None:
        # @brief    Start acquisition of frames.
        #
        # Shall be invoked only after the service is successfully initialized and before any request
        # for new frame (push or pull).
        self.baseStream.Start()

    def stop(self) -> None:
        # @brief    Stop acquisition of frames.
        #
        self.baseStream.Stop()

    def terminate(self) -> None:
        # @brief    Service termination.
        #
        # Shall be invoked when the service is no longer in use and after frames acquisition has stopped.
        self.baseStream.Terminate()

    @property
    def channel_id(self) -> str:
        # @brief    Final stream channel ID as received from InuService.
        #
        # @return ChannelId as string
        return self.baseStream.ChannelID

    def record(self, destination_directory: str, template_name: str = None, duration: int = -1) -> None:
        # @brief Record NU streams
        #
        # @param  destinationDirectory    The Destination directory for recording output. Send empty string to stop
        # recording. @param  templateName . The string which will be concatenated to output file name. @param
        #    duration. The recording time in ms.
        self.baseStream.Record(destination_directory, template_name, duration)

    def snapshot(self, destination_directory: str, template_name: str = None, file_name_index: int = -1) -> None:
        # @brief Snapshot NU streams
        #
        # @param  destinationDirectory    The Destination directory for recording output. Send empty string to stop
        #   recording. @param  templateName            The string which will be concatenated to output file name. @param
        # fileNameIndex           The string which will be concatenated to output file name. If no index is provided
        # then frame index will be used.
        self.baseStream.Snapshot(destination_directory, template_name, file_name_index)

