Implementation
   The project was written in Python, Javascript, HTML, and CSS. The HTML called upon the Javascript and Python files to give it functionality and the CSS formatted the HTML to make it aesthetically pleasing.


app.py
    This is the main file of the code. This file includes the necessary foundation for the webapp including import statements to import the necessary libraries. Additionally, flask is configured and the musica SQL database is defined.
Users can use GET and POST routes to access the various html files and functions. Some of app.py is based on CS50 finance, although many of the functions and code are original.


The first route is “/” and index.html.


The index.html homepage features a general task manager for people to organize their upcoming tasks and track how long they are spending on tasks. This route first checks if there is a current started task by querying into the SQL database to potentially find a unique task id whose start is not null but end is null (meaning the task has been started). Note that by design of the website, only one task can be started at a time (if there is a started task, the user is incapable of selecting another task to start). If the request method is post, we have to check which form was submitted (because there are multiple forms on index.html). If the “task_add” button was clicked and the user submitted everything properly, insert the user’s data into the tasks SQL database. Next, if the user clicked the “task_start” button, check if the user submitted all the information correctly (could be missing fields), then find the current time in datetime format. Then, update the SQL tasks table with this start time. Else if the user clicked the “task_finish” button, update the SQL database with the update function (in helpers.py) to update the elapsed and overtime columns. Else if the user clicked on “task_delete”, then delete the specific task the user indicated. An else statement is included just in case. Else, if the request method is “get”, we want to display all the tasks in a table format. First, we check if there is an active task going on (if started_task_id). If so, we want to update this task’s elapsed and overtime columns. Then, we query the SQL database for various information about both the active task and other non-active tasks, and render_template along with several other dictionaries/variables (tasks, active_task, and current_start=current_start) for use in the HTML. current_start is especially important because it is needed for certain buttons to register whether or not they should be disabled (for instance, current_start is used as an indicator of whether or not there is an active task currently, and if there is, the “Start a task!” buttons are grayed out except for the “finish!” button—multiple other elements function the same way by first checking {% if current_start == 0 %}, which means there is no started task at the moment).




/motivation and motivation.html
In the motivation route, there were a number of things that needed to be implemented. One of the first sections was the API which was built in a helper function and called in the main python function (app.py). The contents of this motivation = get_quote() are then pushed into the HTML and then called in the HTML using the quotes and the author.


The second part of the motivation route is the history which uses SQL commands in Python to query for the total number of tasks finished as well as the ten most recent finished tasks to display. After querying, we loop through the tasks to first figure out how many total tasks were completed by the user. Then, if there is an active task, calculate the percentage to completion (elapsed_time / duration_time * 100, unless elapsed_time > duration_time, in which case the percent would be 100).




/calendar
Calendar.html is the page where users can access their past inputted productivity and mood scores along with their corresponding dates as well as a textbox to which they can input today’s scores. The shades of colors in the table correspond to the exact productivity and mood scores in the respective table cells: in particular, productivity is set to be colored with green, and we vary shades of green (we use RGBA 0, 255, 0, x) by varying the transparency of the ‘A’ value in the relevant RGBA values. Since possible scores range from 0-10 and the transparency parameter ranges from 0-1, we simply divide by 10 to convert from the former to the latter.
This is an overview of calendar.html; we now go a little more systematically through the /calendar route as it appears in app.py. We first check a few trivial conditions for the inputs to the form, such as ensuring the inputs are integers from 0-10 and that inputs actually exist. Once a valid input has been received, we record the date and time at which the user made the submission, and add the user_id, the two scores, and the datetime to a SQL table called scores_history. To ensure the user does not input more than one set of scores per day, before accepting the submission we first check a submission on the same day does not yet exist. Finally, we decided it was reasonable to list 20 past submissions of the user’s productivity and mood scores for the user to look back and reflect on.


/stats
Stats.html shows a few specially selected statistics our group decided were sufficiently interesting, which are immediately visible by going to the navigation bar and clicking on the Statistics option. To obtain the statistics, we simply ran various SQL queries in Python and passed the relevant variables, dictionaries etc. into html through code such as <return render_template("stats.html", days=days, pavg=pavg, mavg=mavg… > - in this example, days=days means that we can access the days variable in HTML (which we ordinarily cannot).


“/login”
    This was borrowed from CS50 Finance. If the ‘GET’ method is used, the login.html page is rendered with blank inputs. Once the inputs are filled and the button is pressed, the ‘POST’ method is used, which takes the user imputed  username and password and logs the user into their account


“/logout”
    This route was also borrowed from CS50 Finance. It clears the current session and refreshes SQL’s storage until the same user or a different user logs in.
“/register”
    Once again, borrowed from CS50 Finance.
login.html and register.html are implemented in the same way as they were in Pset 9: Finance.
    This file contains the code for listing each follower and follow for the user that is logged in. To do this, an SQL query (in the app.py below /follow) retrieves the names of each user that follows and is followed (from the following and follow tables in the musica.db database) by the main user and sends it back to the follow.html. Next, via Jinja these names are listed using a for loop. Additionally, a form with route /search is implemented for each name in the list so that each user can be clicked on and the main user can be sent to those individuals’ pages. This is implemented via an input tag.


helpers.py
    helpers.py has a number of helper files that are used in the app.py. The first one is the apology messaging that is used when the user runs into an input issue or something not permitted by the code.


The second is the api generation of the quote. It is from a quote api generator is referenced in the code. It first checks the API which is taken from the finance and then stores the response (a list that stores a dictionary) into quotes. It returns a section of the list/dictionary that we need by taking quote[0][“q] and quote[0][“a”] which are used in /motivation.


The last thing in the helpers file is the update which updates the amount of time that is elapsed in the task section. It takes the time at which the start button is clicked and subtracts the current time from the original time and updates this into the SQL server and eventually when it is used in app.py into the table.




styles.css
    Styles.css contains mos of the CSS used in the website. This CSS changes the appearance of the html elements. Among the style included in this file are:
    - Images, colors, and properties for the backgrounds of different elements
    -  borders for different elements
    - Sizing, margins, and alignment for certain elements
    - And some other minor aesthetic properties
    We put the CSS in this file instead of the html as it makes for a cleaner HTML file and makes everything cleaner. It also allows for classes to be created that can be applied to many different html elements instead of a single html element.


Schedule.db
    Schedule.db is a SQL database that contains all of the data stored in our webapp. These are stored in tables called “users,” “mood,” “productivity,” and “tasks.” These store user information (id, username, and password hash), task information (user id, task name, subject name, time allotted, and potential overlap), information on mood and productivity (user id, task name, subject name, time allotted, and potential overlap), and the statistics. Throughout app.py, this database is accessed through SQL queries to pull out data that is ultimately fed to the different html templates and displayed on the website.


requirements.txt
    Prescribes the packages on which this app will depend.


static/
    This contains all of the static files that are used throughout the code. This would include things like images which are called in in the nav-bar.


templates/
   This stores the .html files which are rendered when need be in by app.py/




* What design challenge(s) did you run into while completing your project? How did you choose to address them and why?
What motivated you to complete this project? What features did you want to create and why?
The API was a little strange to implement. Getting it to call initially was working fine but it was a challenge to realize why the code wasn’t calling a specific part of the dictionary took a while. We ended up using quote[0][“q”] because instead of just [“q”] because the dictionary was inside a list (because of Json formatting) and we were not aware of that. Getting it to implement in HTML was also a challenge.
Another major design challenge was ‘passing’ variables from HTML and Python into CSS. This challenge arose because in our calendar table, we wanted to shade the cells of the table according to the numerical score within that cell, and ordinarily, it is not possible to pass variables in such a way. We addressed this by implementing Javascript in order to ‘bridge’ the gap between HTML and CSS - this is because Javascript is a more dynamic language and allows more functionality than HTML, as well as the fact that we could define variables in Javascript and through a sort of concatenation method (using “ + “), pass these variables into CSS. We struggled for very many hours on this problem, and for us, this was an essential problem to solve because we believed the unique aspect of our application was the ability to immediately compare historical productivity and mood trends visually through the color-coded design. For example, without such color-coding, our application would be no different than producing a plain table in Notes on one’s iPhone and recording mood and productivity manually there.
Another motivation for this project was that one of the members of the group had gone looking for an user-friendly productivity and mood tracker but did not find one. The goal for this app was to create an user-friendly productivity and mood tracker along with a task manager. We wanted to help people (and ourselves) be more organized and reflective about our work and mood, thus perhaps contributing positively in impacting users’ mental health, if only slightly.


* Was there a feature in your project you could have implemented in multiple ways? Which way did you choose, and why?



Who are the intended users of your project? What do they want, need, or value?
You should consider your project's users to be those who interact _directly_ with your project, as well as those who might interact with it _indirectly_, through others' use of your project.

The intended users of our project are our students and potentially people who are in the workforce doing tasks that are very clean cut. Our target audience values something that is user-friendly and is functional. It should help keep our target audience more organized and hopefully help them to be more reflective upon their daily lives. Those indirectly impacted by this website could include parents and the peers of students.


### How does your project's impact on users change as the project scales up?
You might choose one of the following questions to reflect on:
How could one of your project's features be misused?

Without a login function or weak security, people’s private tasks, productivity and particularly mood could be leaked which may be sensitive to some people.

* Are there any types of users who might have difficulty using your project?

People who suffer from color blindness may have trouble using some of the features as the mood tracker and the calendar function are reliant on color. They may have trouble distinguishing the colors from each other and may be forced to use numbers instead.

* If your project becomes widely adopted, are there social concerns you might anticipate?
If our project became widely adopted, we would almost certainly improve and expand on the functionality and scope of our app, and so we would probably add many more interesting statistics to the statistics page. However, this might create a misincentive for people to focus on improving their statistics (as though it were like some sort of game), rather than enjoying life and improving their mental health in real life. For example, users might be misincentivized to ensure their productivity is always as high as possible, while neglecting other areas of their life.
