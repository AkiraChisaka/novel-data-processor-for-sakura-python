class RealignmentFailed(Exception):
    def __init__(self, current_line, message="Realignment process failed."):
        """
        Initialize a RealignmentException object.

        Args:
            current_line (int): The line number where the error occurred.
            message (str, optional): The error message. Defaults to "Realignment process failed.".
        """
        self.current_line = current_line
        super().__init__(f"{message}" +
                         f"\nCurrent line: {current_line + 1}\n")


class ChaosOverflow(RealignmentFailed):
    def __init__(self, current_line, chaos):
        """
        Exception raised when the chaos intensity is too high, causing the realignment process to stop.

        Args:
            current_line (int): The current line number.
            chaos (float): The current chaos intensity.
        """
        super().__init__(current_line,
                         f"Chaos intensity too high. Stopping the realignment process.\n" +
                         f"Current line: {current_line + 1}\n" +
                         f"Current chaos intensity: {chaos}\n")
        self.chaos = chaos
