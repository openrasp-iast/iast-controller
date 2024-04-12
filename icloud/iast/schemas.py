from ninja import Schema


class TargetFilterSchema(Schema):
    app_id: str = None
    page: int = 1
    perpage: int = 10
    host: str = None
    port: int = None
    scanner_id: int = None
    url_only: bool = None
