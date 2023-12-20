from inu_api.base_stream import BaseStream
from inu_api.base_frame import BaseFrame
from InuStreamsPyth import *

from enum import IntEnum


class SlamFrame(BaseFrame):
    """!  Slam frame.

    Role: Represents frames that are provided by CSlamStream

    """

    # @brief    Define Slam State options
    #
    class EState(IntEnum):
        NotSupportedState = SlamF.ESlamState.NotSupporttedState
        TrackOK = SlamF.ESlamState.TrackOK
        TrackLostNoReloc = SlamF.ESlamState.TrackLostNoReloc
        TrackLostNumFeatures = SlamF.ESlamState.TrackLostNumFeatures
        TrackLostNumStereoPairs = SlamF.ESlamState.TrackLostNumStereoPairs
        TrackLostNumMatcher = SlamF.ESlamState.TrackLostNumMatcher
        TrackLostNumInliners1 = SlamF.ESlamState.TrackLostNumInliners1
        TrackLostNumInliners2 = SlamF.ESlamState.TrackLostNumInliners2
        TrackLost = SlamF.ESlamState.TrackLost
        RelocalizationSucceeded = SlamF.ESlamState.RelocalizationSucceeded
        LoopClosed = SlamF.ESlamState.LoopClosed
        ImuNoVisual = SlamF.ESlamState.ImuNoVisual
        SlamMapPointNotSync = SlamF.ESlamState.SlamMapPointNotSync
        FrameUnexpectedError = SlamF.ESlamState.FrameUnexpectedError

    # @brief    Define Slam Internal State options
    #
    class EInternalState(IntEnum):
        NotSupportedInternalState = SlamF.ESlamInternalState.NotSupporttedInternalState
        Keyframe = SlamF.ESlamInternalState.Keyframe
        InTrack = SlamF.ESlamInternalState.InTrack
        InRelocalization = SlamF.ESlamInternalState.InRelocalization
        InLoopClosing = SlamF.ESlamInternalState.InLoopClosing
        InLBA = SlamF.ESlamInternalState.InLBA
        UnexpectedInternalError = SlamF.ESlamInternalState.UnexpectedInternalError

    def __init__(self, frame: SlamF):
        self.slamFrame = frame
        BaseFrame.__init__(self, frame)
        """! The Imu Frame class initializer.
            @param frame  The SlamFrame  from InuStreamsPyth.
            @return  An instance of the SlamFrame initialized with the specified InuStreamsPyth.SlamF  object.
        """

    # @brief    InuStreamsPyth.SlamF.
    #
    slamFrame = None

    @property
    def state(self) -> EState:
        # @brief  Current Slam state reported to the application
        #
        # @return  TheSlam state.
        return self.slamFrame.State

    @property
    def internal_state(self) -> EInternalState:
        # @brief  Current Slam state reported to the application
        #
        # @return  The Slam internal state.
        return self.slamFrame.InternalState

    @property
    def pose4x4body2world(self):
        # @brief  The transformation matrix describing how the body moves in the World coordinate system
        #   (used to display the trajectory in 3D in the World coordinate system).
        #
        # @return  array float[16].
        return self.slamFrame.Pose4x4BodyToWorld

    @property
    def pose4x4world2body(self):
        # @brief   The transformation matrix describing how objects in the World coordinate system
        #   move relatively to a fixed coordinate system at the body of the robot (used
        #   for graphical display to overlay object over the camera image).
        #
        # @return  array float[16].
        return self.slamFrame.Pose4x4WorldToBody


class SlamStream(BaseStream):
    """! Interface for SLAM service.

    Role: Controls Slam streaming service and provides Slam frames.

    Responsibilities:
          1. Derives BaseStream class
          2. Knows how to acquire one Slam frame (pull)
          3. Knows how to provide a continuous stream of slam frames (push)
    """

    # @brief    Use coordinates transformations according to enumerator: calibrated or virtual coordinate system.
    #
    class ECoordinateSystem(IntEnum):
        # @ brief    Calibrated cameras option. use CameraToModule, ModuleToBody, BodyToWorld transformations to user's
        #       coordinate system, ignoring virtual camera. - CALIBRATED_CAMERA_USER_TRANSFORMATION,
        CalibratedCameraUserTransformation = SlamS.ECoordinateSystem.CalibratedCameraUserTransformation
        # @ brief   default: Virtual cameras option. use the left camera system, ignoring CameraToModule, ModuleToBody,
        #       BodyToWorld - VIRTUAL_CAMERA_LEFT_CAMERA
        VirtualCameraLeftCamera = SlamS.ECoordinateSystem.VirtualCameraLeftCamera
        # @ brief   Virtual cameras option. use the right camera system, ignoring CameraToModule, ModuleToBody,
        #       BodyToWorld - VIRTUAL_CAMERA_RIGHT_CAMERA
        VirtualCameraRightCamera = SlamS.ECoordinateSystem.VirtualCameraRightCamera
        # @ brief   Virtual cameras option. use the baseline center camera system, ignoring CameraToModule,
        #       ModuleToBody, BodyToWorld - VIRTUAL_CAMERA_BASELINE_CENTER
        VirtualCameraBaselineCenter = SlamS.ECoordinateSystem.VirtualCameraBaselineCenter

    class TransformationsParams:
        """!  Transformations Params.

        Role: SLAM output transformation section

        """

        params = None

        def __init__(self, params: SlamTransformationsParams):
            """! The Slam stream class initializer. @param params  The InuStreamsPyth.SlamTransformationsParams.
            @return  An instance of the Slam stream initialized with the specified
                    InuStreamsPyth.SlamTransformationsParams object.
            """
            self.params = params

        @property
        def camera_system(self):
            # @brief   Retrieves Slam CoordinateSystem.
            #
            # @return  The returned slam CoordinateSystem.
            return self.params.CameraSystem

        @camera_system.setter
        def camera_system(self, value) -> None:
            # @brief    camera_system setter.
            self.params.CameraSystem = value

        @property
        def camera2module(self):
            # @brief   Transformation from the module system to physical module system.
            #   The transformation is from the left camera, in slam coordinate system, to the module.
            #   The transformation is a 4x4 matrix ([[R,t],[0,0,0,1]], R is 3x3 rotation), row-wise,
            #   as one row vector. (converted to 4x4).
            # @return  The CameraToModule array.
            return self.params.CameraToModule

        @camera_system.setter
        def camera2module(self, value) -> None:
            # @brief    camera2module setter.
            self.params.CameraToModule = value

        @property
        def module2body(self):
            # @brief   Transformation from the module system to physical module system.
            #
            # Transformation from the module system to the robot's body system (user specified).
            #   The transformation is a 4x4 matrix ([[R,t],[0,0,0,1]], R is 3x3 rotation), row-wise,
            #   as one row vector. (converted to 4x4).
            # @return  The ModuleToBody array.
            return self.params.ModuleToBody

        @camera_system.setter
        def module2body(self, value) -> None:
            # @brief    module2body setter.
            self.params.ModuleToBody = value

        @property
        def body02world(self):
            # @brief   Transformation from the module system to physical module system.
            #
            # Transformation from the body system at frame 0 to world (user) system (stationary, fixed system).
            #   The transformation is a 4x4 matrix ([[R,t],[0,0,0,1]], R is 3x3 rotation), row-wise,
            #   as one row vector. (converted to 4x4).
            # @return  The ModuleToBody array.
            return self.params.ModuleToBody

        @body02world.setter
        def body02world(self, value) -> None:
            # @brief    body02world setter.
            self.params.Body0ToWorld = value

    def __init__(self, stream: TransformationsParams):
        """! The Slam stream class initializer.
            @param stream  The InuStreamsPyth.SlamStream.
            @return  An instance of the Slam stream initialized with the specified InuStreamsPyth.SlamStream object.
        """
        BaseStream.__init__(self, stream)
        self.stream = stream

    def init(self, transformations_params: TransformationsParams = None) -> None:
        # @brief    Service initialization.
        #
        # Hall be invoked once before starting frames acquisition.
        # @param  format            The Output format that should be invoked.
        if transformations_params is None:
            self.stream.Init()
        else:
            self.stream.Init(transformations_params.params)

    def callback_func(self, stream: SlamS, frame: SlamF, error) -> None:
        # @brief    Prototype of callback function which is used by the Register method.
        #
        # This function is invoked any time a frame is ready, or if an error occurs. The parameters of this function
        # are: Caller stream object, received depth frame and result code.
        if error is None:
            print('Undefined error in Stereo stream')
        elif error.code != EErrorCode.OK:
            print('Stereo CallBack callback Error = {} {}'.format(error.code, error.description))
        else:
            self.callback(SlamStream(stream), SlamFrame(frame), error)

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
    def frame(self) -> SlamFrame:
        # @brief   Retrieves new frame (pull)
        #
        # This method returns when a new frame is ready (blocking) or if an input timeout has elapsed.
        # It shall be called only after a start() was invoked but before any invocation of a stop() is invoked.
        # @return  The returned stereo frame.
        return SlamFrame(self.stream.GetFrame())

    @property
    def transformations_params(self):
        # @brief   Composing Transformations Params.
        #
        # @return  The Transformations Params.
        return self.params.ModuleToBody

