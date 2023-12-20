from inu_api.depth_stream import DepthStream
from inu_api.image_stream import ImageStream
from inu_api.stereo import StereoStream
from inu_api.features_tracking import FeaturesTrackingStream
from inu_api.imu import ImuStream
from inu_api.slam import SlamStream
from inu_api.injection import InjectionStream
from inu_api.histogram import HistogramStream
from inu_api.cnn_app import CnnAppStream
from inu_api.point_cloud import PointCloudStream
from inu_api.shared import EStreamType
from InuStreamsPyth import *


class Sensor:
    # @brief    InuStreamsPyth.InuSensor.
    #
    sensor = None

    # @brief    InuStreamsPyth.HwInformation.
    #
    hwInformation = HwInformation()

    # @brief   IP address string.
    #
    ipAddress = None

    def __init__(self, service_id: str = '', ip_address: str = ''):
        self.sensor = InuSensor(service_id)
        self.ipAddress = ip_address
        """! The Sensor class initializer.
            @param serviceId  The Service Id string.
            @param ipAddress  The IP Address string.
            @return  An instance of the Sensor initialized with the specified serviceId and ipAddress.
        """

    def create_stream(self, stream_type: EStreamType, channel_id: int = -1):
        # @brief    SetInjectResolution
        #
        # @Generate all kinds of InuDev streams
        # @param streamType     EStreamType.
        # @param id             The streamer id - channel id or streamer name.
        # @return               An instance of different types of streams with the specified serviceId and ipAddress
        if stream_type == EStreamType.Depth:
            if channel_id == -1:
                return DepthStream(self.sensor.CreateDepthStream())
            return DepthStream(self.sensor.CreateDepthStream(channel_id))
        elif stream_type == EStreamType.Stereo:
            if channel_id == -1:
                return StereoStream(self.sensor.CreateStereoStream())
            return StereoStream(self.sensor.CreateStereoStream(channel_id))
        elif stream_type == EStreamType.GeneralCamera:
            if type(id) == str:
                return ImageStream(self.sensor.CreateImageStream(channel_id))
            elif channel_id == -1:
                return ImageStream(self.sensor.CreateImageStream())
            return ImageStream(self.sensor.CreateImageStream(channel_id))
        elif stream_type == EStreamType.Imu:
            if channel_id == -1:
                return ImuStream(self.sensor.CreateImuStream())
            return ImuStream(self.sensor.CreateImuStream(channel_id))
        elif stream_type == EStreamType.FeaturesTracking:
            if type(channel_id) == str:
                return FeaturesTrackingStream(self.sensor.CreateFeaturesTrackingStream(channel_id))
            return FeaturesTrackingStream(self.sensor.CreateFeaturesTrackingStream())
        elif stream_type == EStreamType.Histogram:
            return HistogramStream(self.sensor.CreateHistogramStream(channel_id))
        elif stream_type == EStreamType.Slam:
            if channel_id == -1:
                return StreamSlam(self.sensor.CreateSlamStream())
            return SlamStream(self.sensor.CreateSlamStream(channel_id))
        elif stream_type == EStreamType.Tracking:
            return ImageStream(self.sensor.CreateImageStream(2))
        # elif streamType is eUserDefine:
        elif stream_type == EStreamType.CnnApp:
            if channel_id == -1:
                return CnnAppStream(self.sensor.CreateCnnAppStream())
            return CnnAppStream(self.sensor.CreateCnnAppStream(channel_id))
        elif stream_type == EStreamType.PointCloud:
            if channel_id == -1:
                return PointCloudStream(self.sensor.CreatePointCloudStream())
            return PointCloudStream(self.sensor.CreatePointCloudStream(channel_id))
        elif stream_type == EStreamType.Injection:
            return InjectionStream(self.sensor.CreateInjectionStream(channel_id), self.sensor)
        return None

    def init(self, device_params: DeviceParamsExt = None, cnn_load_params: CnnLoadParams = None) -> HwInformation:
        # @brief    Service initialization.
        #
        # Invoked once before initialization of any other InuDev stream. After invoking Init method the Device is
        #   still in low power consumption. This function will provide a map with all available HW channels on which a
        #   client application can receive streams of frames.
        # @param    deviceParams    Initialized the Device with these input parameters. It will be set to all assembled
        #   cameras.
        # @param    cnnLoadParams   CNN network. The service will load the specified CNN network in parallel while
        #   InuSensor is initialized & started to reduce CNN loading time.
        # @return HwInformation     Developer should call the function with a CHwInformation
        # class and will receive the Device HW configuration.
        if device_params is None and cnn_load_params is None:
            self.sensor.Init(self.hwInformation)
        elif device_params is not None and cnn_load_params is None:
            self.sensor.Init(self.hwInformation, device_params)
        elif device_params is not None and cnn_load_params is not None:
            self.sensor.Init(self.hwInformation, device_params, cnn_load_params)
        return self.hwInformation

    def start(self, hw_information: HwInformation = None) -> tuple[MapUintPoint, HwInformation]:
        # @brief    Start acquisition of frames.
        #
        # Shall be invoked only after the service is successfully initialized and before any request
        # @param  hwInformation		Initialized the Device with these ChannelsParams per channel.
        # @return MapUintPoint      Image size that is provided by the Device [Width,Height] according to channelID.
        # @return HwInformation		Return real params with which the server works.
        channels_size = MapUintPoint()
        if hw_information is None:
            hwInformation = self.hwInformation
        self.sensor.Start(channels_size, self.hwInformation)
        return channels_size, self.hwInformation

    def terminate(self) -> None:
        # @brief    Service Termination.
        #
        # Shall be invoked when the service is no longer in use and after frames acquisition has stopped.
        self.sensor.Terminate()

    def stop(self) -> None:
        # @brief    Stop acquisition of frames.
        #
        # Shall be invoked after requests for frames are no longer sent and before service termination
        # (only if Start() was invoked).
        self.sensor.Stop()

    def connect(self) -> None:
        # @brief    Try to connect to Inuitive Sensor.
        #
        # Communicate with InuService and try to connect to Inuitive Sensor.
        self.sensor.Connect()

    def disconnect(self) -> None:
        # @brief    Try to disconnect from Inuitive Sensor.
        #
        # Stop Communicate to InuService.
        self.sensor.Disconnect()

    @property
    def connection_state(self) -> None:
        # @brief    Get the connection state of the sensor.
        #
        # @return EConnectionState
        return self.sensor.ConnectionState

    @property
    def sensor_state(self) -> None:
        # @brief  Get the Sensor state.
        #
        # @return ESensorState
        return self.sensor.State

    def get_sensor_temperature(self, type: InuSensor.ETemperatureType) -> float:
        # @brief    Get the Sensor Temperature.
        #
        # @param    type  Temperature sensor type.
        # @return   Temperature    returns the temperature in Celsius .
        return self.sensor.GetSensorTemperature(type)

    # @register.setter
    def register(self, callback) -> None:
        # @brief    Registration for receiving InuSensor state notifications (push).
        #
        # The provided callback function is called only when the Device state is changed.
        # @param callback function which is invoked whenever the sensor state is changed.
        self.sensor.Register(callback)

    register = property(None, register)

    def reset(self) -> None:
        # @brief	SW reset of InuSensor, it resets both SW and HW.
        #
        self.sensor.Reset()

    @property
    def version(self):  # ->MapEntitiesIDVersion:
        # @brief     Get information about the SW and HW components.
        #
        # @return    Version description of each component.
        version = self.sensor.Version
        if len(version) == 0:
            return None
        else:
            return version

    @property
    def sensors_control_params(self):  # ->MapSensorControlParams:
        # @brief    Get Sensor Control (AGC) data.
        #
        # It should be called only if after any related stream (e.g. StereoImage, Webcam, etc.) was initiated.
        # An empty map should be provided, in case the map is not empty the service will clear the map.
        # @return MapSensorControlParams   Will return with the sensor's control params per sensor.
        control_params = self.sensor.SensorsControlParams
        if len(control_params) == 0:
            return None
        else:
            return control_params

    def get_sensor_control_params(self, sensor_id: int) -> SensorControlParams:
        # @brief    Get Sensor Control (AGC) data.
        #
        # It should be called only if after any related stream (e.g. StereoImage, Webcam, etc.) was initiated.
        # An empty map should be provided, in case the map is not empty the service will clear the map.
        # @param  sensorId                  Specify the requested projector type by default - ePatterns.
        # @return SensorsControlParams      Will return with the sensor's control params per sensor.
        return self.sensor.GetSensorControlParams(sensor_id)

    def set_sensor_control_params(self, sensor_id: int, params: SensorControlParams) -> None:
        # @brief    Set Sensor Control (AGC) data.
        #
        # It should be called only if after any related stream (e.g. StereoImage, Webcam, etc.) was initiated.
        # Sets Device control params for specific sensor.
        # @param    sensorId        The sensor id.
        # @param    params          New Sensor Control parameters.
        self.sensor.SetSensorControlParams(sensor_id, params)

    def get_auto_exposure_params(self, sensor_id: int,
                projectorType: InuSensor.EProjectors = InuSensor.EProjectors.ProjectorPatterns) -> AutoExposureParams:
        # @brief    Get Sensor Control Auto Exposure data.
        #
        # It should be called only if after any related stream (e.g. StereoImage, Webcam, etc.) was initiated.
        # Gets Auto Exposure params for specific sensor.
        # @param[in] sensorId           The sensor id.
        # @param[in] projectorType      Specify the requested projector type by default - ePatterns.
        # @return AutoExposureParams    Auto Exposure parameters.
        params = AutoExposureParams()
        self.sensor.GetAutoExposureParams(params, sensor_id, projectorType)
        return params

    def set_auto_exposure_params(self, auto_exposure_params: AutoExposureParams, sensor_id: int,
                                 projector_type: InuSensor.EProjectors = InuSensor.EProjectors.ProjectorPatterns):
        # @brief    Set Sensor Control Auto Exposure configuration.
        #
        # It should be called only if after any related stream (e.g. StereoImage, Webcam, etc.) was initiated.
        # Sets Auto Exposure params for specific sensor.
        # @param autoExposureParams         New Auto Exposure parameters.
        # @param sensorId                   The sensor id.
        # @param ProjectorType              Specify the requested projector type by default - ePatterns.
        self.sensor.SetAutoExposureParams(auto_exposure_params, sensor_id, projector_type)

    def load_registers_configuration_file(self, file_name: str):
        # @brief    Load Registers from input file.
        #
        # It should be called only if after the Device was initiated.
        # The file format should be provided by Inuitive technical staff.
        # @param    fileName    Input file name provided by Inuitive.
        return self.sensor.LoadRegistersConfigurationFile(file_name)

    def get_calibration_data(self, temperature: int = -1, channel_id: int = -1) -> CalibrationData:
        # @brief		Get Calibration data information.
        #
        # @param    temperature         Optical data of which temperature, in case of default the optical data of
        #   active calibration is returned.
        # @param    channelID           Channel ID. @return   InuError  If
        # InuSensor isn't initialized then StateError is returned. @return   CalibrationData     Output optical data
        # information.
        data = CalibrationData()
        if temperature == -1:
            self.sensor.GetCalibrationData(data, channel_id)
        else:
            self.sensor.GetCalibrationData(data, channel_id, temperature)
        return data

    def set_projector_level(self, level: InuSensor.EProjectorLevel, projectorID: InuSensor.EProjectors) -> None:
        # @brief		Set one of the assembled projectors' state
        #
        # @param  level         High - high power, Low low power, Off - projector off.
        # @param  projectorID   Projector name, eNumOfProjectors is illegal value.
        # @return   InuError    Error code, OK if operation successfully completed.
        self.sensor.SetProjectorLevel(level, projectorID)

    def get_projector_level(self, projectorID: InuSensor.EProjectors) -> InuSensor.EProjectorLevel:
        # @brief		Get one of the assembled projectors' state.
        #
        # @param   EProjectors          Projector name, eNumOfProjectors is illegal value.
        # @return  EProjectorLevel      High - high power, Low low power, Off - projector off.
        return self.sensor.GetProjectorLevel(projectorID)

    def record(self, destination_directory: str, templateName: str = '') -> None:
        # @brief Record Device streams
        #
        # @param  destinationDirectory  Destination directory for recording output. Send empty string to stop recording.
        # @param  templateName          String which will be concatenate to output file name.
        self.sensor.Record(destination_directory, templateName)

    def snapshot(self, destination_directory: str, templateName: str = '') -> None:
        # @brief Record Device streams
        #
        # @param[in]    destinationDirectory  Destination directory for recording output. Send empty string to stop
        #       recording.
        # @param[in]    templateName          String which will be concatenated to output file name.
        self.sensor.Snapshot(destination_directory, templateName)

    def load_cnn_networks(self, load_params: CnnLoadParams) -> None:
        # @brief    Load network from input file name.
        #
        # @param    loadParams    Loaded network parameters.
        self.sensor.LoadCnnNetworks(load_params)

    def release_cnn_networks(self) -> None:
        # @brief   Release all previously loaded CNN networks.
        #
        return self.sensor.ReleaseCnnNetworks()

    @property
    def device_time(self) -> int:
        # @brief    GetDeviceTime
        #
        # Should be called only after the Device had initiated. @return  The value generally represents the number of
        #   seconds since 00:00 hours, Jan 1, 1970 UTC (i.e., the current unix timestamp).
        return self.sensor.DeviceTime

    def set_channel_cropping(self, channel_id: int, crop_params: CropParams) -> None:
        # @brief    SetChannelCropping
        #
        # Set channel as "croppable" & define the cropping rectangle size and position.
        # The position of the rectangle can be moved in runtime by calling the stream's API SetCroppingROI
        # @param channelId
        # @param CropParams     Defines the size of the cropped rectangle and its position
        self.sensor.SetChannelCropping(channel_id, crop_params)

    def set_channel_dimensions(self, channel_id: int, channel_dimensions: ChannelDimensions) -> None:
        # @brief    SetChannelDimensions
        #
        # Enables to change channel dimensions (not all channels supports this operation).
        # Should be called only after the sensor had started.
        # @param    channelID           The id of the output channel on which the scaling operation will affect.
        # @param    channelDimensions   The dimension of the actual data inside the output image after scaling.
        self.sensor.SetChannelDimensions(channel_id, channel_dimensions)

    def set_sensor_histograms_roi(self, histograms_roi: VectorROIParams, sensor_id: int) -> None:
        # @brief    Set Sensor Histograms ROI (AGC) data.
        #
        # It should be called only after the Device was started.
        # Sets the sensor's histogram's ROIs.
        # Each sensor has 3 histograms the first histogram in the vector will be used for Automatic Sensor Control
        # At least one ROI should be provided
        # @param histogramsROI      Vector of histograms.
        # @param sensor_id           The sensor id.
        self.sensor.SetSensorHistogramsROI(histograms_roi, sensor_id)

    @property
    def alternate_projector_mode(self) -> AlternateProjectorMode:
        # @brief    AlternateProjectorMode getter
        #
        # Get specific API for projector toggle
        # @return AlternateProjectorMode
        return self.sensor.AlternateProjectorMode

    @alternate_projector_mode.setter
    def alternate_projector_mode(self, value: AlternateProjectorMode) -> None:
        # @brief    AlternateProjectorMode setter
        #
        # Specific API for projector toggle Should be called after the sensor had started, and before the IR/DEPTH
        # channel is started after the sensor had started. value	AlternateProjectorMode
        self.sensor.AlternateProjectorMode = value

    def calibrate_imu(self, csv_path: str = '', yml_path: str = '') -> None:
        # @brief    CalibrateImu
        #
        # Runs the process of IMU calibration based on recorded IMU data and updates configuration accordingly @param
        # csvPath	    Path for the file with the recorded IMU data. If not provided the file will be searched and
        # taken from the last recording directory. @param ymlPath	    Path for the file with the IMU calibration. if
        # not provided the file will be taken from the connected sensor The calculated bias values will be saved to
        # the provided YML if provided, if not it will be saved to the calibration directory
        self.sensor.CalibrateImu(csv_path, yml_path)

    def start_node(self, nodeName: str) -> None:
        # @brief    StartNode
        #
        # Starts a HW Node
        # @param                Node name
        self.sensor.StartNode()

    def stop_node(self, nodeName: str) -> None:
        # @brief    StopNode
        #
        # Stops a HW Node
        # @param nodeName           Node name
        # @return CInuError    Error code, OK if operation successfully completed.
        self.sensor.StopNode()

    def set_inject_resolution(self, streamer_name: str, channel_size: Point2D) -> None:
        # @brief    SetInjectResolution
        #
        # @Should be called only after the sensor had initialized and before it was started.
        # @param streamerName The Streamer Name on which the write operation will affect.
        # @param channelSize The size of the actual data inside the input image after writing.
        # @return InuError    Error code, EErrorCode.OK if operation successfully completed.
        self.sensor.SetInjectResolution(streamer_name, channel_size)
