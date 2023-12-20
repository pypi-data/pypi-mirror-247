# from __future__ import annotations

# from pydantic import BaseModel
# from ci.core.cloud.account import AccountInterface

# from ci.core.system.hercules import HerculesInterface


# class SystemInterface(BaseModel):
#     hercules: HerculesInterface

#     @staticmethod
#     def build(account: AccountInterface) -> SystemInterface:
#         return SystemInterface(
#             hercules=HerculesInterface(account=account),
#         )
