"""EOS Fader"""
from typing import Optional
from pythonosc.udp_client import SimpleUDPClient


class FaderBank:
    """EOS Fader bank"""
    def __init__(self, osc_client: SimpleUDPClient):
        self.osc_client = osc_client
        for i in range(1, 101):
            self.osc_client.send_message(
                    f"/eos/fader/{i}/config/{i}/10", [])

    def page(self, page: int):
        """Returns the page {page}"""
        return FaderPage(page, self.osc_client)

    def fader(self, page: int, fader: int):
        """Returns the fader {fader} of page {page}"""
        return FaderPage(page, self.osc_client).fader(fader)


class FaderPage:
    """EOS Fader page"""
    def __init__(self, page: int, osc_client: SimpleUDPClient):
        self.page = page
        self.osc_client = osc_client

    def fader(self, fader: int):
        """Returns the fader {fader} of the page"""
        return Fader(self.page, fader, self.osc_client)

    def next(self):
        """Returns the next page"""
        return FaderPage(min(100, self.page + 1), self.osc_client)

    def previous(self):
        """Returns the previous page"""
        return FaderPage(max(1, self.page - 1), self.osc_client)


class Fader:
    """EOS Fader"""
    def __init__(self, page: int, fader: int,
                 osc_client: SimpleUDPClient):
        self.page = page
        self.fader = fader
        self.osc_client = osc_client

    def fire(self, value: Optional[float] = None):
        """Starts effect of the fader"""
        if value:
            self.osc_client.send_message(
                    f"/eos/fader/{self.page}/{self.fader}/fire", [value])
        else:
            self.osc_client.send_message(
                    f"/eos/fader/{self.page}/{self.fader}/fire", [])

    def stop(self):
        """Stops effect of the fader"""
        self.osc_client.send_message(
                f"/eos/fader/{self.page}/{self.fader}/stop", [])

    def full(self):
        """Sets the fader to full"""
        self.osc_client.send_message(
                f"/eos/fader/{self.page}/{self.fader}/full", [])

    def min(self):
        """Sets the fader to minimum"""
        self.osc_client.send_message(
                f"/eos/fader/{self.page}/{self.fader}/min", [])

    def max(self):
        """Sets the fader to maximum"""
        self.osc_client.send_message(
                f"/eos/fader/{self.page}/{self.fader}/max", [])

    def plus_10(self):
        """Increases the fader by 10%"""
        self.osc_client.send_message(
                f"/eos/fader/{self.page}/{self.fader}/+%", [])

    def minus_10(self):
        """Decreases the fader by 10%"""
        self.osc_client.send_message(
                f"/eos/fader/{self.page}/{self.fader}/-%", [])
