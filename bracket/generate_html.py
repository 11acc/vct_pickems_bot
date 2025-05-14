
# :: Render vlr bracket with any input data

import os

# Generating other brackets breaks it, lines and spacing are not the same
# deeper generation customisation is necessary

def generate_bracket_html(bracket_data: dict) -> str | None:
    if not bracket_data:
        print(f"Null input bracket data: {bracket_data}")
        return None

    # Read css from file
    css_content = ""

    # Check if file exists
    css_path = os.path.join(os.path.dirname(__file__), "style.css")
    if not os.path.exists(css_path):
        raise FileNotFoundError(f"Template file not found at: {css_path}")

    with open(css_path, "r") as css_file:
        css_content = css_file.read()

    # Build html
    html = f'''
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            {css_content}
        </style>
    </head>
    <body>
        <div class="wrapper">
            <div class="col-container">
                <div class="event-container">
                    <div class="event-content">
                        <div class="wf-card mod-bracket">
                            <div class="event-bracket-wrapper">
                                <div class="event-brackets-container mod-locked">
    '''
    # Data ids for each match
    match_navigation = {
        "upper": {
            0: {
                0: {"curr_id": "111", "next_id": "211", "next_pos": "1", "next_id2": "112", "next_pos2": "0"},
                1: {"curr_id": "121", "next_id": "221", "next_pos": "1", "next_id2": "122", "next_pos2": "0"}
            },
            1: {
                0: {"curr_id": "211", "next_id": "311", "next_pos": "0", "next_id2": "222", "next_pos2": "0"},
                1: {"curr_id": "221", "next_id": "311", "next_pos": "1", "next_id2": "212", "next_pos2": "0"}
            },
            2: {
                0: {"curr_id": "311", "next_id": "411", "next_pos": "0", "next_id2": "412", "next_pos2": "0"}
            },
            3: {
                0: {"curr_id": "411", "next_id": "", "next_pos": "", "next_id2": "", "next_pos2": ""}
            }
        },
        "lower": {
            0: {
                0: {"curr_id": "112", "next_id": "212", "next_pos": "1", "next_id2": "", "next_pos2": ""},
                1: {"curr_id": "122", "next_id": "222", "next_pos": "1", "next_id2": "", "next_pos2": ""}
            },
            1: {
                0: {"curr_id": "212", "next_id": "312", "next_pos": "0", "next_id2": "", "next_pos2": ""},
                1: {"curr_id": "222", "next_id": "312", "next_pos": "1", "next_id2": "", "next_pos2": ""}
            },
            2: {
                0: {"curr_id": "312", "next_id": "412", "next_pos": "1", "next_id2": "", "next_pos2": ""}
            },
            3: {
                0: {"curr_id": "412", "next_id": "411", "next_pos": "1", "next_id2": "", "next_pos2": ""}
            }
        }
    }

    # Upper Bracket
    html += '<div class="bracket-container mod-upper mod-compact">'
    for col_idx, round_data in enumerate(bracket_data["upper"]):
        if col_idx >= 2:
            col_mod = 3  # Upper Final and Grand Final both go in slot 3
        else:
            col_mod = col_idx + 1
        # ba bam!
        html += f'''
        <div class="bracket-col mod-{col_mod}">
        '''
        # For Upper Round 1 add spacing first, then label
        if col_idx == 0:
            html += '''
            <div class="bracket-row mod-spacing">
                <div class="bracket-item mod-empty"></div>
            </div>
            <div class="bracket-col-label">
                ''' + round_data["round"] + '''
            </div>
            '''
        else:
            # For other columns, add the label at the beginning as before
            html += f'''
            <div class="bracket-col-label">
                {round_data["round"]}
            </div>
            '''

        for match_idx, match in enumerate(round_data["matches"]):
            team1 = match["team1"]
            team2 = match["team2"]
            winner = match["winner"]
            # points = match.get("points", "? / 0")
            mod_last = "mod-last" if match_idx == len(round_data["matches"]) - 1 else ""

            # Correct line directions
            if col_idx == 0:  # Upper Round 1
                mod_line = "mod-up"
            elif col_idx == 1:  # Upper Semifinals
                mod_line = "mod-down" if match_idx == 0 else "mod-up"
            elif col_idx >= 2:  # Upper Final and Grand Final
                mod_line = ""  # No line for final rounds

            nav = match_navigation["upper"].get(col_idx, {}).get(match_idx, {})
            curr_id = nav.get("curr_id", "")
            next_id = nav.get("next_id", "")
            next_pos = nav.get("next_pos", "")
            next_id2 = nav.get("next_id2", "")
            next_pos2 = nav.get("next_pos2", "")

            team1_class = "mod-first"
            team2_class = ""
            if winner == "team1":
                team1_class += " mod-winner"
            elif winner == "team2":
                team2_class += " mod-winner"

            html += f'''
            <div class="bracket-row mod-{match_idx + 1}">
                <span class="bracket-item mod-pickem {mod_last}" title="{team1['name']} vs. {team2['name']}" 
                      data-curr-id="{curr_id}" data-next-id="{next_id}" data-next-pos="{next_pos}" 
                      data-next-id2="{next_id2}" data-next-pos2="{next_pos2}">
                    <div class="bracket-item-team {team1_class}" data-curr-pos="0">
                        <div class="bracket-item-team-name">
                            <img src="{team1['logo_url']}">
                            <span>{team1['name']}</span>
                        </div>
                        <div class="bracket-item-team-score">
                        </div>
                    </div>
                    <div class="bracket-item-team {team2_class}" data-curr-pos="1">
                        <div class="bracket-item-team-name">
                            <img src="{team2['logo_url']}">
                            <span>{team2['name']}</span>
                        </div>
                        <div class="bracket-item-team-score">
                        </div>
                    </div>
                    <div class="bracket-item-status">
                            <div class="bracket-item-status-icons">
                            </div>
                            <span></span>
                    </div>
                    '''
            if mod_line:
                html += f'<div class="bracket-item-line {mod_line}"></div>'
            html += f'''
                    <input type="hidden" class="bracket-item-pick mod-winner" value="">
                    <input type="hidden" class="bracket-item-pick mod-loser" value="">
                </span>
            </div>
            '''
            # Add spacing after first match in Upper Round 1
            if col_idx == 0 and match_idx == 0:
                html += '''
                <div class="bracket-row mod-spacing">
                    <div class="bracket-item mod-empty"></div>
                </div>
                '''
        html += '</div>'

    html += '</div>'

    # Lower Bracket
    html += '<div class="bracket-container mod-lower">'
    for col_idx, round_data in enumerate(bracket_data["lower"]):
        html += f'''
        <div class="bracket-col mod-{col_idx + 1}">
            <div class="bracket-col-label">
                {round_data["round"]}
            </div>
        '''
        for match_idx, match in enumerate(round_data["matches"]):
            team1 = match["team1"]
            team2 = match["team2"]
            winner = match["winner"]
            # points = match.get("points", "? / 0")
            mod_last = "mod-last" if match_idx == len(round_data["matches"]) - 1 else ""

            if col_idx == 0:  # Lower Round 1
                mod_line = "mod-up"
            elif col_idx == 1:  # Lower Round 2
                mod_line = "mod-down" if match_idx == 0 else "mod-up"
            elif col_idx == 2:  # Lower Round 3
                mod_line = "mod-up"
            else:  # Lower Final
                mod_line = ""

            nav = match_navigation["lower"].get(col_idx, {}).get(match_idx, {})
            curr_id = nav.get("curr_id", "")
            next_id = nav.get("next_id", "")
            next_pos = nav.get("next_pos", "")
            next_id2 = nav.get("next_id2", "")
            next_pos2 = nav.get("next_pos2", "")

            team1_class = "mod-first"
            if winner == "team1":
                team1_class += " mod-winner"
            team2_class = ""
            if winner == "team2":
                team2_class += " mod-winner"
            elif winner == "team1":
                team2_class += " mod-loser"

            html += f'''
            <div class="bracket-row mod-{match_idx + 1}">
                <span class="bracket-item mod-pickem {mod_last}" title="{team1['name']} vs. {team2['name']}"
                      data-curr-id="{curr_id}" data-next-id="{next_id}" data-next-pos="{next_pos}" 
                      data-next-id2="{next_id2}" data-next-pos2="{next_pos2}">
                    <div class="bracket-item-team {team1_class}" data-curr-pos="0">
                        <div class="bracket-item-team-name">
                            <img src="{team1['logo_url']}">
                            <span>{team1['name']}</span>
                        </div>
                        <div class="bracket-item-team-score">
                        </div>
                    </div>
                    <div class="bracket-item-team {team2_class}" data-curr-pos="1">
                        <div class="bracket-item-team-name">
                            <img src="{team2['logo_url']}">
                            <span>{team2['name']}</span>
                        </div>
                        <div class="bracket-item-team-score">
                        </div>
                    </div>
                    <div class="bracket-item-status">
                            <div class="bracket-item-status-icons">
                            </div>
                            <span></span>
                    </div>
                    '''
            if mod_line:
                html += f'<div class="bracket-item-line {mod_line}"></div>'
            html += f'''
                    <input type="hidden" class="bracket-item-pick mod-winner" value="">
                    <input type="hidden" class="bracket-item-pick mod-loser" value="">
                </span>
            </div>
            '''
        html += '</div>'

    html += '''
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </body>
    </html>
    '''
    return html
