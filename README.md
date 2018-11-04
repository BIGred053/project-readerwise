# Project ReaderWise
Project Readerwise is a database analysis tool created as a solution to the "Logs Analysis" project within the Udacity Full Stack Developer Nanodegree Program. The mission of this project is to analyze the contents of Udacity's provided database of articles, authors, and activity (logs) for an online newspaper, then deliver some meaningful insights from that data.

Project ReaderWise is developed by Evan McCullough using Python version 3.5.2.

### Dependencies
Follow the instructions and links below to download/install Project ReaderWise's dependencies:
##### psycopg2
`pip3 install psycopg2`


Database SQL

### Usage
Execute the following command to run ReaderWise and view the analytics insights provided by the tool.

##### Mac/Linux Users:
`python3 readerwise.py`

##### Windows Users (Git Bash):
`python readerwise.py`

Need Git Bash? Download it at https://gitforwindows.org/.

### Questions Answered
Project ReaderWise has the mission of answering three questions, in particular:

1) What are the newspaper's three most popular articles of all time?

2) Who are the most popular article authors of all time for the newspaper?

3) On which days did more than 1% of page requests by readers result in errors?

### Views
##### logs_article_counts
This view is a table of the view counts for all 8 articles. This is written to return all results so that this
view may be used for both Question 1 (Top 3 Articles) and Question 2 (Author Rankings).

Re-create this view with the following code in psql:
```
create view logs_article_counts as
    select path, count(*) as num
        from log
        where path like '%article%' and status = '200 OK'
        group by path
        order by num desc;
```
### Contributions
Evan McCullough - Python Development
Udacity - Project premise, Database contents

### License
Project ReaderWise is shared under the MIT License.
