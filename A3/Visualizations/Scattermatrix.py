import pandas as pd
import plotly.express as px

df = pd.read_csv("Visualizations/Visualizations/HXPC13_DI_v3_11-13-2019.csv")
updated_df = df[df['grade'] != '0']
updated_df = updated_df[updated_df['grade'] != ' ']
updated_df = updated_df[updated_df['nforum_posts'] != 0]
updated_df = pd.DataFrame(updated_df, columns =['grade', 'nevents', 'ndays_act', 'LoE_DI', 'nplay_video', 'nchapters'])
updated_df['grade'] = pd.to_numeric(updated_df['grade'])

# dropping the rows having NaN values
updated_df = updated_df.dropna()
print(updated_df.shape)
fig = px.scatter_matrix(updated_df,
    dimensions=['grade', 'nevents', 'ndays_act', 'nplay_video', 'nchapters'],
    color="LoE_DI",
    title="Scatter matrix of Harvard dataset",
    labels={col:col.replace('_', ' ') for col in df.columns}) # remove underscore
fig.update_traces(diagonal_visible=False)
fig.show()