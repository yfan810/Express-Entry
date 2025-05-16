from dash import Dash, dcc, callback, Input, Output, html
import dash_bootstrap_components as dbc
import pandas as pd
import altair as alt
from components.data import ee_melt, ee_trend, quota_2025, ee_pool_2025, ee_pool
import dash_vega_components as dvc
import plotly.express as px
import plotly.graph_objects as go

# Initialization
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Components
#EE score distribution histogram
quota_histogram = px.bar(ee_pool_2025, 
                         x='type', 
                         y='invitations_issued', 
                         labels={"type": "Draw Type", "invitations_issued": "# of Invitations Issued"}, 
                         text_auto=True)

quota_histogram.update_layout(
    title=dict(
        text="2025 Quota by Draw Type",
        y=0.96, 
        x=0.5,
        xanchor='center',
        yanchor='top',
        font=dict(size=16)
    ),
    margin=dict(l=50, r=50, t=40, b=40)
    )

category_positions = {category: i for i, category in enumerate(quota_2025["type"])}

for i, row in quota_2025.iterrows():
    x_pos = category_positions[row["type"]] 
    
    quota_histogram.add_shape(
        type="line",
        x0=x_pos - 0.3, x1=x_pos + 0.3, 
        y0=row["low"], y1=row["low"],
        line=dict(color="red", width=3, dash="dash") 
    )
    
    quota_histogram.add_shape(
        type="line",
        x0=x_pos - 0.3, x1=x_pos + 0.3, 
        y0=row["target"], y1=row["target"], 
        line=dict(color="brown", width=3, dash="dash") 
    )
    
    quota_histogram.add_shape(
        type="line",
        x0=x_pos - 0.3, x1=x_pos + 0.3, 
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
    value=['CEC'],
    style={'margin-top': '10px', 'margin-bottom': '10px'} 
)

dropdown_category = dcc.Dropdown(
    id='dropdown_category',
    options=[
        {'label': 'CRS Score', 'value': 'CRS_score'},
        {'label': 'Invitations Issued', 'value': 'invitations_issued'}],
    clearable=False,
    value='CRS_score'
)

#Date slider
valid_timestamps = ee_melt['timestamp'].unique()
valid_timestamps.sort() 

slider_date = dcc.Slider(
    valid_timestamps.min(),
    valid_timestamps.max(),
    step=None,
    id='slider_date',
    value=valid_timestamps.max(),
    marks= {
        int(ts): {
            'label': pd.to_datetime(ts, unit='s').strftime('%d/%m/%y'),
            'style': {'transform': 'rotate(40deg)', 'white-space': 'nowrap', 'font-size': '8px'}
        }
        for ts in valid_timestamps
    },
    updatemode='drag'
    )

input_widget = dcc.Input(id="user_score", type="text", placeholder="Your CRS...",
                         style={'border': 'none', 'border-bottom': '1px solid black', 'outline': 'none'})

input_category = dcc.RadioItems(
    id='input_category',
    options=[
        {'label': 'CRS Score', 'value': 'CRS_score'},
        {'label': 'Invitations Issued', 'value': 'invitations_issued'}
    ],
    value='CRS_score',
    labelStyle={'display': 'inline-block', 'margin-right': '10px'}
)

# Layout
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([title])
    ]),
    
    html.Hr(style={"border": "1px solid #091b33", "width": "100%"}),
    
    dbc.Row([
        dbc.Col([
            input_widget,
            html.Br(),
            #dropdown_category,
            input_category,
            html.Br(),
            checklist_draw_type
        ],md = 2),
        
        dbc.Col([
            dcc.Graph(id='line_chart', config={'displayModeBar': False}),
            ])
    ]),

        
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='histogram_score', config={'displayModeBar': False}),
            ], md=6),
        dbc.Col([
            dcc.Graph(id='quota_histogram', figure = quota_histogram, config={'displayModeBar': False})
            ], md=6),
        ]),
    
    dbc.Row([
        dbc.Col([
            slider_date
            ], md = 6)
        ])

], fluid=True)

# Create line chart 
@callback(
    Output('line_chart', 'figure'),
    #Input('dropdown_category', 'value'),
    Input('input_category', 'value'),
    Input('checklist_draw_type', 'value'),
    Input('user_score', 'value'))  
def update_line_chart(selected_cate, selected_type, user_score):
    # if not selected_type: 
    #     selected_type = ['CEC'] 
    
    # Create a Plotly figure
    fig = go.Figure()

    # Add a line trace for each draw type
    for draw_type in selected_type:
        df = ee_trend[ee_trend['type'] == draw_type]
        fig.add_trace(go.Scatter(
            x=df['date'],
            y=df[selected_cate],
            mode='lines+markers', 
            name=draw_type, 
            line=dict(width=2),
            marker=dict(size=8),
            hovertemplate=(
                f"<b>{draw_type}</b><br>" +
                "Date: %{x|%d/%m/%Y}<br>" +
                f"{selected_cate.replace('_', ' ').title()}: %{{y}}<br>" +
                "<extra></extra>"
            )
        ))
        
    # Add a horizontal line if user_score is provided
    if user_score:
        try:
            user_score = int(user_score)
            fig.add_hline(
                y=user_score,
                line_dash="dash",
                line_color="red",
                annotation_text=f"Your Score: {user_score}",
                annotation_position="top left"
            )
        except ValueError:
            pass  

    # Customize layout
    parts = selected_cate.split('_', 1)  
    first_part = parts[0].title()
    second_part = parts[1].title()
    if first_part == "Crs":
        first_part = first_part.upper() 

    fig.update_layout(
        title=dict(
                text=f"{first_part} {second_part} Over Time",
                y=0.96,
                x=0.5,
                xanchor='center',
                yanchor='top',
                font=dict(size=16)
            ),
        showlegend=True,
        legend=dict(
            orientation='h',  
            yanchor='bottom',  
            y=-0.12, 
            xanchor='center', 
            x=0.5
        ),
        margin=dict(l=50, r=50, t=40, b=40)
    )
    return fig

#Histogram of score distribution
@callback(
    Output('histogram_score', 'figure'),
    Input('slider_date', 'value')) 
def update_score_distribution(selected_timestamp):    
    filtered_ee = ee_melt[ee_melt['timestamp'] == selected_timestamp]
    histo = px.bar(filtered_ee.iloc[::-1], x="range", y="number", labels={"range": "CRS Range", "number": "# of Candidates"})
    
    histo.update_layout(
        title=dict(
            text="CRS Score Distribution",
            y=0.96, 
            x=0.5,
            xanchor='center',
            yanchor='top',
            font=dict(size=16)
            ),
        margin=dict(l=50, r=50, t=40, b=40)
        )
    
    return histo

if __name__ == '__main__':
    app.run(debug=True)