import pandas as pd
import plotly.express as px
import plotly.graph_objs as go

def leitner_proportions(df):
    """
    Calculate proportion of cards belonging to each Leitner level.
    """
    denom = df.shape[0]
    prop_dict = {}

    for i in range(1,6):
        df_i = df[df['comfort_level'] == i]
        numer = df_i.shape[0]
        prop_dict[i] = numer / denom

    prop_df = pd.DataFrame.from_dict([prop_dict], orient='columns') 

    prop_df = prop_df.T.rename(columns={0:'proportion'})   
    
    return prop_df

def get_label_locs(prop_df):
    """
    Get Plotly 'paper' locations for labels to appear in middle of 
    visualization bars regardless of bar size.
    """
    locs = [0 for _ in range(5)]
    
    for i in range(4):
        locs[i+1] = locs[i] + prop_df['proportion'].iloc[i]
        
    for i in range(len(locs)):
        locs[i] += prop_df['proportion'].iloc[i]/2.6

    return locs


def leitner_bar(levels):
    """
    Given user's Leitner levels for a certain deck of flashcards, returns 
    Plotly JSON object for a visualization.
    TODO: Format to accept a list of integers instead of a dataframe. 
    Ultimately it would probably be better to do this without converting to a 
    dataframe at all, but weirdly I'm more comfortable working with 
    dataframes for data manipulation like this, so it was just what occurred 
    to me first.
    """

    df = pd.DataFrame(levels, columns=['comfort_level'])
    prop_df = leitner_proportions(df)
    locs = get_label_locs(prop_df)

    fig = px.bar(prop_df.T, orientation='h', width=400, height=200)
    fig.update_xaxes(
        showticklabels=False,
        showgrid=False,
        title_text='')
    fig.update_yaxes(showticklabels=False,
        showgrid=False,
        showline=False,
        zeroline=False,
        title_text='')
    fig.update_layout(
        plot_bgcolor = '#ffffff',
        showlegend = False,
        annotations=[
            dict(
            x=xval,
            y=0.5,
            text=txt,
            showarrow=False,
            xref='paper',
            yref='paper',
            font=dict(
                family='Lato',
                size=30,
                color="#000000")
            ) for xval, txt in zip(locs, prop_df.index)
        ]
        )
    fig.update_traces(marker=dict(color="#FF909A"),
                     selector=dict(name='1'))
    fig.update_traces(marker=dict(color="#EFC9ED"),
                     selector=dict(name='2'))
    fig.update_traces(marker=dict(color="#C8F5FF"),
                     selector=dict(name='3'))
    fig.update_traces(marker=dict(color="#D5E3FF"),
                     selector=dict(name='4'))
    fig.update_traces(marker=dict(color="#FFF4BD"),
                     selector=dict(name='5'))
    return fig.to_json()
