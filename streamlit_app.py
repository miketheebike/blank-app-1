import streamlit as st
import plotly.graph_objs as go
import pandas as pd

# Set the page configuration to wide mode
st.set_page_config(layout="wide")

# Define the options
options = [
    "Less than -15%",
    "-15% to -10%",
    "-10% to -5%",
    "-5% to 0%",
    "0% to 5%",
    "5% to 10%",
    "10% to 15%",
    "More than 15%"
]

# Initialize a session state to store the probability distribution
if 'prob_dist' not in st.session_state:
    st.session_state.prob_dist = [0.0] * len(options)  # Initialize all probabilities to 0

# Function to calculate the remaining probability
def calculate_remaining_prob():
    return 100.0 - sum(st.session_state.prob_dist)  # Now working with percentages

# Function to update probability distribution
def update_prob_dist(idx, new_height):
    st.session_state.prob_dist[idx] = new_height
    # Ensure the probabilities sum to 100
    total = sum(st.session_state.prob_dist)
    if total > 100.0:
        st.session_state.prob_dist[idx] -= total - 100.0

# Function to reset probabilities to 0
def reset_prob_dist():
    st.session_state.prob_dist = [0.0] * len(options)

# Plotting the probability distribution
def plot_prob_dist():
    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=options, 
        y=st.session_state.prob_dist, 
        marker_color='rgba(50, 205, 50, 0.9)',  # A nice bright green
        marker_line_color='rgba(0, 128, 0, 1.0)',  # Dark green outline for contrast
        marker_line_width=2,  # Width of the bar outline
        text=[f"{p:.0f}%" for p in st.session_state.prob_dist],  # Adding percentage labels to bars
        textposition='auto',
        name='Probability'
    ))

    fig.update_layout(
        title={
            'text': "Probability distribution",
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        xaxis_title="Expectation Range",
        yaxis_title="Probability (%)",
        yaxis=dict(
            range=[0, 100], 
            gridcolor='rgba(255, 255, 255, 0.2)',  # Light grid on dark background
            showline=True,
            linewidth=2,
            linecolor='white',
            mirror=True
        ),
        xaxis=dict(
            tickangle=-45,
            showline=True,
            linewidth=2,
            linecolor='white',
            mirror=True
        ),
        font=dict(color='white'),  # White font color for readability
    )
    return fig

st.title("Interactive Probability Distribution Survey")

# Calculate the remaining probability
remaining_prob = calculate_remaining_prob()

# Display the remaining probability
st.write(f"Remaining Probability: {remaining_prob:.0f}%")

# Select an option to adjust
selected_option = st.selectbox("Select the expectation range to adjust", options=options)

# Get the index of the selected option
click_idx = options.index(selected_option)

# Adjust the slider to be within the remaining probability, or display a message if no remaining probability
if remaining_prob > 0:
    max_value = min(100.0, st.session_state.prob_dist[click_idx] + remaining_prob)
    if max_value > 0:
        new_prob = st.slider("Adjust the probability (%)", 0, int(max_value), int(st.session_state.prob_dist[click_idx]), step=5)
        # Automatically update the probability distribution when the slider is moved
        update_prob_dist(click_idx, new_prob)
    else:
        st.write("No adjustment possible: Maximum probability for this range is already reached.")
else:
    st.write("No remaining probability to allocate.")

# Place the reset button below the slider
if st.button("Reset All Probabilities"):
    reset_prob_dist()

# Layout for table and plot side by side
table_col, plot_col = st.columns([1, 2])

with table_col:
    # Display the updated probability distribution in a table
    st.write("Current Probability Distribution")
    prob_df = pd.DataFrame({
        "Expectation Range": options,
        "Probability (%)": [int(p) for p in st.session_state.prob_dist]  # Display without decimals
    })
    st.table(prob_df)

with plot_col:
    # Replot the updated distribution
    fig = plot_prob_dist()
    st.plotly_chart(fig, use_container_width=True)
