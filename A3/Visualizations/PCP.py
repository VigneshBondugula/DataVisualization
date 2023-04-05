import pandas as pd
import plotly.express as px

df = pd.read_csv("Visualizations/Visualizations/HXPC13_DI_v3_11-13-2019.csv")

def cat_to_num(df, col_names):
    for col_name in col_names:
        lunique = df[col_name].unique()
        mapping = {}
        for idx, name in enumerate(lunique):
            mapping[name] = idx
        
        df[col_name].replace(to_replace=mapping, inplace = True)

updated_df = pd.DataFrame(df, columns =['gender', 'LoE_DI', 'YoB', 'course_id', 'grade'])
updated_df = updated_df.dropna()
updated_df = updated_df[updated_df.grade != '0']
updated_df = updated_df[updated_df.grade != ' ']
updated_df.grade = updated_df.grade.apply(pd.to_numeric)
cat_to_num(updated_df, ['gender', 'LoE_DI', 'course_id'])
# print(updated_df.head)


fig = px.parallel_coordinates(updated_df,
                              color="course_id",
                              dimensions = ['gender', 'LoE_DI', 'YoB', 'grade']
                             )
fig.show()