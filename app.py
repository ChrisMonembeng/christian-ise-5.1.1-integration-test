import streamlit as st

# Set up session state variables
if "ten_x" not in st.session_state:
    # ten_x mode changes our buttons to increment and decrement by 10 instead of by 1
    st.session_state.ten_x = False

if "hundred_x" not in st.session_state:
    # hundred_x mode multiplies the step by 100.
    # ten_x and hundred_x stack: both checked means step = 1 * 10 * 100 = 1000
    st.session_state.hundred_x = False

if "count" not in st.session_state:
    st.session_state.count = 0


def get_step():
    """Return the current step size based on active multipliers."""
    step = 1
    if st.session_state.ten_x:
        step *= 10
    if st.session_state.hundred_x:
        step *= 100
    return step


# Set up callbacks for inputs
def increment():
    st.session_state.count += get_step()


def decrement():
    st.session_state.count -= get_step()
    if st.session_state.count < 0:
        # Minimum count value is zero
        st.session_state.count = 0


# Write to page
with st.expander("Options"):
    st.checkbox("10x mode", key="ten_x", value=st.session_state.ten_x)
    st.checkbox("100x mode", key="hundred_x", value=st.session_state.hundred_x)

step = get_step()
st.write(f"Total count is {st.session_state.count}")

st.button(f"plus {step}", key="increment", on_click=increment)
st.button(f"minus {step}", key="decrement", on_click=decrement)