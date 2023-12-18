class NoStatesProvided(Exception):
    def __init__(self, message:str = "No states was passed as \"define_states\" argument") -> None:
        super().__init__(message)
    pass

class NoEntryPoint(Exception):
    def __init__(self, message:str = "No first state was set") -> None:
        super().__init__(message)
    pass

class MachineAlrStarted(Exception):
    def __init__(self, message:str = "Machine is already in execution") -> None:
        super().__init__(message)
    pass

class VariableNotDefined(Exception):
    def __init__(self, variable) -> None:
        super().__init__(f"Variable \"{variable}\" was not defined!")
    pass

class StateNotExists(Exception):
    def __init__(self, state) -> None:
        super().__init__(f"State \"{state}\" was not defined!")
    pass

class FewArguments(Exception):
    def __init__(self, var) -> None:
        super().__init__(f"Argument \"{var}\" was not provided!")
    pass