from kivy.lang import Builder
from kivymd.app import MDApp
from kmplot.backend_kivy import FigureCanvasKivy
import matplotlib.pyplot as plt
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.storage.jsonstore import JsonStore
from kivymd.toast import toast
import csv

save_data = []

database = {}

# Initializing JSON database
store = JsonStore('database.json')

store.put('points', name=[])  # to delete the json data


def readCSV():
    with open('data.csv', newline='') as csvfile:
        data = csv.reader(csvfile, delimiter=',', quoting=csv.QUOTE_NONNUMERIC)
        for row in data:
            return row


def BarGraph(data):
    courses = []
    for i in range(1, len(data) + 1):
        courses.append("Data {value}".format(value=str(i)))

    print("Lenth of data", len(data))
    # creating the bar plot
    plt.clf()
    plt.bar(courses, data, color='maroon',
            width=0.4)

    # sns.distplot(data)

    plt.xlabel("Data")
    plt.ylabel("Frequency")
    plt.title("Graph")


def LineGraph(data):
    signal = data

    # this will plot the signal on graph
    plt.clf()

    plt.plot(signal, color='red', linewidth=4,
             marker='h', markerfacecolor='blue', markeredgewidth=2,
             markersize=8, markevery=3)

    # setting x label
    plt.xlabel('Time(s)')

    # setting y label
    plt.ylabel('signal (norm)')
    plt.grid(True, color='lightgray')


def PostJSONData(data):
    new_data = store.get('points')['name']
    new_data += data
    store.put('points', name=new_data)


def GetJSONData():
    if store.exists('points'):
        return store.get('points')['name']


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
        PostJSONData(data)  # Add data to json
        self.show_toast('Data Received')

    def show_toast(self, message):
        toast(message)

    def PlotGraph(self):
        data = GetJSONData()  # Generate 10 random data range from 1 to 50

        print(self.check)

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
