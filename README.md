# Project ReaderWise
Project Readerwise is a database analysis tool created as a solution to the "Logs Analysis" project within the Udacity Full Stack Developer Nanodegree Program. The mission of this project is to analyze the contents of Udacity's provided database of articles, authors, and activity (logs) for an online newspaper, then deliver some meaningful insights from that data.

Project ReaderWise is developed by Evan McCullough using Python version 3.5.2.

### Dependencies
Follow the instructions and links below to download/install Project ReaderWise's dependencies:
#### Virtualization - Vagrant and VirtualBox
Execution of Project ReaderWise depends on a Linux environment configured very specifically. To easily reproduce this environment, you may utilize VirtualBox to create a virtualized environment, and Vagrant to configure that environment correctly.

Download VirtualBox here: https://www.virtualbox.org/wiki/Downloads

Download Vagrant here: https://www.vagrantup.com/downloads.html

As mentioned briefly above, Vagrant is a system designed to help you automatically configure virtual machines. More specifically, rather than having to go through the manual setup process normally involved in setting up a virtual machine with VirtualBox, Vagrant allows you to write files that help configure your virtual machine automatically. For a more in-depth explanation of Vagrant and its utility, check out [this YouTube video](https://www.youtube.com/watch?v=wlogPKBEuUM).

The folks at Udacity have provided the configuration that we need for the environment that will run Project ReaderWise, as well as some other files that you might need in this GitHub project: https://github.com/udacity/fullstack-nanodegree-vm

cd into the directory where you would like to store these files and run git clone to download a copy of the repo. After that, cd into the fullstack-nanodegree-vm folder created by this clone, _then_ run git clone on this repository to copy the code here. cd into your new project-readerwise folder and you are ready to go! (Once you have the other dependencies installed below, that is)

##### A fresh copy of the database
To make sure nothing residual throws off the operation of Project ReaderWise, it is best to start fresh with a newly installed copy of the news database. You can get the file for that from Udactiy [here](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip). Unzip this file, make sure to move it into your project-readerwise directory, then run the following two commands to start up and connect to your virtual machine:

```
vagrant up
```

```
vagrant ssh
```
Once in your virtual machine, run this command to access your project files:

```
cd \vagrant
```

Next, use this command to run the newsdata.sql file and set up the database:

```
psql -d news -f newsdata.sql
```

##### psycopg2
`pip3 install psycopg2`

###### pycodestyle (for style linting)
`sudo pip3 install pycodestyle`

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
The following views were created in the process of developing this project. These views are set up to simplify querying the database and organize data logically for operation. To create these views, you will need to access the news database via psql with the following command:

```
psql -d news
```

From here, simply copy and paste any of the code snippets below to re-create my custom views.

#### views_per_day
This view is a table of each date in the log table, along with a count of all records for that date.

Re-create this view with the following code in psql:
```
    create view views_per_day as
        select time::date, count(*) as views
        from log
        group by time::date;
```

#### errors_per_day
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
Project ReaderWise is shared under the MIT License. As a note, other Udacity FSND students should not use this code. Such use would constitute a breach of academic integrity.
