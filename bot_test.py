#! /usr/bin/python
#NICK PARBS REDDIT TEST BOT V1
import praw
import os
import re
import time
import config


searchTxt = "what up"
replyTxt = "beep boop"

def send_email(recipient, subject, body):
    import smtplib

    gmail_user = config.gmail_user
    gmail_pwd = config.gmail_password
    FROM = config.gmail_user
    TO = recipient if type(recipient) is list else [recipient]
    SUBJECT = subject
    TEXT = body

    # Prepare actual message
    message = """From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(gmail_user, gmail_pwd)
        server.sendmail(FROM, TO, message)
        server.close()
        print("successfully sent the mail")
    except:
        print("failed to send mail")		


def bot_login():
	reddit = praw.Reddit(username = config.username,
				password = config.password,
				client_id = config.client_id,
				client_secret= config.client_secret,
				user_agent = config.username + " python bot V1 by /u/nparbs")
					
	return reddit

def run_reply_bot(reddit):	
	# Have we run this code before?
	if not os.path.isfile("posts_replied_to.txt"):
		posts_replied_to = []

	# Load the list of posts we have replied to
	else:
		# Read the file into a list and remove any empty values
		with open("posts_replied_to.txt", "r") as f:
			posts_replied_to = f.read()
			posts_replied_to = posts_replied_to.split("\n")
			posts_replied_to = list(filter(None, posts_replied_to))

	# Get values from our subreddit
	subreddit = reddit.subreddit('ParbsBotTest')
	for submission in subreddit.hot(limit=10):
		#if submission.title
		#print("Title: ", submission.title)
		#print("Text: ", submission.selftext)
		#print("Score: ", submission.score)
		#print("---------------------------------\n")

		# If we haven't replied to this post before
		if submission.id not in posts_replied_to:

			# Do a case insensitive search
			if re.search(searchTxt, submission.title, re.IGNORECASE) or re.search(searchTxt, submission.selftext, re.IGNORECASE):
				# Reply to the post
				submission.reply(replyTxt)
				print("Bot replying to : ", submission.title)

				# Store the current id into our list
				posts_replied_to.append(submission.id)
				
				send_email("nparbs@gmail.com","test","title: " + submission.title + "\n text: " + submission.selftext)
			

	# Write our updated list back to the file
	with open("posts_replied_to.txt", "w") as f:
		for post_id in posts_replied_to:
			f.write(post_id + "\n")
			
def run_PCSALES_bot(reddit):	
	# Have we run this code before?
	if not os.path.isfile("posts_sent.txt"):
		posts_sent = []

	# Load the list of posts
	else:
		# Read the file into a list and remove any empty values
		with open("posts_sent.txt", "r") as f:
			posts_sent = f.read()
			posts_sent = posts_sent.split("\n")
			posts_sent = list(filter(None, posts_sent))

	# Get values from our subreddit
	subreddit = reddit.subreddit('buildapcsales')
	for submission in subreddit.new(limit=3):
		#if submission.title
		#print("Title: ", submission.title)
		#print("Text: ", submission.selftext)
		#print("Score: ", submission.score)
		#print("---------------------------------\n")

		if submission.id not in posts_sent:
			
			print("New post")
			
			send_email("nparbs@gmail.com","New post to r/buildapcsales","title: " + submission.title + "\n link: " + submission.url)
			# Store the current id into our list
			posts_sent.append(submission.id)
			
			time.sleep(1)
				
	# Write our updated list back to the file
	with open("posts_sent.txt", "w") as f:
		for post_id in posts_sent:
			f.write(post_id + "\n")



	
reddit = bot_login()

while True:
	run_PCSALES_bot(reddit)
	time.sleep(1)


