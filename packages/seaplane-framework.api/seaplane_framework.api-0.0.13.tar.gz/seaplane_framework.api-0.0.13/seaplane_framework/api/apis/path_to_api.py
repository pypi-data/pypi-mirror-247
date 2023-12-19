import typing_extensions

from seaplane_framework.api.paths import PathValues
from seaplane_framework.api.apis.paths.stream import Stream
from seaplane_framework.api.apis.paths.stream_stream_name import StreamStreamName
from seaplane_framework.api.apis.paths.flow import Flow
from seaplane_framework.api.apis.paths.flow_flow_name import FlowFlowName
from seaplane_framework.api.apis.paths.flow_flow_name_status import FlowFlowNameStatus
from seaplane_framework.api.apis.paths.flow_flow_name_events import FlowFlowNameEvents
from seaplane_framework.api.apis.paths.flow_flow_name_secrets import FlowFlowNameSecrets
from seaplane_framework.api.apis.paths.flow_flow_name_secrets_secret_name import FlowFlowNameSecretsSecretName
from seaplane_framework.api.apis.paths.object import Object
from seaplane_framework.api.apis.paths.object_bucket_name import ObjectBucketName
from seaplane_framework.api.apis.paths.object_bucket_name_list import ObjectBucketNameList
from seaplane_framework.api.apis.paths.object_bucket_name_store import ObjectBucketNameStore
from seaplane_framework.api.apis.paths.endpoints_endpoint_request import EndpointsEndpointRequest
from seaplane_framework.api.apis.paths.endpoints_endpoint_response_message_id import EndpointsEndpointResponseMessageId
from seaplane_framework.api.apis.paths.endpoints_endpoint_response_message_id_archive import EndpointsEndpointResponseMessageIdArchive
from seaplane_framework.api.apis.paths.kv import Kv
from seaplane_framework.api.apis.paths.kv_kv_store import KvKvStore
from seaplane_framework.api.apis.paths.kv_kv_store_key import KvKvStoreKey
from seaplane_framework.api.apis.paths.kv_kv_store_key_key import KvKvStoreKeyKey
from seaplane_framework.api.apis.paths.webhook_provider_division import WebhookProviderDivision

PathToApi = typing_extensions.TypedDict(
    'PathToApi',
    {
        PathValues.STREAM: Stream,
        PathValues.STREAM_STREAM_NAME: StreamStreamName,
        PathValues.FLOW: Flow,
        PathValues.FLOW_FLOW_NAME: FlowFlowName,
        PathValues.FLOW_FLOW_NAME_STATUS: FlowFlowNameStatus,
        PathValues.FLOW_FLOW_NAME_EVENTS: FlowFlowNameEvents,
        PathValues.FLOW_FLOW_NAME_SECRETS: FlowFlowNameSecrets,
        PathValues.FLOW_FLOW_NAME_SECRETS_SECRET_NAME: FlowFlowNameSecretsSecretName,
        PathValues.OBJECT: Object,
        PathValues.OBJECT_BUCKET_NAME: ObjectBucketName,
        PathValues.OBJECT_BUCKET_NAME_LIST: ObjectBucketNameList,
        PathValues.OBJECT_BUCKET_NAME_STORE: ObjectBucketNameStore,
        PathValues.ENDPOINTS_ENDPOINT_REQUEST: EndpointsEndpointRequest,
        PathValues.ENDPOINTS_ENDPOINT_RESPONSE_MESSAGE_ID: EndpointsEndpointResponseMessageId,
        PathValues.ENDPOINTS_ENDPOINT_RESPONSE_MESSAGE_ID_ARCHIVE: EndpointsEndpointResponseMessageIdArchive,
        PathValues.KV: Kv,
        PathValues.KV_KV_STORE: KvKvStore,
        PathValues.KV_KV_STORE_KEY: KvKvStoreKey,
        PathValues.KV_KV_STORE_KEY_KEY: KvKvStoreKeyKey,
        PathValues.WEBHOOK_PROVIDER_DIVISION: WebhookProviderDivision,
    }
)

path_to_api = PathToApi(
    {
        PathValues.STREAM: Stream,
        PathValues.STREAM_STREAM_NAME: StreamStreamName,
        PathValues.FLOW: Flow,
        PathValues.FLOW_FLOW_NAME: FlowFlowName,
        PathValues.FLOW_FLOW_NAME_STATUS: FlowFlowNameStatus,
        PathValues.FLOW_FLOW_NAME_EVENTS: FlowFlowNameEvents,
        PathValues.FLOW_FLOW_NAME_SECRETS: FlowFlowNameSecrets,
        PathValues.FLOW_FLOW_NAME_SECRETS_SECRET_NAME: FlowFlowNameSecretsSecretName,
        PathValues.OBJECT: Object,
        PathValues.OBJECT_BUCKET_NAME: ObjectBucketName,
        PathValues.OBJECT_BUCKET_NAME_LIST: ObjectBucketNameList,
        PathValues.OBJECT_BUCKET_NAME_STORE: ObjectBucketNameStore,
        PathValues.ENDPOINTS_ENDPOINT_REQUEST: EndpointsEndpointRequest,
        PathValues.ENDPOINTS_ENDPOINT_RESPONSE_MESSAGE_ID: EndpointsEndpointResponseMessageId,
        PathValues.ENDPOINTS_ENDPOINT_RESPONSE_MESSAGE_ID_ARCHIVE: EndpointsEndpointResponseMessageIdArchive,
        PathValues.KV: Kv,
        PathValues.KV_KV_STORE: KvKvStore,
        PathValues.KV_KV_STORE_KEY: KvKvStoreKey,
        PathValues.KV_KV_STORE_KEY_KEY: KvKvStoreKeyKey,
        PathValues.WEBHOOK_PROVIDER_DIVISION: WebhookProviderDivision,
    }
)
