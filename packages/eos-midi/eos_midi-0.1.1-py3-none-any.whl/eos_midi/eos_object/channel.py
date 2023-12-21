"""EOS Channel"""
from pythonosc.udp_client import SimpleUDPClient


class Channel:
    """EOS Channel"""
    def __init__(self, channel_id: int, osc_client: SimpleUDPClient):
        self.channel_id = channel_id
        self.osc_client = osc_client

    def full(self):
        """Sets channel intensity to full"""
        self.osc_client.send_message(f"/eos/chan/{self.channel_id}/full", [])

    def min(self):
        """Sets channel intensity to min"""
        self.osc_client.send_message(f"/eos/chan/{self.channel_id}/min", [])

    def max(self):
        """Sets channel intensity to max"""
        self.osc_client.send_message(f"/eos/chan/{self.channel_id}/max", [])

    def plus_10(self):
        """Increases channel intensity by 10%"""
        self.osc_client.send_message(f"/eos/chan/{self.channel_id}/+%", [])

    def minus_10(self):
        """Decreases channel intensity by 10%"""
        self.osc_client.send_message(f"/eos/chan/{self.channel_id}/-%", [])
