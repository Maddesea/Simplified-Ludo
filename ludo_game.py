# Author: Sean Madden
# GitHub username: Maddesea
# Description: This is a program that allows you to play a simplified version of the game Ludo. Ludo is a strategy board
# game for two to four players, in which the players race their four tokens from start to finish according to the roll
# of a single die. The overall purpose and playing of the game are still the same as the original game, as this program
# covers the primary abilities and possible actions available in-game but lacks minor details and a GUI.


class LudoGame:
    """This is a class which represents the game of Ludo being played. This game can be played for 2-4 players, where
    each player has 2 tokens (up to 8 tokens maximum on the board) and both of these tokens start in the player’s (‘H')
    (Home Yard). This class uses the Player class (located down below) to track the movement of players as they play a
    game of Ludo."""

    def __init__(self):
        self._players = {}

    def get_player_by_position(self, playerid):
        """This is a required method of the LudoGame class that takes a parameter representing the
        player’s position as a string and returns the player object. For an invalid string parameter, it will return
        Player not found!"""
        if playerid in self._players:
            return self._players[playerid]
        return "Player not found!"

    def move_token(self, player, token, steps):
        """This method takes three parameters, the player object, the token name (‘p’ or ‘q’) and the steps the token will move on
        the board (int). This method will take care of one token moving on the board. It will also update the token’s
        total steps, and it will take care of kicking out other opponent tokens as needed. The play_game method will use
        this method."""
        player.move_token_helper(token, steps)

    def move_token(self, player, steps):
        """This is a helper function for the above move_token method"""

        if (player.get_token_p().get_step_count() == -1 and steps == 6):  # Rolled a 6
            player.move_token('p', steps)
        elif (player.get_token_q().get_step_count() == -1 and steps == 6):  # Rolled a 6
            player.move_token('q', steps)
        elif (player.get_token_p().get_step_count() + steps == 57):  # move token to final space
            player.move_token('p', steps)
        elif (player.get_token_q().get_step_count() + steps == 57):  # move token to final space
            player.move_token('q', steps)
        else:  # Landing on opponent space
            p_pos = player.get_space_name(player.get_token_p().get_step_count() + steps)
            q_pos = player.get_space_name(player.get_token_q().get_step_count() + steps)

            for playerID in self._players:
                if (not player.get_playerName() == playerID):
                    player2 = self._players[playerID]

                    p2_p_pos = player2.get_space_name(player2.get_token_p().get_step_count())
                    p2_q_pos = player2.get_space_name(player2.get_token_q().get_step_count())

                    if (p2_p_pos == p_pos):
                        player.move_token('p', steps)
                        player2.get_token_p().set_step_count(-1)
                        player2.get_token_p().set_current_space("H")
                        if (p2_q_pos == p_pos):
                            player2.get_token_q().set_step_count(-1)
                            player2.get_token_q().set_current_space("H")
                        return
                    if (p2_q_pos == p_pos):
                        player.move_token('p', steps)
                        player2.get_token_q().set_step_count(-1)
                        player2.get_token_q().set_current_space("H")
                        return
                    if (p2_p_pos == q_pos):
                        player.move_token('q', steps)
                        player2.get_token_p().set_step_count(-1)
                        player2.get_token_p().set_current_space("H")
                        if (p2_q_pos == q_pos):
                            player2.get_token_q().step_count = -1
                            player2.get_token_q().set_current_space("H")
                        return
                    if (p2_q_pos == q_pos):
                        player.move_token('q', steps)
                        player2.get_token_q().set_step_count(-1)
                        player2.get_token_q().set_current_space("H")
                        return

            # Landing on your own token space
            if (player.get_token_p().get_step_count() == player.get_token_q().get_step_count()):
                player.move_token('p', steps)
                player.move_token('q', steps)

            # Furthest token away from final space moves
            elif (player.get_token_p().get_step_count() < player.get_token_q().get_step_count()):
                if (not player.get_token_p().get_step_count() == -1):
                    player.move_token('p', steps)
                elif (not player.get_token_q().get_step_count() == -1):
                    player.move_token('q', steps)
            else:
                if (not player.get_token_q().get_step_count() == -1):
                    player.move_token('q', steps)
                elif (not player.get_token_p().get_step_count() == -1):
                    player.move_token('p', steps)

    def play_game(self, players, turns):
        """This is a required method of the LudoGame class that takes two parameters, the players list, and
        the turns list. The players list is the list of positions players choose, like [‘A’, ‘C’] means two players will
        play the game at position A and C. Turns list is a list of tuples with each tuple a roll for one player."""
        for playerID in players:
            self._players[playerID] = Player(playerID)
        for roll in turns:
            # prints (roll)
            player = self.get_player_by_position(roll[0])
            steps = roll[1]
            self.move_token(player, steps)

        player_result = []
        for player in self._players:
            player_result.append(self._players[player].get_token_p().get_current_space())
            player_result.append(self._players[player].get_token_q().get_current_space())
        return player_result


class Token:
    """This is a class named Token which represents the Token of a player in a game of Ludo. There are two tokens per p
    layer (up to 8 on the board at one time) and its location is tracked by the LudoGame class"""

    def __init__(self, name):
        self._name = name
        self._step_count = -1
        self._current_space = "H"

    def get_step_count(self):
        """This is a get method that returns the step_count data member"""
        return self._step_count

    def set_step_count(self, count):
        """This is a method that sets/assigns the parameter/variable count to private data member _current_space"""
        self._step_count = count

    def get_current_space(self):
        """This is a get method that returns the current_space data member"""
        return self._current_space

    def set_current_space(self, space):
        """This is a method that sets/assigns the parameter/variable space to private data member _current_space"""
        self._current_space = space

    def move(self, steps):
        """This is a method of the Token class that takes the steps that a player has to make for their token
        as a parameter. This method increments the count of steps made/to be made and ensures the total step is
        not greater than 57"""
        if (self._step_count == -1):
            if (steps == 6):
                self._step_count = 0
                return
        if self.get_step_count() > 50:
            if (self._step_count + steps > 57):
                return
        self._step_count += steps


class Player:
    """This is a class named Player which represents the player who plays the game of Ludo at a certain
    position. It contains methods that check if the player has completed the game of Ludo, the count of p steps
    taken, the count of q steps taken, and the names of the player token’s space on the board"""
    position = 0

    def __init__(self, name):
        self._playerName = name
        self._token_p = Token('p')
        self._token_q = Token('q')
        self._position = 0

    def get_completed(self):
        """This is a required method of the Player class that takes no parameters and returns True or False
        if the player has finished or not finished the game"""
        if self.get_token_p().get_current_space() == "E" and self.get_token_q().get_current_space() == "E":
            return True
        else:
            return False

    def get_playerName(self):
        """This is a get method that returns the _playerName"""
        return self._playerName

    def get_token_p(self):
        """This is a get method that returns token_p"""
        return self._token_p

    def get_token_q(self):
        """This is a get method that returns token_q"""
        return self._token_q

    def get_token_p_step_count(self):
        """This is a method that takes no parameters and returns the total steps the token p has taken on the board (use
         steps = -1 for home yard position and steps = 0 for ready to go position) The total step should not be larger
         than 57."""
        return self._token_p.get_step_count()

    def get_token_q_step_count(self):
        """This is a method that takes no parameters and returns the total steps the token q has taken on the board"""
        return self._token_q.get_step_count()

    def move_token(self, token, steps):
        """This is a method that takes as parameters the token and the total steps of the token. It returns the movement
         of the token on the board depending on whether the string 'p' or 'q' is provided to this method"""

        if token == 'p':
            self.get_token_p().move(steps)
            self.get_token_p().set_current_space(self.get_space_name(self.get_token_p().get_step_count()))
        elif token == 'q':
            self.get_token_q().move(steps)
            self.get_token_q().set_current_space(self.get_space_name(self.get_token_q().get_step_count()))

    def get_space_name(self, steps):
        """This is a method that takes as a parameter the total steps of the token and returns the name of the space the
         token has landed on the board as a string."""
        if steps == -1:
            return 'H'
        elif steps == 0:
            return 'R'
        elif steps == 57:
            return 'E'
        elif steps > 50:
            return self._playerName + str(steps - 50)
        else:
            if self._playerName == 'A':
                return str(steps)
            if self._playerName == 'B':
                return str(steps + 14)
            if self._playerName == 'C':
                return str(steps + 28)
            if self._playerName == 'D':
                return str(steps + 42)
        return 'H'
