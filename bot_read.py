#!/usr/bin/python
import praw
import re
import os

# Create the Reddit instance
reddit = praw.Reddit('AlissonBot')

# Control flags
reply_to_multiple_comments_in_thread = False

# Have we run this code before? If not, create an empty list
if not os.path.isfile("posts_replied_to.txt"):
	posts_replied_to = []
if not os.path.isfile("comments_replied_to.txt"):
	comments_replied_to = []

# If we have run the code before, load the list of posts we have replied to
else:
	# Read the file into a list and remove any empty values
	with open("posts_replied_to.txt", "r") as f:
		posts_replied_to = f.read()
		posts_replied_to = posts_replied_to.split("\n")
		posts_replied_to = list(filter(None, posts_replied_to))
	with open("comments_replied_to.txt", "r") as g:
		comments_replied_to = g.read()
		comments_replied_to = comments_replied_to.split("\n")
		comments_replied_to = list(filter(None, comments_replied_to))

subreddit = reddit.subreddit("LiverpoolFC")
for submission in subreddit.hot(limit=50):
	# If we haven't replied to this post before
	if submission.id not in posts_replied_to:
		submission.comments.replace_more(limit=0)
		found_comment = False
		for comment in submission.comments.list():
			body = comment.body.encode('utf-8')
			if re.search("(allison|allisson|alison)", body, re.IGNORECASE):
				if not re.search("alisson", body, re.IGNORECASE):
					# Reply to the comment
					print('Replying to submission %(submission)s, comment %(comment)s' % {'submission' : submission.id, 'comment' : comment.id})
					comment.reply('The correct spelling is ***Alisson***\n\n^(I am a bot. To reduce spam, corrections will be limited to one per thread)')
					found_comment = True
					# Store the current post into our list
					posts_replied_to.append(submission.id)
					comments_replied_to.append(comment.id)
					break
				else:
					print('Skipping submission %(submission)s, comment %(comment)s. Found both the right & wrong spelling' % {'submission' : submission.id, 'comment' : comment.id})
		# Search title instead if no comments including misspelling
		if not found_comment:
			title = submission.title.encode('utf-8')
			if re.search("(allison|allisson|alison)", title, re.IGNORECASE):
				if not re.search("alisson", title, re.IGNORECASE):
					# Reply to the comment
					print('Replying to submission %(submission)s. Title has misspelling' % {'submission' : submission.id})
					submission.reply('The correct spelling is ***Alisson***\n\n^(I am a bot. To reduce spam, corrections will be limited to one per thread)')
					# Store the current post into our list
					posts_replied_to.append(submission.id)
				else:
					print('Skipping submission %(submission)s. Found both the right & wrong spelling' % {'submission' : submission.id})
	else:
		print('Skipping submission %(submission)s' % {'submission' : submission.id})


# Write our updated list back to the file
with open("posts_replied_to.txt", "w") as f:
	for post_id in posts_replied_to:
		f.write(post_id + "\n")
with open("comments_replied_to.txt", "w") as g:
	for comment_id in comments_replied_to:
		g.write(comment_id + "\n")
