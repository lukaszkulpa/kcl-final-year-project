import sys
from PyQt5.QtWidgets import QGridLayout, QVBoxLayout, QGroupBox, QLabel, \
    QLineEdit, QPlainTextEdit, QPushButton, QDesktopWidget, QWidget, QApplication, \
    QStyleFactory, QMessageBox
from PyQt5.QtGui import QFont
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import networkx as nx
from graph import Graph

"""
Main file in the project.
It can be ran by executing python app.py.
It is responsible for all GUI interactions of the user,
parsing input data to algorithms and displaying visualization
data back to the user.
"""


class PrettyWidget(QWidget):

    def __init__(self):

        super(PrettyWidget, self).__init__()
        # Specifies a query for a font used for drawing text
        font = QFont()
        font.setPointSize(16)
        self.initUI()

    def initUI(self):

        self.setGeometry(100, 100, 1000, 800)
        self.center()
        self.setWindowTitle('Finding Bridges')

        # Creates layout with user input and program output on the left and graph on the right
        grid = QGridLayout()
        self.setLayout(grid)
        self.create_vertical_group_box()

        button_layout = QVBoxLayout()
        button_layout.addWidget(self.vertical_group_box)

        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        grid.addWidget(self.canvas, 0, 1, 9, 9)
        grid.addLayout(button_layout, 0, 0)

        self.show()

    def create_vertical_group_box(self):
        self.vertical_group_box = QGroupBox()
        self.vertical_group_box.setMaximumWidth(300)
        self.vertical_group_box.setMinimumHeight(600)

        layout = QVBoxLayout()

        vertices_label = QLabel("Enter number of vertices:")
        layout.addWidget(vertices_label)

        self.vertices_text = QLineEdit(self)
        layout.addWidget(self.vertices_text)

        edges_label = QLabel("Enter edges:")
        edges_label.setWordWrap(True)
        layout.addWidget(edges_label)

        edges_info = QLabel(
            """Vertices labels have to be non-negative consecutive integers. \neg. 0, 1, 2...
            \nEdges are represented by pairs of connecting vertices labels,\nseparated by a comma and a space.
            \n0, 1\n1, 2 and so on...""")
        edges_info.setWordWrap(True)
        layout.addWidget(edges_info)

        # Place for user's input edges.
        self.edges_text = QPlainTextEdit(self)
        layout.addWidget(self.edges_text)

        """
        Creates buttons for all three algorithms.
        When pressed, suitable algorithm is ran
        and graph with all bridges is shown of the right.
        """
        brute_force_button = QPushButton("Brute-force DFS")
        brute_force_button.setObjectName("Brute-force DFS")
        layout.addWidget(brute_force_button)
        layout.setSpacing(10)
        self.vertical_group_box.setLayout(layout)
        brute_force_button.clicked.connect(self.brute_force_dfs)

        tarjan_button = QPushButton("Tarjan's Algorithm")
        tarjan_button.setObjectName("Tarjan's Algorithm")
        layout.addWidget(tarjan_button)
        layout.setSpacing(10)
        self.vertical_group_box.setLayout(layout)
        tarjan_button.clicked.connect(self.tarjans_algorithm)

        kaiwensun_button = QPushButton("Kaiwensun Algorithm")
        kaiwensun_button.setObjectName("Kaiwensun Algorithm")
        layout.addWidget(kaiwensun_button)
        layout.setSpacing(10)
        self.vertical_group_box.setLayout(layout)
        kaiwensun_button.clicked.connect(self.kaiwensun_bridges)

        output_label = QLabel("Algorithm output:")
        layout.addWidget(output_label)

        self.visualization_data_text = QPlainTextEdit(self)
        layout.addWidget(self.visualization_data_text)

    def parse_text_to_edges(self):
        """
        Parses text input provided to user, checks if it is correct
        and displays error messages.
        Returns number of vertices and a list of lists of edges.
        """
        try:
            number_of_vertices = int(self.vertices_text.text())
        except:
            self.display_error_message()
        plain_text = self.edges_text.toPlainText()
        text = plain_text.split("\n")
        edges = []
        for pair in text:
            try:
                edges.append(list(map(int, pair.split(", "))))
            except:
                self.display_error_message()
        # Display error message if data is not in the correct format.
        if self.check_data(number_of_vertices, edges):
            return number_of_vertices, edges
        else:
            self.display_error_message()

    # Function to alert user that input provided is wrong.
    def display_error_message(self):
        error_message_box = QMessageBox()
        error_message_box.setIcon(QMessageBox.Critical)
        error_message_box.setInformativeText(
            "Data provided is in the wrong format")
        error_message_box.setWindowTitle("Error")
        error_message_box.exec_()

    def check_data(self, number_of_vertices, edges):
        """
        Checks if data provided by the user is in a correct format
        and can be passed further to each algorithm.
        Displays an error message if data is wrong.
        """

        # Check if the number of vertices given is equal to number of vertices in edges.
        flat_list = [item for sublist in edges for item in sublist]
        flat_list.sort()
        vertices_set = set(flat_list)
        if number_of_vertices != len(vertices_set):
            return False
        # Check if graph is connected.
        G = nx.Graph(edges)
        if not nx.is_connected(G):
            return False
        # Check if vertices start with 0
        if flat_list[0] != 0:
            return False
        # Check if vertices are incremented by 1.
        counter = 0
        for i in vertices_set:
            if counter != i:
                return False
            counter = counter + 1

        return True

    def draw_graph(self, edges, bridges):
        """
        Draws graph with bridges found by each algorithm.
        If an edge is a bridge, it is colored red, otherwise blue.
        """
        self.figure.clf()
        G = nx.Graph()
        G.add_edges_from(edges)
        colors = []
        for edge in G.edges:
            if edge in bridges:
                colors.append("red")
            else:
                colors.append("blue")
        pos = nx.spring_layout(G)
        nx.draw(G, pos, with_labels=True, edge_color=colors)
        self.canvas.draw_idle()

    """
    brute_force_dfs(self), tarjans_algorithm(self), kaiwensun_bridges(self)
    are responsible for accepting the user input, creating graphs from it,
    show visualization data and drawing graphs with bridges.
    """

    def brute_force_dfs(self):
        number_of_vertices, edges = self.parse_text_to_edges()
        graph = Graph(number_of_vertices, edges)
        bridges = graph.dfs_brute_force()
        visualization_data = graph.get_visualization_data()
        text = ""
        self.visualization_data_text.setPlainText(text)
        for row in visualization_data:
            text = text + "removed edge: " + \
                str(row[0]) + "\nis a bridge? " + \
                str(row[1]) + "\n"
        self.visualization_data_text.setPlainText(text)
        self.draw_graph(edges, bridges)

    def tarjans_algorithm(self):
        number_of_vertices, edges = self.parse_text_to_edges()
        graph = Graph(number_of_vertices, edges)
        bridges = graph.tarjans_algorithm()
        visualization_data = graph.get_visualization_data()
        text = ""
        self.visualization_data_text.setPlainText(text)
        for row in visualization_data:
            text = text + "time: " + \
                str(row[0]) + "\ndisc: " + \
                str(row[1]) + "\nlow: " + str(row[2]) + \
                "\nbridges: " + str(row[3]) + "\n"
        self.visualization_data_text.setPlainText(text)
        self.draw_graph(edges, bridges)

    def kaiwensun_bridges(self):
        number_of_vertices, edges = self.parse_text_to_edges()
        graph = Graph(number_of_vertices, edges)
        bridges = graph.kaiwensun_bridges()
        visualization_data = graph.get_visualization_data()
        text = ""
        self.visualization_data_text.setPlainText(text)
        for row in visualization_data:
            text = text + "rank: " + \
                str(row[0]) + "\nedges: " + \
                str(row[1]) + "\n"
        self.visualization_data_text.setPlainText(text)
        self.draw_graph(edges, bridges)

    def center(self):
        # Display app in the center of the screen.
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


if __name__ == '__main__':

    app = QApplication(sys.argv)
    app.aboutToQuit.connect(app.deleteLater)
    screen = PrettyWidget()
    screen.show()
    sys.exit(app.exec_())  # finish execution if esc pressed
