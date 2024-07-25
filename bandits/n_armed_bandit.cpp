#include <iostream>
#include <random>
#include <fstream>

using namespace std;

double get_reward(vector<double>& rewards, int action) {
    return rewards[action];
}

void update_values(vector<double>& estim_values, int action, double curr_reward, double step_size) {
    double curr_value = estim_values[action];
    estim_values[action] = curr_value + step_size * (curr_reward - curr_value);
}

// get index of the highest value action
int get_max_value(vector<double>& estim_values) {
    double highest = estim_values[0];
    int i_highest = 0;

    for (int i = 1; i < estim_values.size(); i++) {
        if (estim_values[i] > highest) {
            highest = estim_values[i];
            i_highest = i;
        }
    }

    return i_highest;
}



int main(){
    std::random_device rd;
    std::mt19937 gen(rd());
    uniform_int_distribution<int> dist_10(0, 9);
    uniform_real_distribution<double> value_dist(0, 5);
    normal_distribution<double> noise_dist(0, 1);

    ofstream output("0.1-Greedy.txt");
    ofstream f("True_Values_e.txt");
    // ofstream output("Greedy.txt");
    // ofstream f("True_Values.txt");

    //setup real values
    vector<double> true_values(10, 0);
    for (double& i: true_values) {
        i = value_dist(gen);
    }

    //setup estimated values
    vector<double> estimated_values(10, 0.0);
    vector<double> estimated_values_fixed(10, 0.0);

    //print to file the true values
    // f << "True Values:" << endl;
    // for (double& i: true_values) {
    //     f << i << endl;
    // }
    
    vector<int> times_chosen(10, 0);

    // start learning
    int num_games = 2000;
    double average_reward = 0;
    for (int time = 0; time < num_games; time++) {

        if (time % 500 == 0) {
            for (auto &i: true_values) {
                i += noise_dist(gen);
            }
        }

        int action = get_max_value(estimated_values);

        if (dist_10(gen) == 0) {
            int new_action = dist_10(gen);
            while (new_action == action) {
                new_action = dist_10(gen);
            }
            action = new_action;
        }

        times_chosen[action]++;
        
        
        double reward = get_reward(true_values, action) + noise_dist(gen);
        average_reward += (1.0 / (time + 1)) * (reward - average_reward);
        output << average_reward << endl;

        update_values(estimated_values, action, reward, (1.0 / times_chosen[action]));
        update_values(estimated_values_fixed, action, reward, 0.1);

    }

    ofstream estim_f("estim.txt");
    for (double& i: estimated_values) {
        estim_f << i << endl;
    }
    estim_f.close();

    // ofstream estim_f("estim.txt");
    // for (double& i: estimated_values) {
    //     estim_f << i << endl;
    // }
    // estim_f.close();

    for (double& i: true_values) {
        f << i << endl;
    }

    f.close();
    output.close();
}