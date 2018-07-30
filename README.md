# AlissonBot
A bot that searches through Reddit threads in /r/LiverpoolFC and corrects wrong spellings of Alisson.

- It's limited to the top 50 threads (sorted by Hot).
- The patterns searched for are allison, alison and allisson.
- If the pattern is found, another verification is done to make sure that the correct spelling doesn't also exist in the same comment.
  If the following patterns are also found (Richalison, Alisson), the comment will be ignored.
- If a thread doesn't have any misspelt comments, the title will be also searched in the same way.
- There's a whitelist of users whose comments will not be searched. In some cases, users are referring to other people named Allison or Alison.
