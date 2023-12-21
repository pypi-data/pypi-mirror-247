"""Launchpad"""
from lpminimk3 import LaunchpadMiniMk3, ButtonEvent

VALID_BUTTONS = [
    'up', 'down', 'left', 'right', 'session', 'drums', 'keys', 'user',
    'scene_launch_1', 'scene_launch_2', 'scene_launch_3', 'scene_launch_4',
    'scene_launch_5', 'scene_launch_6', 'scene_launch_7', 'stop_solo_mute',
]


class EventHandler:
    """Event handler for launchpad"""
    def __init__(self, button_name: str):
        self._button_name = button_name

    @property
    def button_name(self):
        """Returns button name"""
        return self._button_name

    def on_press(self, _: ButtonEvent):
        """On button pressed"""

    def on_release(self, _: ButtonEvent):
        """On button released"""


class Pad:
    """Pad Wrapper"""
    def __init__(self, launchpad: LaunchpadMiniMk3):
        self._launchpad = launchpad
        self._event_handlers: dict[str, list[EventHandler]] = {}

    def _validate_button(self, button: str | tuple[int, int]) -> str:
        if isinstance(button, str):
            if button in VALID_BUTTONS:
                return button
            split = button.split('x')
            if len(split) == 2 and \
               split[0].isdigit() and split[1].isdigit() and \
               int(split[0]) >= 0 and int(split[0]) < 8 and \
               int(split[1]) >= 0 and int(split[1]) < 8:
                return button
            raise ValueError(button)
        if isinstance(button, tuple) and len(button) == 2 and \
                isinstance(button[0], int) and isinstance(button[1], int) and \
                button[0] >= 0 and button[0] < 8 and \
                button[1] >= 0 and button[1] < 8:
            return str(button[0]) + 'x' + str(button[1])
        raise ValueError(button)

    def add_event_handler(self, handler: EventHandler):
        """Adds a event handler"""
        button = self._validate_button(handler.button_name)
        lst = self._event_handlers.get(button)
        if lst:
            lst.append(handler)
        else:
            self._event_handlers[button] = [handler]

    def serve_forever(self):
        """Servers forever"""
        buttons = self._launchpad.panel.buttons()
        while True:
            event = buttons.poll_for_event()
            if isinstance(event, ButtonEvent):
                if event.type == ButtonEvent.PRESS:
                    for handler in self._event_handlers.get(
                            event.button.name, []):
                        handler.on_press(event)
                elif event.type == ButtonEvent.RELEASE:
                    for handler in self._event_handlers.get(
                            event.button.name, []):
                        handler.on_release(event)
