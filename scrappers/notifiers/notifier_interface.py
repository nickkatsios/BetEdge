class Notifier_interface:
    """
    Interface for notifiers.

    Provides a framework for adding new notifiers to the project
    All notifiers should inherit from this class
    See: https://realpython.com/python-interface/ for more info
    """
    def __init__(self):
        pass

    def notify_error(self, error_message):
        pass

