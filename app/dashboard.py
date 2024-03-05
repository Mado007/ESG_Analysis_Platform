import plotly.graph_objs as go
from plotly.offline import plot

# Sample data for demonstration
x = ['USA', 'Canada', 'UK', 'Germany', 'France']
y = [80, 75, 70, 85, 78]

# Create a bar chart
data = [go.Bar(
            x=x,
            y=y,
            marker=dict(color='rgb(26, 118, 255)')
    )]

# Layout configuration
layout = go.Layout(
    title='ESG Scores by Country',
    xaxis=dict(title='Country'),
    yaxis=dict(title='ESG Score')
)

# Create a figure
fig = go.Figure(data=data, layout=layout)

# Plot the figure and save as an HTML file
plot(fig, filename='dashboard.html')
