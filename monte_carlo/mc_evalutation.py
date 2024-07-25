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
        Given an action, 25% chance to fail and stay or move opposite direction
        '''
        seed = random.randint(1, 4)
        
        if seed == 1:
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
    
    def first_visit_mc_eval(self, num_episodes):
        """
        Each state is simulated for num_episodes and the average returns are saved in self.state_vals
        """
        for state in range(7):
            total_reward = 0
            for i in range(num_episodes):
                reward = self.generate_episode(state, False, 1)
                total_reward += reward
            self.state_vals[state] = total_reward / num_episodes

        

mdp = SevenStateMDP()

with open("state_value_changes.csv", "w") as f:
    for i in range(1,1000):  # inefficient but only for visualisation purposes
        mdp.first_visit_mc_eval(i)
        values = [str(x) for x in mdp.state_vals[1:-1]]
        f.write(",".join(values) + "\n")
    