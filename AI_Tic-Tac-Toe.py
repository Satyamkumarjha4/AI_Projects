import streamlit as st
import random
from functools import partial
import copy

# Initialize the board and count as session state variables
if 'board' not in st.session_state:
    st.session_state.board = [['', '', ''], ['', '', ''],['', '', '']]
if 'count' not in st.session_state:
    st.session_state.count = 0
if 'level' not in st.session_state:
    st.session_state.level = 'easy'

def clear_board():
    st.session_state.board = [['', '', '',], ['', '', ''], ['', '', '']]
    st.session_state.count = 0

def print_board():
    # Display the current board
    st.write("### Current Board:")
    for i in range(3):
        cols = st.columns(3)
        for j in range(3):
            # Use partial to pass i and j correctly to player_turn
            cols[j].button(st.session_state.board[i][j] if st.session_state.board[i][j] != '' else ' ', key=f'{i}-{j}', on_click=partial(player_turn, i, j))

def check_winner():
    # Check rows, columns, and diagonals for a winner
    for i in range(3):
        if st.session_state.board[i][0] == st.session_state.board[i][1] == st.session_state.board[i][2] != '':
            return st.session_state.board[i][0]
        if st.session_state.board[0][i] == st.session_state.board[1][i] == st.session_state.board[2][i] != '':
            return st.session_state.board[0][i]
    if st.session_state.board[0][0] == st.session_state.board[1][1] == st.session_state.board[2][2] != '':
        return st.session_state.board[0][0]
    if st.session_state.board[0][2] == st.session_state.board[1][1] == st.session_state.board[2][0] != '':
        return st.session_state.board[0][2]
    return None

def check_winner_on_board(board):
    # Check rows, columns, and diagonals for a winner on a specific board
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != '':
            return board[i][0]
        if board[0][i] == board[1][i] == board[2][i] != '':
            return board[0][i]
    if board[0][0] == board[1][1] == board[2][2] != '':
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != '':
        return board[0][2]
    return None

def ai_random_move():
    available_moves = [(i, j) for i in range(3) for j in range(3) if st.session_state.board[i][j] == '']
    if available_moves:
        row, col = random.choice(available_moves)
        st.session_state.board[row][col] = 'O'
        st.session_state.count += 1

def ai_blocking_move():
    for coin in ['O', 'X']:
        for i in range(3):
            if st.session_state.board[i].count(coin) == 2 and '' in st.session_state.board[i]:
                st.session_state.board[i][st.session_state.board[i].index('')] = 'O'
                st.session_state.count += 1
                return
        for i in range(3):
            col = [st.session_state.board[j][i] for j in range(3)]
            if col.count(coin) == 2 and '' in col:
                st.session_state.board[col.index('')][i] = 'O'
                st.session_state.count += 1
                return
        diag1 = [st.session_state.board[i][i] for i in range(3)]
        if diag1.count(coin) == 2 and '' in diag1:
            st.session_state.board[diag1.index('')][diag1.index('')] = 'O'
            st.session_state.count += 1
            return
        diag2 = [st.session_state.board[i][2 - i] for i in range(3)]
        if diag2.count(coin) == 2 and '' in diag2:
            st.session_state.board[diag2.index('')][2 - diag2.index('')] = 'O'
            st.session_state.count += 1
            return
    ai_random_move()

def minimax(board, is_maximizing):
    winner = check_winner_on_board(board)
    if winner == 'O':
        return 1
    elif winner == 'X':
        return -1
    elif all(cell != '' for row in board for cell in row):
        return 0

    if is_maximizing:
        best_score = -float('inf')
        for i in range(3):
            for j in range(3):
                if board[i][j] == '':
                    board[i][j] = 'O'
                    score = minimax(board, False)
                    board[i][j] = ''
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for i in range(3):
            for j in range(3):
                if board[i][j] == '':
                    board[i][j] = 'X'
                    score = minimax(board, True)
                    board[i][j] = ''
                    best_score = min(score, best_score)
        return best_score

def ai_minimax_move():
    best_score = -float('inf')
    best_move = None
    board_copy = copy.deepcopy(st.session_state.board)

    for i in range(3):
        for j in range(3):
            if board_copy[i][j] == '':
                board_copy[i][j] = 'O'
                score = minimax(board_copy, False)
                board_copy[i][j] = ''
                if score > best_score:
                    best_score = score
                    best_move = (i, j)

    if best_move:
        row, col = best_move
        st.session_state.board[row][col] = 'O'
        st.session_state.count += 1

def player_turn(row, col):
    if st.session_state.board[row][col] == '':
        st.session_state.board[row][col] = 'X'
        st.session_state.count += 1
        winner = check_winner()
        if winner:
            print_board()  # Print the board after the winner is declared
            st.success(f"Player 1 (X) wins!")
            st.stop()
        if st.session_state.count >= 9:
            print_board()  # Print the board after the game ends in a draw
            st.warning('The game is a draw!')
            st.stop()

        # AI turn
        AI(st.session_state.level)
        winner = check_winner()
        if winner:
            print_board()  # Print the board after the AI wins
            st.success(f"AI (O) wins!")
            st.stop()
        if st.session_state.count >= 9:
            print_board()  # Print the board after the game ends in a draw
            st.warning('The game is a draw!')
            st.stop()

def AI(level):
    if level == 'easy':
        ai_random_move()
    elif level == 'medium':
        ai_blocking_move()
    elif level == 'hard':
        ai_minimax_move()

def main():
    st.title("Tic-Tac-Toe Game")

    # Difficulty selection
    st.session_state.level = st.selectbox("Select difficulty level:", ('easy', 'medium', 'hard'))

    # Display the board
    print_board()

    if st.button("Reset Game"):
        clear_board()

# Start the game
main()
