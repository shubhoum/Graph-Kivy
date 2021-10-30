from kivy.lang import Builder
from kivymd.app import MDApp
from kmplot.backend_kivy import FigureCanvasKivy

import matplotlib.pyplot as plt
from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.toast import toast
from firebase import firebase
import csv

save_data = []
manager = {}

col_list = ['Frequency', 'Heat', 'Temperature', 'Percentage']

database = firebase.FirebaseApplication("https://kivy-graph-default-rtdb.firebaseio.com/", authentication=None)


def PATCH(data):
    database.patch('/Points',
                   {
                       'Frequency': data['Frequency'],
                       'Heat': data['Heat'],
                       'Percentage': data['Percentage'],
                       'Temperature': data['Temperature']})


def POST(data):
    old_data = GET()

    if old_data is None:  # Initialize Firebase for first time
        PATCH(data)
        return

    new_data = data

    for i in col_list:
        old_data[i] += new_data[i]
        manager[i] = old_data[i]

    PATCH(manager)


def GET():
    return database.get('/Points', None)


def readCSV():
    columns = []
    with open('data.csv') as f:
        reader = csv.reader(f)
        for row in reader:
            if columns:
                for i, value in enumerate(row):
                    columns[i].append(value)
            else:
                columns = [[value] for value in row]
    as_dict = {c[0]: c[1:] for c in columns}
    return as_dict


def BarGraph(data):
    courses = []

    for i in range(1, len(data) + 1):
        courses.append("Data {value}".format(value=str(i)))

    # creating the bar plot
    plt.clf()
    plt.bar(courses, data, color='maroon',
            width=0.4)

    # sns.distplot(data)

    plt.xlabel("Data")
    plt.ylabel("Frequency")
    plt.title("Graph")


def LineGraph(data):
    # this will plot the signal on graph
    plt.clf()

    plt.plot(data['Frequency'], color='red', linewidth=4,
             marker='h', markerfacecolor='blue', markeredgewidth=2,
             markersize=8, markevery=3)

    plt.plot(data['Heat'], color='green', linewidth=4,
             marker='h', markerfacecolor='blue', markeredgewidth=2,
             markersize=8, markevery=3)

    plt.plot(data['Temperature'], color='yellow', linewidth=4,
             marker='h', markerfacecolor='blue', markeredgewidth=2,
             markersize=8, markevery=3)

    plt.plot(data['Percentage'], color='blue', linewidth=4,
             marker='h', markerfacecolor='blue', markeredgewidth=2,
             markersize=8, markevery=3)

    # setting x label
    plt.xlabel('Time(s)')

    # setting y label
    plt.ylabel('signal (norm)')
    plt.grid(True, color='lightgray')


class MenuScreen(Screen):
    check = None

    def callback(self, instance, name):
        if instance:
            if name == 'line':
                self.check = False
            else:
                self.check = True

    def on_enter(self, ):
        return None

    def on_leave(self, *args):
        return None

    def ReadData(self):
        data = readCSV()  # read data from source
        POST(data)  # Add data to json
        self.show_toast('Data Received')

    def show_toast(self, message):
        toast(message)

    def PlotGraph(self):
        print("Data")
        data = GET()
        # Generate 10 random data range from 1 to 50

        if self.check is None:
            self.show_toast('Select Graph Type To Display')
            return

        if self.check is False:
            LineGraph(data)
        else:
            BarGraph(data)

        self.parent.current = "graph"
        self.manager.transition.direction = "left"


class GraphScreen(Screen):

    def on_enter(self, ):
        self.ids.GraphBox.add_widget(FigureCanvasKivy(plt.gcf()))  # Display Graph
        self.ids.GraphBox.add_widget(Builder.load_file('BackButton.kv'))  # Add Back Button to the graph layout

    def on_leave(self, *args):
        self.ids.GraphBox.clear_widgets()


class WindowManager(ScreenManager):
    pass


class MainApp(MDApp):

    def build(self):
        return Builder.load_file('manage.kv')


MainApp().run()
