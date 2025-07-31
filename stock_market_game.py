# Stock Market Education Game (Web App with Charts)
# Teaches concepts: Liquidity Grabs, FVG, BOS, ORB

import streamlit as st
import random
import matplotlib.pyplot as plt
import numpy as np

# Concepts
concepts = {
    "Liquidity Grab": "A liquidity grab happens when price moves beyond a recent high/low to trap traders, then reverses.",
    "FVG": "Fair Value Gap (FVG) is an imbalance between buyers and sellers visible as a gap in price.",
    "BOS": "Break of Structure (BOS) occurs when price breaks a key high or low, indicating a trend change.",
    "ORB": "Opening Range Breakout (ORB) is a strategy using the high and low of the first few minutes after market open."
}

# Game state
if 'balance' not in st.session_state:
    st.session_state.balance = 10000
if 'scenario_index' not in st.session_state:
    st.session_state.scenario_index = 0

scenarios = [
    {
        "name": "Liquidity Grab - Short Setup",
        "description": "Price swept above previous high and closed back inside range.",
        "entry": "short",
        "good_exit": "at previous low",
        "bad_exit": "holding through reversal",
        "chart": "liquidity"
    },
    {
        "name": "FVG Long Setup",
        "description": "Price pulled into FVG and bounced.",
        "entry": "long",
        "good_exit": "at supply zone",
        "bad_exit": "holding through FVG close",
        "chart": "fvg"
    },
    {
        "name": "BOS Confirmation",
        "description": "Structure broke to upside after a higher low.",
        "entry": "long",
        "good_exit": "at next swing high",
        "bad_exit": "entering before BOS",
        "chart": "bos"
    },
    {
        "name": "ORB Failure",
        "description": "Price broke opening range high but reversed hard.",
        "entry": "long",
        "good_exit": "quick scalp on breakout",
        "bad_exit": "holding during pullback",
        "chart": "orb"
    }
]

# Chart renderers
def plot_chart(chart_type):
    fig, ax = plt.subplots()
    x = np.arange(10)
    price = np.random.normal(loc=100, scale=1, size=10).cumsum()

    if chart_type == "liquidity":
        price[6] += 5  # Fake sweep
        price[7] -= 6  # Reversal
        ax.plot(x, price, label='Price')
        ax.axhline(price[5], color='red', linestyle='--', label='Previous High')
        ax.set_title("Liquidity Grab Example")

    elif chart_type == "fvg":
        price[4] += 5
        price[5] += 7
        price[6] += 3
        ax.plot(x, price, label='Price')
        ax.axvspan(4.5, 5.5, color='yellow', alpha=0.3, label='FVG')
        ax.set_title("FVG Example")

    elif chart_type == "bos":
        price[5:] += 6
        ax.plot(x, price, label='Price')
        ax.axhline(price[4], color='green', linestyle='--', label='Structure Break')
        ax.set_title("Break of Structure (BOS)")

    elif chart_type == "orb":
        open_range = (price[0:3].min(), price[0:3].max())
        price[4:] -= 4
        ax.plot(x, price, label='Price')
        ax.axhline(open_range[0], color='purple', linestyle='--', label='ORB Low')
        ax.axhline(open_range[1], color='orange', linestyle='--', label='ORB High')
        ax.set_title("Opening Range Breakout (ORB)")

    ax.legend()
    st.pyplot(fig)

# Display game UI
def show_game():
    st.title("Stock Market Game with Visual Learning")
    st.subheader(f"Balance: ${st.session_state.balance}")
    st.markdown("---")
    st.subheader("📘 Market Concepts")
    for key, val in concepts.items():
        with st.expander(key):
            st.write(val)

    st.markdown("---")

    if st.session_state.scenario_index < len(scenarios):
        scenario = scenarios[st.session_state.scenario_index]
        st.header(scenario['name'])
        st.write(scenario['description'])

        plot_chart(scenario['chart'])

        entry = st.radio("Choose your entry:", ["long", "short", "skip"], key=f"entry_{st.session_state.scenario_index}")
        exit_choice = st.radio("Choose your exit strategy:", ["smart", "greedy"], key=f"exit_{st.session_state.scenario_index}")

        if st.button("Submit Decision"):
            result = ""
            if entry == "skip":
                result = "Skipped the trade."
            elif entry != scenario['entry']:
                result = "Wrong entry type. You entered against the setup."
                st.session_state.balance -= 300
            elif exit_choice == "smart":
                result = f"Smart exit at {scenario['good_exit']}!"
                st.session_state.balance += 500
            else:
                result = f"Poor exit at {scenario['bad_exit']}!"
                st.session_state.balance -= 200

            st.success(result)
            st.session_state.scenario_index += 1
            st.experimental_rerun()
    else:
        st.header("Game Over")
        st.subheader(f"Final Balance: ${st.session_state.balance}")
        if st.session_state.balance > 10000:
            st.success("Well done! You made profitable decisions.")
        else:
            st.error("You need more practice. Review the concepts and try again.")

if __name__ == '__main__':
    show_game()
