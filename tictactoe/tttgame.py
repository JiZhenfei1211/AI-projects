# coding utf-8
import random
import os
positive_infinity = float('Inf')
negative_infinity = float('-Inf')


class TicTacToe:

    def __init__(self):
        self.board = Board()
        self.nine_grid_board = self.create_nine_gird_board()
        self.current_player = None
        self.board_index = 0
        self.need_select_grid = True

    def generate_player(self, model, s, chess='X'):
        if s == '0':
            return human_Player(model, chess), computer_Player(model, 'O')
        else:
            return human_Player(model, 'O'), computer_Player(model, 'X')

    def switch_player(self, player_1, player_2):
        if self.current_player == player_1:
            return player_2
        else:
            return player_1

    def display_all_boards(self):
        print('\nAll boards are shown as below:')
        for i in range(len(self.nine_grid_board)):
            print('No.' + str(i+1) + ' Board')
            if self.nine_grid_board[i].status is not None:
                print('This board ends with ' + "'" + str(self.nine_grid_board[i].status) + "'.")
            self.nine_grid_board[i].display_board()
            print()

    def create_nine_gird_board(self):
        nine_grid_board = []
        for i in range(9):
            nine_grid_board.append(Board(3))
        return nine_grid_board

    def examine_all_grid_winner(self):
        board_list = self.nine_grid_board[:]
        board_status_list = []
        for i in range(len(board_list)):
            if board_list[i].status is not None:
                board_status_list.append(board_list[i].status)
            else:
                board_status_list.append('+')
        win_combos = [board_status_list[0:3], board_status_list[3:6], board_status_list[6:9],
                      board_status_list[0::3], board_status_list[1::3], board_status_list[2::3],
                      board_status_list[0::4], board_status_list[2:7:2]]

        if ['X'] * 3 in win_combos:
            return 'X'
        elif ['O'] * 3 in win_combos:
            return 'O'
        elif '+' not in board_status_list:
            return 'TIE'
        else:
            return None

    @staticmethod
    def display_winner(winner):
        if winner == 'X':
            print('The winner is offensive player who takes X!')
        elif winner == 'O':
            print('The winner is defensive player who takes O!')
        else:
            print('It is a tie game!')

    def start_game(self):
        model = input(
            'Select a game model to start: \n\t'
            '0. Normal TicTacToe Game.\n\t'
            '1. Advanced TicTacToe Game.\n\t'
            '2. Ultimate TicTacToe Game.\n\t'
        )
        while model not in ['0', '1', '2']:
            print('Invalid selection, please select again.')
            model = input(
                'Select a game model to start: \n\t'
                '0. Normal TicTacToe Game.\n\t'
                '1. Advanced TicTacToe Game.\n\t'
                '2. Ultimate TicTacToe Game.\n\t'
            )

        selection = input(
            'Select one chess type to begin the game: \n\t 0. X(offensive player) \n\t 1. O(defensive player)\n\t')
        while selection not in ['0', '1']:
            print('Invalid selection, please select again.')
            selection = input(
                'Select one chess type to begin the game: \n\t 0. X(offensive player) \n\t 1. O(defensive player)\n\t')
        print('Game start!')
        human_player, computer_player = self.generate_player(model, selection)
        if model == '0':
            self.run_normal_ttt(selection, human_player, computer_player)
        elif model == '1':
            self.run_advanced_ttt(selection, human_player, computer_player)
        else:
            self.run_ultimate_ttt(selection, human_player, computer_player)

    def run_normal_ttt(self, selection, human_player, computer_player):
        if selection == '0':
            self.current_player = human_player
        else:
            self.current_player = computer_player
        self.board.display_board()
        while True:
            self.current_player.take_action(self.board, False)
            if self.board.terminal_test():
                winner = self.board.examine_win()
                break
            self.current_player = self.switch_player(human_player, computer_player)
        self.display_winner(winner)
        print('Game over!')

    def run_advanced_ttt(self, selection, human_player, computer_player):
        if selection == '0':
            self.current_player = human_player
        else:
            self.current_player = computer_player
        while True:
            if self.need_select_grid:
                self.board_index = self.current_player.take_action(self.nine_grid_board,
                                                                   need_select_grid=self.need_select_grid)
                self.need_select_grid = False
            else:
                self.current_player = self.switch_player(human_player, computer_player)
                next_board = self.nine_grid_board[self.board_index]
                if next_board.examine_win() == 'TIE':
                    print('The current board is not available, so current can move anywhere.')
                    self.need_select_grid = True
                else:
                    print('On No.' + str(self.board_index + 1) + ' Board')
                    self.board_index = self.current_player.take_action(self.nine_grid_board, self.board_index, False)
                    if next_board.terminal_test():
                        if next_board.examine_win() is not 'TIE':
                            winner = next_board.examine_win()
                            break

            self.display_all_boards()

        self.display_winner(winner)
        print('Game over')

    def run_ultimate_ttt(self, selection, human_player, computer_player):
        if selection == '0':
            self.current_player = human_player
        else:
            self.current_player = computer_player
        if selection == '0':
            self.current_player = human_player
        else:
            self.current_player = computer_player
        while True:
            if self.need_select_grid:
                self.board_index = self.current_player.take_action(self.nine_grid_board,
                                                                   need_select_grid=self.need_select_grid)
                self.need_select_grid = False
            else:
                self.current_player = self.switch_player(human_player, computer_player)
                next_board = self.nine_grid_board[self.board_index]
                if next_board.status is not None:
                    print('The current board is not available, so current player can move anywhere.')
                    self.need_select_grid = True
                else:
                    print('On No.' + str(self.board_index + 1) + ' Board')
                    new_index = self.current_player.take_action(self.nine_grid_board, self.board_index, False)
                    if next_board.terminal_test():
                        winner = next_board.examine_win()
                        next_board.status = winner
                    self.board_index = new_index
            self.display_all_boards()
            winner = self.examine_all_grid_winner()
            if winner is not None:
                break
        self.display_winner(winner)
        print('Game over')


class Board:

    def __init__(self, board_side=3, status=None):
        self.board_side = board_side
        self.status = status
        self.board = ['+' for _ in range(self.board_side ** 2)]

    def display_board(self):
        board = self.board
        for i in range(self.board_side ** 2):
            print(board[i], end=' ')
            if (i + 1) % self.board_side == 0:
                print()

    def get_available_actions(self):
        available_actions = []
        for i in range(self.board_side ** 2):
            if self.board[i] == '+':
                available_actions.append(i)
        return available_actions

    def is_valid_action(self, position):
        return self.board[position] == '+'

    def take_action(self, position, player):
        if self.is_valid_action(position):
            self.board[position] = player
            return True
        else:
            print('Invalid position!')
            return False

    def undo_action(self, position):
        self.board[position] = '+'

    def terminal_test(self):
        if self.examine_win() is not None:
            return True
        return False

    def examine_win(self):
        board = self.board
        win_combos = [board[0:3], board[3:6], board[6:9],
                      board[0::3], board[1::3], board[2::3],
                      board[0::4], board[2:7:2]]

        if ['X'] * 3 in win_combos:
            return 'X'
        elif ['O'] * 3 in win_combos:
            return 'O'
        elif '+' not in board:
            return 'TIE'
        else:
            return None


class Player:

    def __init__(self, model, chess='X'):
        self.model = model
        self.chess = chess

    def take_action(self, board, board_index=-1, need_select_grid=False):
        pass


class human_Player(Player):

    def __init__(self, model, chess):
        super().__init__(model, chess)

    def take_action(self, board, board_index=-1, need_select_grid=False):
        if self.model == '0':
            action = self.take_action_nomal(board)
            board.take_action(action, self.chess)
        else:
            if need_select_grid:
                index, action = self.take_action_advanced(board)
                board[index].take_action(action, self.chess)
            else:
                action = self.take_action_nomal(board[board_index])
                board[board_index].take_action(action, self.chess)
        return action

    def take_action_nomal(self, board):
        while True:
            available_actions = board.get_available_actions()
            if len(available_actions) != 0:
                print('Available positions are : ')
                for i in range(len(available_actions)):
                    print(available_actions[i] + 1, end=', ')
            print()
            action = input('Please select a valid position:\n\t')
            if len(action) == 1 and board.is_valid_action(int(action) - 1):
                return int(action) - 1
            else:
                print('Invalid position, please select a valid position!\n')

    def take_action_advanced(self, board_list):
        while True:
            available_grids = []
            print('Available grids are : ')
            for i in range(len(board_list)):
                if board_list[i].terminal_test() is False:
                    available_grids.append(i)
                    print(i + 1, end=', ')
            print()
            board_index = input('Please enter an available grid to play on:\n')
            if int(board_index)-1 not in available_grids:
                print('Invalid grid, please select a valid grid!\n')
            else:
                board = board_list[int(board_index) - 1]
                board.display_board()
                action = self.take_action_nomal(board)
            return int(board_index)-1, action

class computer_Player(Player):

    def __init__(self, model, chess):
        super().__init__(model, chess)

    def get_opponent_player(self):
        if self.chess is 'X':
            return computer_Player(self.model, 'O')
        else:
            return computer_Player(self.model, 'X')

    def take_action(self, board, board_index=-1, need_select_grid=False):
        print('It' + "'s" + ' Computer_player' + "'" + 's turn:')
        chess = ['X', 'O'][self.chess == 'X']
        opponent_player = computer_Player(self.model, chess)
        if self.model == '0':
            best_action = self.take_action_minimax(board, opponent_player)
            board.take_action(best_action, self.chess)
            board.display_board()
            return best_action
        else:
            if need_select_grid:  # computer needs to decide which grid is better to make move
                best_index = self.get_best_board(board, opponent_player)
                print('On No.'+str(best_index+1)+' Board')
                best_action = self.take_action_alpha_beta(board[best_index], board, opponent_player)
                board[best_index].take_action(best_action, self.chess)
                print('Computer player makes a move at (' + str(best_index+1) + ',' + str(best_action+1) + ')')
                board[best_index].display_board()
                return best_action
            else:
                best_action = self.take_action_alpha_beta(board[board_index], board, opponent_player)
                board[board_index].take_action(best_action, self.chess)
                print('Computer player makes a move at (' + str(board_index+1) + ',' + str(best_action+1) + ')')
                board[board_index].display_board()
                return best_action

    def take_action_minimax(self, board, opponent_player):
        _, action = self.minimax(board, opponent_player)
        return action

    def take_action_alpha_beta(self, board, board_list, opponent_player):
        _, action = self.alpha_beta(board, board_list, opponent_player, negative_infinity, positive_infinity)
        return action

    def get_best_board(self, grids_list, opponent_player):
        current_index = 0
        if self.chess is 'X':
            value = negative_infinity
        else:
            value = positive_infinity
        for i in range(len(grids_list)):
            val, _ = self.alpha_beta(grids_list[i], grids_list, opponent_player, negative_infinity, positive_infinity)
            if self.chess is 'X':
                if val > value:
                    current_index = i
            else:
                if val < value:
                    current_index = i
        return current_index

    def heuristic_func_1(self, board_obj, player):
        self_could_win_num = 0
        opponent_could_win_num = 0
        temp_board = board_obj.board[:]
        for i in range(len(board_obj.board)):
            if board_obj.board[i] == '+':
                temp_board[i] = self.chess
            else:
                temp_board[i] = board_obj.board[i]

        self_win_combos = [temp_board[0:3], temp_board[3:6], temp_board[6:9],
                      temp_board[0::3], temp_board[1::3], temp_board[2::3],
                      temp_board[0::4], temp_board[2:7:2]]

        for j in range(len(self_win_combos)):
            if [self.chess] * 3 == self_win_combos[j]:
                self_could_win_num += 1

        for m in range(len(board_obj.board)):
            if board_obj.board[m] == '+':
                temp_board[m] = player.chess
            else:
                temp_board[m] = board_obj.board[m]

        opponent_win_combos = [temp_board[0:3], temp_board[3:6], temp_board[6:9],
                           temp_board[0::3], temp_board[1::3], temp_board[2::3],
                           temp_board[0::4], temp_board[2:7:2]]

        for n in range(len(opponent_win_combos)):
            if [player.chess] * 3 == opponent_win_combos[n]:
                opponent_could_win_num += 1

        if self.chess == 'X':
            value = (self_could_win_num * 10 / 3) + (-10*opponent_could_win_num/3)
        else:
            value = (-10 * self_could_win_num / 3) + (10 * opponent_could_win_num/3)

        return value

    def heuristic_func_2(self, board_obj, board_list, player):
        value = 0
        corner_boards = [board_list[0], board_list[2], board_list[6], board_list[8]]
        if board_obj.terminal_test():
            if board_obj.examine_win() == 'X':
                if board_obj == board_list[4]:
                    value = value + 13
                elif board_obj in corner_boards:
                    value = value + 9
                else:
                    value = value + 5
            elif board_obj.examine_win() == 'O':
                if board_obj == board_list[4]:
                    value = value - 13
                elif board_obj in corner_boards:
                    value = value - 9
                else:
                    value = value - 5
            elif board_obj.examine_win() == 'TIE':
                value = 0
        return value

    def heuristic_func_3(self, board_obj, board_list, player):
        if board_obj.terminal_test():
            if self.chess == 'X':
                return 3
            else:
                return -3



    def minimax(self, board, player, depth=0):
        if self.chess == 'X':
            value = negative_infinity
        else:
            value = positive_infinity

        if board.terminal_test():
            if board.examine_win() == 'X':
                return 10 - depth, None
            elif board.examine_win() == 'O':
                return -10 - depth, None
            elif board.examine_win() == 'TIE':
                return 0, None

        for action in board.get_available_actions():
            board.take_action(action, self.chess)
            val, _ = player.minimax(board, self, depth + 1)
            board.undo_action(action)

            if self.chess == 'X':
                if val > value:
                    value, best_action = val, action
            else:
                if val < value:
                    value, best_action = val, action

        return value, best_action

    def alpha_beta(self, board, board_list, player, alpha, beta, depth=5):

        if board.terminal_test():
            if self.model == '2':
                val1 = self.heuristic_func_2(board, board_list, player)
                val2 = self.heuristic_func_3(board, board_list, player)
                return val1 + val2, None
            else:
                if board.examine_win() == 'X':
                    return 10 + depth, None
                elif board.examine_win() == 'O':
                    return -10 + depth, None
                elif board.examine_win() == 'TIE':
                    return 0, None

        if depth == 0:
            val = self.heuristic_func_1(board, player)
            return val, None

        if self.chess == 'X':
            value = negative_infinity
            for action in board.get_available_actions():
                board.take_action(action, self.chess)
                val, _ = player.alpha_beta(board_list[action], board_list, self, alpha, beta, depth - 1)
                board.undo_action(action)
                if val > value:
                    value, best_action = val, action
                if val >= beta:
                    return value, None
                if val > alpha:
                    alpha = val
            return value, best_action
        else:
            value = positive_infinity
            for action in board.get_available_actions():
                board.take_action(action, self.chess)
                val, _ = player.alpha_beta(board_list[action], board_list, self, alpha, beta, depth - 1)
                board.undo_action(action)
                if val < value:
                    value, best_action = val, action
                if val <= alpha:
                    return value, None
                if val < beta:
                    beta = val
            return value, best_action


if __name__ == "__main__":
    TicTacToe().start_game()