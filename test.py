from firebase import firebase
import csv

save_data = []
dict = {}
database = firebase.FirebaseApplication("https://kivy-graph-default-rtdb.firebaseio.com/", authentication=None)

col_list = ['Frequency', 'Heat', 'Temperature', 'Percentage']

columns = []
with open('data.csv') as f:
    reader = csv.reader(f)
    for row in reader:
        if columns:
            for i, value in enumerate(row):
                columns[i].append(value)
        else:
            # first row
            columns = [[value] for value in row]
# you now have a column-major 2D array of your file.
as_dict = {c[0]: c[1:] for c in columns}


def GET():
    return database.get('/Points', None)


def POST():
    database.patch('/Points',
                   {
                       'Frequency': [0],
                       'Heat': [0],
                       'Percentage': [0],
                       'Temperature': [0]
                   })


POST()
print(GET())
