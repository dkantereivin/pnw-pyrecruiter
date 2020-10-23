# pnw_pyrecruiter
#### An Open Source Recruitment Bot for Politics & War

## Features
- graphical settings manager, and UI
- package-like integration
- Recruiter class for multiple bot instances
- sqlite3 database for reliable and fast data persistence, as opposed to the traditional text/json/no-persistence techniques
- actively developed and maintained

*All features are currently believed to be working, subject to errors caused by a lack of in game permissions (i.e. captchas on new players)*

## Usage
There are three ways to utilize the recruiter:
1. As a standalone script, by executing `Recruiter.py`
2. As a graphical interface, by executing `main.py`
3. As a Python package, by importing `Recruiter.py` into your own code. Once you have imported the module, you can choose to pass your own config object (`Dict[str, Any]`) to the `Recruiter` constructor, or pass a custom settings path. Alternatively, follow the below.

## Setup
To setup the bot, populate `settings.json` as indicate in Settings.
For non-technical users, consider simply running `main.py`, which offers a graphical interface for completing the setup. 

Prior to running main.py, you will need to install project dependencies. Otherwise, you will experience errors running the bot.
To do so, open your terminal and type `pip install -r requirements.txt` in the project folder. Alternatively, install the dependencies manually.
If you're unsure how to navigate to the project folder, copy the path to the folder and type `cd` followed by the path.

#### Dependencies: 
- `requests`
- `ezgui`, only needed if using `main.py`

### Settings
For all above options, some user settings must be stored the machine running the bot.

To modify settings, edit `settings.json` manually or using the graphical interface. Fill the file with the settings to be applied:
- user: the username (email) of the account which will be sending messages.
- pass: the password, in plaintext, for the account. This data is stored locally on your machine and the bot uses an encrypted connection to PnW (HTTPS), so as long as you do not expose your password via the file system, this is no less secure than accessing PnW via the browser.
- api_key: the API key to be used. This does not need to be the key from the user account sending messages.
- db_path: the relative path to `storage.db`. Changing the default settings is not recommended, unless you intend to use your own database.

- alliance: the name of your alliance.
- target_alliance: a list of the alliance names to send messages to. Follow the [JSON array](https://www.w3schools.com/js/js_json_arrays.asp) format. You can specify as many alliances as you would like; to target users with no alliance, add `"None"`.
- max_inactive: filters nations to only select nations who have been inactive for less than the specified integer (minutes), based on `minutesinactive` from the game api
- exclude: a list of nation ids to exclude, which will never be messaged
- contact_again: the number of days to wait before recontacting a previously contacted user. Use at your own risk.

- subject: the message subject line, in plaintext.
- content: the message content, in plaintext.

### API Usage:
1 API call is used for each round of recruitment. This allows the bot to track changes and message new members of the `target_alliance` groups. To adjust the total API usage, adjust the `frequency` setting.


## TODO & Support:
Recent updates have introduced the bot, added documentation, type checking, bug fixes, etc.
Future updates will depend on the presence of captchas protecting the message system.

__Expect Improvements in the Following Areas:__
- documentation
- graphical interface
- maintenance and support

For support with this bot, contact `Canter#0548` on Discord or email `kanter.dev@gmail.com`.

## Contributing
Open Source, so very happy for you to contribute! Just fork the repo, make any edits you'd like, and submit a pull request. If at all possible, keep your pull requests atomic: this means that you have one major feature per pull request. Make sure to explain each PR!

Thanks for your interest!
