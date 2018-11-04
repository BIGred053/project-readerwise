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

##### author_views
This view is a table of author ids (from the articles table) and the total number of article views accrued by each author. This tallies only pages successfully viewed (status = '200 OK') and ignores 'near-match' paths which resulted in 404 errors.

_As a note, this view depends on the logs_article_counts view, so that view must be created first._

Re-create this view with the following code in psql:
```
create view author_views as
    select author, SUM(num) as view_count
        from articles, logs_article_counts
        where logs_article_counts.path = '/article/' || articles.slug
        group by author;

```

##### views_per_day
This view is a table of each date in the log table, along with a count of all records for that date.

Re-create this view with the following code in psql:
```
    create view views_per_day as
        select time::date, count(*) as views
        from log
        group by time::date;
```

##### errors_per_day
This view is a table of each date in the log table, along with a count of records for that date where the status code was '404 NOT FOUND'. Analysis of the table showed that the only two status codes listed in the log table were '200 OK' and '404 NOT FOUND', meaning the query constructing this view was safe to search specifically for the '404 NOT FOUND' status.

Re-create this view with the following code in psql:
```
    create view errors_per_day as
        select time::date, count(*) as err_count
        from log
        where status = '404 NOT FOUND'
        group by time::date;
```
### Contributions
Evan McCullough - Python Development
Udacity - Project premise, Database contents

### License
Project ReaderWise is shared under the MIT License.
