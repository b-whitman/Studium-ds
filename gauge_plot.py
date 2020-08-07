import base64
import plotly.graph_objects as go


def gauge(x):
    """Create a gauge meter for streaks per week"""
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=x,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Streaks", 'font': {'size': 24}},
        gauge={
            'axis': {'range': [None, 7], 'tickwidth': 1,
                     'tickcolor': "darkblue"},
            'bar': {'color': "#394387"},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 2], 'color': 'rgba(255, 99, 132, 0.6)'},
                {'range': [2, 5], 'color': 'rgba(255, 206, 86, 0.6)'},
                {'range': [5, 7], 'color': 'rgba(75, 192, 192, 0.6)'}],
            'threshold': {
                'line': {'color': '#282f5f', 'width': 4},
                'thickness': 1,
                'value': x}}))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor='rgba(0,0,0,0)',
        font={
            'color': "#222851",
            'family': "Arial"})
    # return fig.write_image("templates/gauge.png")
    plot = fig.write_image("gauge.png")
    with open("gauge.png", "rb") as imageFile:
        str = base64.b64encode(imageFile.read())
        return str
