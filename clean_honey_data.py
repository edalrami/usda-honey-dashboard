import pandas as pd
import numpy as np
import plotly.graph_objects as go


us_state_abbrev = {
    'Alabama': 'AL',
    'Alaska': 'AK',
    'Arizona': 'AZ',
    'Arkansas': 'AR',
    'California': 'CA',
    'Colorado': 'CO',
    'Connecticut': 'CT',
    'Delaware': 'DE',
    'District of Columbia': 'DC',
    'Florida': 'FL',
    'Georgia': 'GA',
    'Hawaii': 'HI',
    'Idaho': 'ID',
    'Illinois': 'IL',
    'Indiana': 'IN',
    'Iowa': 'IA',
    'Kansas': 'KS',
    'Kentucky': 'KY',
    'Louisiana': 'LA',
    'Maine': 'ME',
    'Maryland': 'MD',
    'Massachusetts': 'MA',
    'Michigan': 'MI',
    'Minnesota': 'MN',
    'Mississippi': 'MS',
    'Missouri': 'MO',
    'Montana': 'MT',
    'Nebraska': 'NE',
    'Nevada': 'NV',
    'New Hampshire': 'NH',
    'New Jersey': 'NJ',
    'New Mexico': 'NM',
    'New York': 'NY',
    'North Carolina': 'NC',
    'North Dakota': 'ND',
    'Northern Mariana Islands':'MP',
    'Ohio': 'OH',
    'Oklahoma': 'OK',
    'Oregon': 'OR',
    'Palau': 'PW',
    'Pennsylvania': 'PA',
    'Puerto Rico': 'PR',
    'Rhode Island': 'RI',
    'South Carolina': 'SC',
    'South Dakota': 'SD',
    'Tennessee': 'TN',
    'Texas': 'TX',
    'Utah': 'UT',
    'Vermont': 'VT',
    'Virgin Islands': 'VI',
    'Virginia': 'VA',
    'Washington': 'WA',
    'West Virginia': 'WV',
    'Wisconsin': 'WI',
    'Wyoming': 'WY',
}


abbrev_us_state = dict(map(reversed, us_state_abbrev.items()))

def get_state_dropdown():
    dict_list= []
    for i in us_state_abbrev.keys():
        dict_list.append({'label': i, 'value': i})
    return dict_list


def get_state_names():
    return list(us_state_abbrev.keys())







def generate_map_object(input_, period_, category_):
    '''
    Returns a plotly chloropleth graph object

    input: 
        input_: A dataframe of honey_data containing
        relevant production data
        
        period_: A string value containing the year and quarter of 
                 the data to be displayed. Ex: '2015Q1'
        
        category_: The variable to be used for density on the map.
                   Can be any of the following: 
                   - varroa_mites 
                   - diseases 
                   - other 
                   - unknown 
                   - pesticides
                   - other_pests

    returns:
        fig: A chloropleth graph object

    ''' 
    
    df = input_[input_['period'] == period_]
    
    stressor_keys = {'varroa_mites': "Varroa Mites",
                 'pesticides': "Pesticides",
                 'other': 'Other Categories (Weather, Starvation, etc.)',
                 'unknown': 'Unknown Causes',
                 'other_pests': 'Other Pests (Tracheal Mites, Hive Beetles, Wax Moths, etc.)',
                'diseases': 'Diseases (Foulbrood, Chalkbrood, Stonebrood, Paralysis)'}
    
    fig = go.Figure(data=go.Choropleth(
       
        locations=df.state_code,
        z=df[category_],
        zmin = 0,
        zmax = 70,
        locationmode='USA-states',
        colorscale='Reds',
        autocolorscale=False,
        text=df.state, # hover text
        marker_line_color='white', # line markers between states
        colorbar_title="population %"
     
    ))

    fig.update_layout(
        
        height=500,
        width=800,
        title_text= 'Honey Bee Colony Populations Affected By '+ stressor_keys[category_] + " " + str(period_) + '<br>(Hover for breakdown)',
        geo = dict(
            scope='usa',
            projection=go.layout.geo.Projection(type = 'albers usa'),
            showlakes=True, # lakes
            lakecolor='rgb(255, 255, 255)'),
    )
    
    return fig


def generate_line_plot(input_, col_names, state_):
    '''
    Returns a multiline graph object of stressors for a specfic US state.
    
    input parameters:
        input_: DataFrame containing data
        col_names: Names of lines to be traced
        state_: Name of US State the
    
    output
    '''
    fig = go.Figure()
    annotations = []
    colors = ['crimson', 'LightSkyBlue', "MediumPurple", "green", "orange", "yellowgreen", "brown"]
    color_ix = 0
    for i in col_names:
        
        x_=list(input_[input_.state == state_].period)
        y_=list(input_[input_.state == state_][i])

        line_size = 4
        mode_size = 12
        color_ = colors[color_ix]

        fig.add_trace(go.Scatter(x=x_, y=y_, mode='lines',
            name=i,
            line=dict(color=color_, width=line_size),
            connectgaps=True,
            showlegend=True
        ))

        # endpoints
        max_val = max(y_)
        max_ix = x_[np.argmax(np.array(y_))]
        fig.add_trace(go.Scatter(
            x=[max_ix],
            y=[max_val],
            name=i,
            mode='markers+text',
            marker=dict(color=color_, size=mode_size),
            showlegend = False,
            text = '{}%'.format(round(max_val,2)),
            textposition = 'middle right'
        ))
        
        color_ix = color_ix + 1
        
    
    fig.update_layout(
        width = 800,
        height = 500,
        xaxis=dict(
            showline=True,
            showgrid=False,
            showticklabels=True,
            linecolor='rgb(204, 204, 204)',
            linewidth=2,
            ticks='outside',
            tickfont=dict(
                family='Arial',
                size=12,
                color='rgb(82, 82, 82)',
            ),
        ),
        yaxis=dict(
            showgrid=False,
            zeroline=False,
            showline=False,
            showticklabels=False,
        ),
        autosize=False,
        margin=dict(
            autoexpand=False,
            l=100,
            r=20,
            t=110,
        ),
        showlegend=False,
        plot_bgcolor='white'
    )

    # Title
    annotations.append(dict(xref='paper', yref='paper', x=0.0, y=1.05,
                                  xanchor='left', yanchor='bottom',
                                  text='Bee Colony Stressors in the State of ' + state_,
                                  font=dict(family='Arial',
                                            size=30,
                                            color='rgb(37,37,37)'),
                                  showarrow=False))
    # Source
    annotations.append(dict(xref='paper', yref='paper', x=0.5, y=-0.1,
                                  xanchor='center', yanchor='top',
                                  text='Source: United States Department of Agriculture (USDA)',
                                  font=dict(family='Arial',
                                            size=12,
                                            color='rgb(150,150,150)'),
                                  showarrow=False))
    
    tick_text = ["2015", "", "", "", "2016", "", "", "", "2017", "", "", "", "2018", "", "", ""]
    tick_vals = ["2015Q1", "2015Q2", "2015Q3", "2015Q4",
                 "2016Q1", "2016Q2", "2016Q3", "2016Q4", 
                 "2017Q1", "2017Q2", "2017Q3", "2017Q4", 
                 "2018Q1", "2018Q2", "2018Q3", "2018Q4"]
    fig.update_xaxes(ticktext=tick_text, tickvals = tick_vals, tickangle=0, tickfont=dict(family='Rockwell'))
    fig.update_layout(annotations=annotations, showlegend=True, legend_orientation='h', legend=dict(x=0, y=1.04))
    
    return fig


def generate_bubble_chart(input_, year_, n):
    '''
    Returns a graph object that produces a bubble chart
    
    input: 
        input_: Dataframe containing the honey production data
        year_: The year to subset the data by
        n: The top n data points
        
    returns:
        fig: Plotly graph object
    
    '''
    fig = go.Figure()
    w_ = input_[input_.year==year_].sort_values(by='honey_colonies', ascending = False).head(n).state
    x_=input_[input_.year==year_].sort_values(by='honey_colonies', ascending = False).head(n).avg_price_per_lb
    x_ = x_/100
    y_=input_[input_.year==year_].sort_values(by='honey_colonies', ascending = False).head(n).yield_per_col
    z_ = input_[input_.year==year_].sort_values(by='honey_colonies', ascending = False).head(n).honey_colonies
    
    annotations = []
    for q,i,j,k in zip(w_,x_,y_,z_):
        fig.add_trace(go.Scatter(
            x= [i],
            y= [j],
            name = str(q),
            mode='markers',
            marker=dict(
                opacity=0.6,
                size=[int(k)/5],
            ),
            showlegend = True,
            text = q + '<br>' + 'No. of Colonies: {}'.format(k) + 'k',
            textposition = 'top center'
        ))
        
     # Title
    annotations.append(dict(xref='paper', yref='paper', x=0.0, y=1.05,
                                  xanchor='left', yanchor='bottom',
                                  text='Top ' + str(n) + " Honey Producing States In the Year " + str(year_),
                                  font=dict(family='Arial',
                                            size=30,
                                            color='rgb(37,37,37)'),
                                  showarrow=False))
    # Source
    annotations.append(dict(xref='paper', yref='paper', x=0.5, y=-0.1,
                                  xanchor='center', yanchor='top',
                                  text='Source: United States Department of Agriculture (USDA)',
                                  font=dict(family='Arial',
                                            size=12,
                                            color='rgb(150,150,150)'),
                                  showarrow=False))
    
    fig.update_layout(height=600, width = 800,annotations=annotations,
                     xaxis_title = "Avg. Price Per Pound ($US)",
                     yaxis_title = "Yield Per Colony (lbs.)",
                     plot_bgcolor = 'white')
    
    return fig
