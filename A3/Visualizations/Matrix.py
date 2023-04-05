import pandas as pd
import networkx as nx
import plotly.graph_objects as go
import plotly.express as px

df = pd.read_csv("Visualizations/Visualizations/HXPC13_DI_v3_11-13-2019.csv")
updated_df = pd.DataFrame(df, columns=['grade', 'nevents', 'ndays_act' , 'nchapters', ])
updated_df = updated_df[updated_df['grade'] != ' ']
updated_df['grade'] = pd.to_numeric(updated_df['grade'])
updated_df = updated_df.dropna()
matrix = updated_df.corr()
print(matrix)
fig = px.imshow(matrix, x=['grade', 'nevents', 'ndays_act', 'nchapters'], y=['grade', 'nevents', 'ndays_act', 'nchapters'], color_continuous_scale='Bluered', aspect="auto")
fig.show()