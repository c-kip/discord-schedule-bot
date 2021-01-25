# disorg
![discorg logo](icon.png)

A Discord bot for meeting scheduling and organization, created for QHacks 2021. Learn more [here](https://devpost.com/software/discord-scheduling-bot)!

## inspiration 
In the midst of a pandemic, digital communication has become more important than ever. As people around the world turn to platforms like Discord to stay connected, we realized that Discord lacks many of the features present in platforms like Zoom and Microsoft Teams that allow for better scheduling and meeting organization. Because of this, our team decided to create a Discord bot that adds these functionalities to Discord servers.  

## commands
Users can type the `$help` command to learn more about what commands disorg offers. Here is a general overview of disorg's commands:

* `$meeting` - allows you to schedule a new meeting given a title and various parameters
* `$show_meetings` - will show all currently scheduled meetings
* `$my_meetings` - sends you a direct message of all of your scheduled meetings
* `$edit` - lets meeting organizer/administrator(s) edit meeting details
* `$delete_meeting` - allows the meeting organizer/adminstrator(s) to delete a meeting given its name
* `$add_admin` - adds an administrator to the meeting given the meeting name and the @ of the new administrator
* `$remove_admin` - removes an administrator to the meeting given the meeting name and the @ of the old administrator 
..* `$missing` - checks the sender's voice channel to see if all meeting attendees are present and sends a direct message to those who are missing

## usage
1. `git clone` this repository
2. run `pip install -U python-dotenv` and `pip install -U discord.py`
3. go to the [Discord Developers Portal](https://discord.com/developers/applications) to create a new application
4. get your token for the application and store it in a `.env` file **(your token acts as your password so do NOT share it with others)**
5. run `main.py` to host your bot locally!

## team
* [Alysha Kim](https://github.com/kimalysha93)
* [Callum Kipin](https://github.com/c-kip)
* [Jessica Li](https://github.com/jessicaa-li)
* [Truman Be](https://github.com/trumanbe01)