"""Main module."""
from .eos import EOSConnection
from .pad import Pad, EventHandler
from .eos_object import FaderBank, Fader, Macro
from lpminimk3 import LaunchpadMiniMk3, find_launchpads, ButtonEvent, Mode

COLORS = [3, 21, 37, 45, 81, 95, 5, 9]
FOCUS_MACROS = [901, 902, 903, 906]
SELECT_MACROS = [304, 303, 305, 302, 301]
SELECT_COLORS = [78, 21, 13, 5, 3]


class AbstractColorEventHandler(EventHandler):
    """Abstract color event handler"""
    def __init__(self, launchpad: LaunchpadMiniMk3, line: int, column: int):
        super().__init__(f'{column}x{line}')
        self._launchpad = launchpad
        self._line = line
        self._column = column
        self._launchpad.panel.led(
                self.button_name).color = COLORS[self._column]

    def flash(self):
        """Flash only the current button on the line"""
        for color in range(8):
            self._launchpad.panel.led(
                    f'{color}x{self._line}').color = COLORS[color]
        self._launchpad.panel.led(self.button_name).reset()
        self._launchpad.panel.led(self.button_name,
                                  mode='flash').color = COLORS[self._column]


class ColorBumpEventHandler(AbstractColorEventHandler):
    """Bump button Event handler"""
    def __init__(self, fader_bank: FaderBank,
                 launchpad: LaunchpadMiniMk3, color_id: int):
        super().__init__(launchpad, 5, color_id)
        self._fader = fader_bank.fader(14, color_id + 1)

    def on_press(self, _: ButtonEvent):
        self._fader.fire(1.0)

    def on_release(self, _: ButtonEvent):
        self._fader.fire(0.0)


class ColorFxEventHandler(AbstractColorEventHandler):
    """FX button Event handler"""
    def __init__(self, fader_bank: FaderBank,
                 launchpad: LaunchpadMiniMk3, color_id: int):
        super().__init__(launchpad, 6, color_id)
        self._fader = fader_bank.fader(17, color_id + 1)

    def on_press(self, _: ButtonEvent):
        self.flash()
        self._fader.fire()


class ColorEventHandler(AbstractColorEventHandler):
    """Non-FX button Event handler"""
    def __init__(self, fader_bank: FaderBank,
                 launchpad: LaunchpadMiniMk3, color_id: int):
        super().__init__(launchpad, 7, color_id)
        self._fader = fader_bank.fader(18, color_id + 1)

    def on_press(self, _: ButtonEvent):
        self.flash()
        self._fader.fire()


class FocusEventHandler(EventHandler):
    """Focus event handler"""
    def __init__(self, eos: EOSConnection,
                 launchpad: LaunchpadMiniMk3, column: int):
        super().__init__(f'{column}x2')
        self._macro = eos.macro(FOCUS_MACROS[column])
        self._launchpad = launchpad
        self._launchpad.panel.led(self.button_name).color = 5

    def on_press(self, _: ButtonEvent):
        for col in range(4):
            self._launchpad.panel.led(f'{col}x2').color = 5
        self._launchpad.panel.led(self.button_name).reset()
        self._launchpad.panel.led(self.button_name,
                                  mode='flash').color = 5

        self._macro.fire()


class SimpleFaderEventHandler(EventHandler):
    """Simple fader Event handler"""
    def __init__(self, fader: Fader,
                 launchpad: LaunchpadMiniMk3,
                 button: str, color: int):
        super().__init__(button)
        launchpad.panel.led(button).color = color
        self._fader = fader

    def on_press(self, _: ButtonEvent):
        self._fader.fire(1.0)

    def on_release(self, _: ButtonEvent):
        self._fader.fire(0.0)


class SimpleMacroEventHandler(EventHandler):
    """Simple macro Event handler"""
    def __init__(self, macro: Macro,
                 launchpad: LaunchpadMiniMk3,
                 button: str, color: int):
        super().__init__(button)
        launchpad.panel.led(button).color = color
        self._macro = macro

    def on_press(self, _: ButtonEvent):
        self._macro.fire()


class SelectEventHandler(EventHandler):
    """Select Event handler"""
    def __init__(self, eos: EOSConnection,
                 launchpad: LaunchpadMiniMk3,
                 select_id: int):
        super().__init__(f'{select_id + 3}x0')
        self._launchpad = launchpad
        self._select_id = select_id
        self._macro = eos.macro(SELECT_MACROS[self._select_id])
        self._launchpad.panel.led(
                self.button_name).color = SELECT_COLORS[self._select_id]

    def on_press(self, _: ButtonEvent):
        for i in range(3, 8):
            self._launchpad.panel.led(
                    f'{i}x0').color = SELECT_COLORS[i - 3]
        self._launchpad.panel.led(
                self.button_name).reset()
        self._launchpad.panel.led(
                self.button_name,
                mode='flash').color = SELECT_COLORS[self._select_id]
        self._macro.fire()


def main():
    """main function"""
    launchpad = find_launchpads()[0]
    launchpad.open()
    launchpad.mode = Mode.PROG
    launchpad.panel.reset()
    launchpad.clear_event_queue()

    eos = EOSConnection("192.168.50.36", 8000)
    faderbank = eos.fader_bank()

    pad = Pad(launchpad)

    # 6è-7è-8è ligne

    for i in range(8):
        pad.add_event_handler(ColorBumpEventHandler(faderbank, launchpad, i))
        pad.add_event_handler(ColorFxEventHandler(faderbank, launchpad, i))
        pad.add_event_handler(ColorEventHandler(faderbank, launchpad, i))

    # 3è ligne

    for i in range(4):
        pad.add_event_handler(FocusEventHandler(eos, launchpad, i))
    pad.add_event_handler(SimpleFaderEventHandler(
        faderbank.fader(6, 7), launchpad, '4x2', 9))
    pad.add_event_handler(SimpleFaderEventHandler(
        faderbank.fader(5, 2), launchpad, '6x2', 4))
    pad.add_event_handler(SimpleFaderEventHandler(
        faderbank.fader(5, 4), launchpad, '7x2', 4))

    # 2è ligne
    pad.add_event_handler(SimpleFaderEventHandler(
        faderbank.fader(5, 5), launchpad, '0x1', 21))
    pad.add_event_handler(SimpleFaderEventHandler(
        faderbank.fader(5, 6), launchpad, '1x1', 88))
    pad.add_event_handler(SimpleFaderEventHandler(
        faderbank.fader(7, 1), launchpad, '2x1', 78))
    pad.add_event_handler(SimpleFaderEventHandler(
        faderbank.fader(7, 2), launchpad, '3x1', 32))
    pad.add_event_handler(SimpleMacroEventHandler(
        eos.macro(401), launchpad, '5x1', 95))
    pad.add_event_handler(SimpleMacroEventHandler(
        eos.macro(402), launchpad, '6x1', 95))
    pad.add_event_handler(SimpleMacroEventHandler(
        eos.macro(403), launchpad, '7x1', 95))

    # 1ère ligne

    pad.add_event_handler(SimpleMacroEventHandler(
        eos.macro(6), launchpad, '0x0', 3))
    for i in range(5):
        pad.add_event_handler(SelectEventHandler(
            eos, launchpad, i))

    pad.serve_forever()


if __name__ == '__main__':
    main()
