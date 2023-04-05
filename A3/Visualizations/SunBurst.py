import pandas as pd
import plotly.express as px

df = pd.read_csv("Visualizations\Visualizations\HXPC13_DI_v3_11-13-2019.csv")

updated_df = pd.DataFrame(df, columns =['gender', 'LoE_DI', 'course_id', 'grade'])
updated_df = updated_df[updated_df['grade']!=' ']
updated_df.grade = updated_df.grade.apply(pd.to_numeric)
 
# dropping the rows having NaN values
updated_df = updated_df.dropna()
updated_df.head

fig = px.sunburst(updated_df,path = ['gender', 'LoE_DI', 'course_id']
                 ,color_continuous_scale='RdBu_r', color='grade')
fig.show()