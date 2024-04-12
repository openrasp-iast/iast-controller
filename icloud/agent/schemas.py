from ninja import Schema


class RaspSchema(Schema):
    id: str = None
    version: str = None
    hostname: str = None
    register_ip: str = None
    language: str = None
    language_version: str = None
    server_type: str = None
    server_version: str = None
    heartbeat_interval: int = None
    rasp_home: str = None
    host_type: str = None
    environ: dict = None


class Report(Schema):
    rasp_id: str = None
    time: int = None
    request_sum: int = None


class Heartbeat(Schema):
    rasp_id: str = None
    plugin_md5: str = None
    plugin_version: str = None
    config_time: int = None
    hostname: str = None


class Error(Schema):
    errors: list = None


class Policy(Schema):
    policies: list = None


class Dependency(Schema):
    product: str = None
    version: str = None
    vendor: str = None
    path: str = None
    source: str = None


class Dependencies(Schema):
    dependency: list[Dependency] = None
