import streamlit as st
from scipy.stats import binom

st.title("Dice Pool Probability Calculator (WoD tailored)")

n = st.number_input("Number of Dice (n)", min_value=1, value=5)
difficulty = st.number_input("Difficulty (X, target number to succeed, e.g. 6 means 6-10 counts)", min_value=2, max_value=10, value=6)
k = st.number_input("Successes Needed (k)", min_value=0, value=2)

# Calculate p based on difficulty
p = (11 - difficulty) / 10

prob = 1 - binom.cdf(k-1, n, p)

st.write(f"Difficulty: {difficulty}+ (p = {p:.2f})")
st.write(f"Probability of at least {k} successes with {n} dice: **{prob:.2%}**")
