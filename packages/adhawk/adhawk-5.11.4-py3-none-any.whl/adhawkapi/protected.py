'''This module provides a set of APIs to manipulate protected attributes in TROS'''

import contextlib
import logging
import typing

from . import base, blob_parsers, defaults, product_defs, publicapi, publicapiproxy, register_api, registers
from .version import SemanticVersion


class PersonalizeApi(register_api.RegisterApi):
    '''Provides a protected API to program device specific attributes'''

    def set_multidevice_config(self, device_count, num_trackers, ocular_mode=None):
        '''Sets the number of trackers controlled over the same port'''
        logging.info(f'set_multitracker_config({device_count})')

        if ocular_mode is not None:
            active_eyes, active_trackers = self._get_active_eyes_and_trackers(ocular_mode)
            firmware_info = self.firmware_info._replace(
                num_devices=device_count, dev_id_offset=0, num_trackers=num_trackers,
                active_eyes=tuple(active_eyes), active_trackers=tuple(active_trackers))
        else:
            firmware_info = self.firmware_info._replace(
                num_devices=device_count, dev_id_offset=0, num_trackers=num_trackers)

        self._openports[self.portname] = (self._com, firmware_info)
        self._request(base.GENERAL_BANK, 1, int(device_count | (num_trackers << 16)),
                      control=True, timeout=3)

    def set_autotune_blob(self, autotune_offsets):
        '''Set the autotune offsets blob for a given product'''
        frontend_proxy_api = publicapiproxy.PublicApiProxy(self._portname)
        blob_data = blob_parsers.create_blob(publicapi.BlobType.AUTOTUNE,
                                             publicapi.BlobVersion.AUTOTUNE.value,
                                             None,
                                             autotune_offsets)
        err = frontend_proxy_api.write_blob(publicapi.BlobType.AUTOTUNE, blob_data)
        publicapi.check_result(err, 'Failed to write autotune blob')

    def set_fusion_blob(self, fusion_consts):
        '''Set the dynamic fusion offsets blob for a given product'''
        frontend_proxy_api = publicapiproxy.PublicApiProxy(self._portname)
        blob_data = blob_parsers.create_blob(publicapi.BlobType.DYNAMIC_FUSION,
                                             publicapi.BlobVersion.DYNAMIC_FUSION.value,
                                             None,
                                             fusion_consts)
        err = frontend_proxy_api.write_blob(publicapi.BlobType.DYNAMIC_FUSION, blob_data)
        publicapi.check_result(err, 'Failed to write dynamic fusion blob')

    def set_model_et_blob(self, model_params):
        '''Set the model based et blob for a given product'''
        if SemanticVersion.compare(self.firmware_info.api_version, SemanticVersion(0, 35, 0)) < 0:
            logging.warning('This firmware version does not support model et blob')
            return
        frontend_proxy_api = publicapiproxy.PublicApiProxy(self._portname)
        blob_data = blob_parsers.create_blob(publicapi.BlobType.MODEL_ET,
                                             publicapi.BlobVersion.MODEL_ET.value,
                                             None,
                                             model_params)
        err = frontend_proxy_api.write_blob(publicapi.BlobType.MODEL_ET, blob_data)
        publicapi.check_result(err, 'Failed to write model based et blob')

    def set_model_priors_blob(self, model_params):
        '''Set the model priors blob for a given product'''
        if SemanticVersion.compare(self.firmware_info.api_version, SemanticVersion(0, 40, 0)) < 0:
            logging.warning('This firmware version does not support model priors blob')
            return
        frontend_proxy_api = publicapiproxy.PublicApiProxy(self._portname)
        blob_data = blob_parsers.create_blob(publicapi.BlobType.MODEL_PRIORS,
                                             publicapi.BlobVersion.MODEL_PRIORS.value,
                                             None,
                                             model_params)
        err = frontend_proxy_api.write_blob(publicapi.BlobType.MODEL_PRIORS, blob_data)
        publicapi.check_result(err, 'Failed to write model priors blob')

    def set_geometry_blob(self, geometry):
        '''Set the geometry blob for a given product'''
        if SemanticVersion.compare(self.firmware_info.api_version, SemanticVersion(0, 57, 0)) < 0:
            logging.warning('This firmware version does not support the geometry blob')
            return
        frontend_proxy_api = publicapiproxy.PublicApiProxy(self._portname)
        blob_data = blob_parsers.create_blob(publicapi.BlobType.GEOMETRY,
                                             publicapi.BlobVersion.GEOMETRY.value,
                                             None,
                                             geometry)
        err = frontend_proxy_api.write_blob(publicapi.BlobType.GEOMETRY, blob_data)
        publicapi.check_result(err, 'Failed to write geometry blob')


class PersonalizationSettings(typing.NamedTuple):
    '''Contains all the personalization settings for a device'''
    product_id: registers.SpecProductId
    serial_num: str
    ocular_mode: registers.SpecOcularMode


DEFAULT_DEAD_TIME = 100
# iris imaging defaults
DEFAULT_IRIS_CAPTURE_TIME = 50
DEFAULT_IRIS_SEGMENT_COUNT = 3
DEFAULT_IRIS_SAMPLE_COUNT = 6900
DEFAULT_IRIS_SAMPLE_RATE = 3000000
DEFAULT_IRIS_SAMPLE_PHASE = 140
DEFAULT_IRIS_IMAGE_WIDTH = 140
DEFAULT_IRIS_IMAGE_CORRECTION = registers.AnaloglissajousImageCorrectionType.COSINE
DEFAULT_IRIS_IMAGE_ALGORITHM = registers.AnaloglissajousImageGenerationAlgorithm.ONE_PIXEL_AVERAGING
DEFAULT_IRIS_IMAGE_POSTPROCESSING = registers.AnaloglissajousImagePostprocessing.AVERAGE
DEFAULT_IRIS_STARTUP_PERIOD = 50
DEFAULT_IRIS_NEGATIE_SLEW = -80
DEFAULT_IRIS_SATURATION_LIMIT_HIGH = 30
DEFAULT_IRIS_SATURATION_LIMIT_LOW = 80


class Personalizer:
    '''Helper class for personalizing hardware devices'''

    def __init__(self, portname):
        self._api = PersonalizeApi(portname)
        self._board_id = self._api.get_register(registers.ISP_BOARD_TYPE, control=True)
        serial_num = self._api.get_register(registers.SPEC_SERIAL_NUMBER, control=True)
        product_id = self._api.get_register(registers.SPEC_PRODUCT_ID, control=True)
        try:
            ocular_mode = registers.SpecOcularMode(
                self._api.get_register(registers.SPEC_OCULAR_MODE, control=True))
        except base.MinimumAPIVersion:
            ocular_mode = registers.SpecOcularMode.BINOCULAR

        self._settings = PersonalizationSettings(
            registers.SpecProductId(product_id), serial_num, ocular_mode)

    @property
    def api_version(self):
        '''Returns the firmware api version'''
        return self._api.firmware_info.api_version

    @property
    def supported_products(self):
        '''Returns the list of supported products for the current hardware'''
        return [(spec.DISPLAY_NAME, spec.PRODUCT_ID)
                for spec in product_defs.by_board(self._board_id)]

    @property
    def settings(self):
        '''Returns the current personalization settings from the hardware'''
        return self._settings

    def personalize(self, configs: PersonalizationSettings = None):
        # pylint: disable=too-many-locals
        # pylint: disable=too-many-statements
        # pylint: disable=too-many-branches
        '''Personalize the device according the provided info'''
        if configs is None:
            configs = self._settings

        spec = product_defs.by_id(self._board_id, configs.product_id)
        assert spec.BOARD_TYPE == self._board_id

        control_caps = list(spec.CONTROL_CAPS)
        num_trackers = len(spec.TRACKER_CAPS)
        num_devices = num_trackers + 1

        try:
            self._api.set_register(registers.SPEC_OCULAR_MODE, configs.ocular_mode, control=True)
        except base.MinimumAPIVersion:
            if configs.ocular_mode != registers.SpecOcularMode.BINOCULAR:
                raise base.MinimumAPIVersion('Monocular mode is not supported in this firmware. Please upgrade.')

        if configs.ocular_mode == registers.SpecOcularMode.BINOCULAR:
            # Single tracker optimization allows frequency tuning on monocular devices
            # Binocular devices personalized as monocular can have this capability set as well
            # If re-personalizing to binocular, remove the single tracker optimization capability
            with contextlib.suppress(ValueError):
                control_caps.remove(registers.SpecCapability.SINGLE_TRACKER_OPTIMIZATION)

        self._api.set_multidevice_config(num_devices, num_trackers, configs.ocular_mode)
        self._api.set_register(registers.SPEC_PRODUCT_ID, configs.product_id, control=True)
        self._api.set_register(registers.SPEC_PRODUCT_CATEGORY, spec.PRODUCT_CATEGORY, control=True)
        self._api.set_register(registers.SPEC_CAMERA, spec.CAMERA_TYPE, control=True)
        self._api.set_register(registers.SPEC_CAPABILITY, control_caps, control=True)
        self._api.set_register(registers.SPEC_SERIAL_NUMBER, configs.serial_num, control=True)

        self._api.set_register(registers.GENERAL2_FLUSH, 1, control=True)

        active_trackers = []
        for tracker_id in range(defaults.MAX_SCANNERS):
            if configs.ocular_mode.value & 1 << (tracker_id % defaults.MAX_EYES):
                active_trackers.append(tracker_id)

            self._api.set_tracker_id(tracker_id)
            self._api.set_register(registers.SPEC_CAPABILITY, spec.TRACKER_CAPS[tracker_id])
            pd_order_enc = 0
            for pd_id in reversed(spec.PD_ORDER[tracker_id]):
                pd_order_enc = (pd_order_enc << 4) + (pd_id & 0xf)
            pd_type_enc = 0
            for value in reversed(spec.PD_TYPE[tracker_id]):
                pd_type_enc = (pd_type_enc << 4) + (value & 0xf)
            self._api.set_register(registers.SPEC_PD_ORDER, pd_order_enc)
            with contextlib.suppress(base.MinimumAPIVersion):
                self._api.set_register(registers.SPEC_PD_TYPE, pd_type_enc)
            self._api.set_register(registers.SPEC_SCANNER_ORIENTATION, spec.SCANNER_ORIENTATION[tracker_id])
            self._api.set_register(registers.SPEC_X_MAX, defaults.DEFAULT_X_MAX)
            self._api.set_register(registers.SPEC_X_MIN, defaults.DEFAULT_X_MIN)
            self._api.set_register(registers.SPEC_Y_MAX, defaults.DEFAULT_Y_MAX)
            self._api.set_register(registers.SPEC_Y_MIN, defaults.DEFAULT_Y_MIN)
            self._api.set_register(registers.GENERAL1_DEAD_TIME_X, DEFAULT_DEAD_TIME)
            self._api.set_register(registers.GENERAL1_DEAD_TIME_Y, DEFAULT_DEAD_TIME)

            self._api.set_register(registers.SPEC_MAX_VCSEL_CURRENT, spec.MAX_LASER_CURRENT)
            laser_current = self._api.get_register(registers.GENERAL1_LASER_CURRENT)
            if laser_current > spec.MAX_LASER_CURRENT:
                self._api.set_register(registers.GENERAL1_LASER_CURRENT, spec.MAX_LASER_CURRENT)

            self._api.set_register(registers.SPEC_MAX_DUTY_CYCLE, spec.MAX_DUTY_CYCLE)
            duty_cycle = self._api.get_register(registers.GENERAL1_MODULATION_DUTY_CYCLE)
            if duty_cycle > spec.MAX_DUTY_CYCLE:
                self._api.set_register(registers.GENERAL1_MODULATION_DUTY_CYCLE, spec.MAX_DUTY_CYCLE)

            # set defaults for the productized iris imaging app
            with contextlib.suppress(base.MinimumAPIVersion):
                self._api.set_register(registers.ANALOGLISSAJOUS_CAPTURE_TIME, DEFAULT_IRIS_CAPTURE_TIME)
                self._api.set_register(registers.ANALOGLISSAJOUS_SEGMENT_COUNT, DEFAULT_IRIS_SEGMENT_COUNT)
                self._api.set_register(registers.ANALOGLISSAJOUS_SAMPLE_COUNT, DEFAULT_IRIS_SAMPLE_COUNT)
                self._api.set_register(registers.ANALOGLISSAJOUS_SAMPLE_RATE, DEFAULT_IRIS_SAMPLE_RATE)
                self._api.set_register(registers.ANALOGLISSAJOUS_SAMPLE_PHASE, DEFAULT_IRIS_SAMPLE_PHASE)
                self._api.set_register(registers.ANALOGLISSAJOUS_IMAGE_WIDTH, DEFAULT_IRIS_IMAGE_WIDTH)
                self._api.set_register(registers.ANALOGLISSAJOUS_IMAGE_CORRECTION_TYPE, DEFAULT_IRIS_IMAGE_CORRECTION)
                self._api.set_register(registers.ANALOGLISSAJOUS_IMAGE_GENERATION_ALGORITHM,
                                       DEFAULT_IRIS_IMAGE_ALGORITHM)
                self._api.set_register(registers.ANALOGLISSAJOUS_IMAGE_POSTPROCESSING,
                                       DEFAULT_IRIS_IMAGE_POSTPROCESSING)
                self._api.set_register(registers.ANALOGLISSAJOUS_STARTUP_PERIOD, DEFAULT_IRIS_STARTUP_PERIOD)
                self._api.set_register(registers.ANALOGLISSAJOUS_NEGATIVE_SLEW, DEFAULT_IRIS_NEGATIE_SLEW)
                self._api.set_register(registers.ANALOGLISSAJOUS_SATURATION_LIMIT_HIGH,
                                       DEFAULT_IRIS_SATURATION_LIMIT_HIGH)
                self._api.set_register(registers.ANALOGLISSAJOUS_SATURATION_LIMIT_LOW,
                                       DEFAULT_IRIS_SATURATION_LIMIT_LOW)

        self._api.set_register(registers.GENERAL2_FLUSH, 1, control=True)

        # Attempt to write each of the blob constants
        spec_blob_map = {
            'FUSION_CONSTS': self._api.set_fusion_blob,
            'MODEL_ET': self._api.set_model_et_blob,
            'MODEL_PRIORS': self._api.set_model_priors_blob,
            'GEOMETRY': self._api.set_geometry_blob,
        }

        for spec_key, blob_writer in spec_blob_map.items():
            spec_data = getattr(spec, spec_key)
            if spec_data is not None:
                try:
                    blob_writer(spec_data)
                except ValueError as exc:
                    logging.error(exc)

    def shutdown(self):
        '''Shutdown the personalizer API'''
        self._api.shutdown()
