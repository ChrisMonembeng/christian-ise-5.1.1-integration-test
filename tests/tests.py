"""
Tests for ../app.py

Run from the project directory (not the tests directory) with the invocation `pytest tests/tests.py`
"""
import sys
import logging
import warnings
import io
from contextlib import redirect_stderr
from pathlib import Path
import streamlit as st
from streamlit.testing.v1 import AppTest

sys.path.append(str(Path(__file__).resolve().parent.parent))
logging.getLogger("streamlit").setLevel(logging.ERROR)
warnings.filterwarnings("ignore")

from contextlib import redirect_stdout, redirect_stderr

with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
    from app import increment, decrement

def test_button_increments_counter():
    """Test that the counter increments when the button is clicked."""
    at = AppTest.from_file("app.py").run()

    # Initialize the session state.
    # Note that we use at.session_state, not st.session_state. This is the testing session_state object.
    at.session_state.count = 1

    # Click the button
    at.button(key="increment").click().run()

    # Assert that the counter has been incremented
    assert at.session_state.count == 2

def test_button_decrements_counter():
    # TODO test that the decrement button works
    pass

def test_button_increments_counter_ten_x():
    # TODO test that the increment button works in ten_x mode
    pass

def test_button_decrements_counter_ten_x():
    # TODO test that the decrement button works in ten_x mode
    pass

def test_output_text_correct():
    """Test that the text shows the correct value."""
    at = AppTest.from_file("app.py").run()

    # Initialize session state
    at.session_state.count = 0
    at.session_state.ten_x = False

    # Increment once at 1x, once at 10x.
    at.button(key="increment").click().run()
    at.checkbox(key="ten_x").check().run()
    at.button(key="increment").click().run()

    # Check text value
    assert at.markdown[0].value == "Total count is 11"

# def test_unit_increment_logic():
#     """
#     Unit test:
#     Tests only the increment logic in isolation.
#     No Streamlit app, no button click, no rerender.
#     """
#     print("\n[UNIT TEST]")
#     print("A unit test checks a small piece of logic in isolation.")
#     print("Here, we are only testing: given count=0 and ten_x=False, what should increment return?")

#     st.session_state.count = 0
#     st.session_state.ten_x = False
#     increment()
#     result = st.session_state.count

#     print(f"Input: count=0, ten_x=False")
#     print(f"Expected output: 1")
#     print(f"Actual output: {result}")

#     assert result == 1


# def test_component_increment_button():
#     """
#     Component test:
#     Tests that the increment button component triggers its callback
#     and updates the app state correctly.
#     """
#     print("\n[COMPONENT TEST]")
#     print("A component test checks one UI element and its behavior.")
#     print("Here, we are testing the increment button itself.")
#     print("Flow: initial count=1 -> click increment button -> count should become 2")

#     at = AppTest.from_file("app.py").run()

#     # Initialize only the needed state for this button behavior
#     at.session_state.count = 1
#     at.session_state.ten_x = False

#     print(f"Before click: count={at.session_state.count}, ten_x={at.session_state.ten_x}")

#     at.button(key="increment").click().run()

#     print(f"After click: count={at.session_state.count}")
#     print("This test is not about the whole user journey.")
#     print("It is about whether this one button behaves correctly.")

#     assert at.session_state.count == 2


# def test_output_text_correct():
#     """
#     Integration test:
#     Tests a multi-step user flow across multiple interacting parts:
#     checkbox -> button -> session state -> rerendered output text
#     """
#     print("\n[INTEGRATION TEST]")
#     print("An integration test checks multiple parts working together.")
#     print("Here, we are testing a user flow, not just one function or one button.")
#     print("User flow:")
#     print("1. Start at count=0 in normal mode")
#     print("2. Click increment once (+1)")
#     print("3. Turn on 10x mode")
#     print("4. Click increment again (+10)")
#     print("5. Verify the page output says Total count is 11")

#     at = AppTest.from_file("app.py").run()

#     # Initialize session state
#     at.session_state.count = 0
#     at.session_state.ten_x = False

#     print(f"Initial state -> count={at.session_state.count}, ten_x={at.session_state.ten_x}")

#     # Step 1: increment once in normal mode
#     at.button(key="increment").click().run()
#     print(f"After first increment -> count={at.session_state.count}, ten_x={at.session_state.ten_x}")

#     # Step 2: enable 10x mode
#     at.checkbox(key="ten_x").check().run()
#     print(f"After enabling 10x mode -> count={at.session_state.count}, ten_x={at.session_state.ten_x}")

#     # Step 3: increment again in 10x mode
#     at.button(key="increment").click().run()
#     print(f"After second increment -> count={at.session_state.count}, ten_x={at.session_state.ten_x}")

#     # Step 4: verify rendered text
#     actual_text = at.markdown[0].value
#     print(f"Rendered output -> {actual_text}")
#     print("This is integration testing because we are validating the full interaction chain:")
#     print("widget interaction -> callback execution -> session state update -> UI output")

#     assert actual_text == "Total count is 11"