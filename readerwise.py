#!/usr/bin/python3
# Project ReaderWise
'''
Project ReaderWise is an internal project commissioned by Udacity News Corp
[UNC] (not a real company). This project seeks to deliver meaningful
analytics regarding readership and site reliability. With the data provided
by this tool, UNC will be able to improve site reliability, focus on topics
of significance to its reader base, and recognize the authors within the
organization delivering the most meaningful content to readers.
'''

import psycopg2
import datetime

DBNAME = "news"  # Storing database name in variable

# top_articles() Function
# --------------------
# Queries the database to retrieve a table with the titles and view counts of
# the top 3 articles in logs. Outputs the result of this query in a neatly
# formatted ranking of the top 3 articles with view counts for each.
#
# Utilizes logs_article_counts View (defined in Views section of README),
# which pulls the path and view count of all paths in log table containing
# '/article/' and with a status code of '200 OK'.


def top_articles():
    db = psycopg2.connect(database=DBNAME)  # Open connection to news database
    cur = db.cursor()  # Create cursor for querying

    # Query will return a table containing 3 records. Each record will contain
    # the title of an article, along with a count of how many page views that
    # specific article has received, ordered. The 3 records will be the top 3
    # most-viewed articles, ranked from most views to least.
    #
    # Utilizes PostgreSQL || operator to concatenate the '/aritcle/' portion
    # of the pathname with the article slug.
    query = """SELECT title, count(*) as num
            FROM articles, log
            WHERE '/article/' || articles.slug = log.path
            GROUP BY title
            ORDER BY num DESC
            LIMIT 3;"""
    top_arts = cur.execute(query)  # Execute our query

    # Print out formatted results of top 3 most read articles.
    print("-- Top 3 Most Read Articles --\n")
    # Iterate over results table and print out well-formatted results,
    # utilizing str.format()
    for record in cur:
        title = record[0]
        view_count = record[1]
        formatted_output = "\"{}\" - {} views".format(title.title(),
                                                      view_count)
        print(formatted_output)  # Output will display as "Title" - # views

    # Close cursor and database connection
    cur.close()
    db.close()
# End top_articles function


# author_ranking() function
# --------------------
# Queries the database to retrieve a table with the names of each author and
# the sum of all page views for each article written by that author. Outputs
# a list of each author's name, along with that summation of page views,
# ranked from highest view count (readership) to the lowest.
#
# Utilizes the author_views View (defined in Views section of README). This
# view utilizes the logs_article_counts View, then adds up view counts on a
# per-author basis.
def author_ranking():
    db = psycopg2.connect(database=DBNAME)  # Open connection to news database
    cur = db.cursor()  # Create cursor for querying

    # Query will return a table with the author's name and total page views.
    # Achieves this by matching author's ID in authors table to author's ID in
    # author_views View. Author's ID in author_views View comes from author
    # field in articles table.
    query = """SELECT authors.name, count(*) as num
            FROM authors, log, articles
            WHERE authors.id = articles.author
            AND '/articles/' || articles.slug = log.path
            GROUP BY authors.name
            ORDER BY num DESC;"""

    author_ranks = cur.execute(query)  # Execute query

    # Print out formatted results of author rankings based on page views for
    # articles
    print("-- Author Rankings --\n")

    # Iterate over results table in cursor, print out well-formatted results.
    for record in cur:
        # Pull author's name from each record in cursor.
        auth_name = record[0]
        # Pull total article views from each record in cursor.
        auth_view_count = record[1]
        formatted_output = "{} - {} article views".format(auth_name,
                                                          auth_view_count)
        # Output will display as Author Name - # article views
        print(formatted_output)

    # Close cursor and database connection
    cur.close()
    db.close()
# End author_ranking function

# high_errors() function
# --------------------
# This function queries the database, utilizing the views_per_day and
# errors_per_day Views (defined in README) to find days on which more than 1%
# of page requests resulted in an error status.
#
# The function outputs a list of each date where the
# error rate exceeded 1%, formatted in plain English, along with the error
# rate experienced on that date.


def high_errors():
    db = psycopg2.connect(database=DBNAME)  # Open connection to news database
    cur = db.cursor()  # Create cursor for querying

    # Query joins the views_per_day View and errors_per_day View to find any
    # date where the errors that day, divided by total views that day,
    # multiplied by 100 yields a number greater than 1.
    # Multiplying by 100.0 ensures result is a float number
    query = """SELECT TO_CHAR(views_per_day.time::date, 'Mon DD, YYYY'),
            ((err_count / views)*100.0) as err_rate
            FROM views_per_day JOIN errors_per_day
            ON views_per_day.time::date = errors_per_day.time::date
            AND ((err_count / views)*100.0) > 1;"""

    high_err_days = cur.execute(query)  # Execute query

    # Print out a formatted list of days where the error rate exceeded 1% of
    # page requests
    print("--Days with >1% request errors--\n")

    # Iterate through records returned by the query
    for record in cur:
        # Pull date where >1% of errors occurred
        high_err_date = record[0]
        # Pull error rate on that day.
        err_rate = record[1]
        formatted_output = "{} - {:.2f}% errors".format(
                            high_err_date.strftime("%B %d, %Y"),
                            err_rate)
        # Output will display as - Month DD, YYYY- X.XX% errors
        print(formatted_output)

# End high_errors function

# --Main script--
# Executes functions defined above in order to provide insight on each key
# business inquiry (i.e. each question posed in the Logs Analysis project
# requirements)


# Welcome users to Project ReaderWise, introduce the program's purpose
print("Welcome to Project ReaderWise!\n")
print("This is an internal analytics program designed to provide valuable"
      " business insights for our newspaper. With this tool, we aim to provide"
      " insight regarding the types of content that readers enjoy, the "
      "authors who have gained the greatest readership, and site reliability."
      "\n"
      )

# Explain Question 1
print("Question 1: What are the most popular three articles of all time?")
top_articles()  # Function call to answer Question 1

# Explain Question 2
print("\nQuestion 2: Who are the most popular article authors of all time?")
author_ranking()  # Function call to answer Question 2

# Explain Question 3
print("\n"
      "Question 3: On which days did more than 1% of requests lead to errors?"
      )
high_errors()  # Function call to answer Question 3
