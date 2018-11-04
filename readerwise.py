#!/usr/bin/python3
# Project ReaderWise
'''
Project ReaderWise is an internal project commissioned by Udacity News Corp [UNC] (not a real company). This
project seeks to deliver meaningful analytics regarding readership and site reliability. With the data provided
by this tool, UNC will be able to improve site reliability, focus on topics of significance to its reader base,
and recognize the authors within the organization delivering the most meaningful content to readers.
'''

import psycopg2, datetime

DBNAME = "news" # Even though our database name is fixed, storing in a variable is good practice for reusability of code.

# top_articles() Function
# --------------------
# Queries the database to retrieve a table with the titles and view counts of
# the top 3 articles in logs. Outputs the result of this query in a neatly
# formatted ranking of the top 3 articles with view counts for each.
#
# Utilizes logs_article_counts View (defined in Views section of README), which pulls
# the path and view count of all paths in log table containing '/article/' and with
# a status code of '200 OK'.
def top_articles():
    db = psycopg2.connect(database=DBNAME) # Open connection to news database
    cur = db.cursor() # Create cursor for querying

    # Query will return a table containing 3 records. Each record will contain the
    # title of an article, along with a count of how many page views that specific
    # article has received, ordered. The 3 records will be the top 3 most-viewed
    # articles, ranked from most views to least.
    query = "SELECT title, num from articles, logs_article_counts WHERE '/article/' || articles.slug = logs_article_counts.path ORDER BY num DESC LIMIT 3;" # Utilizes PostgreSQL || operator to concatenate the '/aritcle/' portion of the pathname with the article slug.
    top_arts = cur.execute(query) # Execute our query

    # Print out formatted results of top 3 most read articles.
    print("-- Top 3 Most Read Articles --\n")
    # Iterate over results table and print out well-formatted results, utilizing str.format()
    for record in cur:
        title = record[0]
        view_count = record[1]
        formatted_output = "\"{}\" - {} views".format(title.title(), view_count)
        print(formatted_output) # Output will display as "Title" - # views

    # Close cursor and database connection
    cur.close()
    db.close()
#End top_articles function


# author_ranking() function
# --------------------
# Queries the database to retrieve a table with the names of each author and the
# sum of all page views for each article written by that author. Outputs a list
# of each author's name, along with that summation of page views, ranked from
# highest view count (readership) to the lowest.
#
# Utilizes the author_views View (defined in Views section of README). This view
# utilizes the logs_article_counts View, then adds up view counts on a per-author
# basis.
def author_ranking():
    db = psycopg2.connect(database=DBNAME) # Open connection to news database
    cur = db.cursor() # Create cursor for querying

    # Query will return a table with the author's name and total page views. Achieves
    # this by matching author's ID in authors table to author's ID in author_views View.
    # Author's ID in author_views View comes from author field in articles table.
    query = "SELECT authors.name, view_count FROM authors, author_views WHERE authors.id = author_views.author ORDER BY view_count DESC;"
    author_ranks = cur.execute(query) # Execute query

    # Print out formatted results of author rankings based on page views for articles
    print("\n-- Author Rankings --\n")

    #Iterate over results table in cursor, print out well-formatted results.
    for record in cur:
        auth_name = record[0] # Pull author's name from each record in cursor.
        auth_view_count = record[1] # Pull total article views from each record in cursor.
        formatted_output = "{} - {} article views".format(auth_name, auth_view_count)
        print(formatted_output) # Output will display as Author Name - # article views

    # Close cursor and database connection
    cur.close()
    db.close()
# End author_ranking function

# high_errors() function
# --------------------
# This function queries the database, utilizing the views_per_day and errors_per_day
# Views (defined in README) to find days on which more than 1% of page requests
# resulted in an error status.
#
# The function outputs a list of each date where the
# error rate exceeded 1%, formatted in plain English, along with the error rate
# experienced on that date.
def high_errors():
    db = psycopg2.connect(database=DBNAME) # Open connection to news database
    cur = db.cursor() # Create cursor for querying

    # Query joins the views_per_day View and errors_per_day View to find any date
    # where the errors that day, divided by total views that day, multiplied by 100
    # yields a number greater than 1.
    # "::numeric" ensures that err_count and views are cast as numeric values to
    # ensure proper division
    query = "SELECT views_per_day.time::date, ((err_count::numeric / views::numeric)*100) as err_rate FROM views_per_day JOIN errors_per_day ON views_per_day.time::date = errors_per_day.time::date and ((err_count::numeric / views::numeric)*100) > 1;"
    high_err_days = cur.execute(query) # Execute query

    # Print out a formatted list of days where the error rate exceeded 1% of page requests
    print ("\n--Days with >1% request errors--\n")

    # Iterate through records returned by the query
    for record in cur:
        high_err_date = record[0] # First element in each record is the date where >1% of errors occurred
        err_rate = record[1] # Second element in each record is the error rate on that day.
        formatted_output = "{} - {:.2f}% errors".format(high_err_date.strftime("%B %d, %Y"), err_rate)
        print(formatted_output) # Output will display as - Month DD, YYYY- X.XX% errors

#End high_errors function

# --Main script--
# Executes functions defined above in order to provide insight on each key business
# inquiry (i.e. each question posed in the Logs Analysis project requirements)

# Function call to answer question 1
top_articles()

# Function call to answer question 2
author_ranking()

# Function call to answer question 3
high_errors()
