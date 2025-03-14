# Reobot - VCT Pickem Discord Bot

Reobot is a Discord bot created to make tracking of pick'em more convenient. The main inspiration for the project came from wanting to easily compare my friend's total points across various regional events, such as Kickoff 2025. Using vlr, one has to go to each event's pickem page and add the points for each, which quickly becomes tedious. And so the usual small project started growing with more ideas... leaderboard for whoever had the most points for an event, checking who voted who each day, etc.

The project by no means is trying to be a mainstream solution, rather it very much is a slapstickly built fun side project. As a result, there are many gaps where one needs to do some manual inputting for the bot to work smoothly.
- Manual entry of events and teams into DB
- Scraping method of votes is incomplete (bracket votes still missing)
- Limited flexibility

Nonetheless, I think reobot is pretty cool.

![Gif of repo in action](./gif.gif)


## ⚙️ Commands

| Command | Description | Usage |
|---------|-------------|-------|
| `!vct hello` | Test command to check if the bot is responsive | `!vct hello` |
| `!vct points <event> <year>` | Get the points leaderboard for a specific event | `!vct points bangkok 2025` |
| `!vct leaderboard` | View the global Pickem leaderboard | `!vct leaderboard` |
| `!vct wvw [skip]` | See who voted for which teams in upcoming matches | `!vct wvw` or `!vct wvw 3` to skip to the nth next match day |
| `!vct refresh <type>` | Update the database with fresh data | `!vct refresh pickems`, `!vct refresh matches`, or `!vct refresh votes` |


## 📂 Architecture

```plaintext
.
├── reobot.py                   # Main script to initialise and manage Discord bot commands and events
├── db/
│   ├── db_instance.py          # Low-level database operations and connection management
│   ├── queries.py              # High-level database queries and operations
│   └── entity_classes.py       # Defines Python classes representing database entities and their relationships
├── db_sensitive/
│   └── vct_pickems.db          # File which holds db data, data includes VCT info from Q1 2025, yes I suck at predicting
├── utils/
│   ├── emojis.py               # Utility for retrieving and matching Discord emojis based on team and event names
│   ├── formatting.py           # Functions for formatting Discord embed messages with player points, votes, and rankings
│   └── matching.py             # Utility for fuzzy matching user input to database entries
├── services/
│   ├── leaderboard.py          # Queries and formats player rankings for the global leaderboard Discord command
│   ├── points_for_event.py     # Queries and formats player points for a specific event for Discord display
│   ├── update.py               # Updates database entries by scraping latest event, match, and vote data
│   └── who_voted_who.py        # Retrieves and formats voting information for upcoming matches
└── scraper/
    └── vlr_scraper.py          # Scrapes event, match, and vote data from vlr.gg and updates the database accordingly
```


### Database Structure

The bot uses an SQLite database with the following key entities:

- **players**: User information and Discord IDs
- **teams**: VCT teams and their metadata
- **events**: VCT tournaments and their metadata
- **sub_event**: Additional information for each event by region
- **matches**: Individual matches with teams, dates, and results
- **votes**: Player predictions for matches
- **points**: Points earned by players for each event
- **breakdown_pts**: Breakdown of points by region
- **stars**: Special achievements awarded to players


## 🛠 Setup and Installation

### Prerequisites
- Python 3.8+
- Discord Bot Token
- SQLite Database

### Technologies Used

- **Python** – Main programming language.
- **Discord.py** – Bot API integration.
- **SQLite** – Database management.
- **BeautifulSoup & Requests** – Web scraping from vlr.gg.
- **FuzzyWuzzy** – Fuzzy matching of user inputs to database entries.

### Installation Steps

Clone the repository:
```bash
git clone https://github.com/username/reobot.git
cd reobot
```

Install dependencies:
```bash
pip install -r requirements.txt
```

Create a `.env` file in the project root with the following variables:
```bash
DISCORD_BOT_TOKEN=your_discord_bot_token
DB_PATH=path_to_your_sqlite_database.db
```

Run the bot:
```bash
python reobot.py
```


## Contributing

Fork it, modify it, push it, eat it, summon a duck god with it. Whatever resonable day-to-day activity you prefer ( •ᴗ•)b


## Acknowledgments

- [vlr.gg](https://www.vlr.gg/) for being the data backbone of this project