import dash
import dash_core_components as dcc
import dash_html_components as html
import csv
import psycopg2
import datetime

# ╔══════════════════════════════════════════╗
# ║ • • • • • • • GETTING DATA • • • • • • • ║
# ╚══════════════════════════════════════════╝

# Initialize
g1 = {
    'ios': {},
    'android': {}
}
g2 = {
    'ios': {},
    'android': {}
}
g3 = {
    'ios': {},
    'android': {}
}
g4 = {
    'ios': {},
    'android': {}
}
g5 = {}
g6 = {}
week_ago = datetime.datetime.today() - datetime.timedelta(days=14)

# Read DB

connection = psycopg2.connect(user="postgres",
                              password="12345",
                              host="127.0.0.1",
                              port="5433",
                              database="users")
cur = connection.cursor()
print('Connected to DB')
sql = 'SELECT * from users_test'
cur.execute(sql)
data = cur.fetchall()
for row in data:
    opt_in = False if row[4] == 'False' else True
    createDate = datetime.datetime.strptime(row[7][:10], '%Y-%m-%d')
    updateDate = datetime.datetime.strptime(row[6][:10], '%Y-%m-%d')
    userID = 'Unknown' if row[3] == '' else row[3]
    system = row[0]

    # Creating users objects
    if createDate > week_ago:

        # ==== Android / ios ( All ) =====
        if createDate not in g1[system]: g1[system][createDate] = list()
        g1[system][createDate].append({ 'userID': userID, 'opt_in': opt_in })

        # ==== All platforms ( All ) =====
        if createDate not in g6: g6[createDate] = list()
        g6[createDate].append({ 'userID': userID, 'opt_in': opt_in })

        if userID != 'Unknown' and opt_in:

            # ============ Android / ios ( Has user ) ============
            if createDate not in g2[system]: g2[system][createDate] = list()
            g2[system][createDate].append({ 'userID': userID, 'opt_in': opt_in })

            # ============ All platforms ( Has user ) ============
            if createDate not in g4: g4[createDate] = list()
            g4[createDate].append({ 'userID': userID, 'opt_in': opt_in })

        if userID == 'Unknown' and opt_in:

            # ============ Android / ios ( Has not user ) ========
            if createDate not in g3[system]: g3[system][createDate] = list()
            g3[system][createDate].append({ 'userID': userID, 'opt_in': opt_in })

            # ============ All platforms ( Has not user ) ========
            if createDate not in g5: g5[createDate] = list()
            g5[createDate].append({ 'userID': userID, 'opt_in': opt_in })

# \]

ios_x = list(map(lambda a: a[0], g1['ios'].items()))
ios_y = list(map(lambda a: len(a[1]), g1['ios'].items()))
ios_x2 = list(map(lambda a: a[0], g2['ios'].items()))
ios_y2 = list(map(lambda a: len(a[1]), g2['ios'].items()))
ios_x3 = list(map(lambda a: a[0], g3['ios'].items()))
ios_y3 = list(map(lambda a: len(a[1]), g3['ios'].items()))

android_x = list(map(lambda a: a[0], g1['android'].items()))
android_y = list(map(lambda a: len(a[1]), g1['android'].items()))
android_x2 = list(map(lambda a: a[0], g2['android'].items()))
android_y2 = list(map(lambda a: len(a[1]), g2['android'].items()))
android_x3 = list(map(lambda a: a[0], g3['android'].items()))
android_y3 = list(map(lambda a: len(a[1]), g3['android'].items()))

all_x = list(map(lambda a: a[0], g6.items()))
all_y = list(map(lambda a: len(a[1]), g6.items()))
all_x2 = list(map(lambda a: a[0], g4.items()))
all_y2 = list(map(lambda a: len(a[1]), g4.items()))
all_x3 = list(map(lambda a: a[0], g5.items()))
all_y3 = list(map(lambda a: len(a[1]), g5.items()))

app = dash.Dash(__name__)

app.layout = html.Div(children=[
    dcc.Graph(
        id='Ios',
        figure={
            'data': [
                {'x': ios_x, 'y': ios_y, 'type': 'bar', 'name': 'Ios all users'},
                {'x': ios_x2, 'y': ios_y2, 'type': 'bar', 'name': 'Pushes on and has userID'},
                {'x': ios_x3, 'y': ios_y3, 'type': 'bar', 'name': 'Pushes on and has no userID'}
            ],
            'layout': {
                'title': 'Ios'
            }
        }
    ),
    dcc.Graph(
        id='Android',
        figure={
            'data': [
                {'x': android_x, 'y': android_y, 'type': 'bar', 'name': 'Android all users'},
                {'x': android_x2, 'y': android_y2, 'type': 'bar', 'name': 'Pushes on and has userID'},
                {'x': android_x3, 'y': android_y3, 'type': 'bar', 'name': 'Pushes on and has no userID'}
            ],
            'layout': {
                'title': 'Android'
            }
        }
    ),
    dcc.Graph(
        id='All',
        figure={
            'data': [
                {'x': all_x, 'y': all_y, 'type': 'bar', 'name': 'all users'},
                {'x': all_x2, 'y': all_y2, 'type': 'bar', 'name': 'Pushes on and has userID'},
                {'x': all_x3, 'y': all_y3, 'type': 'bar', 'name': 'Pushes on and has no userID'}
            ],
            'layout': {
                'title': 'All'
            }
        }
    )
])

if __name__ == '__main__':
    app.run_server(debug=True, port=3000, host='0.0.0.0')