import streamlit as st, subprocess

st.set_page_config(page_title="Prematch Trader", layout="centered")
st.title("Prematch Trader — Dashboard")

strategy = st.selectbox("Strategia", ["steam_chaser","mean_reversion"])
data_file = st.text_input("Percorso CSV", "data/sample_data.csv")

if st.button("Esegui Backtest"):
    try:
        out = subprocess.check_output(
            ["prematch-trader","backtest","--strategy", strategy, "--data", data_file],
            text=True
        )
        st.subheader("Output")
        st.text(out)
    except subprocess.CalledProcessError as e:
        st.error(e.output or str(e))
