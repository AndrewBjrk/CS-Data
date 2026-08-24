import pandas as pd
import numpy as np
import plotly.graph_objects as go
from scipy.stats import poisson

def stats_analysis(df, list_players, maps):
    return_df = pd.DataFrame()
    for player in list_players:
        temp1 = df.loc[(df['player'] == player)]

        lavg_kddiff = []
        lstd_kddiff = []
        lavg_assists = []
        lstd_assists = []
        lavg_kast = []
        lstd_kast = []

        for map_id in maps:
            temp2 = temp1.loc[(temp1['map'] == map_id)]

            lavg_kddiff += [temp2['kd_diff'].mean()]
            lstd_kddiff += [temp2['kd_diff'].std()]
            lavg_assists += [temp2['assists'].mean()]
            lstd_assists += [temp2['assists'].std()]
            lavg_kast += [temp2['kast_pct'].mean()]
            lstd_kast += [temp2['kast_pct'].std()]
        rdict = {'player' : player, 'map' : maps, 'avg_kd_diff' : lavg_kddiff, 'std_kd_diff' : lstd_kddiff, 
                     'avg_assists' : lavg_assists, 'std_assists' : lstd_assists, 
                     'avg_kast' : lavg_kast, 'std_kast' : lstd_kast}
        tempreturn = pd.DataFrame(rdict)
        return_df = pd.concat([return_df, tempreturn])
    return return_df

def player_distribution_creater(df, list_players, maps):
    return_df = pd.DataFrame()
    for player in list_players:
        temp1 = df.loc[(df['player'] == player)]

        ldists_kd = []
        l_kd_x = []
        ldists_assists = []
        l_assists_x = []
        ldists_kast = []
        l_kast_x = []
        for map_id in maps:
                temp2 = temp1.loc[(temp1['map'] == map_id)]
                if temp2.empty:
                    print(f"Error, {map_id} cannot be found in {player} data set.")
                    ldists_kd.append(np.nan) ; l_kd_x.append(np.nan)
                    ldists_assists.append(np.nan) ; l_assists_x.append(np.nan)
                    ldists_kast.append(np.nan) ; l_kast_x.append(np.nan)
                    continue
                avg_kd, std_kd = temp2['avg_kd_diff'].iloc[0], temp2['std_kd_diff'].iloc[0]
                dist_kd_coeff = 1 / (std_kd * np.sqrt((2 * np.pi)))
                x_kd = np.linspace(avg_kd - 4 * std_kd, avg_kd + 4 * std_kd, 200)
                l_kd_x += [x_kd]
                dist_kd_fn = np.exp((-0.5) * ((x_kd - avg_kd) / std_kd)**2)
                dist_kd = dist_kd_coeff * dist_kd_fn
                ldists_kd += [dist_kd]

                avg_assists = temp2['avg_assists'].iloc[0]
                x_assists = np.arange(0, int(avg_assists + 4*np.sqrt(avg_assists)) + 1)
                l_assists_x += [x_assists]
                dist_assists = poisson.pmf(x_assists, mu= avg_assists)
                ldists_assists += [dist_assists]

                avg_kast, std_kast = temp2['avg_kast'].iloc[0], temp2['std_kast'].iloc[0]
                dist_kast_coeff = 1 / (std_kast * np.sqrt((2 * np.pi)))
                x_kast = np.linspace(avg_kast - 4 * std_kast, avg_kast + 4 * std_kast, 200)
                l_kast_x += [x_kast]
                dist_kast_fn = np.exp((-0.5) * ((x_kast - avg_kast) / std_kast)**2)
                dist_kast = dist_kast_coeff * dist_kast_fn
                ldists_kast += [dist_kast]
                
        rdict = {'player' : player, 'map' : maps, 'kd_dist' : ldists_kd, 'kd_x' : l_kd_x,
                 'assists_dist' : ldists_assists, 'assists_x' : l_assists_x, 
                 'kast_dist' : ldists_kast, 'kast_x' : l_kast_x}
        temp_return = pd.DataFrame(rdict)
        return_df = pd.concat([return_df, temp_return])
    return return_df


def compare_distributions(df1, df2, player: str, map_id: str):
     df1 = df1.loc[((df1['player'] == player) & (df1['map'] == map_id))]
     df2 = df2.loc[((df2['player'] == player) & (df2['map'] == map_id))]

     fig1 = go.Figure()
     fig1.add_trace(go.Histogram(x= df1['kd_diff'], 
                                histnorm= 'probability density', 
                                name= 'Actual kd_diff'))

     fig1.add_trace(go.Scatter(x= df2['kd_x'].iloc[0], y= df2['kd_dist'].iloc[0],
                                     name= 'Theoretical kd_diff'))

     fig2 = go.Figure()
     max_assists = df1['assists'].max()
     fig2.add_trace(go.Histogram(x= df1['assists'], 
                                     histnorm= 'probability', 
                                     xbins=dict(start=-0.5, end=max_assists + 0.5, size=1),
                                     name= 'Actual assists'))
     
     fig2.add_trace(go.Scatter(x= df2['assists_x'].iloc[0], y= df2['assists_dist'].iloc[0],
                                          name= 'Theoretical assists'))

     fig3 = go.Figure()
     fig3.add_trace(go.Histogram(x= df1['kast_pct'], 
                                     histnorm= 'probability density', 
                                     name= 'Actual kast_pct'))
     
     fig3.add_trace(go.Scatter(x= df2['kast_x'].iloc[0], y= df2['kast_dist'].iloc[0], 
                                          name= 'Theoretical kast_pct'))

     print(f"Actual vs Theoretical distributions for {player} on {map_id}.")

     return fig1, fig2, fig3
