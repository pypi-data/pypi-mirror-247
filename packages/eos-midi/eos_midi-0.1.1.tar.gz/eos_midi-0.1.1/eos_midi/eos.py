"""EOS"""
from pythonosc.udp_client import SimpleUDPClient
from .eos_object.fader import FaderBank
from .eos_object.channel import Channel
from .eos_object.macro import Macro


class EOSConnection:
    """EOS Connection"""
    def __init__(self, address: str, port: int):
        self.osc_client = SimpleUDPClient(address, port)

    def fader_bank(self):
        """Returns the FaderBank"""
        return FaderBank(self.osc_client)

    def channel(self, channel_id: int):
        """Returns the Channel {channel_id}"""
        return Channel(channel_id, self.osc_client)

    def macro(self, macro_id: int):
        """Returns the Macro {macro_id}"""
        return Macro(macro_id, self.osc_client)
