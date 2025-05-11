Installation
1. Clone the repository or download the script.
If you are setting up this bot from a fresh start, create a folder and save the Python script (bot.py or whatever you choose to name it).

2. Install dependencies.
Run the following command to install the necessary dependencies using pip:

bash
Copy
Edit
pip install discord.py
3. Set up your bot token.
Go to the Discord Developer Portal, create a new bot, and copy the bot token. Replace the placeholder value for TOKEN in the script with your bot token:

python
Copy
Edit
TOKEN = "YOUR_BOT_TOKEN"
4. Customize the bot settings:
ID_CANAL_LOG: Set the channel ID where the bot should log responses.

admins: List the Discord IDs of the admins who will receive notifications.

Example:

python
Copy
Edit
ID_CANAL_LOG = 123456789012345678  # Replace with your actual channel ID
admins = [123456789012345678, 987654321098765432]  # Replace with actual admin IDs
5. Run the bot.
Once everything is set up, run the bot with the following command:

bash
Copy
Edit
python bot.py
Bot Flow
When a user joins: The bot sends a series of questions via Direct Message (DM) to the new member.

The user has 2 minutes to respond to each question.

If the user doesn’t respond within the time limit or provides invalid answers, they are either kicked or banned (based on the question).

Questions:

Question 1: "Do you identify as a woman or a man?" The answer must be "no", "nao", or similar variants. Incorrect answers will result in a ban.

Question 2: "What is your age?" The answer must be numeric and under 100. Any invalid input results in a request to retry.

Question 3: "Who is the GOAT (greatest of all time) in basketball?" The answer must be one of the options: a, b, c, d.

Question 4: "Who was more dangerous in their prime: P. Diddy or 4lan?" Any invalid response will prompt a retry.

Question 5: "What do you think of Davi Brito?" (Open-ended question).

Behavior Monitoring:

The bot tracks spam (multiple answers sent in quick succession). If detected, the user is warned and may be kicked if the behavior persists.

The bot kicks users who provide invalid answers or take too long to respond.

Logging:

The bot saves all responses to a CSV file.

The bot sends logs to a specific channel (set by ID_CANAL_LOG).

Admins are notified if a user answers certain questions in specific ways (e.g., identification as a woman).

Commands
There are no direct commands for the bot (as it automatically operates on member joins), but you can configure the following in the code:

!admin_report: Notify the admins when a specific action is taken.

!logs: View stored responses from the question flow in a designated log channel.

Error Handling
Timeout: If the user doesn’t respond within 2 minutes, they will be kicked from the server.

Invalid Response: Invalid answers to the questions will prompt the bot to request a valid response.

Spam Detection: If the bot detects a spammy behavior (too many responses in a short time), the user will be warned and potentially removed.

Customization
You can customize the following aspects:

Questions: Modify the list of questions to suit your needs by editing the perguntas list.

Admin Notifications: Admins can be added or removed from the list by editing the admins variable.

Logging: Customize the log messages and output format for better readability or integration.

Notes
Make sure to handle your bot token with care. Never expose it publicly.

The bot will need to have the kick, ban, and manage messages permissions in the server for full functionality.

You can modify the timeout and retry mechanisms if needed.

License
This project is open-source and free to use. Feel free to make changes or contribute.

Thank you for using our bot! 😊
