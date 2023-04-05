import pandas as pd
import plotly.express as px


df = pd.read_csv("Visualizations/Visualizations/HXPC13_DI_v3_11-13-2019.csv")
updated_df = pd.DataFrame(df, columns =['gender', 'LoE_DI', 'course_id', 'grade'])
updated_df = updated_df[updated_df['grade']!=' ']
updated_df.grade = updated_df.grade.apply(pd.to_numeric)
# dropping the rows having NaN values
updated_df = updated_df.dropna()
fig = px.treemap(updated_df, path=['gender', 'LoE_DI', 'course_id'], color='grade')
fig.update_traces(root_color="lightgrey")
fig.update_layout(margin = dict(t=50, l=25, r=25, b=25))
fig.show()