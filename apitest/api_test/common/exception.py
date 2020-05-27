class ExecutionCheckException(RuntimeError):
    def __init__(self, msg):
        self.msg = msg


class ExecutionFailException(RuntimeError):
    def __init__(self, msg):
        self.msg = msg


class ExecutionPassException(RuntimeError):
    def __init__(self, msg):
        self.msg = msg


class ExecutionStopException(RuntimeError):
    def __init__(self, msg):
        self.msg = msg


class LoopBreakException(RuntimeError):
    def __init__(self):
        pass


class LoopContinueException(RuntimeError):
    def __init__(self):
        pass
