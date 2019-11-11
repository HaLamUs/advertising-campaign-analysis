import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import random
import pymongo
import datetime


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

client = pymongo.MongoClient("localhost", 27017)
db = client.lam_db

poss = []
negs = []
dates = []

def fetchTweetByDate(currentDate):
  now = datetime.date.today()
  for x in range(5):
 	yesterday = now + datetime.timedelta(days=-1*x)
 	pos = db.test_table.count_documents({"$and":[ {"fetching_hashtag":"#WGDP"}, {"datestamp":str(yesterday)}, {"sentiment":"positive"}]})
 	neg = db.test_table.count_documents({"$and":[ {"fetching_hashtag":"#WGDP"}, {"datestamp":str(yesterday)}, {"sentiment":"negative"}]})
 	poss.append(pos)
 	negs.append(neg)
 	dates.append(str(yesterday))
  return {"positive":poss, "negative":negs}
#  print(poss)
 # return {"positive":[4, 1, 2, 6, 2],
  #"negative":[2, 4, 5, 5, 8]}

def fetchRealtimeTweet(currentDate):
  poss.pop(0)
  negs.pop(0)
  pos = random.randint(1, 10)
  neg = random.randint(1, 10)
  poss.insert(0, pos)
  negs.insert(0, neg)
  return {"positive":poss, "negative":negs}
#  print(poss)
 # return {"positive":[4, 1, 2, 6, random.randint(1, 10)],
  #"negative":[2, 4, 5, 5, random.randint(1, 10)]}


def drawDashboard():
  result = fetchTweetByDate("10-14-2019")
  y1 = result["positive"]
  y2 = result["negative"]
  app.layout = html.Div(children=[
  html.H1(children='13th Group', id='first'),
  dcc.Interval(id='timer', interval=10000),
  html.Div(id='dummy'),
  dcc.Graph(
	id='example-graph',
	figure={
  	'data': [
    	{'x': [1, 2, 3, 4, 5],
      	'y': y1,
      	'type': 'bar', 'name': 'Positive'},
    	{'x': [1, 2, 3, 4, 5],
      	'y': y2,
      	'type': 'bar', 'name': 'Negative'},
  	],
  	'layout': {
    	'title': '#WGDP',
    	'xaxis': dict(tickvals = [1, 2, 3, 4, 5], ticktext = dates)
  	}
	}
  )
  ])
  @app.callback(output=Output('example-graph', 'figure'), inputs=[Input('timer', 'n_intervals')])
  def update_grapsh(n_clicks):
	result_1 = fetchRealtimeTweet("10-14-2019")
	y1_1 = result_1["positive"]
	y2_2 = result_1["negative"]
	return {  
  	'data': [
    	{'x': [1, 2, 3, 4, 5],
      	'y': y1_1,
      	'type': 'bar', 'name': 'Positive'},
    	{'x': [1, 2, 3, 4, 5],
      	'y': y2_2,
      	'type': 'bar', 'name': 'Negative'},
    	],
  	'layout': {
    	'title': '#WGDP',
    	'xaxis': dict(tickvals = [1, 2, 3, 4, 5], ticktext = dates)
  	}
	}
  app.run_server(debug=True)

drawDashboard()
