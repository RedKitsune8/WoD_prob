import streamlit as st
from math import comb

def hunter_success_prob(n, difficulty, k):
    p_success = (11 - difficulty) / 10  # Probability of success (≥ difficulty)
    p_10 = 1 / 10  # Probability of rolling a 10 on a d10
    p_non_10_success = p_success - p_10  # Successes excluding 10s
    
    total_prob = 0.0
    
    # total_successes includes critical bonuses from 10s pairing
    # But to handle that properly, we iterate over number of 10s rolled
    for t in range(0, n + 1):  # number of 10s rolled
        critical_bonus = 2 * (t // 2)  # +2 successes per pair of 10s
        min_possible_successes = t + critical_bonus
        max_possible_successes = t + critical_bonus + (n - t)  # all non-10 dice succeed
        
        # total successes must be >= k and in the possible range for this t
        min_needed_non_10_successes = max(0, k - min_possible_successes)
        max_needed_non_10_successes = min(n - t, max_possible_successes - min_possible_successes)
        
        # sum probabilities of having i non-10 successes where i ranges from min_needed_non_10_successes to max_needed_non_10_successes
        for i in range(min_needed_non_10_successes, max_needed_non_10_successes + 1):
            total_successes = t + critical_bonus + i
            if total_successes >= k:
                p_tens = comb(n, t) * (p_10 ** t) * ((1 - p_10) ** (n - t))
                p_non_10 = comb(n - t, i) * (p_non_10_success / (1 - p_10)) ** i * (1 - p_non_10_success / (1 - p_10)) ** (n - t - i)
                total_prob += p_tens * p_non_10

    return total_prob

st.title("Hunter 5e Dice Pool Probability Calculator with Critical 10s")

n = st.number_input("Number of Dice (n)", min_value=1, value=5)
difficulty = st.number_input("Difficulty (X to 10)", min_value=2, max_value=10, value=6)
k = st.number_input("Successes Needed (k)", min_value=0, max_value=n*3, value=2)

prob = hunter_success_prob(n, difficulty, k)

st.write(f"Probability of at least {k} successes (including criticals) with {n} dice at difficulty {difficulty}: **{prob:.2%}**")
