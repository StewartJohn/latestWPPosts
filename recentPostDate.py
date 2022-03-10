# Script for checking the last date of posts for WordPress users on a Reclaim Server
# The script will log into the WP database for each user and check the most recent change in the posts table
# This will return the latest update, not just for posts but also pages and media, which are all stored in the posts table
# John Stewart (johnstewart@ou.edu)

# import required libraries
import mysql.connector
import csv
import datetime

# the output file will be on the server in the same directory as this script
f= csv.writer(open("lastPost.csv", "w"))   # Open the output file for writing before the loop
f.writerow(["Owner", "Latest Post"]) # Write column headers as the first line

# the input file should be a list of WordPress DB on the server with the username in the first column and password in the second
input = csv.reader(open("wordPressAccountsList.csv")) #inport the list of accounts on the server

for item in input:
    try:
        # connecting to the database
        dataBase = mysql.connector.connect(
                             host = "localhost",
                             user = item[0],
                             passwd = item[1],
                             database = item[0])
        # preparing a cursor object
        cursorObject = dataBase.cursor()
        # selecting query
        query = "SELECT post_modified FROM `wp_posts` ORDER BY `wp_posts`.`post_modified` DESC LIMIT 1"
        cursorObject.execute(query)
        myresult = cursorObject.fetchone()
        # convert datetime object into human readable date
        date_string = myresult[0].strftime('%m/%d/%Y %I:%M')
        # write db user and most recent post time to the output csv
        f.writerow([item[0],date_string])
        # disconnecting from server
        dataBase.close()
    except:
        print("bad DB Connection for %s"%item[0]) #let the user know a db couldn't connect
        continue

print("Job Complete")
