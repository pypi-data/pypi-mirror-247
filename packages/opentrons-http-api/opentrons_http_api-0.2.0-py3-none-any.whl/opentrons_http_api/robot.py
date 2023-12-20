from typing import Dict, List, Tuple, BinaryIO, Optional, Sequence
from dataclasses import dataclass
from enum import Enum

from opentrons_http_api.api import API






@dataclass(frozen=True)
class SettingInfo:
    id: str
    old_id: str
    title: str
    description: str
    restart_required: bool
    value: bool

    @staticmethod
    def from_dict(d: dict) -> 'SettingInfo':
        return SettingInfo(**d)


@dataclass(frozen=True)
class HealthInfo:
    name: str
    robot_model: str
    api_version: str
    fw_version: str
    board_revision: str
    logs: List[str]
    system_version: str
    maximum_protocol_api_version: List[int]
    minimum_protocol_api_version: List[int]
    robot_serial: str
    links: Dict[str, str]

    @staticmethod
    def from_dict(d: Dict) -> 'HealthInfo':
        return HealthInfo(**d)


@dataclass(frozen=True)
class ProtocolInfo:
    id: str
    createdAt: str
    files: List[Dict]
    protocolType: str
    robotType: str
    metadata: Dict
    analyses: List
    analysisSummaries: List[Dict]

    @staticmethod
    def from_dict(d: dict) -> 'ProtocolInfo':
        return ProtocolInfo(**d)



class Robot:
    def __init__(self, host: str = 'localhost'):
        self._api = API(host)

    def identify(self, seconds: int) -> None:
        self._api.post_identify(seconds)

    def lights(self) -> bool:
        return self._api.get_robot_lights()['on']

    def set_lights(self, on: bool) -> None:
        self._api.post_robot_lights(on)

    def settings(self) -> Tuple[SettingInfo, ...]:
        response = self._api.get_settings()
        return tuple(SettingInfo.from_dict(d)
                     for d in response.json()['settings'])

    def set_setting(self, id_: SettingId, value: bool) -> None:
        self._api.post_settings(id_.value, value)

    def robot_settings(self) -> Dict:
        response = self._api.get_robot_settings()
        return response.json()

    def calibration_status(self) -> Dict:
        response = self._api.get_calibration_status()
        return response.json()

    def health(self) -> HealthInfo:
        info = self._api.get_health()
        return HealthInfo.from_dict(info)

    def get_all_runs(self):
        return self._api.get_runs().json()


    def create_run(self, protocol_id: str, labware_offsets: Optional[Sequence[dict]] = None) -> ...:
        return self._api.post_runs(protocol_id, labware_offsets)

    def control_run(self, run_id: str, action: ActionType) -> None:

        self._api.post_runs_run_id_actions(run_id, data)

    def upload_protocol(self, protocol_file: BinaryIO,
                        labware_definitions: Optional[Sequence[BinaryIO]] = None) -> ProtocolInfo:
        """
        Upload a protocol with optional labware definitions to the robot.
        :param protocol_file: A Python or JSON protocol binary file object.
        :param labware_definitions: An optional sequence of JSON labware definition binary file objects, only if the
        protocol_file is in Python format.
        :return: ProtocolInfo object containing information about the protocol.
        """
        response = self._api.post_protocols(files)
        return ProtocolInfo.from_dict(response.json()['data'])
