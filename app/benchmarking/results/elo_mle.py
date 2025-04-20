import numpy as np
from scipy.optimize import minimize
import pandas as pd
import re
import os

def extract_results_from_file(file_path):
    with open(file_path, 'r') as f:
        text = f.read()

    agent_match = re.search(r"Final Results \(\[(.+?)\] vs \[(.+?)\]\)", text)
    wld_match = re.search(r"Wins:\s*(\d+),\s*Losses:\s*(\d+),\s*Draws:\s*(\d+)", text)

    if agent_match and wld_match:
        return {
            "Agent 1": agent_match.group(1),
            "Agent 2": agent_match.group(2),
            "Wins": int(wld_match.group(1)),
            "Losses": int(wld_match.group(2)),
            "Draws": int(wld_match.group(3)),
        }
    return None

root_dir = "./"

results = []

for dirpath, _, filenames in os.walk(root_dir):
    for filename in filenames:
        if filename.endswith(".txt"):
            file_path = os.path.join(dirpath, filename)
            extracted = extract_results_from_file(file_path)
            if extracted:
                results.append(extracted)

df = pd.DataFrame(results)

df['Agent 1'] = df['Agent 1'].replace({'AB + Standard Depth=4': 'AB + Standard'})
df['Agent 2'] = df['Agent 2'].replace({'AB + Standard Depth=4': 'AB + Standard'})

agents = [
    "AB + Standard",
    "AB + FF",
    "AB + CNN",
    "MCTS + Standard",
    "MCTS + FF",
    "MCTS + CNN",
    "Random",
    "Stockfish"
]

agent_to_index = {agent: i for i, agent in enumerate(agents)}
index_to_agent = agents
n_agents = len(agents)

fixed_ratings = {
    agent_to_index["Stockfish"]: 1320,
    agent_to_index["Random"]: 255
}

match_counts = {}
for _, row in df.iterrows():
    i = agent_to_index.get(row['Agent 1'])
    j = agent_to_index.get(row['Agent 2'])
    if i is not None and j is not None:
        match_counts[(i, j)] = (row['Wins'], row['Draws'], row['Losses'])

free_indices = [i for i in range(n_agents) if i not in fixed_ratings]
initial_guess = [800.0 for _ in free_indices]

def compute_expected_score(r_i, r_j):
    return 1 / (1 + 10 ** ((r_j - r_i) / 400))

def neg_log_likelihood(free_ratings):
    ratings = np.zeros(n_agents)
    for i in range(n_agents):
        if i in fixed_ratings:
            ratings[i] = fixed_ratings[i]
        else:
            free_index = free_indices.index(i)
            ratings[i] = free_ratings[free_index]

    neg_log_lik = 0
    for (i, j), (w_ij, d_ij, l_ij) in match_counts.items():
        r_i = ratings[i]
        r_j = ratings[j]
        p_ij = compute_expected_score(r_i, r_j)
        p_ji = 1 - p_ij

        if p_ij <= 0 or p_ij >= 1:
            continue

        neg_log_lik -= w_ij * np.log(p_ij)
        neg_log_lik -= l_ij * np.log(p_ji)
        neg_log_lik -= d_ij * np.log(0.5)

    return neg_log_lik

result = minimize(neg_log_likelihood, initial_guess, method='L-BFGS-B')

final_ratings = {}
for i in range(n_agents):
    if i in fixed_ratings:
        final_ratings[i] = fixed_ratings[i]
    else:
        free_index = free_indices.index(i)
        final_ratings[i] = result.x[free_index]

final_df = pd.DataFrame({
    "Agent": [index_to_agent[i] for i in range(n_agents)],
    "Estimated Elo": [final_ratings[i] for i in range(n_agents)]
})

print(final_df)