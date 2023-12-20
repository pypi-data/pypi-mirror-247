from ci.api.account import AccountInterface

# from ci.core.cloud.system import SystemInterface


class Cephalon:
    def __init__(self) -> None:
        self.reinitialize()

    def reinitialize(self) -> None:
        self.account = AccountInterface.load()
        # self.system = SystemInterface.build(self.account)


cephalon = Cephalon()
