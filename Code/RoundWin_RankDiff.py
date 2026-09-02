import pandas as pd
import numpy as np
from multiprocessing import Pool
import os
import plotly.graph_objects as go
import plotly.express as px
import plotly

all_maps = ['Ancient', 'Anubis', 'Cache', 'Dust2', 'Inferno', 'Mirage', 'Nuke']

def multi_match(df, list_games):
    fin_games = []
    fin_maps = []
    fin_team_A = []
    fin_team_B = []
    fin_round_win_pcts_a = []
    fin_round_win_pcts_b = []
    fin_rank_diff_a = []
    fin_rank_diff_b = []
    for game in list_games:
        temp1 = df.loc[(df['game_id'] == game)]
        map_id = temp1['map'].iloc[0]
        teams = temp1['team'].unique().tolist()
        if len(teams) > 1:
            teamA = teams[0]
            teamB = teams[1]

            rankA = temp1['Rank'].loc[(temp1['team'] == teamA)].iloc[0]
            rankB = temp1['Rank'].loc[(temp1['team'] == teamB)].iloc[0]
            rank_diff_A = rankA - rankB
            rank_diff_B = (-1) * rank_diff_A
            round_win_pct_A = temp1['Round_Win_%'].loc[(temp1['team'] == teamA)].iloc[0]
            round_win_pct_B = 1 - round_win_pct_A
            fin_games += [game]
            fin_maps += [map_id]
            fin_team_A += [teamA]
            fin_team_B += [teamB]
            fin_round_win_pcts_a += [round_win_pct_A]
            fin_round_win_pcts_b += [round_win_pct_B]
            fin_rank_diff_a += [rank_diff_A]
            fin_rank_diff_b += [rank_diff_B]
        else:
            print(f"{game} only has 1 team listed in the match. Skipping {game}.")

    findict = {'game_id' : fin_games, 'map' : fin_maps,
               'Team_A' : fin_team_A, 'Team_B' : fin_team_B, 
               'A_Round_Win_%' : fin_round_win_pcts_a, 'B_Round_Win_%' : fin_round_win_pcts_b, 
               'A_Rank_Diff' : fin_rank_diff_a, 'B_Rank_Diff' : fin_rank_diff_b}
    findf = pd.DataFrame(findict)

    return findf

def multi_team(df, list_teams, list_maps):
    df_stack = pd.DataFrame()
    for team in list_teams:
        for map_id in list_maps:
            temp1 = df[['game_id', 'map', 'Team_A', 'A_Round_Win_%', 'A_Rank_Diff']].loc[(df['Team_A'] == team) & (df['map'] == map_id)]
            temp1 = temp1.rename(columns= {'Team_A' : 'team', 'A_Round_Win_%' : 'Round_Win_%', 'A_Rank_Diff' : 'Rank_Diff'})
            temp2 = df[['game_id', 'map', 'Team_B', 'B_Round_Win_%', 'B_Rank_Diff']].loc[(df['Team_B'] == team) & (df['map'] == map_id)]
            temp2 = temp2.rename(columns= {'Team_B' : 'team', 'B_Round_Win_%' : 'Round_Win_%', 'B_Rank_Diff' : 'Rank_Diff'})
            df_stack = pd.concat([df_stack, temp1, temp2], ignore_index= True)
    return df_stack



if __name__ == "__main__":
    raw_data = pd.read_csv('~/Desktop/CS Data/hltv_match_data_final.csv')
    raw_data = raw_data[['match_id', 'game_id', 'map', 'date', 'team', 'Round_Win_%', 'Rank']].drop_duplicates()
    game_ids = raw_data['game_id'].unique().tolist()

    n_splits = os.cpu_count() - 2
    game_chunks = np.array_split(game_ids, n_splits)

    with Pool(processes= n_splits) as pool:
        results = pool.starmap(multi_match, [(raw_data, chunk) for chunk in game_chunks])
    final_df = pd.concat(results, ignore_index= True)
    final_df.to_csv('~/Desktop/CS Data/Round Win Pct & Rank Diff/RoundWin%_vs_RankDiff.csv', index= False)

    raw_data = pd.read_csv('~/Desktop/CS Data/Round Win Pct & Rank Diff/RoundWin%_vs_RankDiff.csv')
    figs = []
    img_paths = []
    fig3 = go.Figure()
    colors = px.colors.qualitative.Plotly
    i = 0
    for map_name in all_maps:
        temp = raw_data.loc[(raw_data['map'] == map_name)]
        img_paths += [f"/Users/bjrk/Desktop/CS Data/Round Win Pct & Rank Diff/{map_name}_RoundWin_RankDiff.png", 
                    f"/Users/bjrk/Desktop/CS Data/Round Win Pct & Rank Diff/{map_name}_RoundWin_RankDiff_hist.png"]

        fig = go.Figure()
        fig2 = go.Figure()
        fig.add_trace(go.Scatter(x= temp['A_Rank_Diff'], y= temp['A_Round_Win_%'],
                                                    name= 'Round_Win_% vs. Rank_Diff ' + map_name,
                                                    mode= 'markers'))

        fig2.add_trace(go.Histogram(x= temp['A_Rank_Diff'], y= temp['A_Round_Win_%'],
                                                    histnorm= 'probability density', 
                                                    name= 'Round_Win_% vs. Rank_Diff  ' + map_name))
        fig3.add_trace(go.Histogram(x= temp['A_Rank_Diff'], y= temp['A_Round_Win_%'],
                                                        histnorm= 'probability density', 
                                                        name= 'Round_Win_% vs. Rank_Diff ' + map_name,
                                                        marker_color= colors[i]))
        figs += [fig, fig2]
        i += 1
    figs += [fig3]
    img_paths += [f"/Users/bjrk/Desktop/CS Data/Round Win Pct & Rank Diff/All_Maps_RoundWin_RankDiff_hist.png"]
    plotly.io.write_images(figs, img_paths)

    teams = ['Spirit', 'Falcons', 'FUT', 'MOUZ',
                'Legacy', 'FURIA', 'Vitality', 'G2', '9z',
                'FaZe', 'Natus Vincere', 'BetBoom', 'Aurora',
                'BIG', 'PARAVISION', 'The MongolZ', 'B8', 
                'Astralis', 'MIBR', 'Liquid', 'Alliance',
                'magic', 'GamerLegion', 'Inner Circle', 'HOTU', 'TYLOO',
                'Ninjas in Pyjamas', 'HEROIC', 'JiJieHao', 'DENDELE']

    raw_data = pd.read_csv('~/Desktop/CS Data/Round Win Pct & Rank Diff/RoundWin%_vs_RankDiff.csv')
    raw_data = multi_team(raw_data, teams, all_maps)
    raw_data.to_csv('~/Desktop/CS Data/Round Win Pct & Rank Diff/Team_Stacked.csv')

    raw_data = pd.read_csv('~/Desktop/CS Data/Round Win Pct & Rank Diff/Team_Stacked.csv')

    img_paths = []
    figs = []
    for team in teams:
        fig = go.Figure()
        i = 0
        for map_id in all_maps:
            fig2 = go.Figure()
            file_path = f"/Users/bjrk/Desktop/CS Data/Team Data/{team}/RoundWin_RankDiff"
            os.makedirs(file_path, exist_ok= True)
            temp = raw_data.loc[(raw_data['team'] == team) & (raw_data['map'] == map_id)]

            fig2.add_trace(go.Histogram(x= temp['Rank_Diff'], y= temp['Round_Win_%'],
                                                    histnorm= 'probability density', 
                                                    name= 'Round_Win_% vs. Rank_Diff  ' + team + ' ' + map_id))
            fig.add_trace(go.Histogram(x= temp['Rank_Diff'], y= temp['Round_Win_%'],
                                                        histnorm= 'probability density', 
                                                        name= 'Round_Win_% vs. Rank_Diff ' + team + ' ' + map_id,
                                                        marker_color= colors[i]))
            i += 1

            img_paths += [f"/Users/bjrk/Desktop/CS Data/Team Data/{team}/RoundWin_RankDiff/{team}_{map_id}.png"]
            figs += [fig2]
        img_paths += [f"/Users/bjrk/Desktop/CS Data/Team Data/{team}/RoundWin_RankDiff/{team}_All_Maps.png"]
        figs += [fig]

    plotly.io.write_images(figs, img_paths)
