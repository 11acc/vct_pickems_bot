
# :: Builds bracket configuration from event information

from db.db_instance import db
from db.queries import db_logic





bracket_data = {
    "upper": [
        {
            "round": "Upper Round 1",
            "matches": [
                {
                    "team1": {"name": "BBL Esports", "logo": "https://owcdn.net/img/65b8ccef5e273.png"},
                    "team2": {"name": "Natus Vincere", "logo": "https://owcdn.net/img/62a4109ddbd7f.png"},
                    "winner": "team1"
                },
                {
                    "team1": {"name": "FNATIC", "logo": "https://owcdn.net/img/62a40cc2b5e29.png"},
                    "team2": {"name": "FUT Esports", "logo": "https://owcdn.net/img/632be9976b8fe.png"},
                    "winner": "team1"
                }
            ]
        },
        {
            "round": "Upper Semifinals",
            "matches": [
                {
                    "team1": {"name": "Team Heretics", "logo": "https://owcdn.net/img/637b755224c12.png"},
                    "team2": {"name": "BBL Esports", "logo": "https://owcdn.net/img/65b8ccef5e273.png"},
                    "winner": ""
                },
                {
                    "team1": {"name": "Team Liquid", "logo": "https://owcdn.net/img/640c381f0603f.png"},
                    "team2": {"name": "FNATIC", "logo": "https://owcdn.net/img/62a40cc2b5e29.png"},
                    "winner": ""
                }
            ]
        },
        {
            "round": "Upper Final",
            "matches": [
                {
                    "team1": {"name": "", "logo": "/img/vlr/tmp/vlr.png"},
                    "team2": {"name": "", "logo": "/img/vlr/tmp/vlr.png"},
                    "winner": ""
                }
            ]
        },
        {
            "round": "Grand Final",
            "matches": [
                {
                    "team1": {"name": "", "logo": "/img/vlr/tmp/vlr.png"},
                    "team2": {"name": "", "logo": "/img/vlr/tmp/vlr.png"},
                    "winner": ""
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
                    "winner": "team1"
                },
                {
                    "team1": {"name": "FUT Esports", "logo": "https://owcdn.net/img/632be9976b8fe.png"},
                    "team2": {"name": "Team Vitality", "logo": "https://owcdn.net/img/6466d79e1ed40.png"},
                    "winner": "team1"
                }
            ]
        },
        {
            "round": "Lower Round 2",
            "matches": [
                {
                    "team1": {"name": "", "logo": "/img/vlr/tmp/vlr.png"},
                    "team2": {"name": "Natus Vincere", "logo": "https://owcdn.net/img/62a4109ddbd7f.png"},
                    "winner": ""
                },
                {
                    "team1": {"name": "", "logo": "/img/vlr/tmp/vlr.png"},
                    "team2": {"name": "FUT Esports", "logo": "https://owcdn.net/img/632be9976b8fe.png"},
                    "winner": ""
                }
            ]
        },
        {
            "round": "Lower Round 3",
            "matches": [
                {
                    "team1": {"name": "", "logo": "/img/vlr/tmp/vlr.png"},
                    "team2": {"name": "", "logo": "/img/vlr/tmp/vlr.png"},
                    "winner": ""
                }
            ]
        },
        {
            "round": "Lower Final",
            "matches": [
                {
                    "team1": {"name": "", "logo": "/img/vlr/tmp/vlr.png"},
                    "team2": {"name": "", "logo": "/img/vlr/tmp/vlr.png"},
                    "winner": ""
                }
            ]
        }
    ]
}

