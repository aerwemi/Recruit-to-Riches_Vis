# import necessary libraries
import pandas as pd


from flask import (
    Flask,
    render_template,
    jsonify)

from sqlalchemy import create_engine
from sqlalchemy import inspect

engine    = create_engine("sqlite:///data/football_new.db") # SQLite DataBase 
inspector = inspect(engine) # make inpector using the engine 

def SQL2df(table):
    df = pd.DataFrame(engine.execute('SELECT * FROM ' + table).fetchall())
    columns = inspector.get_columns(table)
    columns= [c['name'] for c in columns]
    df.columns = columns
    
    return(df)

# Flask Setup
app = Flask(__name__)

### Start plot 1
@app.route("/plot1")
def plot1():
    df = SQL2df("cfb_recruits")

    df0=df.groupby(['STATE', 'STAR'])['PLAYER'].count()
    df0=df0.to_frame()
    df0=df0.reset_index()
    df0=df0.pivot(index='STATE', columns='STAR', values='PLAYER')

    df0['sum'] = df0[list(df0.columns)].sum(axis=1)
    df0.sort_values('sum', ascending=True, inplace=True)
    df0.drop('sum', axis=1, inplace=True)
    df0 = df0.fillna(0)
    df0=df0.reset_index()

    traces=[]
    for i in range(1,6):
        trace = {
            'y': df0.STATE.tolist(), # States 
            'x': df0.iloc[:,i].tolist(), #Star
            'name': i,
            'orientation': 'h',
            'type': 'bar'
            
        }
        traces.append(trace)

    return jsonify(traces)
### End Plot 1

### Start Plot2


@app.route("/plot2")
def plot2():
    df = SQL2df("cfb_recruits")

    lats=df.LAT.tolist()
    lngs=df.LNG.tolist()
    cords = [[lats[i], lngs[i]] for i in range(len(lats))]
    return jsonify(cords)

### End Plot 2

### START plot 3

@app.route("/plot3")
def plot3():
    All = int(SQL2df("cfb_recruits").PLAYER.count()) 
    drafted = int(SQL2df("drafted_recruits").PLAYER.count()) 
    notDraf = All - drafted

    trace = [
        {
        'values': [drafted, notDraf],
        'labels': ['Drafted', 'Not Drafted'],
        'type': 'pie'
        }
    ]
    return jsonify(trace)

### end plot 3
# 
#  

### START plot 4

@app.route("/plot4")
def plot4():

    cfb_recruits = SQL2df("cfb_recruits")

    allPLAYER = cfb_recruits['PLAYER'].value_counts() < 2
    allPLAYER = allPLAYER.to_frame()
    allPLAYER =  allPLAYER [allPLAYER['PLAYER'] == True]

    cr1 = cfb_recruits['PLAYER'].isin(allPLAYER.index.tolist())
    cfb_recruits = cfb_recruits[cr1]

    drafted_recruits = SQL2df("drafted_recruits")
    drafted_recruits['DRAFTED'] = 1
    drafted_recruits = drafted_recruits[['PLAYER', 'DRAFTED']]

    df3=pd.merge(cfb_recruits, drafted_recruits, on = 'PLAYER', how='left').fillna(0)

    count0=df3.groupby('STAR')['PLAYER'].count()
    count1=df3.groupby(['STAR', 'DRAFTED'])['PLAYER'].count()
    countPerC = round(count1/count0*100, 0)
    countPerC = countPerC.reset_index()
    countPerC.loc[-1] = [1, 1, 0.0]
    countPerC = countPerC.sort_values(['STAR', 'DRAFTED']).reset_index().drop('index', axis=1)

    df0=countPerC.pivot(index='STAR', columns='DRAFTED', values='PLAYER').reset_index().astype(int)
    df0.columns = ['STAR', 'Not Drafted', 'Drafted']

    traces=[]
    for i in range(1,3):
        if i == 1:
            name = 'Not Drafted'
        else:
            name = 'Drafted'
            
        trace = {
            'x': df0.STAR.tolist(), # States 
            'y': df0.iloc[:,i].tolist(), #Star
            'name': name,
            'type': 'bar'
        }
        traces.append(trace)

    return jsonify(traces)

### end plot 4

# init route 
@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
