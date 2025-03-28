from typing import List, Optional, Dict, Any, Union, Literal
from pydantic import BaseModel, Field, validator, root_validator

from uptime_kuma_api import MonitorType


class KafkaSaslOptions(BaseModel):
    mechanism: Optional[Literal["None", "plain", "scram-sha-256", "scram-sha-512", "aws"]] = "None"
    username: Optional[str] = None
    password: Optional[str] = None
    authorizationIdentity: Optional[str] = None
    accessKeyId: Optional[str] = None
    secretAccessKey: Optional[str] = None
    sessionToken: Optional[str] = None


class Monitor(BaseModel):
    id: int
    type: MonitorType
    name: str
    parent: Optional[int] = None
    description: Optional[str] = None
    interval: int = 60
    retryInterval: int = 60
    resendInterval: int = 0
    maxretries: int = 1
    upsideDown: bool = False
    notificationIDList: Optional[List] = None

    # HTTP KEYWORD
    url: Optional[str] = None
    expiryNotification: bool = False
    ignoreTls: bool = False
    maxredirects: int = 10
    accepted_statuscodes: Optional[List] = None
    proxyId: Optional[int] = None
    method: str = "GET"
    httpBodyEncoding: str = "json"
    body: Optional[str] = None
    headers: Optional[str] = None
    authMethod: Optional[str] = ""
    tlsCert: Optional[str] = None
    tlsKey: Optional[str] = None
    tlsCa: Optional[str] = None
    basic_auth_user: Optional[str] = None
    basic_auth_pass: Optional[str] = None
    authDomain: Optional[str] = None
    authWorkstation: Optional[str] = None

    # OAUTH
    oauth_auth_method: Optional[str] = "client_secret_basic"
    oauth_token_url: Optional[str] = None
    oauth_client_id: Optional[str] = None
    oauth_client_secret: Optional[str] = None
    oauth_scopes: Optional[str] = None

    timeout: int = 48
    keyword: Optional[str] = None
    invertKeyword: bool = False
    hostname: Optional[str] = None
    packetSize: int = 56
    # Changed to Optional[int] to accept None values
    port: Optional[int] = 53

    # DNS
    dns_resolve_server: str = "1.1.1.1"
    dns_resolve_type: str = "A"

    # MQTT
    mqttUsername: Optional[str] = None
    mqttPassword: Optional[str] = None
    mqttTopic: Optional[str] = None
    mqttSuccessMessage: Optional[str] = None

    # SQLSERVER POSTGRES
    databaseConnectionString: Optional[str] = None
    databaseQuery: Optional[str] = None

    # DOCKER
    docker_container: str = ""
    docker_host: Optional[int] = None

    # RADIUS
    radiusUsername: Optional[str] = None
    radiusPassword: Optional[str] = None
    radiusSecret: Optional[str] = None
    radiusCalledStationId: Optional[str] = None
    radiusCallingStationId: Optional[str] = None

    # GAME
    game: Optional[str] = None
    gamedigGivenPortOnly: bool = False

    jsonPath: Optional[str] = None
    expectedValue: Optional[str] = None

    # KAFKA
    kafkaProducerBrokers: Optional[str] = None
    kafkaProducerTopic: Optional[str] = None
    kafkaProducerMessage: Optional[str] = None
    kafkaProducerSsl: bool = False
    kafkaProducerAllowAutoTopicCreation: bool = False
    kafkaProducerSaslOptions: Optional[KafkaSaslOptions] = None

    @validator('kafkaProducerBrokers', 'kafkaProducerTopic', 'kafkaProducerMessage', pre=True)
    def ensure_string_type(cls, v):
        if v is None:
            return None
        return str(v)

    @root_validator(pre=True)
    def check_auth_method(cls, values):
        if 'authMethod' in values and values['authMethod'] == "":
            values['authMethod'] = None
        return values

    @validator('authMethod')
    def validate_auth_method(cls, v):
        valid_values = ["", "basic", "ntlm", "mtls", "oauth2-cc", None]
        if v not in valid_values:
            raise ValueError(f"authMethod must be one of {valid_values}")
        return v

    class Config:
        use_enum_values = True
        extra = "ignore"  # Ignore extra fields to handle unexpected input


class MonitorUpdate(Monitor):
    type: Optional[MonitorType] = None
    name: Optional[str] = None


class MonitorTag(BaseModel):
    tag_id: int
    value: Optional[str] = ""


class MonitorsResponse(BaseModel):
    monitors: List[Monitor]

class MonitorDashboardResponse(BaseModel):
    monitor: Dict[str, Any]
    avgResponseTime: Any
    uptimes: Dict[str, Any]
    cert: Any
    heartbeats: Any = None

class MonitorActionResponse(BaseModel):
    __root__: Dict[str, Any]
