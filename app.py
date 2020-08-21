import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import dash_daq as daq


#Custom python file made for data wrangling and generating the graph objects to be used
from clean_honey_data import *
import pandas as pd

#CSS style sheet used
external_stylesheets_ = ['https://codepen.io/edalrami/pen/MWKYadE.css', 'https://codepen.io/edalrami/pen/QWywwYr.css']


#import data
honey_data = pd.read_csv('all_honey_data.csv')
colony_data = pd.read_csv('all_colony_data.csv')

#----------PRE PROCESSING------------------------

#Create slider values to be used in layout
period_vals = list(colony_data.period.unique())
slider_markers = {i+1: period_vals[i] for i in range(len(period_vals))}

#colony stressors to be mapped onto choropleth map
stressors = ["varroa_mites", "other_pests", "other", "pesticides", "unknown", "diseases", "lost_perc"]

#stressors to be mapped onto multi-line chart
stressors2 = ["varroa_mites", "other_pests", "pesticides", "diseases", "lost_perc"]

#Get values for the map dropdown selector
state_dropdown = get_state_dropdown()
state_names = get_state_names()




#---------------------------------DASH LAYOUT---------------------------------------------------------
#Create dash instance to initialize app
app = dash.Dash(__name__, external_stylesheets = external_stylesheets_)
server = app.server 


app.title = "Honey Report"
app.layout = html.Div(children=[
        html.H1(children=['USDA Honey Bee Dashboard']),
        html.H2(children = 'Created by Edwin A. Ramirez'),

        #paragraph div
        #Alternative method to make this cleaner would be to be write 
        #paragraphs in text file then read it and load it 
        html.Div(
            id = 'story',
            className = 'four columns input_container mini_container',
            children = [
                    
                html.Div([
                    html.P('In 2006 the US Environmental Protection Agency (EPA)' + \
                    		' reported the high emergence of colony collapse disorder (CCD)' + \
                    		' among bee populations throughout the United States. The large' + \
                    		' number of colonies dying had no single direct cause linked at the' + \
                    		' time even after several studies attempted to suggest' +\
                    		' that the cause could be global warming, pesticides, an unknown disease,'+ \
                    		' specific parasites, etc. With such a vital' + \
                    		' role in the ecosystem as pollinators and as producers of honey,' + \
                    		' the significance of bee preservation is not something to be ignored' + \
                    		' when the consequences affect the very food that is produced in farms across the United States. ' + \
                    		' The effects of CCD are not exclusive to the honey industry. Over ten years after the CCD epidemic began' + \
                    		' researchers discovered that neonicotinoid pesticides were killing off colony' + \
                    		' populations, and the EPA responded by banning all use of known harmful pesticides' + \
                    		' to honey bee populations. However, this single stressor' + \
                    		' can not be considered the one main cause to the CCD epidemic. Since 2006, the loss in' + \
                    		' populations has decreased over time, and scientists have been documenting' + \
                    		' the stressors that are now known to harm colonies,' + \
                    		' such as varroa mites, tracheal mites, starvation, weather conditions, diseases, pesticides, etc.' + \
                    		' In 2015, the USDA began documenting and publishing data recorded on the known stressors that currently' + \
                    		' harm honey bee populations today. The data is published annually with observations per state documented' + \
                    		' quarterly. Thus, the overall goal of this data exploration is to study how the currently known stressors affect regions of the United' + \
                    		' States today, and give greater insight on the story of how these stressors affect each state individually.'),
                    	
            
                    html.P('Additionally, the United States Department of Agriculture (USDA) has been recording' +\
                    		' data on honey production per state since the 1970s. This data could be useful in analyzing the' + \
                    		' honey industry in the United States prior to the CCD outbreak and after' + \
                    		' (2000-2018). With the utilization of the USDA data that is recorded annually, a series of dynamic' + \
                    		' visualizations will be used to study where in the United States certain stressors have' + \
                    		' affected each region more than others. The first of these dynamic visualizations is the choropleth map' + \
                    		'. The map contains two dynamic features that will alter the story told by the data: The dropdown menu' + \
                    		' (includes a specific stressor to be mapped), and the slider (the quarterly time period of the data to be mapped).'),
                           
                    html.P('The dynamic line chart can provide a deeper insight on showing the progression of all stressors from 2015-2018 for a specified state. Therefore, ' +\
                		   'this visual succeeds at effectively illustrating which stressors are affecting each state over time, the percentage of colonies lost, and the max ' + \
                		   'value for each stressor indicated by a marker. Thus, by using the choropleth map for specific quarters, a user can visually see which states may be interesting ' + \
                		   'to view more in depth in the dynamic line plot.'),
                          
                    html.P('The third and final dynamic visualization is a bubble chart that switches focus to the market of the honey industry by analyzing the 10 top producing states' + \
                		   ' from 2000-2018. This visual has one dynamic feature, which is the slider that indicates the year. Each bubble is representative of a state. The legend' + \
                		   ' to the right illustrates the top 10 in order by number of colonies, where the top indicates the state with the largest population of honey bees.' + \
                		   ' The population size is also reflected in the size of each bubble to provide a better visual comparison. The y-axis is the average honey yield per colony in pounds,' + \
                		   ' while the x-axis is the average price per pound. This visual can ultimately show the transition of states in price, production, and population over 18 years of data.' +\
                		   ' Finally, hovering over any of the bubbles triggers a tooltip popup that summarizes the information about the current observation.'),
                           
                    #paragraph
                    html.Div([
                        html.H2('References'),
                        dcc.Link('Source Code', href='https://github.com/edalrami/usda-honey-dashboard'),
                        html.Br(),
                        dcc.Link('USDA Honey Production Data', href = 'https://usda.library.cornell.edu/concern/publications/hd76s004z?locale=en&page=3#release-items'),
                        html.Br(),
                        dcc.Link('USDA Honey Bee Colony Data', href = 'https://usda.library.cornell.edu/concern/publications/rn301137d?locale=en'),
                        html.Br(),
                        dcc.Link('National Pesticide Information Center', href = 'http://npic.orst.edu/envir/ccd.html'),
                    ]),
                ])
        ]),

        html.Div(
            id = 'plots-container',
            className='seven columns',
            children = [
                #div containing choropleth and dropdown
                html.Div(
                    id = 'figure1',
                    className = 'input_container mini_container',
                    children = [
                    #Dropdown selector
                    html.Div(
                        className = 'five columns',
                        children=[
                            dcc.Dropdown(
                                    id = 'dropdown1',
                                    options=[
                                        {'label': 'Varroa Mites', 'value': 'varroa_mites'},
                                        {'label': 'Pesticides', 'value': 'pesticides'},
                                        {'label': 'Other Pests (Tracheal Mites, Nosema, Wax Moths, etc)', 'value': 'other_pests'},
                                        {'label': 'Unknown', 'value': 'unknown'},
                                        {'label': 'Diseases', 'value': 'diseases'},
                                        {'label': 'Other Causes (Weather, Starvation, Queen Failure, etc)', 'value': 'other'}
                                    ],
                                    
                                    #Set default value to varroa mites
                                    value='varroa_mites'
                            ),
                    ], style={'margin-bottom':'2%'}),
            
                   
                    #Create div to contain choropleth map
                    
                    html.Div([
                            dcc.Graph(id='us-map')
                    ]),

                    html.Div(
                            children = [
                            
                                daq.Slider(
                                        id = 'slider1',
                                        min=1,
                                        max=16,
                                        marks = slider_markers,
                                        value=1,
                                        size = 700,
                                        handleLabel={"showCurrentValue":True, "label": "VALUE"}
                                ),
                    ], style={'margin-top':'5%', 'margin-left':'3%'}),
                    
                    html.Br(),
                    
        
                ]),
                            
            
                
        
                
                
        
                html.Div(
                    id='figure2',
                    className = 'input_container mini_container',
                    children = [
                    
                    #Dropdown 2
                    html.Div(
                        className = 'three columns',
                        children = [
                            dcc.Dropdown(
                                    id = 'dropdown2',
                                    options=state_dropdown,
                                    value='California'
                            ),
                        ], style={'margin-bottom':'2%'}),
            
                    #Line plot
                    html.Div([dcc.Graph(id='state-line-plot')]),
        
                ]),
        
            	 html.Div(
                    id='figure3',
                    className = 'input_container mini_container',
                    children = [
                    #div that contains bubbble chart
                	 html.Div([dcc.Graph(id='bubble-plot')]),
                	 #slider to bubble chart
                	 html.Div(
                            [
                                daq.Slider(
                                    id = 'slider2',
                              		min=2000,
                              		max=2018,
                                    marks={i: 'Label {}'.format(i) if i == 1 else str(i) for i in range(2000, 2019)},
                                    value=2000,
                                    size = 700,
                                    handleLabel={"showCurrentValue":True, "label": "VALUE"}
                                ),
                            ], style={'margin-top':'5%', 'margin-left':'3%'}), 
                            html.Br(),
                ]),
            		 	 
    	]),

])


#-------------------------CALLBACKS to udpate figures-------------------------------------------

#Create callback for us choropleth map
#The map is reactive to two inputs, which are the slider and dropdown
#Thus they are placed in a list to indicate that there are multiple inputs
#for the figure with id 'us-map'
@app.callback(
    dash.dependencies.Output('us-map', 'figure'),
    [dash.dependencies.Input('dropdown1', 'value'), dash.dependencies.Input('slider1', 'value')])
def update_map(dropdown_, slider_):
    
    for i in stressors:
        if i in dropdown_:
            #Call generate_map_object from clean_colony_data.py
            fig = generate_map_object(colony_data, slider_markers[slider_], dropdown_)
            figure = fig
    return figure



#Create callback for multiline-plot
#The plot is reactive to one input, which is dropdown selector with state names
@app.callback(
    dash.dependencies.Output('state-line-plot', 'figure'),
    [dash.dependencies.Input('dropdown2', 'value')])
def update_line_plot(dropdown_):
    
    for i in state_names:
        if i in dropdown_:
            fig = generate_line_plot(colony_data, stressors2, dropdown_)
            figure = fig
            
    return figure



#Create callback for bubble-plot
#The plot is reactive to one input, which is the slider 

@app.callback(
    dash.dependencies.Output('bubble-plot', 'figure'),
    [dash.dependencies.Input('slider2', 'value')])
def update_bubble_plot(slider_):
    
   #Call generaete_bubble_chart from clean_colony_data.py
   #value n can be adjusted for the number of data points
   #on the plot. n = 15
   figure = generate_bubble_chart(honey_data, slider_, 10)
   return figure

#---------------------launch app----------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)