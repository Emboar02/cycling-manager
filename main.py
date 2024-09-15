import sys
from PySide6 import QtCore, QtWidgets
from classification import GeneralClassification
from randomPlayer import random_player

class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Cycling Manager")
        self.setGeometry(400, 200, 650, 500)
        self.current_GC = None

        # main layout
        self.main_layout = QtWidgets.QVBoxLayout(self)

        self.button = QtWidgets.QPushButton("New GC")

        # scroll capability
        self.scroll_area = QtWidgets.QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_widget = QtWidgets.QWidget()
        self.layout = QtWidgets.QVBoxLayout(self.scroll_widget)
        
        self.currentGC = QtWidgets.QLabel("", alignment=QtCore.Qt.AlignCenter)
        self.announcement = QtWidgets.QLabel("Welcome to Cycling Manager!\nPlease click the button below to start a new General Classification for a tour!", alignment=QtCore.Qt.AlignCenter)
        self.layout.addWidget(self.currentGC)
        self.layout.addWidget(self.announcement)
        self.layout.addWidget(self.button)

        self.button.clicked.connect(self.infoGC)
        self.scroll_area.setWidget(self.scroll_widget)
        self.main_layout.addWidget(self.scroll_area)
        self.setLayout(self.main_layout)

    @QtCore.Slot()
    def infoGC(self):
        self.button.hide()
        self.announcement.setText("Please input the necessary info about your GC below\n Note that the maximum number of teams possible is 25, and the maximum players per team is 10.")

        self.numberOfTeamsWidget = QtWidgets.QLineEdit(self.scroll_widget)
        self.numberOfTeamsWidget.setPlaceholderText("Number of teams")

        self.numberOfPlayersPerTeamWidget = QtWidgets.QLineEdit(self.scroll_widget)
        self.numberOfPlayersPerTeamWidget.setPlaceholderText("Number of players per team")
        
        self.submit = QtWidgets.QPushButton("Submit info")
        self.submit.clicked.connect(self.makeGC)
        self.layout.addWidget(self.numberOfTeamsWidget)
        self.layout.addWidget(self.numberOfPlayersPerTeamWidget)
        self.layout.addWidget(self.submit)

    def makeGC(self):
        # checking for correct values for number of teams and players
        self.numberOfTeams = self.numberOfTeamsWidget.text()
        self.numberOfPlayersPerTeam = self.numberOfPlayersPerTeamWidget.text()

        if not self.numberOfTeams.isnumeric() or int(self.numberOfTeams) > 25 or int(self.numberOfTeams) < 2:
            self.announcement.setText("Invalid value, or too many/little teams. Try again.")
        elif not self.numberOfPlayersPerTeam.isnumeric() or int(self.numberOfPlayersPerTeam) > 10 or int(self.numberOfPlayersPerTeam) < 1:
            self.announcement.setText("Invalid value, or too many/little players per team. Try again")
        else:
            self.numberOfTeamsWidget.hide()
            self.numberOfPlayersPerTeamWidget.hide()
            self.submit.hide()

            self.current_GC = GeneralClassification()
            self.announcement.setText("Please add players to your team now.")

            # input boxes for players and times
            self.teamNumberWidgets = []
            self.playerNameWidgets = []
            self.teamNameWidgets = []

            for i in range(int(self.numberOfTeams)):
                team_number = QtWidgets.QLabel(f"Team {i+1}", self.scroll_widget)
                team_name = QtWidgets.QLineEdit(self.scroll_widget)
                team_name.setPlaceholderText(f"Enter team {i+1} name")
                self.layout.addWidget(team_number)
                self.layout.addWidget(team_name)
                self.teamNumberWidgets.append(team_number)
                self.teamNameWidgets.append(team_name)
                for j in range(int(self.numberOfPlayersPerTeam)):
                    player_name = QtWidgets.QLineEdit(self.scroll_widget)
                    player_name.setPlaceholderText(f"Add player {j+1}")
                    self.layout.addWidget(player_name)
                    self.playerNameWidgets.append(player_name)

            # submit players
            self.addPlayerButton = QtWidgets.QPushButton("Add players", self.scroll_widget)
            self.addPlayerButton.clicked.connect(self.createTour)
            self.layout.addWidget(self.addPlayerButton)

            # random players
            self.addRandomPlayerButton = QtWidgets.QPushButton("Add randomly generated players", self.scroll_widget)
            self.addRandomPlayerButton.clicked.connect(self.addRandomPlayers)
            self.layout.addWidget(self.addRandomPlayerButton)
    
    def addRandomPlayers(self):
        self.addPlayerButton.hide()
        self.addRandomPlayerButton.hide()
        self.players = [{"name": None, "team": None, "time": None} for _ in range(int(self.numberOfTeams) * int(self.numberOfPlayersPerTeam))]
        self.teamNames = []

        for teamNumber in self.teamNumberWidgets:
            teamNumber.hide()
        # adding players to GC
        player_index = 0
        for i in range(int(self.numberOfTeams)):
            rand_team, _ = random_player()
            for j in range(int(self.numberOfPlayersPerTeam)):
                _, rand_name = random_player()
                self.players[player_index]["name"] = rand_name
                self.players[player_index]["team"] = rand_team
                self.playerNameWidgets[player_index].hide()
                if not self.current_GC.add_player(self.players[player_index]["name"], self.players[player_index]["team"]):
                    print(f"Player {self.players[player_index]["name"]} already exists")
                player_index += 1
            self.teamNameWidgets[i].hide()

        self.announcement.setText("Please make a tour now.")
        self.nameOfTourWidget = QtWidgets.QLineEdit(self.scroll_widget)
        self.nameOfTourWidget.setPlaceholderText("Name of tour")
        self.numberOfStagesWidget = QtWidgets.QLineEdit(self.scroll_widget)
        self.numberOfStagesWidget.setPlaceholderText("Number of stages")
        self.layout.addWidget(self.nameOfTourWidget)
        self.layout.addWidget(self.numberOfStagesWidget)
        self.createTourButton = QtWidgets.QPushButton("Create Tour", self.scroll_widget)
        self.createTourButton.clicked.connect(self.inputTimes)
        self.layout.addWidget(self.createTourButton)


    def createTour(self):
        self.addPlayerButton.hide()
        self.addRandomPlayerButton.hide()
        self.players = [{"name": None, "team": None, "time": None} for _ in range(int(self.numberOfTeams) * int(self.numberOfPlayersPerTeam))]
        self.teamNames = []

        for teamNumber in self.teamNumberWidgets:
            teamNumber.hide()
        # adding players to GC
        player_index = 0
        for i in range(int(self.numberOfTeams)):
            for j in range(int(self.numberOfPlayersPerTeam)):
                self.players[player_index]["name"] = self.playerNameWidgets[player_index].text()
                self.players[player_index]["team"] = self.teamNameWidgets[i].text()
                self.playerNameWidgets[player_index].hide()
                if not self.current_GC.add_player(self.players[player_index]["name"], self.players[player_index]["team"]):
                    print(f"Player {self.players[player_index]["name"]} already exists")
                player_index += 1
            self.teamNameWidgets[i].hide()

        self.announcement.setText("Please make a tour now.")
        self.nameOfTourWidget = QtWidgets.QLineEdit(self.scroll_widget)
        self.nameOfTourWidget.setPlaceholderText("Name of tour")
        self.numberOfStagesWidget = QtWidgets.QLineEdit(self.scroll_widget)
        self.numberOfStagesWidget.setPlaceholderText("Number of stages")
        self.layout.addWidget(self.nameOfTourWidget)
        self.layout.addWidget(self.numberOfStagesWidget)
        self.createTourButton = QtWidgets.QPushButton("Create Tour", self.scroll_widget)
        self.createTourButton.clicked.connect(self.inputTimes)
        self.layout.addWidget(self.createTourButton)

    def inputTimes(self):
        self.createTourButton.hide()

        self.numberOfStages = int(self.numberOfStagesWidget.text())
        self.announcement.setText(f"Welcome to {self.nameOfTourWidget.text()}!\n\nPlease input times with the format HH:MM:SS.")
        
        self.current_GC.set_tour_name(self.nameOfTourWidget.text())

        self.nameOfTourWidget.hide()
        self.submit.hide()
        self.numberOfStagesWidget.hide()

        self.playerTimeWidgets = []
        self.playerNameWidgets = []
        self.teamWidgets = [] 
        index = 0
        for i in range(int(self.numberOfTeams)):
            counter = 0
            teamWidget = QtWidgets.QLabel(f"Team {self.players[index]["team"]}", self.scroll_widget)
            self.teamWidgets.append(teamWidget)
            self.layout.addWidget(teamWidget)
            while counter < int(self.numberOfPlayersPerTeam):
                counter += 1
                player = QtWidgets.QLabel(self.players[index]["name"], self.scroll_widget)
                self.playerNameWidgets.append(player)
                self.layout.addWidget(player)
                temp_time_widgets = []
                for stage in range(self.numberOfStages):
                    player_time = QtWidgets.QLineEdit(self.scroll_widget)
                    player_time.setPlaceholderText(f"Add stage {stage+1} time for {self.players[index]["name"]}")
                    temp_time_widgets.append(player_time)
                    self.layout.addWidget(player_time)
                self.playerTimeWidgets.append(temp_time_widgets)
                index += 1
        self.addTimesButton = QtWidgets.QPushButton("Add times", self.scroll_widget)
        self.addTimesButton.clicked.connect(self.addTimes)
        self.layout.addWidget(self.addTimesButton)

    def addTimes(self):
        self.addTimesButton.hide()
        self.announcement.setText("")
        player_index = 0

        for player in self.playerNameWidgets:
            player.hide()

        for team in self.teamWidgets:
            team.hide()

        for player in self.players:            
            player["time"] = [None for _ in range(self.numberOfStages)]
            for stage in range(self.numberOfStages):
                if not self.current_GC.add_time(player["name"], player["team"], self.playerTimeWidgets[player_index][stage].text()):
                    print("something went wrong")
                player["time"][stage] = self.current_GC.get_time(player["name"], player["team"])
                self.playerTimeWidgets[player_index][stage].hide()
            player_index += 1
        
        self.announcement.setText(self.current_GC.showGC())

if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = MyWidget()
    #widget.showMaximized()
    widget.show()

    sys.exit(app.exec())
