# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.


from dash import Dash, dcc, html
import pandas as pd
import plotly.graph_objs as go
from dash.dependencies import Input, Output

app = Dash(__name__)

# Read csv file
df = pd.read_csv("processed_data.csv")
df = df.sort_values(by="date")

df['sales'] = df['sales'].astype(float)
df['sales_display'] = df['sales'].apply(lambda x: f"{x:.2f}")

# Sales per region
df_region_sales = df.groupby(['date', 'region'], as_index=False)['sales'].sum()

# Total sales on day
df_total_sales = df.groupby(['date'], as_index=False)['sales'].sum()
df_total_sales['region'] = 'Total'

# Initial
fig = go.Figure()

fig.add_trace(go.Scatter(
    x=df_total_sales['date'],
    y=df_total_sales['sales'],
    mode='lines',
    name='Total',
    hovertemplate='<b>Date</b>: %{x|%d %b, %Y}' + '<br>' +
    '<b>Sales</b>: $%{y:.2f}<extra></extra>',
))

fig.update_layout(
    title=f"Sales Over Time - Total",
    xaxis_title="Date",
    xaxis_tickformat='%B %Y',
    xaxis=dict(
        tickmode="linear",
        dtick="M6"
    ),
    yaxis_title="Sales ($)",
    width=1200,
    height=600,
)


@app.callback(
    Output('line-chart', 'figure'),
    [Input('region-filter', 'value')]
)
def update_graph(selected_region):
    if selected_region == 'Total':
        filtered_df = df_total_sales
    else:
        filtered_df = df_region_sales[df_region_sales['region'] ==
                                      selected_region.lower()]

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=filtered_df['date'],
        y=filtered_df['sales'],
        mode='lines',
        name='Total',
        hovertemplate='<b>Date</b>: %{x|%d %b, %Y}' + '<br>' +
        '<b>Sales</b>: $%{y:.2f}<extra></extra>',
    ))

    fig.update_layout(
        title=f"Sales Over Time - {selected_region.capitalize()}",
        xaxis_title="Date",
        xaxis_tickformat='%B %Y',
        xaxis=dict(
            tickmode="linear",
            dtick="M6",
        ),
        yaxis_title="Sales ($)",
        width=1200,
        height=600,
    )

    return fig


app.layout = html.Div(style={'display': 'flex', 'flexDirection': 'row', 'alignItems': 'center', 'justifyItems': 'center', 'fontFamily': 'Helvitica, sans-serif'}, children=[
    html.Div(
        style={'display': 'flex', 'justifyContent': 'center'},
        children=[
            dcc.Graph(
                id='line-chart',
                figure=fig,
            ),

        ]
    ),
    html.Div(
        children=[
            html.H3("Filter by region"),
            dcc.RadioItems(
                id='region-filter',
                options=[{'label': region.capitalize(), 'value': region} for region in df['region'].unique(
                )] + [{'label': 'Total', 'value': 'Total'}],
                value="Total",
                labelStyle={'display': 'inline-block', 'margin': '5px',
                            'padding': '8px', 'backgroundColor': '#f0f0f0', 'borderRadius': '8px'},
                style={'display': 'flex', 'flex-direction': 'column'}
            )
        ]
    )
])

if __name__ == '__main__':
    app.run(debug=True)
