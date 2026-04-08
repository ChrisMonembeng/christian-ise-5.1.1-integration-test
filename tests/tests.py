"""
Tests for ../app.py

Run from the project directory (not the tests directory) with the invocation `pytest tests/tests.py`
"""
import streamlit as st
from streamlit.testing.v1 import AppTest


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def fresh(ten_x=False, hundred_x=False, count=0) -> AppTest:
    """Return a freshly-run AppTest with the given initial session state."""
    at = AppTest.from_file("app.py").run()
    at.session_state.count = count
    at.session_state.ten_x = ten_x
    at.session_state.hundred_x = hundred_x
    return at


# ---------------------------------------------------------------------------
# 1x mode (default)
# ---------------------------------------------------------------------------

def test_button_increments_counter():
    """Increment adds 1 in default mode."""
    at = fresh(count=1)
    at.button(key="increment").click().run()
    assert at.session_state.count == 2


def test_button_decrements_counter():
    """Decrement subtracts 1 in default mode."""
    at = fresh(count=5)
    at.button(key="decrement").click().run()
    assert at.session_state.count == 4


def test_decrement_floor_at_zero_1x():
    """Decrement cannot push count below 0 in default mode."""
    at = fresh(count=0)
    at.button(key="decrement").click().run()
    assert at.session_state.count == 0


def test_decrement_floor_partial_1x():
    """Decrement clamps to 0 when count is less than the step."""
    at = fresh(count=0)
    # count is already 0; one more decrement must stay at 0
    at.button(key="decrement").click().run()
    assert at.session_state.count == 0


# ---------------------------------------------------------------------------
# 10x mode
# ---------------------------------------------------------------------------

def test_button_increments_counter_ten_x():
    """Increment adds 10 when ten_x is active."""
    at = fresh(ten_x=True, count=0)
    at.button(key="increment").click().run()
    assert at.session_state.count == 10


def test_button_decrements_counter_ten_x():
    """Decrement subtracts 10 when ten_x is active."""
    at = fresh(ten_x=True, count=20)
    at.button(key="decrement").click().run()
    assert at.session_state.count == 10


def test_decrement_floor_at_zero_ten_x():
    """Decrement cannot push count below 0 in ten_x mode."""
    at = fresh(ten_x=True, count=5)
    at.button(key="decrement").click().run()
    assert at.session_state.count == 0


def test_decrement_floor_exact_ten_x():
    """Decrement lands exactly on 0 when count equals the step."""
    at = fresh(ten_x=True, count=10)
    at.button(key="decrement").click().run()
    assert at.session_state.count == 0


# ---------------------------------------------------------------------------
# 100x mode
# ---------------------------------------------------------------------------

def test_button_increments_counter_hundred_x():
    """Increment adds 100 when hundred_x is active."""
    at = fresh(hundred_x=True, count=0)
    at.button(key="increment").click().run()
    assert at.session_state.count == 100


def test_button_decrements_counter_hundred_x():
    """Decrement subtracts 100 when hundred_x is active."""
    at = fresh(hundred_x=True, count=200)
    at.button(key="decrement").click().run()
    assert at.session_state.count == 100


def test_decrement_floor_at_zero_hundred_x():
    """Decrement cannot push count below 0 in hundred_x mode."""
    at = fresh(hundred_x=True, count=50)
    at.button(key="decrement").click().run()
    assert at.session_state.count == 0


def test_decrement_floor_exact_hundred_x():
    """Decrement lands exactly on 0 when count equals the step."""
    at = fresh(hundred_x=True, count=100)
    at.button(key="decrement").click().run()
    assert at.session_state.count == 0


# ---------------------------------------------------------------------------
# 1000x mode (ten_x + hundred_x both active — multipliers stack)
# ---------------------------------------------------------------------------

def test_button_increments_counter_thousand_x():
    """Increment adds 1000 when both ten_x and hundred_x are active."""
    at = fresh(ten_x=True, hundred_x=True, count=0)
    at.button(key="increment").click().run()
    assert at.session_state.count == 1000


def test_button_decrements_counter_thousand_x():
    """Decrement subtracts 1000 when both multipliers are active."""
    at = fresh(ten_x=True, hundred_x=True, count=2000)
    at.button(key="decrement").click().run()
    assert at.session_state.count == 1000


def test_decrement_floor_at_zero_thousand_x():
    """Decrement cannot push count below 0 with both multipliers active."""
    at = fresh(ten_x=True, hundred_x=True, count=500)
    at.button(key="decrement").click().run()
    assert at.session_state.count == 0


# ---------------------------------------------------------------------------
# Output text
# ---------------------------------------------------------------------------

def test_output_text_correct():
    """Text reflects count correctly after a mix of increment modes."""
    at = AppTest.from_file("app.py").run()

    # Initialize session state
    at.session_state.count = 0
    at.session_state.ten_x = False
    at.session_state.hundred_x = False

    # +1 at 1x
    at.button(key="increment").click().run()
    # +10 at 10x
    at.checkbox(key="ten_x").check().run()
    at.button(key="increment").click().run()
    # +100 at 100x (ten_x still on → step is 1000, not 100)
    # Uncheck ten_x first so we isolate the 100x step
    at.checkbox(key="ten_x").uncheck().run()
    at.checkbox(key="hundred_x").check().run()
    at.button(key="increment").click().run()

    # 1 + 10 + 100 = 111
    assert at.markdown[0].value == "Total count is 111"


def test_output_text_after_clamp():
    """Text shows 0 after decrement clamps the count."""
    at = fresh(count=3)
    at.button(key="decrement").click().run()
    at.button(key="decrement").click().run()
    at.button(key="decrement").click().run()
    at.button(key="decrement").click().run()  # would go negative without clamp
    assert at.markdown[0].value == "Total count is 0"