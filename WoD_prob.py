import streamlit as st
from math import comb

def hunter_success_prob(n, difficulty, k):
    p_success = (11 - difficulty) / 10  # Probability of success (≥ difficulty)
    p_10 = 1 / 10  # Probability of rolling a 10 on a d10
    p_non_10_success = p_success - p_10  # Successes excluding 10s
    
    total_prob = 0.0
    
    for t in range(0, n + 1):  # number of 10s rolled
        critical_bonus = 2 * (t // 2)  # +2 successes per pair of 10s
        min_possible_successes = t + critical_bonus
        max_possible_successes = t + critical_bonus + (n - t)
        
        min_needed_non_10_successes = max(0, k - min_possible_successes)
        max_needed_non_10_successes = min(n - t, max_possible_successes - min_possible_successes)
        
        for i in range(min_needed_non_10_successes, max_needed_non_10_successes + 1):
            total_successes = t + critical_bonus + i
            if total_successes >= k:
                p_tens = comb(n, t) * (p_10 ** t) * ((1 - p_10) ** (n - t))
                p_non_10 = comb(n - t, i) * (p_non_10_success / (1 - p_10)) ** i * (1 - p_non_10_success / (1 - p_10)) ** (n - t - i)
                total_prob += p_tens * p_non_10

    return total_prob

st.title("Hunter 5e Dice Pool Probability Calculator with Criticals")

n = st.number_input("Number of Dice (n)", min_value=1, value=5)
difficulty = st.number_input("Difficulty (X to 10)", min_value=2, max_value=10, value=6)
k = st.number_input("Successes Needed (k)", min_value=0, max_value=n*3, value=3)

prob = hunter_success_prob(n, difficulty, k)

# Color-coded display with your custom thresholds
if prob < 0.25:
    color = "#dc3545"  # red
elif prob < 0.45:
    color = "#fd7e14"  # orange
elif prob < 0.75:
    color = "#ffc107"  # yellow
else:
    color = "#28a745"  # green

st.markdown(f"<h2 style='color:{color}; font-weight:bold;'>Probability: {prob:.2%}</h2>", unsafe_allow_html=True)

