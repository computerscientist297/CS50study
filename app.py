import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
from datetime import date

from helpers import apology, login_required, get_quote, update
# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///schedule.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET", "POST"])
@login_required
def index():

    # Checking if there is a current started task (start is not null and end is null)
    started_task_id = db.execute(
        "SELECT id FROM tasks WHERE user_id = ? AND start IS NOT NULL AND end IS NULL", session["user_id"])
    if not started_task_id:
        current_start = 0
    else:
        current_start = 1


    # If request method is post:
    if request.method == "POST":

        # If the user clicked the "add task" button
        if "task_add" in request.form:
            subject = request.form.get("subject")
            task_name = request.form.get("task_name")

            if not subject:
                return apology("Please enter a subject")

            elif not task_name:
                return apology("Please enter your task")

            db.execute("INSERT INTO tasks (user_id, subject, task_name) VALUES (?, ?, ?)",
                       session["user_id"], subject, task_name)
            return redirect("/")

        # If the user clicked the "start"/"finish" button
        elif "task_start" in request.form:

            started_task = request.form.get("started_task")
            duration = request.form.get("duration")

            # Check if the user put in the duration and task they want to start
            if not duration:
                return apology("Please enter a planned duration in minutes")

            elif not started_task:
                return apology("Please select a task to start")

            # From https://stackoverflow.com/questions/34046634/insert-into-a-mysql-database-timestamp
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            db.execute("UPDATE tasks SET duration = ?, start = ? WHERE user_id = ? AND task_name = ?",
                       duration, current_time, session["user_id"], started_task)
            active_task = db.execute(
                "SELECT * FROM tasks WHERE user_id = ? AND end IS NULL AND start IS NOT NULL", session["user_id"])

            return redirect("/")

        # If the task has already been started
        elif "task_finish" in request.form:
            # Get current time
            # From https://stackoverflow.com/questions/34046634/insert-into-a-mysql-database-timestamp
            update()
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            # Update end time for the task
            db.execute("UPDATE tasks SET end = ? WHERE user_id = ? AND id = ?",
                       current_time, session["user_id"], int(started_task_id[0]["id"]))

            return redirect("/")

        elif "task_delete" in request.form:
            deleted_task = request.form.get("delete_task")
            db.execute("DELETE FROM tasks WHERE user_id = ? AND task_name = ?",
                       session["user_id"], deleted_task)
            return redirect("/")

        elif "update_task" in request.form:

            update()
            return redirect("/")

        else:
            return apology("Not found")

    # If request method is get:
    else:

        # Display user's tasks in table format

        if started_task_id:
            update()
        tasks = db.execute(
            "SELECT * FROM tasks WHERE user_id = ? AND end IS NULL AND start IS NULL", session["user_id"])
        active_task = db.execute(
            "SELECT * FROM tasks WHERE user_id = ? AND end IS NULL AND start IS NOT NULL", session["user_id"])
        return render_template("index.html", tasks=tasks, active_task=active_task, current_start=current_start)


@app.route("/motivation", methods=["GET"])
@login_required
def motivation():

    finished_tasks = db.execute(
        "SELECT * FROM tasks WHERE user_id = ? AND start IS NOT NULL AND end IS NOT NULL ORDER BY end DESC LIMIT 10", session["user_id"])
    total_finished = db.execute(
        "SELECT * FROM tasks WHERE user_id = ? AND start IS NOT NULL AND end IS NOT NULL", session["user_id"])
    task_count = 0
    for _ in total_finished:
        task_count += 1

    motivation = get_quote()
    if db.execute("SELECT task_name FROM tasks WHERE user_id = ? AND start IS NOT NULL AND end IS NULL", session["user_id"]):
        active_task = db.execute(
            "SELECT task_name FROM tasks WHERE user_id = ? AND start IS NOT NULL AND end IS NULL", session["user_id"])[0]["task_name"]
        update()
        elapsed_time = db.execute(
            "SELECT elapsed FROM tasks WHERE user_id = ? AND start IS NOT NULL AND end IS NULL", session["user_id"])[0]["elapsed"]
        duration_time = db.execute(
            "SELECT duration FROM tasks WHERE user_id = ? AND start IS NOT NULL AND end IS NULL", session["user_id"])[0]["duration"]

        percentage = elapsed_time / duration_time * 100
        if percentage > 100:
            percentage = 100

        # From https://stackoverflow.com/questions/3400965/getting-only-1-decimal-place
        rounded_percentage = round(percentage, 1)

        return render_template("motivation.html", active_task=active_task, motivation=motivation, rounded_percentage=rounded_percentage, finished_tasks=finished_tasks)

    else:
        return render_template("motivation.html", motivation=motivation, finished_tasks=finished_tasks, task_count=task_count)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?",
                          request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


def password_check(password):
    special_char = ["$", "@", "#", "%", "!", "*"]
    if not any(char in special_char for char in password):
        return False
    else:
        return True


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # If request method is GET, render register.html
    if request.method == "GET":
        return render_template("register.html")

    # If request method is POST
    else:

        # Defining username, password, and confirmation variables (because password and confirmation are used twice)

        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Checking if username, password, and password confirmation are entered
        if not username:
            return apology("No username")

        elif not password:
            return apology("No password")

        # This line below is not technically needed (since password and confirmation will be compared anyway), but it was included to specify an error if the user doesn't enter their password confirmation
        elif not confirmation:
            return apology("No password confirmation")

        # If password doesn't match password confirmation
        elif password != confirmation:
            return apology("Your passwords don't match")

        # If password doesn't contain a special character
        elif not password_check(password):
            return apology("Password must contain a special character")

        # Try to insert username and password into users table
        try:
            db.execute("INSERT INTO users (username, hash) VALUES (?, ?)",
                       username, generate_password_hash(request.form.get("password")))

        # If this doesn't work (it means the username was already taken because username is unique), return apology
        except:
            return apology("That username already exists")

        return redirect("/")


@app.route("/calendar", methods=["GET", "POST"])
@login_required
def calendar():
    """Get user's productivity score and add to a SQL table"""

    """SQL table (to be added separately, manually) (call it productivity_history) must contain user's score (0-10), and the date,
    FOR EACH USER (so note we'll need some user_id also))"""

    # Side note: in the SQL structure of the table, make sure the TYPE of date is string! because date is not of type datetime.

    if request.method == "POST":

        # do I put the *id* or *name* of the productivity form entry (which is "productivity") or something else?
        if not request.form.get("productivity"):
            return apology("Please enter productivity score")

        elif not request.form.get("mood"):
            return apology("Please enter mood score")

        pscore = int(request.form.get("productivity"))
        mscore = int(request.form.get("mood"))
        # Check something was inputted

        # Check input is integer between 0-10
        if not 0 <= pscore <= 10 or not 0 <= mscore <= 10:
            return apology("Enter numbers between 0-10", 400)

        # Get today's date
        today = date.today()

        # Ensure user cannot input more than once per day
        scores_entries = db.execute("SELECT * FROM scores_history WHERE user_id = ? AND date = ?",
                                    session["user_id"], today)
        if len(scores_entries) > 0:
            return apology("Cannot input more than one entry per day!", 400)

        # Add user's input to history
        db.execute("INSERT INTO scores_history (user_id, pscore, mscore, date) VALUES (?, ?, ?, ?)",
                   session["user_id"], pscore, mscore, today)
        return redirect("/calendar")

    else:
        # Take previous TWENTY entries' worth of mood AND productivity entries
        lines = db.execute(
            "SELECT date, pscore, mscore FROM scores_history WHERE user_id = ? ORDER BY DATE DESC LIMIT 20", session["user_id"])

        # Ensure lines has data
        if not lines:
            return render_template("calendar.html")



# Delete this below?????
        # Create dictionaries of colours corresponding to the productivity and mood scores

        # Transfer colors (as dictionaries, not arrays!) over to calendar.html code
        return render_template("calendar.html", lines=lines)


@app.route("/stats", methods=["GET"])
@login_required
def stats():
    # Execute SQL queries for stats in order

    # Total number of days you've been tracking your productivity and mood:
    query = db.execute("SELECT * FROM scores_history")
    days = len(query)
    pavg = db.execute("SELECT AVG(pscore) FROM scores_history")
    pavg = round(pavg[0]["AVG(pscore)"], 1)
    mavg = db.execute("SELECT AVG(mscore) FROM scores_history")
    mavg = round(mavg[0]["AVG(mscore)"], 1)

    # percentage of days where mood and productivity have been 7 or higher
    happy = db.execute(
        "SELECT * FROM scores_history WHERE pscore >= 7 AND mscore >= 7")
    percent = (len(happy) / days * 100)
    percent = round(percent, 1)

    # Correlation between mood and productivity (all-time; outputs value between -1 and 1)

    # Average productivity over past 10 entries
    pavg10 = db.execute(
        "SELECT AVG(pscore) FROM (SELECT pscore FROM scores_history ORDER BY date DESC LIMIT 10)")

    pavg10 = round(pavg10[0]["AVG(pscore)"])

    # Average mood over past 10 entries
    mavg10 = db.execute(
        "SELECT AVG(mscore) FROM (SELECT mscore FROM scores_history ORDER BY date DESC LIMIT 10)")
    mavg10 = round(mavg10[0]["AVG(mscore)"])

    return render_template("stats.html", days=days, pavg=pavg, mavg=mavg, percent=percent, pavg10=pavg10, mavg10=mavg10)
