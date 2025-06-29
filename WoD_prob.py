import streamlit as st
from math import comb

def hunter_success_prob(n, difficulty, k):
    p_success = (11 - difficulty) / 10
    p_10 = 1 / 10
    p_non_10_success = p_success - p_10
    total_prob = 0.0
    for t in range(0, n + 1):
        critical_bonus = 2 * (t // 2)
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

# Initialize session state for difficulty if not yet set
if "difficulty" not in st.session_state:
    st.session_state["difficulty"] = 6

col1, col2 = st.columns(2)

with col1:
    n = st.number_input("Number of Dice (n)", min_value=1, value=5, step=1)
    k = st.number_input("Successes Needed (k)", min_value=0, max_value=n*3, value=3, step=1)

with col2:
    st.markdown("**Difficulty (X to 10)**")
    difficulty = st.session_state["difficulty"]

    # First row: 1 to 5
    cols1 = st.columns(5)
    for idx, val in enumerate(range(1, 6)):
        with cols1[idx]:
            if st.button(str(val), key=f"diff_{val}"):
                st.session_state["difficulty"] = val
                difficulty = val  # immediate update

    # Second row: 6 to 10
    cols2 = st.columns(5)
    for idx, val in enumerate(range(6, 11)):
        with cols2[idx]:
            if st.button(str(val), key=f"diff_{val}"):
                st.session_state["difficulty"] = val
                difficulty = val  # immediate update

    st.write(f"Current Difficulty: **{difficulty}**")

# Calculate probability
prob = hunter_success_prob(n, difficulty, k)

# Determine color coding
if prob < 0.25:
    color = "#dc3545"  # red
elif prob < 0.45:
    color = "#fd7e14"  # orange
elif prob < 0.75:
    color = "#ffc107"  # yellow
else:
    color = "#28a745"  # green

# Display results
st.markdown(f"<h2 style='color:{color}; font-weight:bold;'>Probability: {prob:.2%}</h2>", unsafe_allow_html=True)

