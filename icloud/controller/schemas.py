from ninja import Schema


class AppSchema(Schema):
    app_id: str = None
    app_name: str = None
    app_language: str = None
    app_description: str = None


class AppFilterSchema(Schema):
    app_id: str = None
    app_name: str = None
    page: int = None
    perpage: int = None


class PluginFilterSchema(Schema):
    app_id: str = None
    plugin_id: str = None
    plugin_name: str = None
    page: int = None
    perpage: int = None


class DependencyFilterSchema(Schema):
    app_id: str = None
    keyword: str = None
    page: int = None
    perpage: int = None


class RaspFilterSchema(Schema):
    app_id: str = None
    keyword: str = None
    page: int = None
    perpage: int = None


class PluginSchema(Schema):
    plugin_id: str
    fuzz_server: str = None
    request_timeout: int = None
    byhost_regex: str = None


class VulnFilterSchema(Schema):
    vuln_id: str = None
    app_id: str = None
    keyword: str = None
    plugin_name: str = None
    page: int = None
    perpage: int = None


class SettingSchema(Schema):
    cloud_backend_url: str = None


class SettingFilterSchema(Schema):
    name_start_with: str = None
