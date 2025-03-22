from dash import Dash, dcc, callback, Input, Output, html
import dash_bootstrap_components as dbc
import pandas as pd
import altair as alt
from components.data import ee_melt, ee_trend, quota_2025, ee_pool_2025
import dash_vega_components as dvc
import plotly.express as px
import plotly.graph_objects as go
#alt.data_transformers.enable('vegafusion')

# Initialization
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Components
quota_histogram = px.bar(ee_pool_2025, 
                         x='type', 
                         y='invitations_issued', 
                         labels={"type": "Draw Type", "invitations_issued": "# of Invitations Issued"}, 
                         text_auto=True)

category_positions = {category: i for i, category in enumerate(quota_2025["type"])}

for i, row in quota_2025.iterrows():
    x_pos = category_positions[row["type"]] 
    
    quota_histogram.add_shape(
        type="line",
        x0=x_pos - 0.2, x1=x_pos + 0.2, 
        y0=row["low"], y1=row["low"],
        line=dict(color="red", width=3, dash="dash") 
    )
    
    quota_histogram.add_shape(
        type="line",
        x0=x_pos - 0.2, x1=x_pos + 0.2, 
        y0=row["target"], y1=row["target"], 
        line=dict(color="brown", width=3, dash="dash") 
    )
    
    quota_histogram.add_shape(
        type="line",
        x0=x_pos - 0.2, x1=x_pos + 0.2, 
        y0=row["high"], y1=row["high"], 
        line=dict(color="green", width=3, dash="dash") 
    )



title = html.H5(
    'Express Entry',
    style={
        'padding': 10,
        'color': '#112d54',
        'text-align': 'left',
        'font-size': '28px'
    }
)
checklist_draw_type = dcc.Checklist(
    id = 'checklist_draw_type',
   options=['CEC', 'PNP', 'French', 'General', 'STEM', 'Trade', 'Agriculture', 'FSW', 'Health', 'Transport'],
   value=['CEC']
)

dropdown_category = dcc.Dropdown(
    id='dropdown_category',
    options=[
        {'label': 'CRS Score', 'value': 'CRS_score'},
        {'label': 'Invitations Issued', 'value': 'invitations_issued'}],
    clearable=False,
    value='CRS_score'
)

dropdown_draw_type = dcc.Dropdown(
    id='dropdown_draw_type',
    options=[{'label': type_, 'value': type_} for type_ in ee_trend['type'].unique()],
    value=['CEC'],
    multi=True
)

dropdown_date = dcc.Dropdown(
    id='dropdown_date',
    options=[{'label': date_, 'value': date_} for date_ in ee_melt['date'].dt.strftime('%Y-%m-%d').unique()],
    value=ee_melt['date'].dt.strftime('%Y-%m-%d').unique()[-1],
    clearable=False
)

input_widget = dcc.Input(id="user_score", type="text", placeholder="",
                         style={'border': 'none', 'border-bottom': '1px solid black', 
                                'outline': 'none', 'width': '100%', 'margin-bottom': '15px'})

sidebar = dbc.Col([
    title,
    html.H6("How about you?"),
    input_widget,
    html.Br(),
    dropdown_category,
    html.Br(),
    checklist_draw_type,
    html.Br(),
    dropdown_date
    ],
    md=2,
    style={
        'background-color': '#e4f0f4',
        'padding': 10,
        'height': '100vh', 
        'display': 'flex', 
        'flex-direction': 'column', 
    }
) 

# Layout
app.layout = dbc.Container([
    dbc.Row([
        sidebar, 
        dbc.Col([
            dbc.Row([
                dbc.Col([
                    #dvc.Vega(id='line_chart', opt={"renderer": "svg", "actions": False})
                    dcc.Graph(id='line_chart')
                ], md=10)
                ]),
            
            dbc.Row([
                dbc.Col([
                    dcc.Graph(id='histogram_score', config={'displayModeBar': False}),
                ], md=6),
                dbc.Col([
                    dcc.Graph(id='quota_histogram', figure = quota_histogram, config={'displayModeBar': False})
                ], md=6),
                
                ])
            ])
        ])
], fluid=True)

# Create line chart 
@callback(
    Output('line_chart', 'figure'),
    Input('dropdown_category', 'value'),
    Input('checklist_draw_type', 'value'),
    Input('user_score', 'value'))  
def update_line_chart(selected_cate, selected_type, user_score):
    # Filter data based on selected draw types
    filtered_ee = ee_trend[ee_trend['type'].isin(selected_type)]
    
    # Create a Plotly figure
    fig = go.Figure()

    # Add a line trace for each draw type
    for draw_type in selected_type:
        df = filtered_ee[filtered_ee['type'] == draw_type]
        fig.add_trace(go.Scatter(
            x=df['date'],
            y=df[selected_cate],
            mode='lines+markers',  # Lines and markers
            name=draw_type,  # Legend name
            line=dict(width=2),
            marker=dict(size=8),
            hovertemplate=(
                f"<b>{draw_type}</b><br>" +
                "Date: %{x|%b %Y}<br>" +
                f"{selected_cate.replace('_', ' ').title()}: %{{y}}<br>" +
                "<extra></extra>"
            )
        ))
    # Add a horizontal line if user_score is provided
    if user_score:
        try:
            user_score = float(user_score)
            fig.add_hline(
                y=user_score,
                line_dash="dash",
                line_color="red",
                annotation_text=f"Your Score: {user_score}",
                annotation_position="top left"
            )
        except ValueError:
            pass  # Ignore invalid input

    # Customize layout
    fig.update_layout(
        title=f"{selected_cate.replace('_', ' ').title()} Over Time",
        xaxis_title="Date",
        yaxis_title=selected_cate.replace('_', ' ').title(),
        font=dict(size=14),
        showlegend=True,
        legend_title="Draw Type",
        hovermode="x unified"
    )

    return fig


# # Create line chart 
# @callback(
#     Output('line_chart', 'spec'),
#     Input('dropdown_category', 'value'),
#     Input('checklist_draw_type', 'value'),
#     Input('user_score', 'value'))  
 
# def update_line_chart(selected_cate, selected_type, user_score):
#     filtered_ee = ee_trend[ee_trend['type'].isin(selected_type)]
    
#     line_chart = alt.Chart(filtered_ee).mark_line().encode(
#         x=alt.X('date:T', axis=alt.Axis(format="%b/%Y", title=None, grid=False)),
#         y=alt.Y(selected_cate, title = None, scale=alt.Scale(zero=False)),
#         color='type').properties(width=1000, height=250)
    
#     point_chart = alt.Chart(filtered_ee).mark_point(filled = True).encode(
#         x=alt.X('date:T', axis=alt.Axis(format="%b/%Y", title=None)),
#         y=alt.Y(selected_cate, title = None),
#         color=alt.Color('type', title = 'Draw Type'),
#         tooltip=["date", "type", selected_cate]).properties(width=1000, height=250).interactive()
    
#     combine_chart = line_chart + point_chart
    
#     # Horizontal Line (if user_score is entered)
#     if user_score:
#         try:
#             user_score = float(user_score) 
#             hline = alt.Chart(pd.DataFrame({'y': [user_score]})).mark_rule(
#                 color='red', strokeDash=[6, 6]  
#             ).encode(y='y:Q', size = alt.value(2))
            
#             return (combine_chart + hline).to_dict() 
#         except ValueError:
#             pass 
    
#     return combine_chart.to_dict()


#Histogram of score distribution
@callback(
    Output('histogram_score', 'figure'),
    Input('dropdown_date', 'value'))
def update_score_distribution(selected_date):    
    filtered_ee = ee_melt[ee_melt['date'] == selected_date]
    histo = px.bar(filtered_ee, x="range", y="number", labels={"range": "CRS Range", "number": "# of Candidates"})
    
    return histo

if __name__ == '__main__':
    app.run(debug=True)