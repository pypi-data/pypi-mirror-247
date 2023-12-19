import ray


class ModelError(Exception):
    pass


class MeshError(Exception):
    pass


class SolveError(Exception):
    pass


class PostError(Exception):
    pass


class FEMCrash(Exception):
    pass


class FemtetAutomationError(Exception):
    pass


class UserInterruption(Exception):
    pass


@ray.remote
class _InterprocessVariables:

    def __init__(self):
        self.state = 'undefined'
        self.history = []
        self.allowed_idx = 0

    def set_state(self, state):
        self.state = state

    def get_state(self) -> 'ObjectRef':
        return self.state

    def append_history(self, row):
        self.history.append(row)

    def get_history(self) -> 'ObjectRef':
        return self.history

    def set_allowed_idx(self, idx):
        self.allowed_idx = idx

    def get_allowed_idx(self):
        return self.allowed_idx


class InterprocessVariables:

    def __init__(self):
        self.ns = _InterprocessVariables.remote()

    def set_state(self, state):
        print(f'---{state}---')
        self.ns.set_state.remote(state)

    def get_state(self):
        return ray.get(self.ns.get_state.remote())

    def append_history(self, row):
        self.ns.append_history.remote(row)

    def get_history(self):
        return ray.get(self.ns.get_history.remote())

    def set_allowed_idx(self, idx):
        self.ns.set_allowed_idx.remote(idx)

    def get_allowed_idx(self):
        return ray.get(self.ns.get_allowed_idx.remote())


