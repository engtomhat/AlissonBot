#!/usr/bin/python
import praw
import prawcore
import re
import os
import sys
from file_operations import read_file_into_list, write_list_into_file

# Use this print to instantly print to console
def my_print(messages):
	print(messages)
	sys.stdout.flush()

# Search for wrong spelling in text. Return '1' if found, '2' if correct & wrong spelling found, '0' if not found
def is_wrong_spelling_found(body_text):
	pattern_found = 0
	# Search text body for wrong spelling
	if re.search(misspelt_pattern, body_text, re.IGNORECASE):
		if not re.search(allowed_pattern, body_text, re.IGNORECASE):
			pattern_found = 1
		else:
			pattern_found = 2
	return pattern_found

# Variables
misspelt_pattern = "(allison|allisson|alison)"
allowed_pattern = "(alisson)"
bot_message = 'The correct spelling is ***Alisson***\n\n^(I am a bot. To reduce spam, corrections will be limited to one per thread)'

# Whitelisted authors
allowed_authors = read_file_into_list("whitelisted_authors.txt")

# Read posts and comments that were written before
posts_file = "posts_replied_to.txt"
comments_file = "comments_replied_to.txt"
posts_replied_to = read_file_into_list(posts_file)
comments_replied_to = read_file_into_list(comments_file)

# Create the Reddit instance
reddit = praw.Reddit('AlissonBot')
# Connect to required subreddit
subreddit = reddit.subreddit("LiverpoolFC")
for submission in subreddit.hot(limit=50):
	# If we haven't replied to this post before
	if submission.id not in posts_replied_to:
		submission.comments.replace_more(limit=0)
		found_comment = False
		for comment in submission.comments.list():
			# Skip comments from some authors
			if comment.author in allowed_authors:
				my_print('Skipping. Allowed author. Submission %(submission)s, comment %(comment)s' % {'submission' : submission.id, 'comment' : comment.id})
				continue
			# Search comment
			search_result = is_wrong_spelling_found(comment.body.encode('utf-8'))
			if search_result == 1:
				# Reply to the comment
				my_print('Replying to submission %(submission)s, comment %(comment)s' % {'submission' : submission.id, 'comment' : comment.id})
				comment.reply(bot_message)
				found_comment = True
				# Store the current post into our list
				posts_replied_to.append(submission.id)
				comments_replied_to.append(comment.id)
				break
			elif search_result == 2:
				my_print('Skipping submission %(submission)s, comment %(comment)s. Found both the right & wrong spelling' % {'submission' : submission.id, 'comment' : comment.id})
		if not found_comment:
			# Search title instead if no comments including misspelling
			search_result = is_wrong_spelling_found(submission.title.encode('utf-8'))
			if search_result == 1:
				# Reply to the submission
				my_print('Replying to submission %(submission)s. Title has misspelling' % {'submission' : submission.id})
				submission.reply(bot_message)
				# Store the current post into our list
				posts_replied_to.append(submission.id)
			elif search_result == 2:
				my_print('Skipping submission %(submission)s. Found both the right & wrong spelling' % {'submission' : submission.id})
	else:
		my_print('Skipping submission %(submission)s' % {'submission' : submission.id})


# Write our updated list back to the file
write_list_into_file(posts_replied_to, posts_file)
write_list_into_file(comments_replied_to, comments_file)
