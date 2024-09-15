from datetime import timedelta

class GeneralClassification():
    def __init__(self):
        self.players = {}
        self.nameOfTour = None

    def set_tour_name(self, tourName):
        self.nameOfTour = tourName

    # for debugging
    def show_players(self):
        print(self.players)

    def add_player(self, player, team):
        # time format: HH:MM:SS
        if self.check_player(player, team) == False:
            self.players[(player, team)] = timedelta(hours=0, minutes=0, seconds=0)
            return True
        else:
            # No duplicates
            return False
    
    def remove_player(self, player, team):
        if self.check_player(player, team) == False:
            return False
        else:
            self.players.pop(player)
            return True

    def add_time(self, player, team, time):
        spliced_time = time.split(":")
        if len(spliced_time) == 3:
            try:
                new_time = timedelta(hours=int(spliced_time[0]), minutes=int(spliced_time[1]), seconds=int(spliced_time[2]))
            except:
                return False
        if self.check_player(player, team):
            self.players[(player, team)] += new_time
            return True
        else:
            return False

    # return true if player already exists
    def check_player(self, player, team):
        if (player, team) in self.players:
            return True
        return False
    
    def get_time(self, player, team):
        if self.check_player(player, team):
            return self.players[(player, team)]
        else:
            return False
        
    def showGC(self):
        print("--GENERAL CLASSIFICATION--")
        counter = 1
        order_to_use = self.correctOrder()
        player_list = "--GENERAL CLASSIFICATION--\n"
        for i in order_to_use.keys():
            print(f"Rank {counter}: {i[0]} | Time: {self.players[i]}")
            player_list += f"Rank {counter}: {i[0]} | Time: {self.players[i]}\n"
            counter += 1
        return player_list

    def correctOrder(self):
        sorted_players = dict(sorted(self.players.items(), key=lambda item: item[1]))
        return sorted_players

