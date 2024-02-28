a3.py is a program that allows a user to create and modify
a dsu profile locally on their computer as well as publish to an
online dsu server. Users can also open existing dsu profiles, 
and then continue editing them.

A dsu profile contains a username, password, bio, and posts
with timestamps. Each time a new dsu profile is created, the
user must create a username, password, and bio.

At program entry, the user make choose to create a file, open
a file, or quit the program.

There are 2 commands in the edit menu, edit (E), and print (P).
For edit, the options include -usr, -pwd, -bio, -addpost, and
-delpost, -publish, and -publishbio. These options allow the 
user to edit the dsu profile directly. -publish lets the user send a post
to an online server. It prompts the user for an IP address if there
isn't one saved in the dsu profile already. -publishbio allows the
user to publish a new bio to the server without posting an entry.
For print, the options include -usr, -pwd, -bio, -posts, -post, and 
-all. These options print out different contents of the open dsu file.
