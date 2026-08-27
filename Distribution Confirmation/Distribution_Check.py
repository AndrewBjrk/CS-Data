import pandas as pd
import numpy as np
from scipy import stats

data_path = "~/Desktop/CS Data/hltv_match_data_final.csv"
raw_data = pd.read_csv(data_path)
raw_data = raw_data[['match_id', 'game_id', 'match_url', 'date', 'team', 'player', 'map', 'kd_diff', 
                     'assists', 'kast_pct', 'Round_Win_%', 'W/L', 'Rank', 'Points']]

player_ids = raw_data['player'].to_list()
player_ids = list(dict.fromkeys(player_ids))
map_ids = ['Ancient', 'Anubis', 'Dust2', 'Inferno', 'Mirage', 'Nuke']

'''
Confirm general normality of kd_diff & kast_pct distributions.
'''
'''
rng = np.random.default_rng()
ints = rng.integers(low=0, high= (len(player_ids)), size= 300).tolist()
shapiro_stats_kd = []
shapiro_stats_kast = []
shapiro_ps_kd = []
shapiro_ps_kast = []
ns = []
random_players = []
tested_map = []
for position in ints:
    player = player_ids[position]
    temp1 = raw_data.loc[(raw_data['player'] == player)]
    for map_id in map_ids:
        temp2 = temp1.loc[(temp1['map'] == map_id)]
        if len(temp2) >= 42:
            shapiro_stat_kd, shapiro_p_kd = stats.shapiro(temp2['kd_diff'])
            shapiro_stat_kast, shapiro_p_kast = stats.shapiro(temp2['kast_pct'])
            n = len(temp2)
            shapiro_stats_kd += [shapiro_stat_kd]
            shapiro_stats_kast += [shapiro_stat_kast]
            shapiro_ps_kd += [shapiro_p_kd]
            shapiro_ps_kast += [shapiro_p_kast]
            ns += [n]
            random_players += [player]
            tested_map += [map_id]
        else:
            print(f"Sample size too small for {player} on {map_id} to count towards the check.")

fdict = {'player' : random_players, 'map' : tested_map, 
         'N' : ns, 
         'Stats_kd' : shapiro_stats_kd, 'Stats_kast' : shapiro_stats_kast, 
         'P_kd' : shapiro_ps_kd, 'P_kast' : shapiro_ps_kast}
final_df = pd.DataFrame(fdict)
final_df['reject_kd'] = (final_df['P_kd'] < 0.05).astype(int)
final_df['reject_kast'] = (final_df['P_kast'] < 0.05).astype(int)
final_df.to_csv('~/Desktop/CS Data/kd_kast_run_4.csv', index= False)
'''
run1 = pd.read_csv('~/Desktop/CS Data/Distribution Confirmation/kd_kast_run_1.csv')
run2 = pd.read_csv('~/Desktop/CS Data/Distribution Confirmation/kd_kast_run_2.csv')
run3 = pd.read_csv('~/Desktop/CS Data/Distribution Confirmation/kd_kast_run_3.csv')
run4 = pd.read_csv('~/Desktop/CS Data/Distribution Confirmation/kd_kast_run_4.csv')

random_sample = pd.concat([run1, run2, run3, run4])
reject_kds_pct = []
reject_kasts_pct = []
maps = []
total_N = []
for map_id in map_ids:
    temp = random_sample.loc[(random_sample['map'] == map_id)]
    reject_kds_pct += [(temp['reject_kd'].sum() / temp['reject_kd'].count()) * 100]
    reject_kasts_pct += [(temp['reject_kast'].sum() / temp['reject_kast'].count()) * 100]
    maps += [map_id]
    total_N += [temp['N'].sum()]
fdict = {'map' : maps, 'Total Sample Size' : total_N, 'Rejected_kd_%' : reject_kds_pct, 'Rejected_kast_%' : reject_kasts_pct}
final_df = pd.DataFrame(fdict)
final_df.to_csv('~/Desktop/CS Data/Distribution Confirmation/reject_pcts.csv', index= False)

