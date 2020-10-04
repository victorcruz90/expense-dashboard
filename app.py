import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
from datetime import datetime as dt


app = dash.Dash(__name__, title='Rec-Vic Expenses')

dateparse = lambda x: dt.strptime(x, '%Y-%m-%d')
df = pd.read_csv('./data/processed/final.csv', parse_dates=['date'], date_parser=dateparse)
df.drop('account_balance',axis=1, inplace=True)


app.layout = html.Div([
    html.H1(id='title', children=['Expense Dashboard'], style={'textAlign': 'center'}),
    html.Div(id='filtering-expense',
    children=[
        dcc.Dropdown(
            id='expense-dropdown',
            options=[
                {'label': 'All expenses', 'value': 'ALL'},
                {'label': 'Monthly total', 'value': 'M'},
                {'label': 'Fornightly total', 'value': '2W'},
            ],
            value='ALL',
            placeholder='Group Expenses...',
            style={'width': '55%', 'align': 'center', ''},
            clearable=False,
        )]),
    html.Div(id='table-to-filter',
    children=[
        dash_table.DataTable(
            id='table',
            style_table={'width': '20%', 'align': 'center' },
            style_header={'font-style': 'oblique', 'background-color':'black', 'color':'white'},
            style_cell={'textAlign': 'center', 'fontFamily': 'Georgia, serif', 'color': 'navy'}

        )
        ])   
])
@app.callback([
    Output('table','data'),
    Output('table' ,'columns')],
    [Input('expense-dropdown', 'value')])
def filter_table(expense):
    if expense == 'ALL':
        df2 = df
        df2['Date'] = df2['date'].apply(lambda x : '{}-{}-{}'.format(x.day,x.month_name(),x.year))
        return df2.to_dict('records'), [{'id': c, 'name': c.capitalize()} for c in df2.columns if c != 'date']       
    else:
        dff = df[['date','value']].groupby(pd.Grouper(key='date', freq=expense)).sum().reset_index(level='date')
        dff['date'] = dff['date'].dt.month_name()
        return dff.to_dict('records'), [{'id': c, 'name': c.capitalize()} for c in dff.columns]
            

            
if __name__ == "__main__":
    app.run_server(debug=True)