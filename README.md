This code requires a specific CSV to produce the needed gaussian and poisson distributions parquet. However, since the CSV is nearly 100MB and the parquet is over 100MB, I will not be uploading those datasets here. Please reach out to me if you want them. They are large because I built a webscraper to get all of the CS2 professional match data that I could: it is well over 500,000 rows by now.

This repository is filled with some of the exploratory code I created to gain a better understanding of basic professional CS2 metrics.

cs_analysis_functions contains methods for pulling raw stats from the CSV, transform them into a parquet with the necessary statistics to create the theoretical distributions, and compare functions for plotting actual vs. theoretical.

Raw_Distributions.ipynb is a jupyter notebook for creating the parquet. The code runs on order O(players x maps), so relatively quickly; I multiprocess over # cores - 2 to finish the process in <5 seconds (at least on my machine).

DistributionApp.py uses streamlit to overlay actual vs theoretical on a plotly graph. Since I'm on macOS, I run it through Distributions.command.

As an example, here is a comparison for NiKo on Dust2:

<img width="767" height="348" alt="image" src="https://github.com/user-attachments/assets/636b229f-b77a-47aa-9aaf-8dd1d0fc4662" />
<img width="826" height="382" alt="image" src="https://github.com/user-attachments/assets/5715fdd8-8a55-4276-aab0-7989f1e47d55" />
<img width="748" height="348" alt="image" src="https://github.com/user-attachments/assets/8b7c0035-ca5b-4b10-b431-54f4fa58bd9c" />

Understanding these distributions is key, because it allows for random sampling and Monte Carlo simulation to evaluate and predict player and team performances across a tournament.
