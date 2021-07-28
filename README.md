# PositivityTracker
Our project for LancerHacks 2021 - Rohan Sinha and Aditya Tomar

## Inspiration

The inspiration for this project came from our own experiences, as well as those of our peers. Ever since the beginning of this pandemic, it has been difficult for school students, particularly in terms of mental health, to express their true feelings and anxieties. These experiences led us to consider creating an application to monitor students' emotions by having them write in a diary.

## What it does

This application enables students to express themselves; their thoughts, feelings, and anxieties; by writing in a diary, at any frequency they want. Then, this application conducts sentiment analysis on the diary entry to come up with a score - the closer to 1 the score is, the more positive the student feels. In contrast, the closer to -1 the score is, the more negative the student feels. This score can be adjusted by the user. These scores are plotted on a graph. Furthermore, this program alerts the student when their mental health is declining severely, or if it is too low; it advises the student to seek advice from their counselor in these scenarios. Furthermore, the program stores all of the information about each entry - the date, the text, and the sentiment analysis score - in a database, so that the student's mental health can be tracked over a period of time.

## How we built it

We built Positivity Tracker with the help of Python and its libraries - PostgreSQL, Flask, and Flask SQLAlchemy for connecting to the database and giving data access to the user - as well as NLTK, a machine learning library to give a sentiment analysis score, to judge how positive or negative the user's entry is. We first created a database - called positivityTracker - that would store data from each entry. Then we created classes for multiple different tables in the database - Student and DiaryEntry - to store information. Afterward, we set up endpoints on the Flask server to create, read, update, and delete students and diary entries in the database. HTML files were created for each of these operations, and they employed libraries like Bootstrap CSS to style the page, as well as libraries like Chart.js to graph sentiment analysis scores.

## Challenges we ran into

One major challenge we ran into was with the NLTK model, particularly in accurately predicting the sentiment analysis score for a given entry. The NLTK library had a SentimentIntensityAnalyzer, which used a polarity_scores method, to calculate this score, but it was not perfect, as it had to be adjusted for longer strings, like diary entries. Therefore, we had to create new algorithms that would adjust for the library's flaws. Another challenge was in styling each webpage, as that could prove difficult as the webpage grew more complex.

## Accomplishments that we're proud of

We are proud of the fact that we were able to create such a complex project - conducting sentiment analysis and connecting to databases in the backend and displaying this complicated backend work coherently in the front end. Furthermore, we are proud that we were able to conduct sentiment analysis using the NLTK library to judge the positivity or negativity of diary entries, considering that we were not really familiar with this library before. Additionally, another accomplishment that we take pride in is that we were able to set up a fully functioning webpage that could display the backend information in multiple different ways that the user could understand.

## What we learned

We learned how to use the NLTK's in-built models, as well as adjust them to make them more accurate and suit our needs. We also became more comfortable with Flask SQLAlchemy to connect databases to webpages. Furthermore, we learned more about Bootstrap CSS in styling webpages and understood the connection between object-oriented programming and databases even more clearly.

## What's next for Positivity Tracker

Some next steps for Positivity Tracker include working more on the NLTK model to have it provide even more accurate results when judging each diary entry as positive or negative, and giving each a score. Furthermore, we would add some more UI functionality to make the application more convenient to use; for example, we would consider adding the ability to move points on the graph to adjust sentiment analysis scores visually. Lastly, we would add the option of creating goals of how much positivity/happiness the student would want to achieve, and also help the student keep track of this goal.

## A few notes for running the project
A few commands have to be run for this project to work.
First, to start the PostgreSQL server:
- Windows: `Windows key + R -> services.msc -> find postgresql -> click start`
- MacOS/Linux: `terminal -> pg_ctl -D /usr/local/var/postgres start`

Then, to create the database:
- Windows CMD: `createdb -U postgres positivityTracker`
- MacOS/Linux: `createdb positivityTracker`

Then, to set the flask app:
- Windows CMD: `set FLASK_APP=route.py`
- MacOS/Linux: `export FLASK_APP=route.py`

Finally, to run:
`flask run`

Additionally, the username in route.py on line 7, for the database URI, has to be changed to the username on the computer the project is being run.
