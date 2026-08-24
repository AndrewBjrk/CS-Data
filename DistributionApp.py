import pandas as pd
import numpy as np
import streamlit as st
from cs_analysis_functions import compare_distributions

raw_data_path = '~/Desktop/CS Data/hltv_match_data_final.csv'
distributions_path = '~/Desktop/CS Data/player_distributions.parquet'

@st.cache_data
def load_data():
    rdf = pd.read_csv(raw_data_path)
    rdf = rdf[['match_id', 'game_id', 'match_url', 'date', 'team', 'player', 'map', 'kd_diff', 
                        'assists', 'kast_pct']]
    return rdf
    
@st.cache_data
def load_distributions():
    ddf = pd.read_parquet(distributions_path)
    return ddf

@st.cache_data
def get_all_players(df):
    plist = sorted(df['player'].dropna().unique().tolist())
    return plist

@st.cache_data
def get_all_maps(df):
    mlist = sorted(df['map'].dropna().unique().tolist())
    return mlist

raw_data = load_data()
all_players = get_all_players(raw_data)
all_maps = get_all_maps(raw_data)

players, maps = st.columns(2)
with players:
    player = st.selectbox('Player Name', all_players)
with maps:
    map_id = st.selectbox('Map Name', all_maps)

distribution_data = load_distributions()
if st.button("Display Actual vs. Theoretical Distributions"):
    if not player or not map_id:
        st.error("Please select a Player or a Map to proceed")
    else:
        fig1, fig2, fig3 = compare_distributions(raw_data, distribution_data, player, map_id)
        st.plotly_chart(fig1)
        st.plotly_chart(fig2)
        st.plotly_chart(fig3)
