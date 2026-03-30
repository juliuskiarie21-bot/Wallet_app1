import json
import os

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.properties import StringProperty


# -------------------------
# FILE NAMES
# -------------------------

USER_FILE = "users.json"
DATA_FILE = "wallet_data.json"


# -------------------------
# CREATE FILES IF MISSING
# -------------------------

def create_files():

    if not os.path.exists(USER_FILE):
        with open(USER_FILE, "w") as f:
            json.dump({}, f)

    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w") as f:
            json.dump({
                "balance": 0,
                "history": [],
                "goals": []
            }, f)


create_files()


# -------------------------
# LOAD / SAVE FUNCTIONS
# -------------------------

def load_data():
    with open(DATA_FILE, "r") as f:
        return json.load(f)


def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)


def load_users():
    with open(USER_FILE, "r") as f:
        return json.load(f)


def save_users(users):
    with open(USER_FILE, "w") as f:
        json.dump(users, f)


# -------------------------
# SCREENS
# -------------------------

class LoginScreen(Screen):

    def login(self):

        username = self.ids.username.text
        password = self.ids.password.text

        users = load_users()

        if username in users and users[username] == password:

            self.manager.current = "dashboard"

        else:
            print("Wrong login")

    def register(self):

        username = self.ids.username.text
        password = self.ids.password.text

        users = load_users()

        users[username] = password

        save_users(users)

        print("User registered")


# -------------------------

class DashboardScreen(Screen):

    balance_text = StringProperty("KES 0")

    def on_enter(self):

        data = load_data()

        self.balance_text = "KES " + str(data["balance"])


# -------------------------

class SendScreen(Screen):

    def send_money(self, amount):

        data = load_data()

        amount = int(amount)

        if data["balance"] >= amount:

            data["balance"] -= amount

            data["history"].append(
                "Sent KES " + str(amount)
            )

            save_data(data)

            print("Money Sent")

        else:
            print("Not enough balance")


# -------------------------

class ReceiveScreen(Screen):

    def receive_money(self, amount):

        data = load_data()

        data["balance"] += int(amount)

        data["history"].append(
            "Received KES " + amount
        )

        save_data(data)

        print("Money Received")


# -------------------------

class SavingsScreen(Screen):

    def add_goal(self, name, amount):

        data = load_data()

        goal = {
            "name": name,
            "amount": amount
        }

        data["goals"].append(goal)

        save_data(data)

        print("Goal added")


# -------------------------

class HistoryScreen(Screen):

    def on_enter(self):

        data = load_data()

        history_text = "\n".join(
            data["history"]
        )

        self.ids.history_label.text = history_text


# -------------------------

class GoalScreen(Screen):

    def on_enter(self):

        data = load_data()

        goals_text = ""

        for g in data["goals"]:

            goals_text += (
                g["name"]
                + " - KES "
                + str(g["amount"])
                + "\n"
            )

        self.ids.goal_label.text = goals_text


# -------------------------
# WINDOW MANAGER
# -------------------------

class WindowManager(ScreenManager):
    pass


# -------------------------
# MAIN APP
# -------------------------

class WalletApp(App):

    def build(self):

        return Builder.load_file("wallet.kv")


# -------------------------

if __name__ == "__main__":

    WalletApp().run()