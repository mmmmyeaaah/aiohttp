import json

from aiohttp import web


class ApiError(web.HTTPException):

    def __init__(self, status_code: int, message: str | dict | list, *args, **kwargs):
        self.status_code = status_code
        self.message = message
        super().__init__(*args, **kwargs, text=json.dumps({'error': self.message}), content_type='application/json')
