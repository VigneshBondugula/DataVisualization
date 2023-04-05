import pandas as pd
import networkx as nx
import plotly.graph_objects as go
import plotly.express as px

def countrywise(df, country):
    df = df[df['final_cc_cname_DI'] == country]
    return df
df = pd.read_csv("Visualizations/Visualizations/HXPC13_DI_v3_11-13-2019.csv")

updated_df = df[df['certified'] == 1]
updated_df = countrywise(updated_df, "Nigeria")
G = nx.Graph()

unique_courses = updated_df['course_id'].unique()
print(len(updated_df['userid_DI'].unique()))
for course in unique_courses:
    new_df = updated_df[updated_df['course_id'] == course]
    for i in range(new_df.shape[0]):
        for j in range(new_df.shape[0]):
            if i!=j:
                u = new_df.iloc[i].userid_DI
                v = new_df.iloc[j].userid_DI
                G.add_edge(u, v)

def plotGraph(G,force_positions, layout_type):
    edge_x = []
    edge_y = []
    for edge in G.edges():
        #extract the node info of edges
        x0, y0 = force_positions[edge[0]][0],force_positions[edge[0]][1]
        x1, y1 = force_positions[edge[1]][0],force_positions[edge[1]][1]
        #update the node attributes.
        edge_x.append(x0)
        edge_x.append(x1)
        edge_x.append(None)
        edge_y.append(y0)
        edge_y.append(y1)
        edge_y.append(None)


    # get the edges to plot as a Scatter object
    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=0.5, color='#888'),
        hoverinfo='none',
        mode='lines')

    
    node_x = []
    node_y = []
    for node in G.nodes():
        x, y = force_positions[node][0],force_positions[node][1]
        node_x.append(x)
        node_y.append(y)

    # get the node trace to plot as a Scatter object.
    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers',
        hoverinfo='text',
        marker=dict(
            showscale=True,
            colorscale='Hot',
            reversescale=True,
            color=[],
            size=10,
            colorbar=dict(
                thickness=15,
                title='Node Connections',
                xanchor='left',
                titleside='right'
            ),
            line_width=2))

    # update the hover information for each node to show 
    # number of node adjacencies
    node_adjacencies = []
    node_text = []
    for node, adjacencies in enumerate(G.adjacency()):
        node_adjacencies.append(len(adjacencies[1]))
        node_text.append('# of connections: '+str(len(adjacencies[1])))

    #use the previously calculated values to colour the nodes
    node_trace.marker.color = node_adjacencies
    node_trace.text = node_text
    
    # Plot the flot with appropriate parameters.
    fig = go.Figure(data =[edge_trace,node_trace],
                    layout=go.Layout(
                    title='<br>Network graph with {} layout'.format(layout_type),
                    titlefont_size=16,
                    showlegend=False,
                    hovermode='closest',
                    margin=dict(b=20,l=5,r=5,t=40),
                    annotations=[ dict(
                        showarrow=False,
                        xref="paper", yref="paper",
                        x=0.005, y=-0.002 ) ],
                    xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                    )
    fig.show()

# Plot the network for different types of layouts.
# force_positions = nx.spring_layout(G,iterations=100,k=0.10)
# plotGraph(G,force_positions, "force directed ")

circular_positions = nx.circular_layout(G,scale=0.70)
plotGraph(G,circular_positions," circular")