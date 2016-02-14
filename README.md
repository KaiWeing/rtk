# Summary
A simple Webapp that takes the kanji number from Heisig's 'Remember the Kanji' and redirects to that kanji on Jisho.org.
Helpful if you want to know more details like, sample sencences, stroke order or other meanings of that kanji.

# Howto Install
1. Clone this repo
2. Build docker image from it
3. Run docker image (e.g. on Amazon ec2 instance)

# About the App
This is based on python flask using a sqlite db serving the kanji data. 
The data is taken from this anki collection: https://ankiweb.net/shared/info/1354129669
