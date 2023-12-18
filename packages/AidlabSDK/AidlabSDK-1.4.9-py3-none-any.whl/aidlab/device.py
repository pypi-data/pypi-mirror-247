"""
Created by Szymon Gesicki on 09.05.2020.
"""

import logging
import os
import sys
from ctypes import (CDLL, CFUNCTYPE, POINTER, Structure, c_bool, c_char,
                    c_char_p, c_float, c_int, c_uint8, c_uint16, c_uint32,
                    c_uint64, c_void_p, cdll)
from time import time
from typing import Dict, Tuple, Optional, List

from bleak import BleakClient
from bleak.backends.characteristic import BleakGATTCharacteristic
from bleak.backends.device import BLEDevice
from bleak.exc import BleakError
from packaging import version

from .body_position import BodyPosition
from .wear_state import WearState
from .data_type import DataType

# from .aidlab_delegate import AidlabDelegate

logger = logging.getLogger(__name__)

class AidlabSDKPointer(Structure):
    """AidlabSDK pointer"""

class Device:
    """
    The `Device` class is the main interface for interacting with an Aidlab or Aidmed One.

    This class provides methods for configuring the device and controlling its configuration. 

    It also stores basic information about the device, like its firmware version, serial number,
    hardware version, and MAC address.

    Attributes:
        firmware_revision (str): The firmware version of the device.
        hardware_revision (str): The hardware version of the device.
        serial_number (str): The serial number of the device.
        manufacture_name (str): The name of the manufacturer of the device.
        address (str): The MAC address of the device.
    """

    firmware_revision: str = ""
    hardware_revision: str = ""
    serial_number: str = ""
    manufacture_name: str = ""
    address: str = ""

    _aidlab_sdk_ptr = None

    _COMMAND_CHARACTERISTIC = "51366e80-cf3a-11e1-9ab4-0002a5d5c51b"

    sample_time_callback_type = CFUNCTYPE(None, c_void_p, c_uint64, c_float)
    samples_time_callback_type = CFUNCTYPE(None, c_void_p, c_uint64, POINTER(c_float), c_int)
    activity_callback_type = CFUNCTYPE(None, c_void_p, c_uint64, c_uint8)
    respiration_rate_callback_type = CFUNCTYPE(None, c_void_p, c_uint64, c_uint32)
    accelerometer_callback_type = CFUNCTYPE(None, c_void_p, c_uint64, c_float, c_float, c_float)
    gyroscope_callback_type = CFUNCTYPE(None, c_void_p, c_uint64, c_float, c_float, c_float)
    magnetometer_callback_type = CFUNCTYPE(None, c_void_p, c_uint64, c_float, c_float, c_float)
    battery_callback_type = CFUNCTYPE(None, c_void_p, c_uint8)
    steps_callback_type = CFUNCTYPE(None, c_void_p, c_uint64, c_uint64)
    orientation_callback_type = CFUNCTYPE(None, c_void_p, c_uint64, c_float, c_float, c_float)
    body_position_callback_type = CFUNCTYPE(None, c_void_p, c_uint64, c_uint8)
    quaternion_callback_type = CFUNCTYPE(
        None, c_void_p, c_uint64, c_float, c_float, c_float, c_float)
    wear_state_callback_type = CFUNCTYPE(None, c_void_p, c_uint8)
    heart_rate_callback_type = CFUNCTYPE(None, c_void_p, c_uint64, c_int)
    rr_callback_type = CFUNCTYPE(None, c_void_p, c_uint64, c_int)
    pressure_callback_type = CFUNCTYPE(None, c_void_p, c_uint64, POINTER(c_int), c_int)
    pressure_wear_state_callback_type = CFUNCTYPE(None, c_void_p, c_uint8)
    sound_volume_callback_type = CFUNCTYPE(None, c_void_p, c_uint64, c_uint16)
    exercise_callback_type = CFUNCTYPE(None, c_void_p, c_uint8)
    received_command_callback_type = CFUNCTYPE(None, c_void_p)
    sync_state_callback_type = CFUNCTYPE(None, c_void_p, c_uint8)
    unsynchronized_size_callback_type = CFUNCTYPE(None, c_void_p, c_uint16, c_float)
    received_message_type = CFUNCTYPE(None, c_void_p, POINTER(c_char), POINTER(c_char))
    user_event_callback_type = CFUNCTYPE(None, c_void_p, c_uint64)
    did_receive_error_callback_type = CFUNCTYPE(None, c_void_p, c_char_p)
    signal_quality_callback_type = CFUNCTYPE(None, c_void_p, c_uint64, c_int)

    Activity_type = {
        1: "automotive",
        2: "walking",
        4: "running",
        8: "cycling",
        16: "still",
        32: "still"
    }

    Exercise = {
        0: "pushUp",
        1: "jump",
        2: "sitUp",
        3: "burpee",
        4: "pullUp",
        5: "squat",
        6: "plankStart",
        7: "plankEnd"
    }

    Sync_state = {
        0: "start",
        1: "end",
        2: "stop",
        3: "empty"
    }

    ecgFiltrationMethod = {"normal": False, "aggressive": True}

    lib: CDLL

    _device: BLEDevice
    _client: BleakClient
    _uuid_function_map: Dict[Tuple[str, int], callable] = {} # type: ignore

    def __init__(self, device: BLEDevice):

        self._device = device

        self.address = device.address

        self.ecg_c_callback = self.samples_time_callback_type(
            self._ecg_callback)
        self.respiration_c_callback = self.samples_time_callback_type(
            self._respiration_callback)
        self.temperature_c_callback = self.sample_time_callback_type(
            self._temperature_callback)
        self.activity_c_callback = self.activity_callback_type(
            self._activity_callback)
        self.steps_c_callback = self.steps_callback_type(
            self._steps_callback)
        self.accelerometer_c_callback = self.accelerometer_callback_type(
            self._accelerometer_callback)
        self.gyroscope_c_callback = self.gyroscope_callback_type(
            self._gyroscope_callback)
        self.magnetometer_c_callback = self.magnetometer_callback_type(
            self._magnetometer_callback)
        self.quaternion_c_callback = self.quaternion_callback_type(
            self._quaternion_callback)
        self.orientation_c_callback = self.orientation_callback_type(
            self._orientation_callback)
        self.body_position_c_callback = self.body_position_callback_type(
            self._body_position_callback)
        self.heart_rate_c_callback = self.heart_rate_callback_type(
            self._heart_rate_callback)
        self.rr_c_callback = self.rr_callback_type(
            self._rr_callback)
        self.respiration_rate_c_callback = self.respiration_rate_callback_type(
            self._respiration_rate_callback)
        self.wear_state_c_callback = self.wear_state_callback_type(
            self._wear_state_did_change)
        self.sound_volume_c_callback = self.sound_volume_callback_type(
            self._sound_volume_callback)
        self.exercise_c_callback = self.exercise_callback_type(
            self._exercise_callback)
        self.receive_command_c_callback = self.received_command_callback_type(
            self._receive_command_callback)
        self.pressure_c_callback = self.pressure_callback_type(
            self._pressure_callback)
        self.pressure_wear_state_c_callback = self.pressure_wear_state_callback_type(
            self._pressure_wear_state_did_change)
        self.received_message_c_callback = self.received_message_type(
            self._received_message_callback)
        self.user_event_c_callback = self.user_event_callback_type(
            self._user_event_callback)
        self.did_receive_error_c_callback = self.did_receive_error_callback_type(
            self._did_receive_error_callback)
        self.battery_c_callback = self.battery_callback_type(
            self._battery_callback)
        self.signal_quality_c_callback = self.signal_quality_callback_type(
            self._signal_quality_callback)

        self.sync_state_c_callback = self.sync_state_callback_type(
            self._sync_state_did_change)
        self.unsynchronized_size_c_callback = self.unsynchronized_size_callback_type(
            self._did_receive_unsynchronized_size)
        self._past_ecg_c_callback = self.samples_time_callback_type(
            self._past_ecg_callback)
        self._past_respiration_c_callback = self.samples_time_callback_type(
            self._past_respiration_callback)
        self._past_temperature_c_callback = self.sample_time_callback_type(
            self._past_temperature_callback)
        self._past_activity_c_callback = self.activity_callback_type(
            self._past_activity_callback)
        self._past_steps_c_callback = self.steps_callback_type(
            self._past_steps_callback)
        self._past_accelerometer_c_callback = self.accelerometer_callback_type(
            self._past_accelerometer_callback)
        self._past_gyroscope_c_callback = self.gyroscope_callback_type(
            self._past_gyroscope_callback)
        self._past_magnetometer_c_callback = self.magnetometer_callback_type(
            self._past_magnetometer_callback)
        self._past_quaternion_c_callback = self.quaternion_callback_type(
            self._past_quaternion_callback)
        self._past_orientation_c_callback = self.orientation_callback_type(
            self._past_orientation_callback)
        self._past_body_position_c_callback = self.body_position_callback_type(
            self._past_body_position_callback)
        self._past_heart_rate_c_callback = self.heart_rate_callback_type(
            self._past_heart_rate_callback)
        self._past_rr_c_callback = self.rr_callback_type(
            self._past_rr_callback)
        self._past_respiration_rate_c_callback = self.respiration_rate_callback_type(
            self._past_respiration_rate_callback)
        self._past_sound_volume_c_callback = self.sound_volume_callback_type(
            self._past_sound_volume_callback)
        self._past_pressure_c_callback = self.pressure_callback_type(
            self._past_pressure_callback)
        self._past_user_event_c_callback = self.user_event_callback_type(
            self._past_user_event_callback)
        self._past_signal_quality_c_callback = self.signal_quality_callback_type(
            self._past_signal_quality_callback)

    async def connect(self, delegate, data_types: list[DataType], data_types_to_store: Optional[List[DataType]] = None):
        """
        Connects to the device.
        """
        self._delegate = delegate

        if data_types_to_store is None:
            data_types_to_store = []

        self._create()

        self._client = BleakClient(self._device, loop=self._did_disconnect)

        try:
            await self._client.connect(timeout=10)

            # Harvest Device Information
            self.firmware_revision = (await self._client.read_gatt_char("00002a26-0000-1000-8000-00805f9b34fb")).decode('ascii')
            self._set_firmware_revision(self.firmware_revision)

            self.hardware_revision = (await self._client.read_gatt_char("00002a27-0000-1000-8000-00805f9b34fb")).decode('ascii')
            self._set_hardware_revision(self.hardware_revision)

            self.manufacture_name = (await self._client.read_gatt_char("00002a29-0000-1000-8000-00805f9b34fb")).decode('ascii')
            self.serial_number = (await self._client.read_gatt_char("00002a25-0000-1000-8000-00805f9b34fb")).decode('ascii')

            self._delegate.did_connect(self)

            self._uuid_function_map = {
                self._uuid(DataType.ECG): self._calculate_ecg,
                self._uuid(DataType.RESPIRATION): self._calculate_respiration,
                self._uuid(DataType.SKIN_TEMPERATURE): self._calculate_temperature,
                self._uuid(DataType.MOTION): self._calculate_motion,
                self._uuid(DataType.BATTERY): self._calculate_battery,
                self._uuid(DataType.ACTIVITY): self._calculate_activity,
                self._uuid(DataType.ORIENTATION): self._calculate_orientation,
                self._uuid(DataType.STEPS): self._calculate_steps,
                self._uuid(DataType.HEART_RATE): self._calculate_heart_rate,
                self._uuid(DataType.SOUND_VOLUME): self._calculate_sound_volume,
                self._uuid(DataType.RR): self._calculate_heart_rate, # Same as HEART_RATE
                # PRESSURE = 12
            }

            for characteristic in self._converter_to_uuids(data_types):
                try:
                    await self._client.start_notify(characteristic, self._handle_notification)
                except BleakError as e:
                    logger.debug("%s (this might be due to compatibility with older aidlabs)", e)

            await self.set_time(time())

            if version.parse("3.6.0") < version.parse(self.firmware_revision):
                logger.debug("Version later than 3.6 start collect data")
                await self._start_collect_data(data_types, data_types_to_store)
            else:
                logger.debug("Version older than 3.6")

        except Exception as e:
            logger.error("Exception %s", e)

    async def disconnect(self):
        """
        Disconnect from the device.
        """
        await self._client.disconnect()

    async def start_synchronization(self):
        """Start sending data from internal memory."""
        await self.send("sync start")

    async def stop_synchronization(self):
        """Stop sending data from internal memory.
        """
        await self.send("sync stop")

    async def set_time(self, timestamp: float):
        """Sets the time on the device.
        """
        timestamp = int(timestamp)
        message = [b for b in timestamp.to_bytes(4, "little")]
        await self._client.write_gatt_char("00002a2b-0000-1000-8000-00805f9b34fb",
                                     bytearray(message), True)

    def set_ecg_filtration_method(self, method: str = "normal"):
        """
        Set ECG filtration method (e.g. to change LED brightness).
        
        This method provides you the flexibility to adjust the electrocardiogram (ECG) filtration to
        your specific needs. Depending on your specific use case, you might prefer a more aggressive
        filtration to reduce noise or a normal filtration to retain more details in the signal.
        """
        self.lib.setAggressiveECGFiltration(self.ecgFiltrationMethod.get(method, False),
                                            self._aidlab_sdk_ptr)

    async def send(self, command: str):
        """
        Sends a command to the device (e.g. to change LED brightness).
        """
        write_value = self._get_command(command)
        size = write_value[3] | (write_value[4] << 8)
        message = [write_value[i] for i in range(size)]
        await self._send(message, size)

    def _create(self):
        self.lib = self._load_aidlab_sdk()
        self.lib.initial.restype = POINTER(AidlabSDKPointer)
        self._aidlab_sdk_ptr = self.lib.initial()

        # Setting up type of variables and return values
        self._setup_process_types()

        self.lib.initUserServiceCallback(
            self.ecg_c_callback,
            self.respiration_c_callback,
            self.temperature_c_callback,
            self.accelerometer_c_callback,
            self.gyroscope_c_callback,
            self.magnetometer_c_callback,
            self.battery_c_callback,
            self.activity_c_callback,
            self.steps_c_callback,
            self.orientation_c_callback,
            self.quaternion_c_callback,
            self.respiration_rate_c_callback,
            self.wear_state_c_callback,
            self.heart_rate_c_callback,
            self.rr_c_callback,
            self.sound_volume_c_callback,
            self.exercise_c_callback,
            self.receive_command_c_callback,
            self.received_message_c_callback,
            self.user_event_c_callback,
            self.pressure_c_callback,
            self.pressure_wear_state_c_callback,
            self.body_position_c_callback,
            self.did_receive_error_c_callback,
            self.signal_quality_c_callback,
            self._aidlab_sdk_ptr)

        self.lib.initSynchronizationCallback(
            self.sync_state_c_callback,
            self.unsynchronized_size_c_callback,
            self._past_ecg_c_callback,
            self._past_respiration_c_callback,
            self._past_temperature_c_callback,
            self._past_heart_rate_c_callback,
            self._past_rr_c_callback,
            self._past_activity_c_callback,
            self._past_respiration_rate_c_callback,
            self._past_steps_c_callback,
            self._past_user_event_c_callback,
            self._past_sound_volume_c_callback,
            self._past_pressure_c_callback,
            self._past_accelerometer_c_callback,
            self._past_gyroscope_c_callback,
            self._past_quaternion_c_callback,
            self._past_orientation_c_callback,
            self._past_magnetometer_c_callback,
            self._past_body_position_c_callback,
            self._past_rr_c_callback,
            self._past_accelerometer_c_callback,
            self._aidlab_sdk_ptr)

    def _calculate_temperature(self, data):
        self.lib.processTemperaturePackage((c_uint8 * len(data))(*data),
                                           len(data), self._aidlab_sdk_ptr)

    def _calculate_respiration(self, data):
        self.lib.processRespirationPackage((
            c_uint8 * len(data))(*data), len(data), self._aidlab_sdk_ptr)

    def _calculate_ecg(self, data):
        self.lib.processECGPackage((c_uint8 * len(data))(*data), len(data), self._aidlab_sdk_ptr)

    def _calculate_battery(self, data):
        self.lib.processBatteryPackage((c_uint8 * len(data))(*data), len(data), self._aidlab_sdk_ptr)

    def _calculate_motion(self, data):
        self.lib.processMotionPackage((c_uint8 * len(data))(*data), len(data), self._aidlab_sdk_ptr)

    def _calculate_activity(self, data):
        self.lib.processActivityPackage((c_uint8 * len(data))(*data),
                                        len(data),
                                        self._aidlab_sdk_ptr)

    def _calculate_orientation(self, data):
        self.lib.processOrientationPackage(
            (c_uint8 * len(data))(*data),
            len(data),
            self._aidlab_sdk_ptr)

    def _calculate_steps(self, data):
        self.lib.processStepsPackage((c_uint8 * len(data))(*data),
                                     len(data), self._aidlab_sdk_ptr)

    def _calculate_heart_rate(self, data):
        self.lib.processHeartRatePackage((c_uint8 * len(data))(*data),
                                         len(data), self._aidlab_sdk_ptr)

    def _calculate_sound_volume(self, data):
        self.lib.processSoundVolumePackage(
            (c_uint8 * len(data))(*data), len(data), self._aidlab_sdk_ptr)

    def _did_receive_raw_cmd_value(self, data):
        """Calculate raw command data from raw data"""
        logger.debug("Received command: %s", str(data))
        self.lib.processCMD((c_uint8 * len(data))(*data), len(data), self._aidlab_sdk_ptr)

    def _set_firmware_revision(self, firmware_revision):
        """Set firmware revision"""""
        firmware_revision_utf8 = firmware_revision.encode('utf-8')

        # Create c_uint8 array from encoded string
        firmware_revision_array = (c_uint8 * len(firmware_revision))(*firmware_revision_utf8)

        self.lib.setFirmwareRevision(
            firmware_revision_array, len(firmware_revision), self._aidlab_sdk_ptr)

    def _set_hardware_revision(self, hardware_revision: str):
        data = (c_uint8 * len(hardware_revision))(*hardware_revision.encode('utf-8'))
        self.lib.setHardwareRevision(data, len(hardware_revision), self._aidlab_sdk_ptr)

    def _setup_process_types(self):

        self.lib.processECGPackage.argtypes = [POINTER(c_uint8), c_int, c_void_p]
        self.lib.processECGPackage.restype = None

        self.lib.processTemperaturePackage.argtypes = [POINTER(c_uint8), c_int, c_void_p]
        self.lib.processTemperaturePackage.restype = None

        self.lib.processMotionPackage.argtypes = [POINTER(c_uint8), c_int, c_void_p]
        self.lib.processMotionPackage.restype = None

        self.lib.processRespirationPackage.argtypes = [POINTER(c_uint8), c_int, c_void_p]
        self.lib.processRespirationPackage.restype = None

        self.lib.processBatteryPackage.argtypes = [ POINTER(c_uint8), c_int, c_void_p]
        self.lib.processBatteryPackage.restype = None

        self.lib.processActivityPackage.argtypes = [POINTER(c_uint8), c_int, c_void_p]
        self.lib.processActivityPackage.restype = None

        self.lib.processStepsPackage.argtypes = [POINTER(c_uint8), c_int, c_void_p]
        self.lib.processStepsPackage.restype = None

        self.lib.processOrientationPackage.argtypes = [POINTER(c_uint8), c_int, c_void_p]
        self.lib.processOrientationPackage.restype = None

        self.lib.processHeartRatePackage.argtypes = [POINTER(c_uint8), c_int, c_void_p]
        self.lib.processHeartRatePackage.restype = None

        self.lib.processCMD.argtypes = [POINTER(c_uint8), c_int, c_void_p]
        self.lib.processCMD.restype = None

        self.lib.setHardwareRevision.argtypes = [POINTER(c_uint8), c_int, c_void_p]
        self.lib.setHardwareRevision.restype = None

        self.lib.setFirmwareRevision.argtypes = [POINTER(c_uint8), c_int, c_void_p]
        self.lib.setFirmwareRevision.restype = None

        self.lib.setAggressiveECGFiltration.argtypes = [c_bool, c_void_p]
        self.lib.setAggressiveECGFiltration.restype = None

        self.lib.destroy.argtypes = [c_void_p]
        self.lib.destroy.restype = None

        self.lib.get_command.argtypes = [POINTER(c_uint8), c_void_p]
        self.lib.get_command.restype = POINTER(c_uint8)

        self.lib.get_collect_command.argtypes = [POINTER(c_uint8),
                                                 c_int,
                                                 POINTER(c_uint8),
                                                 c_int,
                                                 c_void_p]

        self.lib.get_collect_command.restype = POINTER(c_uint8)

    def _user_event_callback(self, _, timestamp):
        self._delegate.did_detect_user_event(self, timestamp)

    def _did_receive_error_callback(self, _, log_text):
        try:
            logger.error("[LIB] %s", log_text.decode("utf-8"))
        except UnicodeDecodeError:
            logger.error("[LIB] %s", str(log_text))

    def _exercise_callback(self, _, exercise):
        exercise = self.Exercise.get(exercise, "None")
        self._delegate.did_detect_exercise(self, exercise)

    def _ecg_callback(self, _, timestamp, values, size):
        values = [values[i] for i in range(size)]
        self._delegate.did_receive_ecg(self, timestamp, values)

    def _respiration_callback(self, _, timestamp, values, size):
        values = [values[i] for i in range(size)]
        self._delegate.did_receive_respiration(self, timestamp, values)

    def _battery_callback(self, _, state_of_charge):
        self._delegate.did_receive_battery_level(self, state_of_charge)

    def _temperature_callback(self, _, timestamp, value):
        self._delegate.did_receive_skin_temperature(self, timestamp, value)

    def _accelerometer_callback(self, _, timestamp, ax, ay, az):
        self._delegate.did_receive_accelerometer(self, timestamp, ax, ay, az)

    def _gyroscope_callback(self, _, timestamp, gx, gy, gz):
        self._delegate.did_receive_gyroscope(self, timestamp, gx, gy, gz)

    def _magnetometer_callback(self, _, timestamp, mx, my, mz):
        self._delegate.did_receive_magnetometer(self, timestamp, mx, my, mz)

    def _orientation_callback(self, _, timestamp, roll, pitch, yaw):
        self._delegate.did_receive_orientation(self, timestamp, roll, pitch, yaw)

    def _quaternion_callback(self, _, timestamp, qw, qx, qy, qz):
        self._delegate.did_receive_quaternion(self, timestamp, qw, qx, qy, qz)

    def _body_position_callback(self, _, timestamp, body_position: int):
        self._delegate.did_receive_body_position(self, timestamp, BodyPosition(body_position))

    def _activity_callback(self, _, timestamp, activity):
        activity = self.Activity_type.get(activity, "still")
        self._delegate.did_receive_activity(self, timestamp, activity)

    def _steps_callback(self, _, timestamp, value):
        self._delegate.did_receive_steps(self, timestamp, value)

    def _heart_rate_callback(self, _, timestamp, heart_rate):
        self._delegate.did_receive_heart_rate(self, timestamp, heart_rate)

    def _rr_callback(self, _, timestamp, rr):
        self._delegate.did_receive_rr(self, timestamp, rr)

    def _respiration_rate_callback(self, _, timestamp, value):
        self._delegate.did_receive_respiration_rate(self, timestamp, value)

    def _pressure_callback(self, _, timestamp, values, size):
        values = [values[i] for i in range(size)]
        self._delegate.did_receive_pressure(self, timestamp, values)

    def _pressure_wear_state_did_change(self, _, wear_state):
        self._delegate.pressure_wear_state_did_change(self, WearState(wear_state))

    def _wear_state_did_change(self, _, wear_state):
        self._delegate.wear_state_did_change(self, WearState(wear_state))

    def _sound_volume_callback(self, _, timestamp, sound_volume):
        self._delegate.did_receive_sound_volume(self, timestamp, sound_volume)

    def _receive_command_callback(self, _):
        self._delegate.did_receive_command(self)

    def _received_message_callback(self, context, process, message):
        pass

    def _signal_quality_callback(self, _, timestamp, value):
        self._delegate.did_receive_signal_quality(self, timestamp, value)

    # Synchronization

    def _past_user_event_callback(self, _, timestamp):
        self._delegate.did_receive_past_user_event(self, timestamp)

    def _past_ecg_callback(self, _, timestamp, values, size):
        values = [values[i] for i in range(size)]
        self._delegate.did_receive_past_ecg(self, timestamp, values)

    def _past_respiration_callback(self, _, timestamp, values, size):
        values = [values[i] for i in range(size)]
        self._delegate.did_receive_past_respiration(self, timestamp, values)

    def _past_temperature_callback(self, _, timestamp, value):
        self._delegate.did_receive_past_skin_temperature(self, timestamp, value)

    def _past_accelerometer_callback(self, _, timestamp, ax, ay, az):
        self._delegate.did_receive_past_accelerometer(self, timestamp, ax, ay, az)

    def _past_gyroscope_callback(self, _, timestamp, gx, gy, gz):
        self._delegate.did_receive_past_gyroscope(self, timestamp, gx, gy, gz)

    def _past_magnetometer_callback(self, _, timestamp, mx, my, mz):
        self._delegate.did_receive_past_magnetometer(self, timestamp, mx, my, mz)

    def _past_orientation_callback(self, _, timestamp, roll, pitch, yaw):
        self._delegate.did_receive_past_orientation(self, timestamp, roll, pitch, yaw)

    def _past_quaternion_callback(self, _, timestamp, qw, qx, qy, qz):
        self._delegate.did_receive_past_quaternion(self, timestamp, qw, qx, qy, qz)

    def _past_activity_callback(self, _, timestamp, activity):
        activity = self.Activity_type.get(activity, "still")
        self._delegate.did_receive_past_activity(self, timestamp, activity)

    def _past_body_position_callback(self, _, timestamp, body_position):
        self._delegate.did_receive_past_body_position(self, timestamp, BodyPosition(body_position))

    def _past_pressure_callback(self, _, timestamp, values, size):
        values = [values[i] for i in range(size)]
        self._delegate.did_receive_past_pressure(self, timestamp, values)

    def _past_steps_callback(self, _, timestamp, value):
        self._delegate.did_receive_past_steps(self, timestamp, value)

    def _past_heart_rate_callback(self, _, timestamp, heart_rate):
        self._delegate.did_receive_past_heart_rate(self, timestamp, heart_rate)

    def _past_rr_callback(self, _, timestamp, rr):
        self._delegate.did_receive_past_rr(self, timestamp, rr)

    def _past_respiration_rate_callback(self, _, timestamp, value):
        self._delegate.did_receive_past_respiration_rate(self, timestamp, value)

    def _past_sound_volume_callback(self, _, timestamp, sound_volume):
        self._delegate.did_receive_past_sound_volume(self, timestamp, sound_volume)

    def _past_signal_quality_callback(self, _, timestamp, value):
        self._delegate.did_receive_past_signal_quality(self, timestamp, value)

    def _sync_state_did_change(self, _, sync_state):
        sync_state = self.Sync_state.get(sync_state, "empty")
        self._delegate.sync_state_did_change(self, sync_state)

    def _did_receive_unsynchronized_size(self, _, unsynchronized_size, sync_bytes_per_second):
        self._delegate.did_receive_unsynchronized_size(self,
                                                       unsynchronized_size,
                                                       sync_bytes_per_second)

    def _uuid(self, data_type: DataType):
        orientation_handle: int = 58 if version.parse("3.0.0") < version.parse(self.firmware_revision) else 55
        motion_handle: int = 61 if version.parse("3.0.0") < version.parse(self.firmware_revision) else 58

        uuids: Dict[DataType, Tuple[str, int]]  = {
            DataType.ECG:              ("46366e80-cf3a-11e1-9ab4-0002a5d5c51b", 16),
            DataType.RESPIRATION:      ("48366e80-cf3a-11e1-9ab4-0002a5d5c51b", 19),
            DataType.SKIN_TEMPERATURE: ("45366e80-cf3a-11e1-9ab4-0002a5d5c51b", 25),
            DataType.BATTERY:          ("47366e80-cf3a-11e1-9ab4-0002a5d5c51b", 22),
            DataType.ACTIVITY:         ("61366e80-cf3a-11e1-9ab4-0002a5d5c51b", 49),
            DataType.STEPS:            ("62366e80-cf3a-11e1-9ab4-0002a5d5c51b", 52),
            DataType.SOUND_VOLUME:     ("52366e80-cf3a-11e1-9ab4-0002a5d5c51b", 31),
            DataType.HEART_RATE:       ("00002a37-0000-1000-8000-00805f9b34fb", 45),

            DataType.ORIENTATION:      ("63366e80-cf3a-11e1-9ab4-0002a5d5c51b", orientation_handle),
            DataType.MOTION:           ("49366e80-cf3a-11e1-9ab4-0002a5d5c51b", motion_handle),

            # Same as HEART_RATE
            DataType.RR:               ("00002a37-0000-1000-8000-00805f9b34fb", 45),
            # Same as ACTIVITY
            DataType.BODY_POSITION:    ("63366e80-cf3a-11e1-9ab4-0002a5d5c51b", orientation_handle),
        }

        if data_type in uuids:
            return uuids[data_type]

        raise ValueError("Invalid DataType: {}".format(data_type))

    def _load_aidlab_sdk(self):
        script_dir = os.path.dirname(os.path.abspath(__file__))

        if 'linux' in sys.platform:
            library_name = "aidlabsdk-linux-gnueabihf.so" if os.uname()[4][:3] == 'arm' else "aidlabsdk-linux-gnu.so"
        elif 'win32' in sys.platform:
            library_name = "aidlabsdk.dll"
            if sys.version_info >= (3, 8) and os.name == 'nt':
                os.add_dll_directory(os.path.join(script_dir, "libmingw64/"))
        elif 'darwin' in sys.platform:
            library_name = "aidlabsdk.dylib"
        else:
            raise RuntimeError("Unsupported operating system: {}".format(sys.platform))

        library_path = os.path.join(script_dir, library_name)
        return cdll.LoadLibrary(library_path)

    def _converter_to_uuids(self, signals: list[DataType]):
        # We always want to notify the command line
        out = [self._COMMAND_CHARACTERISTIC]

        for signal in signals:
            uuid = self._uuid(signal)
            if signal == DataType.BATTERY:
                # Also add standard GATT
                out.append("00002a19-0000-1000-8000-00805f9b34fb")
                out.append(uuid[0])
            elif signal == DataType.PRESSURE or signal == DataType.BODY_POSITION or signal == DataType.RESPIRATION_RATE:
                pass
            elif uuid:
                out.append(uuid[0])
            else:
                logging.error("DataType %s not supported", str(signal.value))
                self._delegate.did_disconnect(self)
                sys.exit()
        return out

    async def _start_collect_data(self,
                                  data_types: list[DataType],
                                  data_types_to_store: list[DataType]):
        write_value = self._get_collect_command(
            [signal.value for signal in data_types],
            [signal.value for signal in data_types_to_store]
        )
        size = write_value[3] | (write_value[4] << 8)
        message = [write_value[i] for i in range(size)]
        await self._send(message, size)

    async def _send(self, message, size: int):
        max_cmd_length: int = 20

        for i in range(round(int(size/max_cmd_length) + (size % max_cmd_length > 0))):
            message_byte = bytearray(message[i*max_cmd_length:(i+1)*max_cmd_length])
            logger.debug("Sending bytes: %s", str(message_byte))
            await self._client.write_gatt_char(self._COMMAND_CHARACTERISTIC,
                                         message_byte, True)

    def _get_command(self, message):
        data_array = (c_uint8 * (len(message)+1))(*message.encode('utf-8'))
        return self.lib.get_command(data_array, self._aidlab_sdk_ptr)

    def _get_collect_command(self, realtime, sync):
        data = (c_uint8 * len(realtime))(*realtime)
        return self.lib.get_collect_command(data,
                                            len(realtime),
                                            (c_uint8 * len(sync))(*sync),
                                            len(sync),
                                            self._aidlab_sdk_ptr)

    def _handle_notification(self, sender: BleakGATTCharacteristic, data: bytearray):
        for (uuid, handle), func in self._uuid_function_map.items():
            if sender.handle == handle or sender.uuid.upper() == uuid.upper():
                func(data)
                return

        if sender.handle == 13 or sender.uuid == self._COMMAND_CHARACTERISTIC.upper():
            self._did_receive_raw_cmd_value(data)

    def _did_disconnect(self, _: BleakClient):
        self.lib.destroy(self._aidlab_sdk_ptr)
        self._delegate.did_disconnect(self)
