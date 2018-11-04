#!/usr/bin/python3
# Project ReaderWise
'''
Project ReaderWise is an internal project commissioned by Udacity News Corp [UNC] (not a real company). This
project seeks to deliver meaningful analytics regarding readership and site reliability. With the data provided
by this tool, UNC will be able to improve site reliability, focus on topics of significance to its reader base,
and recognize the authors within the organization delivering the most meaningful content to readers.
'''

import psycopg2

DBNAME = "news" # Even though our database name is fixed, storing in a variable is good practice for reusability of code.

# top_articles() Function
# Queries the database to retrieve a table with the titles and view counts of
# the top 3 articles in logs.
#
# Utilizes logs_top_arts View (defined in Views section of readme), which pulls
# the path and view count of the 3 most visited paths containing '/article/'
def top_articles():
    db = psycopg2.connect(database=DBNAME) # Open connection to news database
    cur = db.cursor() # Create cursor for querying
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

def author_ranking():
    db = psycopg2.connect(database=DBNAME) # Open connection to news database
    cur = db.cursor() # Create cursor for querying

    query = "SELECT authors.name, view_count FROM authors, author_views WHERE authors.id = author_views.author ORDER BY view_count DESC;"
    author_ranks = cur.execute(query)

    print("\n-- Author Rankings --\n")

    for record in cur:
        auth_name = record[0]
        auth_view_count = record[1]
        formatted_output = "{} - {} article views".format(auth_name, auth_view_count)
        print(formatted_output)

    # Close cursor and database connection
    cur.close()
    db.close()

# Function call to answer question 1
top_articles()

# Function call to answer question 2
author_ranking()
