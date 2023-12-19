from InuStreamsPyth import DisparityParams, TemporalFilterParams, OutlierRemoveParams, HoleFillFilterParams, \
    StaticTemporalFilterParams, BlobFilterParams, Point2D

# class DisparityParams:
#     """! DepthProperties class.
#         Role: Controls DepthProperties .
#     """
#
#     def __init__(self):
#     """! The DepthProperties class initializer.
#         @return  An instance of the DisparityParams object.
#     """
#
#     @property
#     def confidence_threshold_region1(self) -> int:
#         # @brief    All pixels in the Region 1 area with lower confidence value should be set to invalid, should be
#         #   used in Host disparity2depth algorithm.
#         #
#         # @return confidence_threshold_region1 as int
#
#     @confidence_threshold_region1.setter
#     def confidence_threshold_region1(self, value: int) -> None:
#         # @brief    confidence_threshold_region1 setter
#
#     @property
#     def confidence_threshold_region2(self) -> int:
#         # @brief    All pixels in the Region 2 area with lower conf value should be set to invalid, should be used
#         #     in Host disparity2depth algorithm.  If  ConfidenceStartRegion2 == ConfidenceEndRegion2 == 0 than this
#         #     values will not be used in Host disparity2depth algorithm.
#         #
#         # @return confidence_threshold_region2 as int
#
#     @confidence_threshold_region2.setter
#     def confidence_threshold_region2(self, value: int) -> None:
#         # @brief    confidence_threshold_region2 setter
#
#     @property
#     def max_distance(self) -> int:
#         # @brief    Maximum depth in mm, depth above this value will be invalidated.
#         #
#         # @return max_distance as int
#
#     @max_distance.setter
#         def max_distance(self, value: int) -> None:
#         # @brief    max_distance setter
#
#     @property
#     def depth_scale(self) -> int:
#         # @brief    Depth scaling factor, 1.0f is to get depth in mm (default).
#         #
#         # @return depth_scale as int
#
#     @depth_scale.setter
#     def depth_scale(self, value: int) -> None:
#         # @brief    depth_scale setter
#
#     @property
#     def point_cloud_scale(self) -> int:
#         # @brief    Point cloud scaling factor, 0.001f is to get point cloud in meters (default).
#         #
#         # @return point_cloud_scale as int
#
#     @point_cloud_scale.setter
#         def point_cloud_scale(self, value: int) -> None:
#         # @brief    point_cloud_scale setter


# class TemporalFilterParams:
#     """! TemporalFilterParams class.
#         Role: Controls TemporalFilterParams .
#     """
#
#     def __init__(self):
#     """! The TemporalFilterParams class initializer.
#         @return  An instance of the TemporalFilterParams object.
#     """
#
#     @property
#     def stable_threshold(self) -> int:
#         # @brief   Temporal Filter stable threshold .
#         #
#         # @return stable_threshold as int
#
#     @stable_threshold.setter
#         def stable_threshold(self, value: int) -> None:
#         # @brief    stable_threshold setter
#
#     @property
#     def rapid_threshold(self) -> int:
#         # @brief   Temporal Filter rapid threshold .
#         #
#         # @return rapid_threshold as int
#
#     @rapid_threshold.setter
#         def rapid_threshold(self, value: int) -> None:
#         # @brief    rapid_threshold setter


# class OutlierRemoveParams:
#     """! OutlierRemoveParams class.
#         Role: Controls OutlierRemoveParams .
#     """
#
#     def __init__(self):
#     """! The OutlierRemoveParams class initializer.
#         @return  An instance of the OutlierRemoveParams object.
#     """
#
#     @property
#     def max_percent(self) -> int:
#         # @brief   OutlierRemove Filter max percent.
#         #
#         # @return max_percent as int
#
#     @max_percent.setter
#         def max_percent(self, value: int) -> None:
#         # @brief    max_percent setter
#
#     @property
#         def min_dist(self) -> int:
#         # @brief   Filter min dist.
#         #
#         # @return min_dist as int
#
#     @min_dist.setter
#     def min_dist(self, value: int) -> None:
#         # @brief    min_dist setter


# class HoleFillFilterParams:
#     """! HoleFillFilterParams class.
#         Role: Controls HoleFillFilterParams .
#     """
#
#     def __init__(self):
#     """! The HoleFillFilterParams class initializer.
#         @return  An instance of the HoleFillFilterParams object.
#     """
#
#     @property
#     def max_radius(self) -> int:
#         # @brief   Hole Fill Max Radius.
#         #
#         # @return max_radius as int
#
#     @max_percent.setter
#         def max_radius(self, value: int) -> None:
#         # @brief    max_radius setter

# class StaticTemporalFilterParams:
#     """! StaticTemporalFilterParams class.
#         Role: Controls StaticTemporalFilterParams .
#     """
#
#     def __init__(self):
#     """! The StaticTemporalFilterParams class initializer.
#         @return  An instance of the StaticTemporalFilterParams object.
#     """
#
#     @property
#     def filter_length(self) -> int:
#         # @brief   Static Temporal Filter BAll.
#         #
#         # @return filter_length as int.
#
#     @filter_length.setter
#         def filter_length(self, value: int) -> None:
#         # @brief    filter_length setter.
#
#     @property
#         def ball(self) -> int:
#         # @brief   Static Temporal Filter Length.
#         #
#         # @return ball as int.
#
#     @ball.setter
#         def filter_length(self, value: int) -> None:
#         # @brief    ball setter.
#
#     @property
#         def thread_num(self) -> int:
#         # @brief  Static Temporal Filter Num Thread.
#         #
#         # @return thread_num as int.
#
#     @thread_num.setter
#         def thread_num(self, value: int) -> None:
#         # @brief    thread_num setter.

# class BlobFilterParams:
#     """! BlobFilterParams class.
#         Role: Controls BlobFilterParams .
#     """
#
#     def __init__(self):
#     """! The BlobFilterParams class initializer.
#         @return  An instance of the BlobFilterParams object.
#     """
#     @property
#     def blob_mode(self) -> int:
#         # @ Blob algorithm mode : 2 - Blob1, 3 - Blob2, 4 - Blob 1 + 2
#         # @ Blob mode 2 –remove small patches
#         # @ Blob mode 3 – fill small patches
#         # @ Blob mode 4 – both mode 2 and mode 3
#         # @return blob_mode as int.
#
#     @blob_mode.setter
#     def blob_mode(self, value: int) -> None:
#         # @brief    blob_mode setter.
#
#     @property
#      def blob_max_size(self) -> int:
#         # @ Maximum number of pixels which be considered as Blob.
#         # @ Less than this number will be a candidate to filtering, larger than this value will be not a candidate
#         #   to be blob for filtering.
#
#     @blob_max_size.setter
#     def blob_max_size(self, value: int) -> None:
#         # @brief    blob_max_size setter.
#
#     @property
#     def blob_max_height(self) -> int:
#         # @ The maximum number of rows which be considered as Blob.
#         # @ Less than this number will be a candidate to filtering, larger than this value will be not a candidate
#         #   to be blob for filtering.
#
#     @blob_max_height.setter
#     def blob_max_height(self, value: int) -> None:
#         # @brief    blob_max_height setter.
#
#     @property
#     def blob_disparity_threshold(self) -> int:
#         # @ Blob algorithm : disparity threshold, will be executed as pre - process
#
#     @blob_disparity_threshold.setter
#     def blob_disparity_threshold(self, value: int) -> None:
#         # @brief    blob_disparity_threshold setter.
#
#     @property
#     def blob_max_height(self) -> int:
#         # @This parameter represents the max difference for pixels disparity to be considered as the same Blob.
#         # @As this parameter is bigger more pixels will labeled as the same blob.
#
#     @blob_max_height.setter
#     def blob_max_height(self, value: int) -> None:
#         # @brief    blob_max_height setter.


class DepthProperties:
    """! Interface for DepthProperties.

    Role: Controls DepthProperties .

    Responsibilities:
    """

    # @brief    InuStreamsPyth.DepthStream or InuStreamsPyth.ImageStream.
    #
    depth_properties = None

    def __init__(self, stream):
        self.depthProperties = stream
        """! The DepthProperties class initializer.
            @param stream  The InuStreamsPyth.DepthStream or InuStreamsPyth.ImageStream.
            @return  An instance of the DepthProperties initialized with the specified stream object.
        """

    @property
    def disparity_params(self) -> DisparityParams:
        # @brief disparity_params getter
        #
        # @Detailed description:        Get current DisparityParams
        # @return                       The Disparity Params
        return self.depth_properties.DisparityParams

    @disparity_params.setter
    def disparity_params(self, value: DisparityParams) -> None:
        # @brief    disparity_params setter
        #
        # @Detailed description:    Send the TemporalFilterParams to temporal filter.
        #                           By default, is set from InuServiceParams.xml
        # @param[in] value	        New DisparityParams
        self.depth_properties.DisparityParams = value

    @property
    def temporal_filter_params(self) -> TemporalFilterParams:
        # @brief temporal_filter_params getter
        #
        # @Detailed description:        Get current TemporalFilterParams.
        # @return                       The current Temporal Filter Params
        return self.depth_properties.TemporalFilterParams

    @temporal_filter_params.setter
    def temporal_filter_params(self, value: TemporalFilterParams) -> None:
        # @brief    temporal_filter_params setter
        #
        # @Detailed description:    Send the TemporalFilterParams to temporal filter.
        #                           By default, it is set from InuServiceParams.xml
        # @param[in]   value	    New DisparityParams
        self.depth_properties.TemporalFilterParams = value

    @property
    def outlier_remove_params(self) -> OutlierRemoveParams:
        # @brief outlier_remove_params getter
        #
        # @Detailed description:        Get current OutlierRemoveParams.
        # @return                       The current OutlierRemoveParams
        return self.depth_properties.OutlierRemoveParams

    @outlier_remove_params.setter
    def outlier_remove_params(self, value: OutlierRemoveParams) -> None:
        # @brief    outlier_remove_params setter
        #
        # @Detailed description:    Send the OutlierRemoveParams to temporal filter.
        #                           By default, it is set from InuServiceParams.xml
        # @param[in]   value	    New OutlierRemoveParams
        self.depth_properties.OutlierRemoveParams = value

    @property
    def hole_fill_params(self) -> HoleFillFilterParams:
        # @brief hole_fill_params getter
        #
        # @Detailed description:        Get current HoleFillParams.
        # @return                       The current HoleFillParams
        return self.depth_properties.HoleFillParams

    @hole_fill_params.setter
    def hole_fill_params(self, value: HoleFillFilterParams) -> None:
        # @brief    hole_fill_params setter
        #
        # @Detailed description:    Send the HoleFillParams to temporal filter.
        #                           By default, it is set from InuServiceParams.xml
        # @param[in]   value	    New HoleFillParams
        self.depth_properties.HoleFillParams = value

    @property
    def static_temporal_filter_params(self) -> StaticTemporalFilterParams:
        # @brief static_temporal_filter_params getter
        #
        # @Detailed description:        Get current StaticTemporalFilterParams.
        # @return                       The current StaticTemporalFilterParams
        return self.depth_properties.StaticTemporalFilterParams

    @static_temporal_filter_params.setter
    def static_temporal_filter_params(self, value: StaticTemporalFilterParams) -> None:
        # @brief    static_temporal_filter_params setter
        #
        # @Detailed description:    Send the StaticTemporalFilterParams to temporal filter.
        #                           By default, it is set from InuServiceParams.xml
        # @param[in]   value	    New StaticTemporalFilterParams
        self.depth_properties.StaticTemporalFilterParams = value

    @property
    def blob_filter_params(self) -> BlobFilterParams:
        # @brief blob_filter_params getter
        #
        # @Detailed description:        Get current BlobFilterParams.
        # @return                       The current BlobFilterParams
        return self.depth_properties.BlobFilterParams

    @blob_filter_params.setter
    def blob_filter_params(self, value: BlobFilterParams) -> None:
        # @brief    blob_filter_params setter
        #
        # @Detailed description:    Send the BlobFilterParams to temporal filter.
        #                           By default, it is set from InuServiceParams.xml
        # @param[in]   value	    New BlobFilterParams
        self.depth_properties.BlobFilterParams = value


# class Point2D:
#     """! Point2D class.
#         Role: Controls Point2D  .
#     """
#
#     def __init__(self):
#     def __init__(self, x: int, y: int):
#     """! The Point2D class initializer.
#         @return  An instance of the Point2D object.
#     """
#     @property
#     def x(self) -> int:
#         # @ x
#
#     @x.setter
#     def x(self, value: int) -> None:
#         # @brief    x setter.
#
#     @property
#     def y(self) -> int:
#         # @ y
#
#     @y.setter
#     def y(self, value: int) -> None:
#         # @brief    y setter.

class CroppingROI:
    """! Interface for CroppingROI.

    Role: Controls CroppingROI .

    Responsibilities:
    """

    # @brief    InuStreamsPyth.DepthStream or InuStreamsPyth.ImageStream.
    #
    cropping_roi = None

    def __init__(self, stream):
        self.cropping = stream
        """! The DepthProperties class initializer.
            @param stream  The InuStreamsPyth.DepthStream or InuStreamsPyth.ImageStream.
            @return  An instance of the DepthProperties initialized with the specified stream object.
        """

    def cropping_roi(self, start: Point2D) -> None:
        # @brief    Moves the cropping region of interest in runtime
        #
        # Enables to move the region of interest rectangle that was set using the InuSensor::SetChannelCropping
        # before starting the device. In case InuSensor.SetChannelCropping wasn't called the operation will fail.
        # Moving the rectangle outside the bookbinderies of the viewable area will cause the image to freeze. @param
        # start:     The position in Point2D of the upper left corner of the rectangle
        self.cropping.SetCroppingROI(start.x, start.y)

    cropping_roi = property(None, cropping_roi)
