from nicegui import ui

from ..rosys import config
from .automator import Automator


class AutomationControls:
    """This UI element contains start/stop/pause/resume buttons for controlling a given automator.

    See [Play-pause-stop](https://rosys.io/examples/play-pause-stop/) for a simple example of the automation controls.
    """

    def __init__(self, automator: Automator) -> None:
        play_button = ui.button(on_click=automator.start) \
            .props('icon=play_arrow unelevated').tooltip('start automation')
        pause_button = ui.button(on_click=lambda: automator.pause(because='pause button was pressed')) \
            .props('icon=pause outline').tooltip('pause automation')
        resume_button = ui.button(on_click=automator.resume) \
            .props('icon=play_arrow outline').tooltip('resume automation')
        stop_button = ui.button(on_click=lambda: automator.stop(because='stop button was pressed')) \
            .props('icon=stop outline').tooltip('stop automation')

        def refresh() -> None:
            play_button.visible = automator.is_stopped
            pause_button.visible = automator.is_running
            resume_button.visible = automator.is_paused
            self._disable(play_button, automator.default_automation is None or not automator.enabled)
            self._disable(stop_button, automator.is_stopped)

        ui.timer(config.ui_update_interval, refresh)

    def _disable(self, button: ui.button, should_disable: bool) -> None:
        if should_disable:
            button.props('disable')
        else:
            button.props(remove='disable')
