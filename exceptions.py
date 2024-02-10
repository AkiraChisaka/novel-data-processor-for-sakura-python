class ChaosOverflow(Exception):

    def __init__(self, chaos, current_line):
        """
        Exception raised when the chaos intensity is too high, causing the realignment process to stop.

        Args:
            chaos (float): The current chaos intensity.
            current_line (int): The current line number.
        """
        super().__init__(f"Chaos intensity too high. Stopping the realignment process.\n" +
                         f"Current chaos intensity: {chaos}\n" +
                         f"Current line: {current_line + 1}")
        self.chaos = chaos
        self.current_line = current_line
