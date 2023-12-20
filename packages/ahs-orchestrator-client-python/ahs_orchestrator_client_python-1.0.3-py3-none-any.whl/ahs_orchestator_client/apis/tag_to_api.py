import typing
import typing_extensions

from ahs_orchestator_client.apis.tags.default_api import DefaultApi
from ahs_orchestator_client.apis.tags.cas_firmware_api import CasFirmwareApi
from ahs_orchestator_client.apis.tags.corrective_actions_api import CorrectiveActionsApi
from ahs_orchestator_client.apis.tags.device_locations_api import DeviceLocationsApi
from ahs_orchestator_client.apis.tags.health_api import HealthApi
from ahs_orchestator_client.apis.tags.health_checks_api import HealthChecksApi
from ahs_orchestator_client.apis.tags.health_check_sequences_api import HealthCheckSequencesApi
from ahs_orchestator_client.apis.tags.jenkins_api import JenkinsApi
from ahs_orchestator_client.apis.tags.metric_api import MetricApi
from ahs_orchestator_client.apis.tags.testbed_api import TestbedApi

TagToApi = typing.TypedDict(
    'TagToApi',
    {
        "default": typing.Type[DefaultApi],
        "Cas Firmware": typing.Type[CasFirmwareApi],
        "Corrective Actions": typing.Type[CorrectiveActionsApi],
        "Device Locations": typing.Type[DeviceLocationsApi],
        "Health": typing.Type[HealthApi],
        "Health Checks": typing.Type[HealthChecksApi],
        "Health Check Sequences": typing.Type[HealthCheckSequencesApi],
        "Jenkins": typing.Type[JenkinsApi],
        "Metric": typing.Type[MetricApi],
        "Testbed": typing.Type[TestbedApi],
    }
)

tag_to_api = TagToApi(
    {
        "default": DefaultApi,
        "Cas Firmware": CasFirmwareApi,
        "Corrective Actions": CorrectiveActionsApi,
        "Device Locations": DeviceLocationsApi,
        "Health": HealthApi,
        "Health Checks": HealthChecksApi,
        "Health Check Sequences": HealthCheckSequencesApi,
        "Jenkins": JenkinsApi,
        "Metric": MetricApi,
        "Testbed": TestbedApi,
    }
)
