import plotly.express as px


def plot_pie_chart(health_data):
    labels = list(health_data.keys())
    values = list(health_data.values())

    fig = px.pie(
        names=labels,
        values=values,
        title="Health Check Data",
        hole=0.3,
    )

    fig.show()
