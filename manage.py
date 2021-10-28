import csv

from kivy.lang import Builder
from kivymd.app import MDApp
from kmplot.backend_kivy import FigureCanvasKivy
import matplotlib.pyplot as plt
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen, ScreenManager
import seaborn as sns
import random

save_data = []

database = {}

def Graph(data):
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


def GenerateRandomData():
    data = []
    l = random.randint(5, 15)
    for i in range(l):
        data.append(random.randint(1, 150))
    print("Length of data in generate ", len(data))

    return data


class MenuScreen(Screen):
    count = 1
    check = False

    def callback(self, instance):
        self.check = True
        print("Data received  ", save_data[database[instance.text]])
        Graph(save_data[database[instance.text]])  # instance.text is a key
        self.parent.current = 'graph'

    def on_enter(self, ):
        return None

    def DisableCheck(self):
        self.check = False
        data = GenerateRandomData()  # Generate 10 random data range from 1 to 50
        Graph(data)  # Plot the data
        save_data.append(data)

    def on_leave(self, *args):
        if self.check:
            return
        # Dont call if data is pressed

        key = "Data {value}".format(value=self.count)
        b1 = Button(
            text=key,
            size=(200, 50),
            size_hint=(None, None), )
        b1.bind(on_press=lambda x: self.callback(b1))
        self.ids.view.add_widget(b1)
        database[key] = self.count - 1
        self.count = self.count + 1


class GraphScreen(Screen):

    def on_enter(self, ):
        self.Call()

    def on_leave(self, *args):
        self.ids.GraphBox.clear_widgets()

    def Call(self):
        self.ids.GraphBox.add_widget(FigureCanvasKivy(plt.gcf()))  # Display Graph
        self.ids.GraphBox.add_widget(Builder.load_file('BackButton.kv'))  # Add Back Button to the graph layout


class WindowManager(ScreenManager):
    pass


class MainApp(MDApp):
    def build(self):
        return Builder.load_file('manage.kv')


MainApp().run()

# Data1 ==> save_data[0]
