import os
import requests
import urllib.parse

from cs50 import SQL
from flask import redirect, render_template, request, session
from functools import wraps
from datetime import datetime

db = SQL("sqlite:///schedule.db")


def apology(message, code=400):
    # Render message as an apology to user.
    def escape(s):

       # Escape special characters.

       # https://github.com/jacebrowning/memegen#special-characters

        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code

def login_required(f):

    # Decorate routes to require login.

    # https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


# Contact API

def get_quote():
# Contact API

    try:
        url = f"https://zenquotes.io/api/random"
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException:
        return None

    # Parse response
    try:
        quote = response.json()
        return {
            #should return a nicely formatted quote
            "q": quote[0]["q"],
            "a": quote[0]["a"]
        }

    except (KeyError, TypeError, ValueError):
        return None


def update():

    started_task_id = db.execute("SELECT id FROM tasks WHERE user_id = ? AND start IS NOT NULL AND end IS NULL", session["user_id"])

    # note all below (and above) ONLY WORKS IF start and end are STRINGS!!! (Lots of converting between STRING and DATETIME going on)

    # From https://stackoverflow.com/questions/1345827/how-do-i-find-the-time-difference-between-two-datetime-objects-in-python
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Current_time in datetime format (not string format as in the above line of code)
    current_time_f = datetime.strptime(current_time, '%Y-%m-%d %H:%M:%S')

    # Get start_time from database (in string format by default)
    start_time = db.execute("SELECT start FROM tasks WHERE user_id = ? AND end IS NULL AND start IS NOT NULL", session["user_id"])[0]["start"]

    # Convert start_time to datetime format as well
    start_time_f = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')

    # Time difference (by function definition, since both current_time_f and start_time_f are of TYPE datetime now)
    elapsed_time = current_time_f - start_time_f

    # Duration of elapsed_time in seconds
    duration_in_s = elapsed_time.total_seconds()

    # Duration of elapsed_time in minutes
    duration_in_m = int(duration_in_s / 60)

    db.execute("UPDATE tasks SET elapsed = ? WHERE user_id = ? AND id = ?", duration_in_m, session["user_id"], int(started_task_id[0]["id"]))

    active_duration = int(db.execute("SELECT duration FROM tasks WHERE user_id = ? AND id = ?", session["user_id"], int(started_task_id[0]["id"]))[0]["duration"])
    if duration_in_m >= active_duration:
        overtime = duration_in_m - active_duration
        db.execute("UPDATE tasks SET overtime = ? WHERE user_id = ? AND id = ?", overtime, session["user_id"], int(started_task_id[0]["id"]))

    return True

