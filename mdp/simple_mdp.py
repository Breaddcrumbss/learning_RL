class Simple_MDP():
# to extend mdp, add variable state_value length, policy generation, default uniform policy, automatic non-deterministic transitions
    def __init__(self, gamma) -> None:
        self.gamma = gamma
        self.state_values = [0, 0, 0]
        self.policy = {0: (1, 0), 1: (1, 0), 2: (1, 0)}  # mapping from states to probability over actions (p(a1), p(a2)), indices are the actions
    

    def evaluate_policy_iter(self, iters) -> None:
        for i in range(iters):
            for state in self.policy.keys():
                self.state_values[state] = self.estimate_value(state)
        
        print(self.state_values)


    def get_reward(self, state) -> int:
        if state == 0:
            return 0
        
        return -1

    def transition(self, state, action) -> int:
        if state == 0:
            if action == 0:
                return 2
            
            return 1
        
        return 0

    def estimate_value(self, state) -> float:
        action_space = self.policy[state]
        value = 0
            
        for action, prob in enumerate(action_space):
            next_state = self.transition(state, action)
            value += prob * (self.get_reward(state) + self.gamma * ((0.9*self.state_values[next_state]) + \
                             0.1*(self.state_values[state])))  # multiple values in this expression if transition is non-deterministic
            
            # print(f"from state s{state}, taking action a{action+1} leads to state s{next_state} with probability {prob} and reward {self.get_reward(next_state)}")
            
        return value
        
mdp = Simple_MDP(0.9)
mdp.evaluate_policy_iter(10000)
