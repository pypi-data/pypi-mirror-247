import json
import requests
from pydantic import BaseModel
from typing import Optional, Union


class Endpoint(BaseModel):
    uri: str
    parser: Optional[BaseModel] = None
    detail: Optional[str] = None

    def get(self, data: dict) -> Union[dict, BaseModel]:
        response = requests.get(self.uri, json=data).json()
        if isinstance(response, str):
            response = json.loads(response)
        if self.parser is None:
            return response
        else:
            return self.parser.model_validate(response)

    def post(self, data: dict) -> Union[dict, BaseModel]:
        response = requests.post(self.uri, json=data).json()
        if isinstance(response, str):
            response = json.loads(response)
        if self.parser is None:
            return response
        else:
            return self.parser.model_validate(response)


root: str = "https://api.cephalon.io"

# * account endpoints

account: str = f"{root}/account"
account_register: Endpoint = Endpoint(uri=f"{account}/register")
account_confirm: Endpoint = Endpoint(uri=f"{account}/confirm")
account_login: Endpoint = Endpoint(uri=f"{account}/login")
account_info: Endpoint = Endpoint(uri=f"{account}/info")
account_access: Endpoint = Endpoint(uri=f"{account}/access")
account_enable: Endpoint = Endpoint(uri=f"{account}/enable")
account_password: Endpoint = Endpoint(uri=f"{account}/password")
# account_finances = f"{account}/finances"
