# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.


from dash import Dash, dcc, html, dash_table
import plotly.express as px
import pandas as pd
import plotly.graph_objs as go

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

# Just show total sales for now
df_combined = pd.concat([df_total_sales], ignore_index=True)

# fig = go.Figure()
# Add lines for each region
# for region in df_combined['region'].unique():
#     region_df = df_combined[df_combined['region'] == region]
#     fig.add_trace(go.Scatter(x=region_df['date'], y=region_df['sales'], mode='lines', name=region,
#                              hovertemplate='<b>Date</b>: %{x|%d %b, %Y}' + '<br>' +
#                              '<b>Sales</b>: $%{y:.2f}<extra></extra>',))

fig = go.Figure()
fig.add_trace(go.Scatter(
    x=df_combined['date'], 
    y=df_combined['sales'],
    mode='lines', 
    name='Total',
    hovertemplate='<b>Date</b>: %{x|%d %b, %Y}' + '<br>' +
                 '<b>Sales</b>: $%{y:.2f}<extra></extra>',
))

# Customize layout
fig.update_layout(
    title="Total Sales Over Time",
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

app.layout = html.Div(style={'display': 'flex', 'flexDirection': 'column'}, children=[
    html.Div(
        style={'display': 'flex', 'justifyContent': 'center'}, children=[
            dcc.Graph(
                id='line-chart',
                figure=fig
            )
        ]),

    html.Div(
        children=[
            dash_table.DataTable(
                data=df.to_dict('records'),
                columns=[
                    {'id': 'sales_display', 'name': 'sales'},
                    {'id': 'region', 'name': 'region'},
                    {'id': 'date', 'name': 'date'}
                ],
                style_table={
                    'height': '300px',
                    'overflowX': 'auto',
                },
                style_header={
                    'font-weight': 'bold'
                },
                style_cell_conditional=[
                    {
                        'if': {'column_id': c},
                        'textAlign': 'center'
                    } for c in ['sales_display', 'date', 'region']
                ],
                style_as_list_view=True
            )
        ]
    ),
])

if __name__ == '__main__':
    app.run(debug=False)
