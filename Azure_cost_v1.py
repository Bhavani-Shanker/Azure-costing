import streamlit as st

# Set canvas background color
st.markdown(
    """
    <style>
    .stApp {
        background-color: #f0f2f6; /* Light gray default background */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Title
st.title("Token Cost Calculator")

# Disclaimer in smaller font
st.markdown(
    """
    <p style="font-size: 0.85em; color: gray;">
    <strong>Disclaimer</strong><br>
    • The cost provided is an approximate estimate.<br>
    • Cost variations depend on the region, as each region has distinct tariffs.<br>
    • Users may adjust the per-token rate based on region-specific rates or any updated tariffs.
    </p>
    """,
    unsafe_allow_html=True
)

# Canvas background color selection
bg_color = st.color_picker("Choose canvas background color", "#f0f2f6")
st.markdown(
    f"""
    <style>
    .stApp {{
        background-color: {bg_color};
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# Input fields for tokens
total_requests = st.number_input("Total Requests", min_value=0)
prompt_tokens = st.text_input("Prompt Token Count (Input Tokens)", "0")
completion_tokens = st.text_input("Completion Token Count (Output Tokens)", "0")

# Convert units to millions
def convert_to_millions(value):
    try:
        if 'K' in value.upper():
            return float(value.replace('K', '')) / 1000
        elif 'M' in value.upper():
            return float(value.replace('M', ''))
        else:
            return float(value) / 1_000_000
    except ValueError:
        return None

# Convert prompt and completion tokens to millions
prompt_tokens_m = convert_to_millions(prompt_tokens)
completion_tokens_m = convert_to_millions(completion_tokens)

# Calculate total tokens in millions programmatically
total_tokens_m = (prompt_tokens_m if prompt_tokens_m else 0) + (completion_tokens_m if completion_tokens_m else 0)

# Display the calculated Total Token Count
st.write("### Calculated Total Token Count")
st.write(f"Total Token Count: {total_tokens_m * 1_000_000:.0f} tokens (in millions: {total_tokens_m:.2f}M)")

# Editable checkboxes
col1, col2 = st.columns(2)
with col1:
    editable = st.checkbox("Edit cost per million tokens")
with col2:
    region_editable = st.checkbox("Region")

# Cost per million tokens input, editable only if checkbox is selected
prompt_cost_per_million = st.number_input(
    "Cost per million tokens for Prompt Token Count ($)", 
    value=7.5, 
    step=0.01, 
    disabled=not editable
)
completion_cost_per_million = st.number_input(
    "Cost per million tokens for Completion Token Count ($)", 
    value=66.0, 
    step=0.01, 
    disabled=not editable
)

# Region input with default value "WEST US", editable only if checkbox is selected
region = st.text_input("Region", value="WEST US", disabled=not region_editable)

# Calculation of total costs
try:
    total_prompt_cost = prompt_tokens_m * prompt_cost_per_million if prompt_tokens_m else 0
    total_completion_cost = completion_tokens_m * completion_cost_per_million if completion_tokens_m else 0
    total_cost = total_prompt_cost + total_completion_cost

    # Display calculated costs with $ symbol
    st.write("### Calculated Costs")
    st.write(f"Prompt Token Cost: ${total_prompt_cost:.2f}")
    st.write(f"Completion Token Cost: ${total_completion_cost:.2f}")
    st.write(f"Total Cost: ${total_cost:.2f}")
    st.write(f"Region: {region}")

except TypeError:
    st.warning("Please ensure valid numbers for cost calculation.")
