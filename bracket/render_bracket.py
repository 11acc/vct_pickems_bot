
from generate_html import generate_bracket_html


bracket_data = {
    "upper": [
        {
            "round": "Upper Round 1",
            "matches": [
                {
                    "team1": {"name": "BBL Esports", "logo": "https://owcdn.net/img/65b8ccef5e273.png"},
                    "team2": {"name": "Natus Vincere", "logo": "https://owcdn.net/img/62a4109ddbd7f.png"},
                    "winner": "team1",
                    "points": "0 / 5"
                },
                {
                    "team1": {"name": "FNATIC", "logo": "https://owcdn.net/img/62a40cc2b5e29.png"},
                    "team2": {"name": "FUT Esports", "logo": "https://owcdn.net/img/632be9976b8fe.png"},
                    "winner": "team1",
                    "points": "0 / 5"
                }
            ]
        },
        {
            "round": "Upper Semifinals",
            "matches": [
                {
                    "team1": {"name": "Team Heretics", "logo": "https://owcdn.net/img/637b755224c12.png"},
                    "team2": {"name": "BBL Esports", "logo": "https://owcdn.net/img/65b8ccef5e273.png"},
                    "winner": "",
                    "points": "? / 10"
                },
                {
                    "team1": {"name": "Team Liquid", "logo": "https://owcdn.net/img/640c381f0603f.png"},
                    "team2": {"name": "FNATIC", "logo": "https://owcdn.net/img/62a40cc2b5e29.png"},
                    "winner": "",
                    "points": "? / 10"
                }
            ]
        },
        {
            "round": "Upper Final",
            "matches": [
                {
                    "team1": {"name": "", "logo": "/img/vlr/tmp/vlr.png"},
                    "team2": {"name": "", "logo": "/img/vlr/tmp/vlr.png"},
                    "winner": "",
                    "points": "? / 15"
                }
            ]
        },
        {
            "round": "Grand Final",
            "matches": [
                {
                    "team1": {"name": "", "logo": "/img/vlr/tmp/vlr.png"},
                    "team2": {"name": "", "logo": "/img/vlr/tmp/vlr.png"},
                    "winner": "",
                    "points": "? / 50"
                }
            ]
        }
    ],
    "lower": [
        {
            "round": "Lower Round 1",
            "matches": [
                {
                    "team1": {"name": "Natus Vincere", "logo": "https://owcdn.net/img/62a4109ddbd7f.png"},
                    "team2": {"name": "Karmine Corp", "logo": "https://owcdn.net/img/627403a0d9e48.png"},
                    "winner": "team1",
                    "points": "0 / 10"
                },
                {
                    "team1": {"name": "FUT Esports", "logo": "https://owcdn.net/img/632be9976b8fe.png"},
                    "team2": {"name": "Team Vitality", "logo": "https://owcdn.net/img/6466d79e1ed40.png"},
                    "winner": "team1",
                    "points": "0 / 10"
                }
            ]
        },
        {
            "round": "Lower Round 2",
            "matches": [
                {
                    "team1": {"name": "", "logo": "/img/vlr/tmp/vlr.png"},
                    "team2": {"name": "Natus Vincere", "logo": "https://owcdn.net/img/62a4109ddbd7f.png"},
                    "winner": "",
                    "points": "? / 20"
                },
                {
                    "team1": {"name": "", "logo": "/img/vlr/tmp/vlr.png"},
                    "team2": {"name": "FUT Esports", "logo": "https://owcdn.net/img/632be9976b8fe.png"},
                    "winner": "",
                    "points": "? / 20"
                }
            ]
        },
        {
            "round": "Lower Round 3",
            "matches": [
                {
                    "team1": {"name": "", "logo": "/img/vlr/tmp/vlr.png"},
                    "team2": {"name": "", "logo": "/img/vlr/tmp/vlr.png"},
                    "winner": "",
                    "points": "? / 30"
                }
            ]
        },
        {
            "round": "Lower Final",
            "matches": [
                {
                    "team1": {"name": "", "logo": "/img/vlr/tmp/vlr.png"},
                    "team2": {"name": "", "logo": "/img/vlr/tmp/vlr.png"},
                    "winner": "",
                    "points": "? / 40"
                }
            ]
        }
    ]
}


bracket = generate_bracket_html(bracket_data)

with open('bracket.html', 'w', encoding='utf-8') as f:
    f.write(bracket)

print("Saved the thing")