#############################
##                         ##
##  BasicFSM by Levorin    ##
##                         ##
##  ver. 0.1               ##
##                         ##
#############################

from fsm_errors import *
from threading import Thread

class FSMconstructor:
    def __init__(self):
        self.states: dict = {}
        self.states_names: list
        self.check_function: function = None
        self.prev_variables: dict = {}
        self.variables: dict = {}
        self.change_checklist: dict = {}
        self.conditions: dict = {}

        self.loop_thread = None
        self.check_thread = None

        # private
        self._current_state: str

    def define_states(self, *args: list) -> list:
        '''
        Used to declare all machine states, pass as argument all the associated function
        '''
        # error check
        if not args: raise NoStatesProvided()

        for func in args:
            self.states[func.__name__] = func

        self.states_names = list(self.states.keys())
        return self.states_names
    
    def change_state(self, state: str):
        '''
        safe method to switch between states
        '''
        if not state in self.states_names: raise StateNotExists(state)
        self._current_state = state
    
    def thread_check(self):
        while True:
            # user defined
            if self.check_function:
                self.check_function()

            # if defined check condition
            if self._current_state in self.conditions.keys():
                self.conditions[self._current_state]()

            # check vars changes
            for var in self.change_checklist:
                if self.variables[var] != self.prev_variables[var]:
                    self.change_state(self.change_checklist[var])
                    self.prev_variables[var] = self.variables[var]

    def thread_loop(self):
        while True: self.states[self._current_state]()
    
    def start(self, entry_point: str) -> None:
        '''
        Start the Finite State Machine. The machine will be executed as a separate process
        '''
        # error check
        if not self.states: raise NoStatesProvided()
        if not entry_point: raise NoEntryPoint()
        if not entry_point in self.states_names: raise StateNotExists(entry_point)
        if self.loop_thread or self.check_thread: raise MachineAlrStarted()

        self._current_state = entry_point
        self.loop_thread = Thread(target = self.thread_check, daemon = True)
        self.check_thread = Thread(target = self.thread_loop, daemon = True)
        self.loop_thread.start()
        self.check_thread.start()
    
    def on_change(self, var_name: str, change_to: str) -> None:
        '''
        Change to the specified state when the variable passed as argument is changed
        '''
        # error check
        if var_name not in self.variables.keys(): raise VariableNotDefined(variable = var_name)
        if change_to not in self.states_names: raise StateNotExists(change_to)

        # change_to, block
        self.prev_variables[var_name] = self.variables[var_name]
        self.change_checklist[var_name] = change_to

    def addCondition(self, attach_to: str, condition):
        '''
        Attach switch state condition to the specified state
        '''
        if attach_to not in self.states_names: raise StateNotExists(attach_to)

        self.conditions[attach_to] = condition