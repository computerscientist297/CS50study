CS50study: A productivity and mood tracker
By: Kevin Cho, Harvey Lin, and Brendon Lau

Video Link: https://youtu.be/9Ki7Dd8SxK8

Description:
As students who have had challenging semesters and have looked for solutions to track mood and productivity, we wanted to design a general wellness web application that we could use to not only track our own mood and productivity on a daily basis, but also manage and organize the tasks and work we had to do. Users can track tasks and record how long they take as well as input mood scores and productivity scores on a daily basis. We represent these scores visually using shades of colors corresponding to the scores themselves (darker shades corresponding to higher scores), allowing users to easily see their trends in mood and productivity, and thus giving them an opportunity to reflect and improve. In the main page, there is a table where tasks and information about the task like the subject and the duration of time planned to work on a task. In the motivation page, there is a percentage tracker that shows the percentage of elapsed designated time to work on the task as well as a motivational quote and photos that are generated to help stay motivated. In the calendar section, mood and productivity for a given day can be imputed. In the last section, the statistics section, number of days on the app, the average productivity, and average mood are displayed.

Running the Website:
This website was implemented using HTML, Python, CSS, and Javascript. To implement, download the zip file and upload it into vscode. Unzip the file and remove the zip file. Typing “cd CS50study” into the terminal will get to the proper directory. After that, using “flask run” will create a link which can be used to access the website.

Registering and Logging in:
To register, click the register button and fill out the username and password sections. Please note that there must be an approved special character in the password ["$", "@", "#", "%", "!", "*"]. After this, go back to the login page and enter the username and password you’ve created, you will then have access to the functions of the website.

Using the task function:
One of the main functions of the website is to add tasks that need to be done and the amount of time allotted to work/complete the task. To do this, first add the subject of the task and the task itself, both a subject and a task must be added. When starting a task, select a task to start and allocate an amount of time that you would like to work on it for. This will start the task where a timer will update every time an update button is clicked and the amount of time worked over the allotted time will show up in the table as overtime. When finished with a task, it will show up in the motivation page as history. If you would like to remove a task from the history page, in the main page, select a task to remove and click the remove button.


Motivation/history:
In the motivation/history section, there is a display of the percentage of the amount time elapsed of total allotted time to a task. This will be updated when visiting the page again. Aside from this, it also contains the ten most recently completed tasks. There is also a motivational quote in the corner of the page that will be updated every time the page is visited again.

Calendar:
In this section, a calendar and form are available for the user to input their mood and productivity for the current day. This will encourage the user to immediately reflect on their mood for the day instead of delaying their reflection until they may not remember how they felt about their mood and productivity on that day. Based on the score imputed (1-10), the table will display a color (that can be changed) based on the score given for productivity and mood with better mood and productivity corresponding to a darker color.

Statistics:
In the statistics section, the page will display various statistics about the users mood and productivity score. It is a good place for users to reflect on their general productivity and mood and is helpful in helping users be aware of their own tendencies of productivity and mood.

Logging out:
To log out, use the navigation bar and click on the last option which should be to log out.

This should be an adequate description of our project. It was designed to be helpful to users in tracking wellness and productivity as well as the tasks they have to do. It was something that we actually wanted for ourselves initially to help us in our daily lives. We hope that it will be helpful to users as well.

Happy Coding!
Kevin, Harvey, and Brendon
