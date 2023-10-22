How it works:

Setup: You start by providing the URLs where you typically find lists of potential IPTV URLs in a text file named '[leech].txt.'
Run the Python script 'main.py,' and the application will automatically begin analyzing all the URLs you've listed in the 'leech' file.
The application will store the results in a text file named 'urls.txt.' Once the initial data collection is complete, it will execute the 
searcher.py to filter and retrieve essential information including sub duration, channel count, categories,maximum active users, and current active users...

The results will be displayed in the console for immediate viewing, and will be saved in another text file called '[results].txt.'
Moreover, any valid URLs discovered during this process will be cataloged in the '/history/history.txt' file, enabling you to revisit and verify their current status at a later time.
