import numpy as np

# deterministic case, to generalise to non-deterministic
class Grid_MDP():
    def __init__(self, dim_x, dim_y, gamma) -> None:
        self.gamma = gamma
        self.dim_x = dim_x
        self.dim_y = dim_y
        self.num_states = dim_x*dim_y
        self.state_values = np.zeros((self.num_states,), dtype=np.float32)
        self.terminal_states = [0]
        self.walls = []
        self.policy = {state: ((0.25,)*4 if state not in self.terminal_states else (0.0,)*4) for state in range(self.num_states)}  # mapping from states to probability over actions (p(a1), p(a2)), indices are the actions



    def evaluate_policy_iter(self, iters, to_print=False) -> None:
        for i in range(iters):
            for state in range(self.num_states):
                if state not in self.walls and state not in self.terminal_states:
                    self.state_values[state] = self.estimate_value_by_policy(state)
        
        self.state_values = self.state_values.round(4)

        if to_print: self.print_state_values()

    def update_policy(self, to_print=False) -> None:
        for state in range(self.num_states):
            if state in self.terminal_states or state in self.walls: continue

            action_values = [self.state_values[self.transition(state, action)] for action in range(4)]
            max_value = max(action_values)
            greedy_actions = [action for action, value in enumerate(action_values) if value == max_value]
            prob = 1 / len(greedy_actions)
            self.policy[state] = tuple((prob if action in greedy_actions else 0.0) for action in range(4))
        
        if to_print: print(self.policy)


    def transition(self, state, action) -> int:
        # (U, D, L, R)
        next_state = None

        if action == 0:
            next_state = state if (state - self.dim_x) < 0 else state - self.dim_x
        
        if action == 1:
            next_state = state if (state + self.dim_x) > (self.num_states-1) else state + self.dim_x
        
        if action == 2:
            next_state = state if (state % self.dim_x) == 0 else state - 1
        
        if action == 3:
            next_state = state if ((state+1) % self.dim_x) == 0 else state + 1

        if next_state in self.walls:
            return state
        
        return next_state
       

    def estimate_value_by_policy(self, state) -> float:
        # used in policy iteration step, alternative to solving linear system of equations
        action_space = self.policy[state]
        value = 0
            
        for action, prob in enumerate(action_space):
            next_state = self.transition(state, action)
            value += prob * (self.get_reward(next_state) + (self.gamma * self.state_values[next_state]))  # does it matter if rewards are given before or after transition?
            
            # print(f"from state s{state}, taking action a{action+1} leads to state s{next_state} with probability {prob}")
            
        return value
    
    def estimate_value_by_reward(self, state) -> float:
        # used in value iteration step:
        # TO DO
        value = self.get_reward(state)
        next_values = []
        pass
    
    def print_state_values(self):
        for i in range(0, self.num_states, self.dim_x):
            print(self.state_values[i:i+self.dim_x])
            
    def get_reward(self, state) -> int:
        # if state in self.terminal_states:
        #     return 1
        
        # if state == 7:
        #     return -1
        
        return -1
    
grid_mdp = Grid_MDP(4, 4, 1)
for i in range(5):
    grid_mdp.evaluate_policy_iter(1, True)
    grid_mdp.update_policy(1)




