import pandas as pd
import numpy as np
from multiprocessing import Pool
import os
import plotly.graph_objects as go
import plotly.express as px
import plotly


raw_data = pd.read_csv('~/Desktop/CS Data/hltv_match_data_final.csv')
raw_data = raw_data[['match_id', 'game_id', 'map', 'date', 'team', 'Round_Win_%', 'Rank']].drop_duplicates()
game_ids = raw_data['game_id'].unique().tolist()
all_maps = ['Ancient', 'Anubis', 'Cache', 'Dust2', 'Inferno', 'Mirage', 'Nuke']

def multi_match(df, list_games):
    fin_games = []
    fin_maps = []
    fin_round_win_pcts = []
    fin_rank_diff = []
    for game in list_games:
        temp1 = df.loc[(df['game_id'] == game)]
        map_id = temp1['map'].iloc[0]
        teams = temp1['team'].unique().tolist()
        if len(teams) > 1:
            teamA = teams[0]
            teamB = teams[1]

            rankA = temp1['Rank'].loc[(temp1['team'] == teamA)].iloc[0]
            rankB = temp1['Rank'].loc[(temp1['team'] == teamB)].iloc[0]
            rank_diff = rankA - rankB
            round_win_pct = temp1['Round_Win_%'].loc[(temp1['team'] == teamA)].iloc[0]
            fin_games += [game]
            fin_maps += [map_id]
            fin_round_win_pcts += [round_win_pct]
            fin_rank_diff += [rank_diff]
        else:
            print(f"{game} only has 1 team listed in the match. Skipping {game}.")

    findict = {'game_id' : fin_games, 'map' : fin_maps, 'Round_Win_%' : fin_round_win_pcts, 'Rank_Diff' : fin_rank_diff}
    findf = pd.DataFrame(findict)

    return findf

n_splits = os.cpu_count() - 2
game_chunks = np.array_split(game_ids, n_splits)

if __name__ == "__main__":
    with Pool(processes= n_splits) as pool:
        results = pool.starmap(multi_match, [(raw_data, chunk) for chunk in game_chunks])
    final_df = pd.concat(results, ignore_index= True)
    final_df.to_csv('~/Desktop/CS Data/RoundWin%_vs_RankDiff.csv', index= False)

del raw_data, game_ids, n_splits, game_chunks

raw_data = pd.read_csv('~/Desktop/CS Data/RoundWin%_vs_RankDiff.csv')
figs = []
img_paths = []
for map_name in all_maps:
    temp = raw_data.loc[(raw_data['map'] == map_name)]
    img_paths += [f"/Users/bjrk/Desktop/CS Data/Round Win Pct & Rank Diff/{map_name}_RoundWin_RankDiff.png", f"/Users/bjrk/Desktop/CS Data/Round Win Pct & Rank Diff/{map_name}_RoundWin_RankDiff_hist.png"]

    fig = go.Figure()
    fig2 = go.Figure()
    fig.add_trace(go.Scatter(x= temp['Rank_Diff'], y= temp['Round_Win_%'],
                                                name= 'Round_Win_% vs. Rank_Diff ' + map_name,
                                                mode= 'markers'))

    fig2.add_trace(go.Histogram(x= temp['Rank_Diff'], y= temp['Round_Win_%'],
                                                histnorm= 'probability density', 
                                                name= 'Round_Win_% vs. Rank_Diff  ' + map_name))
    
    figs += [fig, fig2]
plotly.io.write_images(figs, img_paths)