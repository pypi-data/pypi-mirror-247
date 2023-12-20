from inu_api.base_stream import BaseStream
from inu_api.base_frame import BaseFrame
# from InuStreamsPyth import CnnAppF, CnnAppS, MapUintString, VectorString
from inu_api.InuStreamsPyth import *

from enum import IntEnum


class CnnAppFrame(BaseFrame):
    """!  CnnApp frame.

    Role: Represents generic buffer that is provided by some of InuDev streams

    Responsibilities:
          1. Buffer attributes: data and size.
          2. Memory management control.

    Comment: The interpretation of provided buffers should be done by the caller application.
             The caller application should be familiar with the internal format of
             each provided frame.

    """

    # @brief    Define Cnn App's Output formats
    #
    class EOutputType(IntEnum):
        Unknown = CnnAppF.EOutputType.Unknown
        # Object detection SSD fast but less accurate
        ObjectDetection = CnnAppF.EOutputType.ObjectDetection
        Segmentation = CnnAppF.EOutputType.Segmentation
        Classification = CnnAppF.EOutputType.Classification
        FaceRecognition = CnnAppF.EOutputType.FaceRecognition
        # Similar behavior as eObjectDetection but a different network(YoloV3) slower & accurate.
        ObjectDetectionYoloV3 = CnnAppF.EOutputType.ObjectDetectionYoloV3
        EnrollFace = CnnAppF.EOutputType.EnrollFace
        Yolact = CnnAppF.EOutputType.Yolact
        ObjectDetectionYoloV7 = CnnAppF.EOutputType.ObjectDetectionYoloV7

    # @brief    Define Define Cnn App's FacePose formats
    #
    class EFacePose(IntEnum):
        # Unrecognized position .
        NonePose = CnnAppF.EFacePose.NonePose
        # Looking to the left (Horizontal).
        Left = CnnAppF.EFacePose.Left
        # Looking to the right (Horizontal).
        Right = CnnAppF.EFacePose.Right
        # Looking to the top (Vertical).
        Top = CnnAppF.EFacePose.Top
        # Object Looking to the bottom (Vertical)
        Bottom = CnnAppF.EFacePose.Bottom
        # Looking to the center (Horizontal/Vertical).
        Center = CnnAppF.EFacePose.Center

    # class DetectedObject:
    #     """!  Detected Object struct.
    #
    #     Role: Represents DetectedObject.
    #
    #     """
    #     object: InuStreamsPyth.DetectedObject = None
    #
    #     def __init__(self, object: InuStreamsPyth.DetectedObject):
    #         self.object = object
    #
    #     @property
    #     def class_id(self)-> str:
    #         #@brief	Classification identifier of this object
    #         return self.object.ClassID
    #
    #     @property
    #     def confidence(self) -> float:
    #         # @brief	Confidence score of this object
    #         return self.object.Confidence
    #
    #     @property
    #     def closed_rect_top_left(self) -> Point2D:
    #         # @brief	Top Left coordinates of detected object.
    #         return self.object.ClosedRectTopLeft
    #
    #     @property
    #     def closed_rect_size(self) -> Point2D:
    #         # @brief	Size of recognized face.
    #         return self.object.ClosedRectSize
    #
    #     @property
    #     def ObjectColor(self) -> float:
    #         # @brief	Color of the object(if applicable - Yolact).
    #         return self.object.ObjectColor
    #
    #
    # class RecognizedFace:
    #     """!  Recognized Face struct.
    #
    #     Role: Represents DetectedObject.
    #
    #     """
    #     face: InuStreamsPyth.RecognizedFace = None
    #
    #     LANDMARKS_POINTS = 5
    #
    #     def __init__(self, face: InuStreamsPyth.RecognizedFace):
    #         self.face = face
    #
    #     @property
    #     def face_id(self)-> str:
    #         #@brief	Classification identifier of this object
    #         return self.face.FaceId
    #
    #     @property
    #     def confidence(self)-> float:
    #         #@brief	Confidence score of this object
    #         return self.face.Confidence;
    #
    #     @property
    #     def closed_rect_top_left(self)-> Point2D:
    #         #@brief	Top Left coordinates of detected object.
    #         return self.face.ClosedRectTopLeft
    #
    #     @property
    #     def closed_rect_size(self)-> Point2D:
    #         #@brief	Size of recognized face.
    #         return self.face.ClosedRectSize
    #
    #     @property
    #     def horizontal_position(self)-> EFacePose:
    #         #@brief	Horizontal face position (Left/Right/Center).
    #         return self.face.poseH
    #
    #     @property
    #     def vertical_position(self)-> EFacePose:
    #         #@brief	Vertical face position (Top/Bottom/Center).
    #         return self.face.poseH
    #
    #     @property
    #     def landmarks(self)-> VectorRecognizedFaces:
    #         #@brief	Vertical face position (Top/Bottom/Center).
    #         return self.face.Landmarks
    #
    # class ClassificationData:
    #     """!  Classification Data struct.
    #
    #     Role: Represents ClassificationData.
    #
    #     """
    #     data: InuStreamsPyth.ClassificationData = None
    #
    #     def __init__(self, data: InuStreamsPyth.ClassificationData):
    #         self.data = data
    #
    #     @property
    #     def class_id(self)-> str:
    #         #@brief	Classification identifier of this object
    #         return self.data.ClassID
    #
    #     @property
    #     def confidence(self)-> float:
    #         #@brief	Confidence score of this object
    #         return self.data.Confidence
    #

    def __init__(self, frame: CnnAppF):
        self.cnnAppFrame = frame
        BaseFrame.__init__(self, frame)
        """! The Imu Frame class initializer.
                @param frame  The CnnAppFrame  from InuStreamsPyth.
                @return  An instance of the ImuFr initialized with the specified InuStreamsPyth.CnnAppFrame  object.
            """

    # @brief    InuStreamsPyth.CnnAppF.
    #
    cnnAppFrame = None

    @property
    def output_type(self) -> EOutputType:
        # @brief Getter for Cnn OutputType
        return EOutputType(self.cnnAppFrame.OutputType)

    @property
    def data(self):  # InuStreamsPyth.VectorRecognizedFaces or InuStreamsPyth.VectorDetectedObject or
        #  InuStreamsPyth.SegmentationData or InuStreamsPyth.SegmentationData
        # @brief	Getter for cnn app frame data
        cnn_output_type = self.frame.OutputType
        if cnn_output_type == ObjectDetection or cnn_output_type == ObjectDetectionYoloV3 or \
                cnn_output_type == ObjectDetectionYoloV7 or cnn_output_type == Yolact:
            return self.cnnAppFrame.ObjectData
        elif cnn_output_type == FaceRecognition:
            return self.cnnAppFrame.FaceData
        elif cnn_output_type == Segmentation:
            return self.cnnAppFrame.Segmentation
        elif cnn_output_type == Classification:
            return self.cnnAppFrame.Classification
        else:  # Unknown or EnrollFace
            return None

    @property
    def width(self) -> int:
        # @ Getter for Width
        return self.cnnAppFrame.Width

    @property
    def height(self) -> int:
        # @ Getter for Height
        return self.cnnAppFrame.Height


class CnnAppStream(BaseStream):
    """! Interface for Cnn App service.

    Role: Controls Cnn App streaming service and provides general or Cnn App frames.
          IMU frames are provided only if the connected device supports Cnn App HW components.
          The caller application should be familiar with provided frames and should know how to interpret them.

    Responsibilities:
          1. Derives BaseStream class
          2. Knows how to acquire one depth image frame (pull)
          3. Knows how to provide a continuous stream of depth image frames (push)
    """

    # @brief    InuStreamsPyth.CnnAppS.
    #
    stream = None

    def __init__(self, stream: CnnAppS):
        """! The Cnn App stream class initializer.
            @param stream  The InuStreamsPyth.CnnAppS.
            @return  An instance of the Cnn App stream initialized with the specified InuStreamsPyth.CnnAppS object.
        """
        BaseStream.__init__(self, stream)
        self.stream = stream

    def init(self) -> None:
        # @brief    Service initialization.
        #
        # Hall be invoked once before starting frames acquisition.
        self.stream.Init()

    def callback_func(self, stream, frame, error) -> None:
        # @brief    Prototype of callback function which is used by the Register method.
        #
        # This function is invoked any time a frame is ready, or if an error occurs. The parameters of this function
        # are: Caller stream object, received Imu frame and result code.
        if error is None:
            print('Undefined error in Imu stream')
        elif error.code != EErrorCode.OK:
            print('Imu CallBack callback Error = {} {}'.format(error.code, error.description))
        else:
            self.callback(CnnAppStream(stream), CnnAppFrame(frame), error)

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
    def frame(self) -> CnnAppFrame:
        # @brief   Retrieves new frame (pull)
        #
        # This method returns when a new frame is ready (blocking) or if an input timeout has elapsed.
        # It shall be called only after a start() was invoked but before any invocation of a stop() is invoked.
        # @return  The returned Cnn App frame.
        return CnnAppFrame(self.stream.GetFrame())

    @property
    def segmentation_labels(self) -> MapUintString:
        # @brief    Getter segmentation labels for segmentation image
        #
        # @return SegmentationLabels Labels returned from AI lib.
        return self.stream.SegmentationLabels

    def enroll_person(self, person_name: str, path: str = None) -> None:
        # @brief    Enroll new person(face) for Face recognition AI, can be used only after Enroll stream is initialized and started.
        #
        # @param person_name - Name of the person to enroll
        # @param path - Path to folder with images to enroll, default images will be taken from "C:\Program Files\Inuitive\InuDev\config\AI\FaceDetection\faces"
        return self.stream.EnrollPerson(person_name, path)

    def delete_person(self, person_name: str) -> None:
        # @brief    Delete person(face) from Face recognition AI Database, can be used only after Enroll stream is initialized and started.
        #
        # @param person_name - Name of the person to enroll
        return self.stream.DeletePerson(person_name, path)

    @property
    def list_of_faces(self) -> VectorString:
        # @brief    Retrieve vector of names from face recognition AI Database, can be used only after Enroll stream is initialized and started.
        #
        # @return Names of enrolls
        return self.stream.ListOfFaces

    @property
    def image_channel(self) -> int:
        # @brief    Retrieve Image channel ID connected to the CNNApp Stream. Can only be called after CnnAppStream is started.
        #
        # @return Image channel ID as set by default or by user.
        return self.stream.ImageChannel
