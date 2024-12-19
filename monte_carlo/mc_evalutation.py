import random

"""
Modelling Monte Carlo Methods for policy evaluation.
On-policy evaluation with a hidden transition model.
"""

class SevenStateMDP():
    def __init__(self) -> None:
        self.rewards = [0 for _ in range(6)]
        self.rewards.append(1)
        self.terminal_states = [0, 6]
        self.state_vals = [0 for _ in range(6)]
        self.state_vals.append(1)
    
    def transition(self, curr_state, action) -> int:
        '''
        Returns the next state given some internal transition model
        Given an action, 50% chance to fail and stay or move opposite direction
        '''
        seed = random.random()
        
        if seed < 0.5:
            return random.choice([curr_state, curr_state-action])
        
        return curr_state + action
    
    def generate_episode(self, starting_state, save_trajectory, gamma) -> float:
        '''
        Simulates an entire episode, up to num_episodes
        Returns the discounted return starting from starting_state
        '''
        reward = 0
        traj_len = 1
        curr_gamma = gamma
        next_state = starting_state   

        trajectory = [starting_state]
        while next_state not in self.terminal_states:
            traj_len += 1
            action = random.choice((-1, 1))  # implicitly actions have equal chance to be selected
            next_state = self.transition(next_state, action)
            curr_reward = self.rewards[next_state]
            reward += curr_gamma * curr_reward
            curr_gamma *= gamma
            
            
            # trajectory.append(action)
            # trajectory.append(curr_reward)
            if save_trajectory: trajectory.append(next_state)
        # print(trajectory)

        return reward
    
    def first_visit_mc_eval(self, num_episodes, alpha):
        """
        Simulate multiple episodes and perform state value updates over each episode
        Uses constant-alpha updates
        """
        for i in range(num_episodes):
            for state in range(1,6):
                curr_return = self.generate_episode(state, False, 1)
                self.state_vals[state] += alpha * (curr_return - self.state_vals[state])
            
            if i % 1000 == 0: print(self.state_vals)

        

mdp = SevenStateMDP()

mdp.first_visit_mc_eval(10000, 0.001)
    