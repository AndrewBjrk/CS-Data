import pandas as pd
import numpy as np
from cs_analysis_functions import compare_distributions
import os
import plotly

Spirit = ['sh1ro', 'donk', 'zont1x', 'magixx', 'tN1R']
Falcons = ['karrigan', 'NiKo', 'kyousuke', 'TeSeS', 'm0NESY']
FUT = ['xfl0ud', 'Krabeni', 'dem0n', 'dziugss', 'cmtry']
MOUZ = ['torzsi', 'Spinx', 'xertioN', 'PR', 'xelex']
Legacy = ['arT', 'dumau', 'latto', 'n1ssim', 'try']
FURIA = ['FalleN', 'yuurih', 'YEKINDAR', 'KSCERATO', 'molodoy']
Vitality = ['ZywOo', 'apEX', 'flameZ', 'mezii', 'ropz']
G2 = ['huNter-', 'NertZ', 'HeavyGod', 'MATYS', 'r1nkle']
Nz = ['max', 'dgt', 'meyern', 'luchov', 'HUASOPEEK']
FaZe = ['frozen', 'Twistzz', 'Neityu', 'jcobbb', 'JBOEN']
NAVI = ['Aleksib', 'iM', 'b1t', 'w0nderful', 'makazze']
BetBoom = ['Boombl4', 'zorte', 'S1ren', 'd1ledez', 'Magnojez']
Aurora = ['XANTARES', 'woxic', 'Jimpphat', 'kyxsan', 'Wicadia']
BIG = ['tabseN', 'JDC', 'faveN', 'blameF', 'gr1ks']
PARAVISION = ['FL1T', 'Jame', 'xiELO', 'zweih', 'slaxejezzz']
MongolZ = ['bLitz', 'Techno', '910', 'tikuak', 'DarkMeister']
B8 = ['alex666', 'npl', 'kensizor', 'esenthial', 's1zzi']
Astralis = ['HooXi', 'phzy', 'jabbi', 'Staehr', 'ryu']
MIBR = ['LNZ', 'nqz', 'brnz4n', 'insani', 'venomzera']
Liquid = ['NAF', 'EliGE', 'malbsMD', 'JT', 'Jorko']
Alliance = ['twist', 'eraa', 'bobeksde', 'upE', 'avid']
magic = ['MaSvAl', 'sFade8', 'AW', 'moON', 'tenzy']
GL = ['Snax', 'REZ', 'Tauson', 'FL4MUS', 'hypex']
InnerCircle = ['cptkurtka023', 'headtr1ck', 'zeRRFIX', 'onic', 'Dawy']
HOTU = ['n0rb3r7', 'kade0', 'mizu', 'dwushka', 'frontales']
TYLOO = ['JamYoung', 'Jee', 'Mercury', 'Moseyuh', 'Zero']
NIP = ['Snappi', 'stavn', 'sjuush', 'n0te', 'xKacpersky']
HEROIC = ['Brollan', 'nilo', 'susp', 'MartinezSa', 'Chr1zN']
JJH = ['m1N1', 'sinnopsyy', 'Bibu', 'CacaNito', '0SAMAS']
DENDELE = ['gafolo', 'koala', 'maxxkor', 'rdnzao', 'doc']
references = {'Spirit' : Spirit, 'Falcons' : Falcons, 'FUT' : FUT, 'MOUZ' : MOUZ,
              'Legacy' : Legacy, 'FURIA' : FURIA, 'Vitality' : Vitality, 'G2' : G2, '9z' : Nz,
              'FaZe' : FaZe, 'Natus Vincere' : NAVI, 'BetBoom' : BetBoom, 'Aurora' : Aurora,
              'BIG' : BIG, 'PARAVISION' : PARAVISION, 'The MongolZ' : MongolZ, 'B8' : B8, 
              'Astralis' : Astralis, 'MIBR' : MIBR, 'Liquid' : Liquid, 'Alliance' : Alliance,
              'magic' : magic, 'GamerLegion' : GL, 'Inner Circle' : InnerCircle, 'HOTU' : HOTU, 'TYLOO' : TYLOO,
              'Ninjas in Pyjamas' : NIP, 'HEROIC' : HEROIC, 'JiJieHao' : JJH, 'DENDELE' : DENDELE}

raw_data = pd.read_csv('~/Desktop/CS Data/hltv_match_data_final.csv')
player_distributions = pd.read_parquet('~/Desktop/CS Data/player_distributions.parquet')
all_maps = ['Ancient', 'Anubis', 'Cache', 'Dust2', 'Inferno', 'Mirage', 'Nuke']

image_paths = []
figs = []
for team, players in references.items():
    file_path = f"/Users/bjrk/Desktop/CS Data/Team Data/{team}"
    os.makedirs(file_path, exist_ok= True)
    for player in players:
        fig1, fig2, fig3 = compare_distributions(raw_data, player_distributions, player, all_maps)
        figs += [fig1, fig2, fig3]
        image_paths += [f"{file_path}/{player}_kd_diff_dists.png"]
        image_paths += [f"{file_path}/{player}_assists_dists.png"]
        image_paths += [f"{file_path}/{player}_kast_dists.png"]
plotly.io.write_images(figs, image_paths)

