# utcnormalise
Given problem: I had a file with a list of data, each line starting with a timestamp. But the timestamps were not all of the same time zone; I had UTC+0, UTC+1, and UTC+2. The time stamps in the file look like this:

2015-04-16 19:54:55 +2

Now I wanted to bring them all to UTC+0 to be able to sort and compare them. I had been warned: Playing with time strings might not be funny. Well, it took me a day, but now the script is working.

The script starts without parameters. File names (input and output) must be declared in the code.
