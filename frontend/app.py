import os
import json
import textwrap
from typing import Optional

import httpx
import streamlit as st


BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000").rstrip("/")


def call_backend_solve(problem: str, system_prompt: Optional[str], temperature: float, max_tokens: int) -> dict:
    payload = {
        "problem": problem,
        "system_prompt": system_prompt or None,
        "temperature": float(temperature),
        "max_tokens": int(max_tokens),
    }
    with httpx.Client(timeout=60) as client:
        resp = client.post(f"{BACKEND_URL}/solve", json=payload)
        resp.raise_for_status()
        return resp.json()


st.set_page_config(page_title="Competitive Programming Assistant", page_icon="🤖", layout="wide")
st.title("Competitive Programming Assistant")
st.caption("Frontend: Streamlit · Backend: FastAPI · Model: Hosted on Colab/HF")

with st.sidebar:
    st.header("Settings")
    backend_url_input = st.text_input("Backend URL", BACKEND_URL, help="FastAPI base URL")
    if backend_url_input.strip():
        BACKEND_URL = backend_url_input.strip().rstrip("/")
    temperature = st.slider("Temperature", min_value=0.0, max_value=2.0, value=0.2, step=0.05)
    max_tokens = st.slider("Max tokens", min_value=32, max_value=4096, value=512, step=32)
    system_prompt = st.text_area(
        "System prompt (optional)",
        value="You are an expert competitive programming assistant. Provide clear, efficient solutions.",
        height=120,
    )
    st.markdown("—")
    st.caption("Tip: Ensure backend is running and COLAB_ENDPOINT is configured.")

problem = st.text_area(
    "Problem statement",
    placeholder="Paste the competitive programming problem here...",
    height=240,
)

col1, col2 = st.columns([1, 3])
with col1:
    run = st.button("Solve", type="primary", use_container_width=True)
with col2:
    example = st.button("Load example", use_container_width=True)

if example and not problem:
    example_text = textwrap.dedent(
        """
        Given an array of integers nums and an integer target, return indices of the two numbers
        such that they add up to target. You may assume that each input would have exactly one solution,
        and you may not use the same element twice. You can return the answer in any order.
        """
    ).strip()
    st.session_state["problem"] = example_text
    problem = example_text

if run:
    if not problem.strip():
        st.warning("Please provide a problem statement.")
    else:
        with st.spinner("Contacting backend and solving..."):
            try:
                result = call_backend_solve(problem, system_prompt, temperature, max_tokens)
                answer = result.get("output", "")
                raw = result.get("raw")
            except httpx.HTTPError as exc:
                st.error(f"Backend error: {exc}")
                result = None
                answer = ""
                raw = None

        if result:
            st.subheader("Answer")
            st.markdown(answer if answer else "_No answer returned._")

            with st.expander("Raw response"):
                st.code(json.dumps(result, indent=2))


