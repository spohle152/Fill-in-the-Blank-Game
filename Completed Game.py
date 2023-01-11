import tkinter as tk
import random as r
from tkinter import *
from tkinter import messagebox
import sys


top = tk.Tk()
top.geometry('1280x720')
top.title("Fill in the Blank Cards")
canvas=Canvas(top, highlightthickness=0)
canvas.grid_columnconfigure(0, weight=1)
myscrollbar=Scrollbar(top,orient="vertical")
myscrollbar.pack(side="right",fill="y")
myscrollbar.config(command=canvas.yview)
canvas.config(yscrollcommand=myscrollbar.set)
canvas.pack(side=TOP,expand=True,fill=BOTH)
canvas.grid_columnconfigure(0, weight=1)
frame = Frame(canvas)
frame.grid_columnconfigure(0, weight=1)
frame.bind(
    "<Configure>",
    lambda e: canvas.configure(
        scrollregion=canvas.bbox("all")
    )
)
canvas.create_window((0, 0), window=frame, anchor="nw")
players = []
num_players = 0
scores = []
winning_score = 0
selecting_players_i = []
master_player_i = 0
possible_white_cards = []
white_cards_by_player = []
selected_white_cards = []
black_cards = []
used_black_cards = []
completed_cards = []
completed_cards_shuffled = []
num_blanks = 0
current_black_card = 0

#Initially set up the game to set users names and select a player at random to be first master (setup function) Use for loop to iterate through selecting_players. (playing_round function) Once all of them have chosen, have the master_player select a card from completed cards shuffle (selecting_winner function). Give out white cards using random to give to different users, making sure no duplicate cards are in use at the same time (probably find() function) Trace back the selected card to choose new master player and update variables, including score, accordingly. (score_calculation function) Repeat until a player has a score of 5, then list winners. (winning function)

def clearFrame():
    # destroy all widgets from frame
    for widget in frame.winfo_children():
       widget.destroy()

def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        top.destroy()

def handler(e):
   var.set(1)

top.protocol("WM_DELETE_WINDOW", on_closing)
top.bind('<Return>', handler)
while True:
    white_cards_file = open("white_cards.txt", "r")
    possible_white_cards_temp = white_cards_file.readlines()
    possible_white_cards = [line.replace('\n', '') for line in possible_white_cards_temp]
    while ("" in possible_white_cards):
        possible_white_cards.remove("")
    if ("Choose..." in possible_white_cards):
        tk.messagebox.showerror(title="ERROR", message='"Choose..." cannot be a white card. Please remove all occurrences of this white card in white_cards.txt')
        top.destroy()
    black_cards_file = open("black_cards.txt", "r")
    black_cards_temp = black_cards_file.readlines()
    black_cards = [line.replace('\n', '') for line in black_cards_temp]
    noBlanks = False
    for card in black_cards:
        if card.count("&") == 0:
            noBlanks = True
    if noBlanks:
        tk.messagebox.showerror(title="ERROR", message='All Black Cards must have at least one blank denoted by an "&"')
        top.destroy()
    #Enter Number of Players
    num_players_label = Label (frame, text="Enter the Number of Players:")
    num_players_label.grid()
    enter_num_players = Text (frame, width=5, height=1)
    enter_num_players.grid()
    enter_num_players.focus_set()
    var = tk.IntVar()
    selecting_card = tk.IntVar()
    submit_btn1 = Button (frame, text="Submit", command=lambda: var.set(1))
    submit_btn1.grid()
    #Enter Player's Names
    submit_btn1.wait_variable(var)
    while ((enter_num_players.get(1.0, END).replace('\n', '')).isnumeric()) == False:
        tk.messagebox.showerror(title="ERROR", message="Please Enter a positive integer greater than 1")
        submit_btn1.wait_variable(var)
    while int(enter_num_players.get(1.0, END).replace('\n', '')) <= 1:
        tk.messagebox.showerror(title="ERROR", message="Please Enter a positive integer greater than 1")
        submit_btn1.wait_variable(var)
    max_blanks = 0
    for card in black_cards:
        if card.count("&") > max_blanks:
            max_blanks = card.count("&")
    while len(possible_white_cards)//int(enter_num_players.get(1.0, END).replace('\n', '')) <= max_blanks:
        tk.messagebox.showerror(title="ERROR", message="The maximum number of blanks of all the black cards must not exceed number of white cards distributed to each player. Either increase the number of white cards, or decrease the number of blanks in the black cards or decrease the number of players")
        submit_btn1.wait_variable(var)
    num_players=int(enter_num_players.get(1.0, END).replace('\n', ''))
    clearFrame()
    for player in range(num_players):
        player_num_label = Label(frame, text = "Enter Player "+ str(player + 1) +"'s Name")
        player_num_label.grid()
        player_name = Text (frame, width=15, height=1)
        player_name.grid()
        player_name.focus_set()
        submit_btn1 = Button (frame, text="Submit", command=lambda: var.set(1))
        submit_btn1.grid()
        submit_btn1.wait_variable(var)
        players.append(player_name.get(1.0, END).replace('\n', ''))
        scores.append(0)
        white_cards_by_player.append([])
        selected_white_cards.append([])
        clearFrame()
    #Enter a score to reach for game to be won
    winning_score_label = Label(frame, text="What score will it take to win the game?")
    winning_score_label.grid()
    enter_winning_score = Text (frame, width=5, height=1)
    enter_winning_score.grid()
    enter_winning_score.focus_set()
    submit_btn1 = Button (frame, text="Submit", command=lambda: var.set(1))
    submit_btn1.grid()
    submit_btn1.wait_variable(var)
    while ((enter_winning_score.get(1.0, END).replace('\n', '')).isnumeric()) == False:
        tk.messagebox.showerror(title="ERROR", message="Please Enter a positive integer")
        submit_btn1.wait_variable(var)
    winning_score = int(enter_winning_score.get(1.0, END).replace('\n', ''))
    clearFrame()
    #Select a Player to be First Master
    master_player_i = r.randint(0,num_players - 1)
    for player in range(len(players)):
        if player != master_player_i:
            selecting_players_i.append(player)
    #Give out white cards to each user
    if ((len(possible_white_cards)//num_players) < 10):
        for player in range(len(players)):
            while len(white_cards_by_player[player]) < (len(possible_white_cards)//num_players):
                temp_white_card = r.randint(0, len(possible_white_cards) - 1)
                found = False
                for list_element in white_cards_by_player:
                    if temp_white_card in list_element:
                        found = True
                if found == False:
                    white_cards_by_player[player].append(temp_white_card)
    else:
        for player in range(len(players)):
                while len(white_cards_by_player[player]) < 10:
                    temp_white_card = r.randint(0, len(possible_white_cards) - 1)
                    found = False
                    for list_element in white_cards_by_player:
                        if temp_white_card in list_element:
                            found = True
                    if found == False:
                        white_cards_by_player[player].append(temp_white_card)
    #Select a Black Card
    current_black_card = r.randint(0,len(black_cards)-1)
    used_black_cards.append(current_black_card)

    #Find the number of blanks for particular black card
    num_blanks = black_cards[current_black_card].count("&")
    while max(scores) < winning_score:
        #For Loop of selecting_players
        for player_i in selecting_players_i:
            #Label for score and player name
            #For loop in range of number of blanks
            for blank in range(num_blanks):
                player_name_label = Label(frame, text=players[player_i], wrap = 800)
                player_name_label.grid()
                score_label = Label(frame, text="Score: " + str(scores[player_i]))
                score_label.grid()
                black_card_label = Label(frame, text=(black_cards[current_black_card]).replace("&", "_______"), wrap = 800)
                black_card_label.grid()
                blank_num_label = Label (frame, text="Please select a white card for blank number " + str(blank + 1))
                blank_num_label.grid()
                i = 0
                for white_card_i in white_cards_by_player[player_i]:
                    radio = Radiobutton(frame, text = possible_white_cards[white_card_i], wrap = 800, value = i, variable = selecting_card)
                    i = i + 1
                    radio.grid(sticky = 'w')
                submit_btn1 = Button (frame, text="Submit", command=lambda: var.set(1))
                submit_btn1.grid()
                submit_btn1.wait_variable(var)
                selected_white_cards[player_i].append(white_cards_by_player[player_i][selecting_card.get()])
                white_cards_by_player[player_i].pop(selecting_card.get())
                clearFrame()
            #Update completed cards
            black_card_split = black_cards[current_black_card].split('&')
            completed_card = ""
            for blank in range(num_blanks):
                completed_card = completed_card + (black_card_split[blank]) + (possible_white_cards[selected_white_cards[player_i][blank]])
            if (black_cards[current_black_card])[-1] != '&':
                completed_card = completed_card + (black_card_split[-1])
            completed_cards.append(completed_card)
        #Update Interface for master selection
        player_name_label = Label(frame, text=players[master_player_i], wrap = 800)
        player_name_label.grid()
        score_label = Label(frame, text="Score: " + str(scores[master_player_i]))
        score_label.grid()
        black_card_label = Label(frame, text=(black_cards[current_black_card]).replace("&", "_______"), wrap = 800)
        black_card_label.grid()
        blank_num_label = Label (frame, text="Please select the card that will win the round")
        blank_num_label.grid()
        #Make completed_cards_shuffled a copy of completed_cards and shuffle it
        completed_cards_shuffled = completed_cards.copy()
        r.shuffle(completed_cards_shuffled)
        i = 0
        for card in completed_cards_shuffled:
            radio = Radiobutton(frame, text = card, wrap = 800, value = i, variable = selecting_card)
            i = i + 1
            radio.grid(sticky = 'w')
        submit_btn1 = Button (frame, text="Submit", command=lambda: var.set(1))
        submit_btn1.grid()
        submit_btn1.wait_variable(var)
        clearFrame()
        #Once Master selects a card, trace it back using original completed_cards
        scores[selecting_players_i[completed_cards.index(completed_cards_shuffled[selecting_card.get()])]] = (scores[selecting_players_i[completed_cards.index(completed_cards_shuffled[selecting_card.get()])]]) + 1        
        #Round Winner Label
        round_winner = Label(frame, text="The winner of the round is " + players[selecting_players_i[completed_cards.index(completed_cards_shuffled[selecting_card.get()])]], wrap = 800)
        round_winner.grid()
        submit_btn1 = Button (frame, text="Next", command=lambda: var.set(1))
        submit_btn1.grid()
        submit_btn1.wait_variable(var)
        clearFrame()
        #Update master_player_i
        master_player_i = selecting_players_i[completed_cards.index(completed_cards_shuffled[selecting_card.get()])]
        #Update selecting_players_i
        selecting_players_i = []
        for player in range(len(players)):
            if player != master_player_i:
                selecting_players_i.append(player)
        #Reset Variable to setup for next round
        selected_white_cards = []
        for player in players:
            selected_white_cards.append([])
        completed_cards = []
        completed_cards_shuffled = []
        if ((len(possible_white_cards)//num_players) < 10):
            for player in range(len(players)):
                while len(white_cards_by_player[player]) < (len(possible_white_cards)//num_players):
                    temp_white_card = r.randint(0, len(possible_white_cards) - 1)
                    found = False
                    for list_element in white_cards_by_player:
                        if temp_white_card in list_element:
                            found = True
                    if found == False:
                        white_cards_by_player[player].append(temp_white_card)
        else:
            for player in range(len(players)):
                    while len(white_cards_by_player[player]) < 10:
                        temp_white_card = r.randint(0, len(possible_white_cards) - 1)
                        found = False
                        for list_element in white_cards_by_player:
                            if temp_white_card in list_element:
                                found = True
                        if found == False:
                            white_cards_by_player[player].append(temp_white_card)
        if (len(black_cards) == len(used_black_cards)):
            used_black_cards = []
        while(current_black_card in used_black_cards):
            current_black_card = r.randint(0,len(black_cards)-1)
        used_black_cards.append(current_black_card)
        num_blanks = black_cards[current_black_card].count("&")

    #Update interface to show leader board
    for player in sorted(zip(scores, players), reverse=True):
        leader_board = Label(frame, text = str(player[1]) + " - " + str(player[0]) + " pts.", wrap = 800)
        leader_board.grid()
    #Button to restart game
    submit_btn1 = Button (frame, text="Reset", command=lambda: var.set(1))
    submit_btn1.grid()
    #Wait On Button press
    submit_btn1.wait_variable(var)
    clearFrame()
    players = []
    num_players = 0
    scores = []
    winning_score = 0
    selecting_players_i = []
    master_player_i = 0
    possible_white_cards = []
    white_cards_by_player = []
    selected_white_cards = []
    black_cards = []
    used_black_cards = []
    completed_cards = []
    completed_cards_shuffled = []
    num_blanks = 0
    current_black_card = 0
top.protocol("WM_DELETE_WINDOW", on_closing)
top.mainloop()