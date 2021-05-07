"""CSC111 Winter Final project: Display of multiple screens of the Upside app.

DESCRIPTION:
===============================

This module contains 8 classes: The first class, UpsideApp() initialises the
main app window, the second class, StartPage() initialises the first page of the app which includes
buttons and an image, the third class, Options() initialises the second page of the app that
displays four main options: description, effects, causes and coping mechanism, the fourth class,
Specifics() initialises the third page of the app that either only displays specific information
(description, effects or causes) or displays specific information (coping mechanisms) and options
to add healthy and unhealthy coping mechanisms. The fifth class, Journal() initialises another page
of the app where users can pick coping mechanisms, add journal entries and rate that specific coping
mechanism. The sixth class, Recommendations() initialises another page of the app that displays a
random healthy coping mechanism that is connected by a path to the inputted unhealthy coping
mechanism. The seventh class, DisplayJournals() initialises another page of the app that displays
all journal entries associated with a specific coping mechanism. The last class, HabitTracker(),
initialises a new window that displays the amount of days since the user has last engaged in an
unhealthy coping mechanism. (options to start and restart the tracker)
There are also 10 functions (including helper functions) that assist in creating the different pages
and functions for when specific buttons are clicked in the app.

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of instructors and TAs
from CSC111 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited.

This file is Copyright (c) Sophia Abolore, Michelle Chernyi, Emily Chang and Umayrah Chonee.
"""
# import statements
import tkinter as tk
from tkinter import ttk
import textwrap
import datetime
from typing import Union, Any
from PIL import ImageTk, Image
import pandas as pd
import upside2


class UpsideApp(tk.Tk):
    """
    The main class: the main window of the Upside app.

    Instance Attributes:
        - graph: The graph generated from the emotions.csv file and journal_entries.csv file
        - frames: widget container in main window
    """
    graph: upside2.Graph
    frames: Any

    def __init__(self, graph: upside2.Graph, frames: Any) -> None:
        """
        Initialize a new window and show the Start Page of the Upside app.
        """
        self.frames = frames
        tk.Tk.__init__(self)
        self.geometry('600x650')
        self.title('Upside')
        self.resizable(False, False)
        container = tk.Frame(self)
        container.pack(side='top', fill='both', expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}

        frame = StartPage(container, self, graph)
        self.frames[StartPage] = frame

        frame.grid(row=0, column=0, sticky='nsew')

        self.show_frame(StartPage)

    def show_frame(self, frame: Any) -> None:
        """
        Stacks inputted frame on top of self.
        """
        frame = self.frames[frame]
        frame.tkraise()


class StartPage(tk.Frame):
    """
    The first page of the Upside app.

    Instance Attributes:
        - parent: The frame/parent of self
        - controller: The main window of the page/main point of intersection for all pages
        - graph: The graph used to represent an emotion app network.
    """
    parent: tk.Frame
    controller: tk.Tk
    graph: upside2.Graph

    def __init__(self, parent: tk.Frame, controller: tk.Tk, graph: upside2.Graph) -> None:
        """
        Initialize a new window which is the Start Page of the Upside app. (first main page)
        """
        tk.Frame.__init__(self, parent)
        upper_frame = tk.LabelFrame(self, width=580, height=200)
        upper_frame.grid(row=0, column=0, padx=10, pady=10)
        lower_frame = tk.LabelFrame(self, width=580, height=400, bg="pink")
        lower_frame.grid(column=0, padx=10, pady=10)

        # adding picture
        picture = ImageTk.PhotoImage(Image.open("logo.png"))
        my_label = tk.Label(upper_frame, image=picture)
        my_label.image = picture
        my_label.grid(row=0, column=0)

        # creating label
        tk.Label(lower_frame, text="What emotion are you feeling today?", bg="black",
                 fg="white",
                 font="none 12 bold").place(x=145, y=25)

        # creating buttons for the different emotions
        tk.Button(lower_frame, text="Sad", height=3, width=20,
                  bg="white",
                  command=lambda: options('Sadness', parent, controller, graph)).place(x=25, y=75)
        tk.Button(lower_frame, text="Fear", height=3, width=20,
                  bg="white",
                  command=lambda: options('Fear', parent, controller, graph)).place(x=212, y=75)
        tk.Button(lower_frame, text="Vulnerability", height=3, width=20,
                  bg="white",
                  command=lambda: options('Vulnerability', parent, controller,
                                          graph)).place(x=400, y=75)
        exhaustion_button = tk.Button(lower_frame, text="Exhaustion", height=3, width=20,
                                      bg="white",
                                      command=lambda: options('Exhaustion', parent, controller,
                                                              graph))
        exhaustion_button.place(x=25, y=155)
        envy_button = tk.Button(lower_frame, text="Envy", height=3, width=20,
                                bg="white",
                                command=lambda: options('Envy', parent, controller, graph))
        envy_button.place(x=212, y=155)
        jealous_button = tk.Button(lower_frame, text="Jealousy", height=3, width=20,
                                   bg="white",

                                   command=lambda: options('Jealousy', parent, controller, graph))
        jealous_button.place(x=400, y=155)
        anger_button = tk.Button(lower_frame, text="Anger", height=3, width=20,
                                 bg="white",
                                 command=lambda: options('Anger', parent, controller, graph))
        anger_button.place(x=25, y=235)
        stress_button = tk.Button(lower_frame, text="Stress", height=3, width=20,
                                  bg="white",

                                  command=lambda: options('Stress', parent, controller, graph))
        stress_button.place(x=212, y=235)
        anxious_button = tk.Button(lower_frame, text="Anxiousness", height=3, width=20,
                                   bg="white",

                                   command=lambda: options('Anxiousness', parent, controller,
                                                           graph))
        anxious_button.place(x=400, y=235)
        procrastination_button = tk.Button(lower_frame, text="Procrastination", height=3, width=20,
                                           bg="white",
                                           command=lambda: options(
                                               'Procrastination', parent, controller, graph))
        procrastination_button.place(x=212, y=315)


class Options(tk.Frame):
    """
    The Options page (second page) of the Upside App that displays the four options:
    description, effects, causes and coping mechanism.

    Instance Attributes:
        - parent: The frame/parent of self
        - controller: The main window of the page/main point of intersection for all pages
        - emotion: The emotion whose options are going to be displayed. (selected emotion)
        - graph: The graph used to represent an emotion app network.
    """
    parent: tk.Frame
    controller: tk.Tk
    emotion: str
    graph: upside2.Graph

    def __init__(self, parent: tk.Frame, controller: tk.Tk, emotion: str, graph: upside2.Graph) \
            -> None:
        """
        Initialize a new window which second page of the Upside app. Display the four OPTIONS:
        description, effects, causes and coping mechanism for the inputted emotion. (This window
        only shows the options, not the actual description, effects, etc.)

        Preconditions:
            - emotion in {'Sadness', 'Fear', 'Vulnerability', 'Exhaustion', 'Envy', 'Jealousy',
              'Anger', 'Stress', 'Anxiousness', 'Procrastination'}
        """
        tk.Frame.__init__(self, parent, bg="pink")

        # creating label
        label2 = tk.Label(self, text="What would you like to read about?", bg="pink",
                          fg="white", font="none 20 bold")
        label2.place(x=75, y=100)

        # adding description button
        des_button = tk.Button(self, text="Description", height=3, width=20,
                               command=lambda: specifics(emotion, 'description', parent,
                                                         controller, graph))
        des_button.place(x=80, y=300)

        # adding effects button
        effects_button = tk.Button(self, text="Effects", height=3, width=20,
                                   command=lambda: specifics(emotion, 'effects', parent,
                                                             controller, graph))
        effects_button.place(x=370, y=300)

        # adding causes button
        causes_button = tk.Button(self, text="Causes", height=3, width=20,
                                  command=lambda: specifics(emotion, 'causes', parent,
                                                            controller, graph))
        causes_button.place(x=80, y=500)

        # adding coping mechanism button
        coping_button = tk.Button(self, text="Coping Mechanisms", height=3, width=20,
                                  command=lambda: specifics(emotion, 'coping mechanism', parent,
                                                            controller, graph))
        coping_button.place(x=370, y=500)

        # adding back button -> returns to start page (previous page)
        back_button = tk.Button(self, text="Back", height=3, width=12,
                                command=lambda: controller.show_frame(StartPage))
        back_button.place(x=500, y=590)


class Specifics(tk.Frame):
    """
    The specifics page (third page) of the Upside App that either displays the associated
    description, effects or causes of the selected emotion or the associated coping mechanism of
    selected emotion and options to add new coping mechanism (healthy or unhealthy).

    Instance Attributes:
        - parent_controller: A tuple representing the parent: The frame/parent of self and the
          controller: The main window of the page/main point of intersection for all pages
        - info: The associated text (str) that is to be displayed (filtered by inputted kind and
                inputted emotion)
        - kind_emotion: kind is the type of the vertex that is to be accessed: 'emotion' or
                        'description' or 'causes' or 'effects' or 'coping mechanism' or 'journal'
                        and emotion: The emotion whose options are going to be displayed.
                        (selected emotion) :
                        'Sadness' or 'Fear' or 'Vulnerability' or 'Exhaustion' or 'Envy' or
                         'Jealousy' or 'Anger' or 'Stress' or 'Anxiousness' or 'Procrastination'
        - graph: The graph used to represent an emotion app network.
    """
    parent_controller: tuple
    info: str
    kind_emotion: tuple
    graph: upside2.Graph

    def __init__(self, parent_controller: tuple, info: str, kind_emotion: tuple,
                 graph: upside2.Graph) -> None:
        """
        Initialize a new window that either displays the associated
        description, effects or causes of the selected emotion or the associated coping mechanism of
        selected emotion and options to add new coping mechanism (healthy or unhealthy).

        Preconditions:
            - emotion in {'Sadness', 'Fear', 'Vulnerability', 'Exhaustion', 'Envy', 'Jealousy',
              'Anger', 'Stress', 'Anxiousness', 'Procrastination'}
            - kind in {'emotion', 'description', 'causes', 'effects','coping mechanism', 'journal'}
        """
        # parent, controller = parent_controller[0], parent_controller[1]
        tk.Frame.__init__(self, parent_controller[0], bg="pink")
        info_lines = textwrap.fill(info, 54)
        max_so_far = 0
        for i in range(len(info_lines)):
            if len(info_lines[i]) > max_so_far:
                max_so_far = len(info_lines[i])

        if kind_emotion[0] == 'causes':
            split_lines = info.split(',')
            for line in split_lines:
                if len(line) > 55:
                    split_lines.remove(line)
                    split_lines.append(textwrap.fill(line, 55))

            # adding text and scrollbar
            t = tk.Text(self, width=55, height=300, wrap=None,
                        bg="pink", font="none 16 bold", fg="white")
            scroll = ttk.Scrollbar(self, command=t.yview)

            for line in split_lines:
                t.insert("end", line + "\n\n")

            scroll.pack(side="right", fill="y")
            t.configure(state="disabled")
            t.pack(side="top", fill="x")
        elif kind_emotion[0] == 'coping mechanism':
            split_lines = info.split(',')
            for line in split_lines:
                if len(line) > 30:
                    split_lines.remove(line)
                    split_lines.append(textwrap.fill(line, 30))

            t = tk.Text(self, width=55, height=300, wrap=None,
                        bg="pink", font="none 16 bold", fg="white")
            scroll = ttk.Scrollbar(self, command=t.yview)

            for line in split_lines:
                t.insert("end", line + "\n\n")

            scroll.pack(side="right", fill="y")
            t.configure(state="disabled")
            t.pack(side="top", fill="x")

            # adding journal button (opens up journal window)
            tk.Button(self, text="Journal", height=3, width=20,
                      command=lambda: journal(info, parent_controller[0], parent_controller[1],
                                              kind_emotion[1],
                                              graph)).place(x=310, y=590)

            # textbox
            tk.Label(self, text='Enter a Coping Mechanism', bg='pink', fg='white',
                     font='none 12 bold').place(x=350, y=10)

            # entry box
            entry = tk.Entry(self, width=35)
            entry.place(x=350, y=40)
            tk.Label(self, text='Is this healthy or unhealthy:', bg='pink',
                     fg='white', font='none 12 bold').place(x=350, y=70)

            # inserting healthy button
            tk.Button(self, text='Healthy',
                      command=lambda: _insert_mechanism(parent_controller, entry,
                                                        (kind_emotion[1], 'coping mechanism'),
                                                        ('data/emotions.csv', graph)),
                      bg='white').place(x=350, y=100)

            # inserting unhealthy button
            tk.Button(self, text='Unhealthy',
                      command=lambda: _insert_mechanism(parent_controller, entry,
                                                        (kind_emotion[1], 'unhealthy'),
                                                        ('data/emotions.csv', graph)),
                      bg='white').place(x=450, y=100)

            tk.Button(self, text='Unhealthy Habit Tracker', bg='white',
                      height=1, width=30,
                      command=lambda: habit_tracker(parent_controller[0], parent_controller[1],
                                                    'data/time.csv')).place(x=350, y=150)
        else:
            # insert information in a label
            tk.Label(self, text=info_lines, bg="pink",
                     fg="white", font="none 16 bold").place(x=max_so_far + 15,
                                                            y=300 - (((len(
                                                                info) // 54) // 2) * 20) - 50)

        # insert back button (goes back to previous page)
        tk.Button(self, text="Back", height=3, width=12,
                  command=lambda: parent_controller[1].show_frame(Options)).place(x=470, y=590)


class Journal(tk.Frame):
    """
    The Options page that displays an option to choose a coping mechanism, add text and
    rate the selected coping mechanism.

    Instance Attributes:
        - parent_controller: A tuple representing the parent: The frame/parent of self and the
          controller: The main window of the page/main point of intersection for all pages
        - info: The coping mechanisms (str) that is associated with the emotion attribute.
        - emotion: The emotion for which the user uses the journal window. (selected emotion):
                  'Sadness' or 'Fear' or 'Vulnerability' or 'Exhaustion' or 'Envy' or 'Jealousy' or
                  'Anger' or 'Stress' or 'Anxiousness' or 'Procrastination'
        - graph: The graph used to represent an emotion app network.
    """
    parent_controller: tuple
    info: str
    emotion: str
    graph: upside2.Graph

    def __init__(self, parent_controller: tuple, info: str, emotion: str,
                 graph: upside2.Graph) -> None:
        """
        Initialize a new window that displays an option to choose a coping mechanism, add text and
        rate the selected coping mechanism.
        Initialize button to view past journal entries.

        Preconditions:
            - emotion in {'Sadness', 'Fear', 'Vulnerability', 'Exhaustion', 'Envy', 'Jealousy',
              'Anger', 'Stress', 'Anxiousness', 'Procrastination'}
        """
        parent, controller = parent_controller[0], parent_controller[1]
        tk.Frame.__init__(self, parent, bg="pink")
        # frame to insert the drop down menu
        upper_frame = tk.LabelFrame(self, width=580, height=150)
        upper_frame.grid(row=0, column=0, padx=10, pady=10)

        # drooped down menu
        clicked = tk.StringVar()
        clicked.set("Pick a coping mechanism")
        menu_options = info.split(',')
        tk.OptionMenu(upper_frame, clicked, *menu_options).pack()

        # frame to insert text box
        middle_frame = tk.LabelFrame(self, width=580, height=400)
        middle_frame.grid(column=0)
        txt_edit = tk.Text(middle_frame, width=71, height=25)
        txt_edit.place(x=0, y=0)

        # frame to rate the chosen coping mechanism
        # contains the Yes or No button and Submit button
        bottom_frame = tk.LabelFrame(self, width=580, height=100, bg="pink")
        bottom_frame.grid(column=0, padx=10, pady=10)
        # Question label
        tk.Label(bottom_frame, text="Was this coping mechanism useful?", bg="black",
                 fg="white",
                 font="none 12 bold").place(x=0, y=0)

        clicked_radio = tk.BooleanVar()

        # insert yes radio button
        tk.Radiobutton(bottom_frame, text="Yes", value=True,
                       variable=clicked_radio,
                       height=2, width=10).place(x=25, y=40)
        # insert no radio button
        tk.Radiobutton(bottom_frame, text="No", value=False,
                       variable=clicked_radio,
                       height=2, width=10).place(x=150, y=40)

        # insert submit button
        tk.Button(bottom_frame, text="Submit", height=2, width=10,
                  bg="white", font="none 12 bold",
                  command=lambda: _submit_clicked(clicked_radio.get(),
                                                  clicked.get(), (emotion, info), parent_controller,
                                                  (txt_edit.get(1.0, 'end-1c'), graph)
                                                  )).place(x=325, y=20)

        # insert past_entries button (opens up past displays of journal entries)
        past_entries_button = tk.Button(bottom_frame, text="Past Journal Entries", height=3,
                                        width=15, bg="white", font="none 8 bold",
                                        command=lambda: display_journal(clicked.get(),
                                                                        parent_controller, info,
                                                                        emotion,
                                                                        graph))
        past_entries_button.place(x=450, y=20)

        # back to start page button
        tk.Button(self, text="Back To Main Page", height=3,
                  width=15, bg="white", font="none 8 bold",
                  command=lambda: controller.show_frame(StartPage)).place(x=465, y=580)


class Recommendations(tk.Frame):
    """
    The recommendations page that displays a random healthy coping mechanism that is connected by a
    path to the inputted unhealthy coping mechanism.

    Instance Attributes:
        - parent_controller: A tuple representing the parent: The frame/parent of self and the
          controller: The main window of the page/main point of intersection for all pages
        - unhealthy: The text inputted by the user as being an unhealthy coping mechanism
        - emotion: The emotion that is selected by the user in start page:
                  'Sadness' or 'Fear' or 'Vulnerability' or 'Exhaustion' or 'Envy' or 'Jealousy' or
                  'Anger' or 'Stress' or 'Anxiousness' or 'Procrastination'
        - graph: The graph used to represent an emotion app network.
    """
    parent_controller: tuple
    unhealthy: str
    emotion: str
    graph: upside2.Graph

    def __init__(self, parent_controller: tuple, unhealthy: str, emotion: str,
                 graph: upside2.Graph) -> None:
        """
        Initialize a new window that that displays a random healthy coping mechanism that is
        connected by a path to the inputted unhealthy coping mechanism.

        Preconditions:
            - emotion in {'Sadness', 'Fear', 'Vulnerability', 'Exhaustion', 'Envy', 'Jealousy',
              'Anger', 'Stress', 'Anxiousness', 'Procrastination'}
        """
        parent, controller = parent_controller[0], parent_controller[1]
        tk.Frame.__init__(self, parent, bg="pink")
        label1 = tk.Label(self, text="We recommend you to try" + upside2.
                          recommend_coping_mechanism(graph, unhealthy),
                          bg="pink",
                          fg="white",
                          font="none 12 bold")
        label1.place(x=0, y=0)
        back_button = tk.Button(self, text="Back", height=3, width=12,
                                command=lambda: specifics(emotion, 'coping mechanism',
                                                          parent, controller, graph))
        back_button.place(x=470, y=590)


class DisplayJournals(tk.Frame):
    """
    The page that displays all the past entries for a specific coping mechanism of a specific
    emotion.

    Instance Attributes:
        - parent_controller: A tuple representing the parent: The frame/parent of self and the
          controller: The main window of the page/main point of intersection for all pages
        - journals: All the journal entries that are associated with the selected coping mechanism
                    (Multiple journal entries but kept type as str)
        - copmech_emotion: copmech is a coping mechanism selected by the user and emotion is the
                           emotion that is selected by the user in start page:
                           'Sadness' or 'Fear' or 'Vulnerability' or 'Exhaustion' or 'Envy' or
                           'Jealousy' or 'Anger' or 'Stress' or 'Anxiousness' or 'Procrastination'
        - graph: The graph used to represent an emotion app network.
    """
    parent_controller: tuple
    journals: str
    copmech_emotion: tuple
    graph: upside2.Graph

    def __init__(self, parent_controller: tuple, journals: list, copmech_emotion: tuple,
                 graph: upside2.Graph) -> None:
        """
        Initialize a new window that displays all the journal entries (journals) for a selected
        coping mechanism (info)

        Preconditions:
            - emotion in {'Sadness', 'Fear', 'Vulnerability', 'Exhaustion', 'Envy', 'Jealousy',
              'Anger', 'Stress', 'Anxiousness', 'Procrastination'}
        """
        parent, controller = parent_controller[0], parent_controller[1]
        tk.Frame.__init__(self, parent, bg="pink")
        split_lines = [','.join(journals)]
        for i in range(0, len(split_lines)):
            if len(split_lines[i]) > 55:
                new_lines = textwrap.fill(split_lines[i], 55)
                split_lines.remove(split_lines[i])
                split_lines.append(new_lines)

        # insert text and scroll bar
        t = tk.Text(self, width=55, height=300, wrap=None,
                    bg="pink", font="none 16 bold", fg="white")
        scroll = ttk.Scrollbar(self, command=t.yview)

        for line in split_lines:
            t.insert("end", line + "\n")

        scroll.pack(side="right", fill="y")
        t.configure(state="disabled")
        t.pack(side="top", fill="x")

        # insert back button (brings back to Journal page)
        back_button = tk.Button(self, text="Back", height=3, width=12,
                                command=lambda: journal(copmech_emotion[0],
                                                        parent, controller, copmech_emotion[1],
                                                        graph))
        back_button.place(x=470, y=590)


class HabitTracker(tk.Frame):
    """
    The page that displays the amount of days since the user has last engaged in an unhealthy coping
    mechanism. (options to start and restart the tracker)

    Instance Attributes:
        - parent: The frame/parent of self
        - controller: The main window of the page/main point of intersection for all pages
        - started: False if user has not pressed on start button or pressed on restart button and
                   True if start button has been pressed.
        - days: the number of days that has elapsed since the an unhealthy coping mechanism has been
                entered
    """
    parent: tk.Frame
    controller: tk.Tk
    started: bool
    days: Union[str, int]

    def __init__(self, parent: tk.Frame, controller: tk.Tk, started: bool, days: Union[str, int]) \
            -> None:
        """
        Initialize a new window that displays the amount of days since user has last engaged in an
        unhealthy coping mechanism.
        """
        tk.Frame.__init__(self, parent, bg='pink')
        if started is False:
            label = tk.Label(self, text='Press start to start timer:', bg='pink', fg='white',
                             font='none 12 bold')
            label.place(x=170, y=250)
            start_button = tk.Button(self, text='Start', command=lambda: start_timer(
                True, days, parent, controller, 'data/time.csv'))
            start_button.place(x=370, y=250)
        else:
            label = tk.Label(self, text="Congratulations! \n You haven't engaged in an unhealthy "
                                        "coping mechanism in " + days + " days.", bg='pink',
                             fg='white', font='none 12 bold')
            label.place(x=50, y=250)
            restart_button = tk.Button(self, text='Restart Timer', command=lambda: start_timer(
                False, days, parent, controller, 'data/time.csv'))
            restart_button.place(x=250, y=300)

        # back button to return to the Specifics page
        back_button = tk.Button(self, text="Back", height=3, width=12,
                                command=lambda: controller.show_frame(Specifics))
        back_button.place(x=470, y=590)


def options(emotion: str, parent: tk.Frame, controller: tk.Tk, graph: upside2.Graph) -> None:
    """
    Display a new screen with four options: description, causes, effects, and coping mechanisms for
    the inputted emotion.

    Preconditions:
        - emotion in {'Sadness', 'Fear', 'Vulnerability', 'Exhaustion', 'Envy', 'Jealousy',
          'Anger', 'Stress', 'Anxiousness', 'Procrastination'}
    """
    frame = Options(parent, controller, emotion, graph)
    controller.frames[Options] = frame
    frame.grid(row=0, column=0, sticky='nsew')
    frame.tkraise()


def specifics(emotion: str, kind: str, parent: tk.Frame, controller: tk.Tk, graph: upside2.Graph) \
        -> None:
    """
    Display a new screen with the associated description/causes/effects/coping mechanisms for the
    inputted emotion.

    Preconditions:
        - emotion in {'Sadness', 'Fear', 'Vulnerability', 'Exhaustion', 'Envy', 'Jealousy',
          'Anger', 'Stress', 'Anxiousness', 'Procrastination'}
        - kind in {'emotion', 'description', 'causes', 'effects','coping mechanism', 'journal'}
    """
    tuple_parent_controller = (parent, controller)
    tuple_kind_emotion = (kind, emotion)
    if kind != 'coping mechanism':
        info = graph.get_neighbour_by_kind(emotion, kind)
        frame = Specifics(tuple_parent_controller, info[0], tuple_kind_emotion, graph)
    else:
        # only display the coping mechanism whose vertices have rating True
        info = graph.get_neighbour_by_kind_rate(emotion, rating=True, kind=kind)
        new_list = [','.join(info)]
        frame = Specifics(tuple_parent_controller, new_list[0], tuple_kind_emotion, graph)

    controller.frames[Specifics] = frame
    frame.grid(row=0, column=0, sticky='nsew')
    frame.tkraise()


def journal(coping_mechanism: str, parent: tk.Frame, controller: tk.Tk, emotion: str,
            graph: upside2.Graph) -> None:
    """Display a new screen where the user can select a coping mechanism, add text, and choose
    whether the coping mechanism was helpful or not.

    Preconditions:
        - emotion in {'Sadness', 'Fear', 'Vulnerability', 'Exhaustion', 'Envy', 'Jealousy',
          'Anger', 'Stress', 'Anxiousness', 'Procrastination'}
    """
    tuple_parent_controller = (parent, controller)
    frame = Journal(tuple_parent_controller, coping_mechanism, emotion, graph)
    controller.frames[Options] = frame
    frame.grid(row=0, column=0, sticky='nsew')
    frame.tkraise()


def recommendations(parent: tk.Frame, controller: tk.Tk, unhealthy: str, emotion: str,
                    graph: upside2.Graph) -> None:
    """
    Display a new screen that displays a randomly selected healthy coping mechanism for the inputted
    unhealthy coping mechanism, unhealthy.

    Preconditions:
        - emotion in {'Sadness', 'Fear', 'Vulnerability', 'Exhaustion', 'Envy', 'Jealousy',
          'Anger', 'Stress', 'Anxiousness', 'Procrastination'}
    """
    tuple_parent_controller = (parent, controller)
    frame = Recommendations(tuple_parent_controller, unhealthy, emotion, graph)
    controller.frames[Recommendations] = frame
    frame.grid(row=0, column=0, sticky='nsew')
    frame.tkraise()


def display_journal(coping_mechanism: str, parent_controller: tuple, info: str,
                    emotion: str, graph: upside2.Graph) -> None:
    """
    Display a new screen containing the journal entries for the inputted coping_mechanism.

    Preconditions:
        - emotion in {'Sadness', 'Fear', 'Vulnerability', 'Exhaustion', 'Envy', 'Jealousy',
          'Anger', 'Stress', 'Anxiousness', 'Procrastination'}
    """
    # get all journal entries for the inputted coping mechanism
    journal_entries = graph.get_neighbour_by_kind(coping_mechanism, 'journal')
    info_emotion = (info, emotion)
    frame = DisplayJournals(parent_controller, journal_entries, info_emotion, graph)
    parent_controller[1].frames[DisplayJournals] = frame
    frame.grid(row=0, column=0, sticky='nsew')
    frame.tkraise()


def habit_tracker(parent: tk.Frame, controller: tk.Tk, file_name: str) -> None:
    """
    Display a new screen that displays the amount of days that the user has last engaged in an
    unhealthy coping mechanism.
    Include a start and reset button.

    Preconditions:
        - file_name is the path to the time.csv file
    """
    data = upside2.read_time_csv(file_name)
    started = False
    days = int(float(data['day']))
    if data['started'] == 'yes':
        started = True
        current_time = datetime.datetime.now().date()
        past_time = datetime.datetime.strptime(data['past time'], '%Y-%m-%d')
        temp = current_time - past_time.date()
        temp = temp.days
        days = days + temp
        upside2.edit_time_csv(started, days, file_name)
    frame = HabitTracker(parent, controller, started, str(days))
    controller.frames[HabitTracker] = frame
    frame.grid(row=0, column=0, sticky='nsew')
    frame.tkraise()


def start_timer(started: bool, days: int, parent: tk.Frame, controller: tk.Tk, file_name: str) -> \
        None:
    """
    If started is True, edit the start time in the file with path file_name, else does not edit the
    start time.

    Preconditions:
        - file_name is the path to the time.csv file
    """
    upside2.edit_time_csv(started, days, file_name)

    habit_tracker(parent, controller, file_name)


def _submit_clicked(value: bool, coping_mechanism: str, emotion_info: tuple,
                    parent_controller: tuple, text_graph: tuple) -> None:
    """
    Set the value of the selected _Vertex of kind coping mechanism to the selected value.
    Add the journal entry to the graph as a _Vertex with kind 'journal' and add an edge
    between the entered coping mechanism vertex and the created journal vertex.
    Save the text in the csv file with filename: 'data/journal_entries.csv' along with the selected
    coping mechanism.

    Preconditions:
        - emotion in {'Sadness', 'Fear', 'Vulnerability', 'Exhaustion', 'Envy', 'Jealousy',
          'Anger', 'Stress', 'Anxiousness', 'Procrastination'}
    """
    emotion, info = emotion_info[0], emotion_info[1]
    text, graph = text_graph[0], text_graph[1]
    # if user did not find the coping mechanism helpful -> remove it from emotions.csv file
    if value is False:
        graph.change_vertex_rate(coping_mechanism, value)
        upside2.edit_file('data/emotions.csv',
                          graph.get_neighbour_by_kind_rate(emotion, True, 'coping mechanism'),
                          emotion)

    journal(info, parent_controller[0], parent_controller[1], emotion, graph)

    # add text in the graph as a vertex with kind 'journal'
    graph.add_vertex(text, 'journal')
    graph.add_edge(coping_mechanism, text)

    # add the entered text to the csv file
    _save_text(text, coping_mechanism, 'data/journal_entries.csv')


def _save_text(text: str, coping_mechanism: str, file_name: str) -> None:
    """
    Save the text along with the inputted coping_mechanism in a csv file with the inputted
    filename.

    Preconditions:
        - file_name is the path to the journal_entries.csv file
    """
    file = pd.read_csv(file_name)
    index_list = file.index[file['Coping Mechanisms'] == coping_mechanism].tolist()
    # inputted coping mechanism does not exist in the csv file
    if index_list == []:
        file = file.append({'Coping Mechanisms': coping_mechanism, 'Journal Entries': text},
                           ignore_index=True)
    # inputted coping mechanism already exists in the csv file -> add new entry
    else:
        index = index_list[0]
        file.at[index, 'Journal Entries'] += ',' + text
    file.to_csv(file_name, index=False)


def _insert_mechanism(parent_controller: tuple, entry: tk.Entry, emotion_kind: tuple,
                      file_name_graph: tuple) -> None:
    """
    Add user input, entry a vertex in the graph adjacent to the inputted emotion.
    Add user input, entry to the file with path file_name
    If coping mechanism is unhealthy, then display a healthy coping mechanism using the
    recommendations window.

    Preconditions:
        - emotion in {'Sadness', 'Fear', 'Vulnerability', 'Exhaustion', 'Envy', 'Jealousy',
          'Anger', 'Stress', 'Anxiousness', 'Procrastination'}
        - kind in {'emotion', 'description', 'causes', 'effects','coping mechanism', 'journal'}
        - file_name is the path to the emotions.csv file
    """
    emotion, kind = emotion_kind[0], emotion_kind[1]
    parent, controller = parent_controller[0], parent_controller[1]
    file_name, graph = file_name_graph[0], file_name_graph[1]
    user_input = entry.get()
    graph.add_vertex(user_input, kind, True)
    graph.add_edge(user_input, emotion)

    if kind == 'coping mechanism':
        specifics(emotion, 'coping mechanism', parent, controller, graph)
        upside2.edit_file(file_name,
                          graph.get_neighbour_by_kind(emotion, 'coping mechanism'),
                          emotion)
    else:
        recommendations(parent, controller, user_input, emotion, graph)


if __name__ == '__main__':
    import python_ta.contracts
    python_ta.contracts.check_all_contracts()

    import doctest
    doctest.testmod(verbose=True)

    import python_ta
    python_ta.check_all(config={
        'extra-imports': ['tkinter', 'upside2', 'textwrap', 'PIL', 'pandas', 'datetime',
                          'typing.Union', 'typing.Any'],
        'allowed-io': [],
        'max-line-length': 100,
        'disable': ['E1136']
    })
