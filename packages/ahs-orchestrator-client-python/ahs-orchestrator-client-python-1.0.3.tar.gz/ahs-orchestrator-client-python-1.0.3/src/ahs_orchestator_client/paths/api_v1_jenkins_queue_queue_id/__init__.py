# do not import all endpoints into this module because that uses a lot of memory and stack frames
# if you need the ability to import all endpoints from this module, import them with
# from ahs_orchestator_client.apis.paths.api_v1_jenkins_queue_queue_id import ApiV1JenkinsQueueQueueId

path = "/api/v1/jenkins/queue/{queue_id}"