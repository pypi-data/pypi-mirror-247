import typing
import typing_extensions

from ahs_orchestator_client.apis.paths.solidus import Solidus
from ahs_orchestator_client.apis.paths.api_v1_casfirmware import ApiV1Casfirmware
from ahs_orchestator_client.apis.paths.api_v1_correctiveactions_testbed_build_number_status import ApiV1CorrectiveactionsTestbedBuildNumberStatus
from ahs_orchestator_client.apis.paths.api_v1_correctiveactions_testbed_testbed_id import ApiV1CorrectiveactionsTestbedTestbedId
from ahs_orchestator_client.apis.paths.api_v1_correctiveactions_testbed_testbed_id_run import ApiV1CorrectiveactionsTestbedTestbedIdRun
from ahs_orchestator_client.apis.paths.api_v1_device_device_id_location import ApiV1DeviceDeviceIdLocation
from ahs_orchestator_client.apis.paths.api_v1_health import ApiV1Health
from ahs_orchestator_client.apis.paths.api_v1_health_env import ApiV1HealthEnv
from ahs_orchestator_client.apis.paths.api_v1_healthchecks_testbed_build_build_number_status import ApiV1HealthchecksTestbedBuildBuildNumberStatus
from ahs_orchestator_client.apis.paths.api_v1_healthchecks_testbed_testbed_id_run import ApiV1HealthchecksTestbedTestbedIdRun
from ahs_orchestator_client.apis.paths.api_v1_healthcheks import ApiV1Healthcheks
from ahs_orchestator_client.apis.paths.api_v1_healthcheks_health_check_id import ApiV1HealthcheksHealthCheckId
from ahs_orchestator_client.apis.paths.api_v1_healthchekssequence import ApiV1Healthchekssequence
from ahs_orchestator_client.apis.paths.api_v1_healthchekssequence_health_check_definition_id import ApiV1HealthchekssequenceHealthCheckDefinitionId
from ahs_orchestator_client.apis.paths.api_v1_jenkins_build_trigger import ApiV1JenkinsBuildTrigger
from ahs_orchestator_client.apis.paths.api_v1_jenkins_build_build_number_status import ApiV1JenkinsBuildBuildNumberStatus
from ahs_orchestator_client.apis.paths.api_v1_jenkins_jobs import ApiV1JenkinsJobs
from ahs_orchestator_client.apis.paths.api_v1_jenkins_queue_queue_id import ApiV1JenkinsQueueQueueId
from ahs_orchestator_client.apis.paths.api_v1_metric import ApiV1Metric
from ahs_orchestator_client.apis.paths.api_v1_metric_metric_testbed_testbed_id import ApiV1MetricMetricTestbedTestbedId
from ahs_orchestator_client.apis.paths.api_v1_testbed import ApiV1Testbed
from ahs_orchestator_client.apis.paths.api_v1_testbed_details import ApiV1TestbedDetails
from ahs_orchestator_client.apis.paths.api_v1_testbed_status import ApiV1TestbedStatus
from ahs_orchestator_client.apis.paths.api_v1_testbed_testbed_id import ApiV1TestbedTestbedId

PathToApi = typing.TypedDict(
    'PathToApi',
    {
    "/": typing.Type[Solidus],
    "/api/v1/casfirmware": typing.Type[ApiV1Casfirmware],
    "/api/v1/correctiveactions/testbed/{build_number}/status": typing.Type[ApiV1CorrectiveactionsTestbedBuildNumberStatus],
    "/api/v1/correctiveactions/testbed/{testbed_id}": typing.Type[ApiV1CorrectiveactionsTestbedTestbedId],
    "/api/v1/correctiveactions/testbed/{testbed_id}/run": typing.Type[ApiV1CorrectiveactionsTestbedTestbedIdRun],
    "/api/v1/device/{device_id}/location": typing.Type[ApiV1DeviceDeviceIdLocation],
    "/api/v1/health": typing.Type[ApiV1Health],
    "/api/v1/health/env": typing.Type[ApiV1HealthEnv],
    "/api/v1/healthchecks/testbed/build/{build_number}/status": typing.Type[ApiV1HealthchecksTestbedBuildBuildNumberStatus],
    "/api/v1/healthchecks/testbed/{testbed_id}/run": typing.Type[ApiV1HealthchecksTestbedTestbedIdRun],
    "/api/v1/healthcheks": typing.Type[ApiV1Healthcheks],
    "/api/v1/healthcheks/{health_check_id}": typing.Type[ApiV1HealthcheksHealthCheckId],
    "/api/v1/healthchekssequence": typing.Type[ApiV1Healthchekssequence],
    "/api/v1/healthchekssequence/{health_check_definition_id}": typing.Type[ApiV1HealthchekssequenceHealthCheckDefinitionId],
    "/api/v1/jenkins/build/trigger": typing.Type[ApiV1JenkinsBuildTrigger],
    "/api/v1/jenkins/build/{build_number}/status": typing.Type[ApiV1JenkinsBuildBuildNumberStatus],
    "/api/v1/jenkins/jobs": typing.Type[ApiV1JenkinsJobs],
    "/api/v1/jenkins/queue/{queue_id}": typing.Type[ApiV1JenkinsQueueQueueId],
    "/api/v1/metric": typing.Type[ApiV1Metric],
    "/api/v1/metric/{metric}/testbed/{testbed_id}": typing.Type[ApiV1MetricMetricTestbedTestbedId],
    "/api/v1/testbed": typing.Type[ApiV1Testbed],
    "/api/v1/testbed/details": typing.Type[ApiV1TestbedDetails],
    "/api/v1/testbed/status": typing.Type[ApiV1TestbedStatus],
    "/api/v1/testbed/{testbed_id}": typing.Type[ApiV1TestbedTestbedId],
    }
)

path_to_api = PathToApi(
    {
    "/": Solidus,
    "/api/v1/casfirmware": ApiV1Casfirmware,
    "/api/v1/correctiveactions/testbed/{build_number}/status": ApiV1CorrectiveactionsTestbedBuildNumberStatus,
    "/api/v1/correctiveactions/testbed/{testbed_id}": ApiV1CorrectiveactionsTestbedTestbedId,
    "/api/v1/correctiveactions/testbed/{testbed_id}/run": ApiV1CorrectiveactionsTestbedTestbedIdRun,
    "/api/v1/device/{device_id}/location": ApiV1DeviceDeviceIdLocation,
    "/api/v1/health": ApiV1Health,
    "/api/v1/health/env": ApiV1HealthEnv,
    "/api/v1/healthchecks/testbed/build/{build_number}/status": ApiV1HealthchecksTestbedBuildBuildNumberStatus,
    "/api/v1/healthchecks/testbed/{testbed_id}/run": ApiV1HealthchecksTestbedTestbedIdRun,
    "/api/v1/healthcheks": ApiV1Healthcheks,
    "/api/v1/healthcheks/{health_check_id}": ApiV1HealthcheksHealthCheckId,
    "/api/v1/healthchekssequence": ApiV1Healthchekssequence,
    "/api/v1/healthchekssequence/{health_check_definition_id}": ApiV1HealthchekssequenceHealthCheckDefinitionId,
    "/api/v1/jenkins/build/trigger": ApiV1JenkinsBuildTrigger,
    "/api/v1/jenkins/build/{build_number}/status": ApiV1JenkinsBuildBuildNumberStatus,
    "/api/v1/jenkins/jobs": ApiV1JenkinsJobs,
    "/api/v1/jenkins/queue/{queue_id}": ApiV1JenkinsQueueQueueId,
    "/api/v1/metric": ApiV1Metric,
    "/api/v1/metric/{metric}/testbed/{testbed_id}": ApiV1MetricMetricTestbedTestbedId,
    "/api/v1/testbed": ApiV1Testbed,
    "/api/v1/testbed/details": ApiV1TestbedDetails,
    "/api/v1/testbed/status": ApiV1TestbedStatus,
    "/api/v1/testbed/{testbed_id}": ApiV1TestbedTestbedId,
    }
)
