# AlissonBot
A bot that searches through Reddit threads in /r/LiverpoolFC and corrects wrong spellings of Alisson.

I use [PRAW](https://praw.readthedocs.io/en/latest/index.html) to connect to Reddit API.

**NOTE: I am ignoring my praw.ini file but you would need to [define a praw.ini](https://praw.readthedocs.io/en/latest/getting_started/configuration/prawini.html) file containing your reddit bot's info.**

- It's limited to the top 50 threads (sorted by Hot).
- The patterns searched for are allison, alison and allisson.
- If the pattern is found, another verification is done to make sure that the correct spelling doesn't also exist in the same comment.
  If the following patterns are also found (Richalison, Alisson), the comment will be ignored.
- If a thread doesn't have any misspelt comments, the title will be also searched in the same way.
- There's a whitelist of users whose comments will not be searched. In some cases, users are referring to other people named Allison or Alison. This is maintained in _whitelisted_authors.txt_ file.
- To avoid spamming the subreddit, I maintain 2 files that are appended everytime the bot responds to a comment (or thread).
- _posts_replied_to.txt_ has all the post (aka thread) ids that the bot has responded to. These will be skipped in any subsequent run.
- _comments_replied_to.txt_ has all the comment ids that the bot has responded to. This is kept just for reference now. I'm not really using this information.
