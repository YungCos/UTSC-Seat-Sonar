# UTSC-Seat-Sonar
Discord bot that notifies you when a seat has become available

## Commands

- !help 
  - View list of commands
- !watch [Course Code] [Tutorial Name] 
  - Adds a tutorial to be watched. Note that the tutorial name needs to be exact
- !courses
  - View the tutorials that you are currently watching
- !remove [Course Code] [Tutorial Name]
  - Removes a tutorial from the watchlist. Note the format is the same as !watch
- !removeall [Course Code] (optional)
  - Removes all tutorial from the given course. If no course is given, than it will remove all tutorials from all courses

## Notes
- This project is set up to run in heroku, as it includes a Procfile and requirements.txt file
- The chromedriver.exe executable is for testing locally, and is not needed for hosting
- A firebase project needs to be set up, and connected through the authentication
- You may change the settings manually by editing the `settings.py` file or when hosting in heroku, set the following Config Vars:
  - **CRED_OBJ:** Name of json file with firebase credentials
  - **DB_URL:** URL to Firebase database
  - **DRIVER_PATH:** "/app/.chromedriver/bin/chromedriver" **OR** "chromedriver.exe" if run locally
  - **GOOGLE_CHROME_BIN:** "/app/.apt/usr/bin/google-chrome" (only required if run on Heroku)
  - **TOKEN:** Token to discord bot
