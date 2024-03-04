from input.input_handler import InputHandler


class InputStatus:
    # singleton instance
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(InputStatus, cls).__new__(cls)
            cls._handler = InputHandler()
        return cls._instance

    def is_pressed(self, keycode):
        return self._handler.keys[keycode]

    @property
    def selected_close(self):
        return self._handler.selected_close
