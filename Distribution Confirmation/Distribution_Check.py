import pandas as pd
import numpy as np
from scipy import stats
from scipy.stats import poisson, chi2, chisquare

data_path = "~/Desktop/CS Data/hltv_match_data_final.csv"
raw_data = pd.read_csv(data_path)
raw_data = raw_data[['match_id', 'game_id', 'match_url', 'date', 'team', 'player', 'map', 'kd_diff', 
                     'assists', 'kast_pct', 'Round_Win_%', 'W/L', 'Rank', 'Points']]

player_ids = raw_data['player'].to_list()
player_ids = list(dict.fromkeys(player_ids))
map_ids = ['Ancient', 'Anubis', 'Dust2', 'Inferno', 'Mirage', 'Nuke']


#Test normality of kd_diff & kast_pct distributions

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
'''

#Test assists distribution for Poisson compatability

def possion_dispersion_test(df):
    n = len(df)
    xbar = df['assists'].mean()
    s2 = df['assists'].var(ddof= 1)
    D = (n - 1) * s2 / xbar
    p = 2 * min(chi2.cdf(D, n - 1), chi2.sf(D, n - 1))
    return D, p, s2 / xbar

def poisson_chisquare_gof(df, min_expected=5):
    n = len(df)
    lam = df['assists'].mean()
    kmax = int(df['assists'].max())
    obs = np.bincount(df['assists'].to_numpy(), minlength= kmax + 1).astype(float)
    exp = np.empty(kmax + 1)
    exp[:kmax] = n * poisson.pmf(np.arange(kmax), lam)
    exp[kmax] = n * poisson.sf(kmax - 1, lam)

    o, e = list(obs), list(exp)
    while len(e) > 2 and e[-1] < min_expected:
        e[-2] += e[-1]; o[-2] += o[-1]; e.pop(); o.pop()
    while len(e) > 2 and e[0] < min_expected:
        e[1] += e[0]; o[1] += o[0]; e.pop(0); o.pop(0)

    o, e = np.array(o), np.array(e)
    e *= o.sum() / e.sum()
    stat, p = chisquare(o, e, ddof= 1)
    return stat, p, len(e)
'''
rng = np.random.default_rng()
ints = rng.integers(low=0, high= (len(player_ids)), size= 300).tolist()
fin = []
for position in ints:
    player = player_ids[position]
    temp1 = raw_data.loc[(raw_data['player'] == player)]
    for map_id in map_ids:
        temp2 = temp1.loc[(temp1['map'] == map_id)]
        if len(temp2) < 42:
            print(f"Sample size too small for {player} on {map_id} to count towards the check.")
        else:
            D, p_disp, vmr = possion_dispersion_test(temp2)
            chi_stat, p_chi, nbins = poisson_chisquare_gof(temp2)
            fin.append({'player' : player, 'map' : map_id, 'N' : len(temp2),
                        'lambda' : temp2['assists'].mean(), 'VMR' : vmr,
                        'Disp_Stat' : D, 'P_disp' : p_disp, 
                        'Chi_stat' : chi_stat, 'P_chi' : p_chi, 'n_bins' : nbins,
                        'reject_disp' : int(p_disp < 0.05),
                        'reject_chi' : int(p_chi < 0.05)})
final_df = pd.DataFrame(fin)
final_df.to_csv('~/Desktop/CS Data/Distribution Confirmation/assists_run_4.csv', index= False)
'''

'''
run1 = pd.read_csv('~/Desktop/CS Data/Distribution Confirmation/assists_run_1.csv')
run2 = pd.read_csv('~/Desktop/CS Data/Distribution Confirmation/assists_run_2.csv')
run3 = pd.read_csv('~/Desktop/CS Data/Distribution Confirmation/assists_run_3.csv')
run4 = pd.read_csv('~/Desktop/CS Data/Distribution Confirmation/assists_run_4.csv')

random_sample = pd.concat([run1, run2, run3, run4])
out = []
for map_id in map_ids:
    temp = random_sample.loc[(random_sample['map'] == map_id)]
    out.append({'map' : map_id, 
                'Total Sample Size' : temp['N'].sum(),
                '#_Cells' : len(temp),
                'Rejected_disp_%' : temp['reject_disp'].mean() * 100,
                'Rejected_chi_%' : temp['reject_chi'].mean() * 100,
                'Mean_VMR' : temp['VMR'].mean(),
                'Median_VMR' : temp['VMR'].median(),
                'Overdispersed_%' : (temp['VMR'] > 1).mean() * 100})
final_df = pd.DataFrame(out)
final_df.to_csv('~/Desktop/CS Data/Distribution Confirmation/assists_reject_pcts.csv', index= False)

assists_rejects_pcts.csv shows that assists do NOT follow a Poisson distribution. They are consistently overdispersed,
meaning it makes sense to test for a Negative Binomial Distribution instead. 
These files are moved to /Poisson Disproven/ for clarity.
'''