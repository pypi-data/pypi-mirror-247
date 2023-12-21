""""EOS Macro"""
from pythonosc.udp_client import SimpleUDPClient


class Macro:
    """EOS Macro"""
    def __init__(self, macro_id: int, osc_client: SimpleUDPClient):
        self.macro_id = macro_id
        self.osc_client = osc_client

    def fire(self):
        """Fires macro"""
        self.osc_client.send_message(f"/eos/macro/{self.macro_id}/fire", [])
