
# :: ...?

VLR_CSS = '''
html, body {
    font-family: 'Roboto', sans-serif;
    font-size: 12px;
    color: #333;
    min-width: 1160px;
    text-rendering: optimizeLegibility;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
}
/* Core bracket styling */
.bracket-container {
  display: flex;
}

.bracket-col {
  margin-right: 56px;
}

.bracket-col-label {
  margin-bottom: 15px;
  color: #444;
  font-size: 11px;
  font-weight: 700;
  text-align: center;
}

.bracket-row {
  position: relative;
}

.bracket-item {
  right: 0;
  font-size: 11px;
  font-weight: 400;
  display: block;
  margin-bottom: 31px;
  position: relative;
  border: 2px solid #aaa;
  border-radius: 3px;
  z-index: 1;
}

/* Team boxes */
.bracket-item-team {
  display: flex;
  justify-content: space-between;
  width: 140px;
  border-top: 1px solid #ccc;
}

.bracket-item-team.mod-winner {
  background: #cee9d3;
  font-weight: 700;
}

.bracket-item-team.mod-loser {
  /* No special styling for losers except when selected in pickem */
}

.bracket-item-team.mod-first {
  border-bottom: 1px solid #ccc;
  border-top: 0;
}

/* Team name and logo */
.bracket-item-team-name {
  height: 32px;
  display: flex;
  align-items: center;
}

.bracket-item-team-name span {
  width: 75px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  padding: 5px 0;
}

.bracket-item img {
  width: 20px;
  height: 20px;
  margin: 0 5px;
  image-rendering: -webkit-optimize-contrast;
}

/* Team score display */
.bracket-item-team-score {
  flex: 0 0 32px;
  height: 32px;
  justify-content: center;
  border-left: 1px solid #ccc;
  align-items: center;
  display: flex;
}

/* Bracket lines connecting matches */
.bracket-item-line {
  position: absolute;
  width: 30px;
  height: 31px;
  right: -30px;
  top: 32px;
  border: 2px solid #aaa;
  border-left: 0;
  border-bottom: 0;
  border-radius: 0 3px 0 0;
}

.bracket-item-line:after {
  content: '';
  position: absolute;
  bottom: -4px;
  height: 4px;
  right: -30px;
  width: 30px;
  border: 2px solid #aaa;
  border-top: 0;
  border-right: 0;
  border-radius: 0 0 0 3px;
}

.bracket-item-line.mod-up {
  border-top: 0;
  border-bottom: 2px solid #aaa;
  top: 3px;
  border-radius: 0 0 3px 0;
}

.bracket-item-line.mod-up:after {
  top: -4px;
  border-top: 2px solid #aaa;
  border-bottom: 0;
  border-radius: 3px 0 0 0;
}

/* Compact bracket mode (reduces spacing) */
.bracket-container.mod-compact .bracket-col {
  margin-right: 23px;
}

.bracket-container.mod-compact .bracket-item-line {
  width: 13px;
  right: -13px;
}

.bracket-container.mod-compact .bracket-item-line:after {
  right: -15px;
  width: 15px;
}

/* Last item in a column */
.bracket-item.mod-last {
  margin-bottom: 0 !important;
}

/* Pickem specific styles */
.bracket-item.mod-pickem .bracket-item-team:hover {
  background: #e8f5fc;
  cursor: pointer;
}

.bracket-item-status {
  position: absolute;
  bottom: -22px;
  left: 0;
  font-size: 11px;
  padding-left: 8px;
  width: 100%;
  display: flex;
  justify-content: space-between;
  height: 15px;
  line-height: 15px;
}

/* Draggable container */
.event-brackets-container {
  padding: 15px 20px;
  padding-bottom: 25px;
  padding-right: 150px;
  overflow-x: auto;
}

.drag {
  width: 220%;
  cursor: grab;
  -moz-user-select: none;
  -webkit-user-select: none;
  -ms-user-select: none;
  -khtml-user-select: none;
  user-select: none;
}

/* Upper bracket specific */
.bracket-container.mod-upper .bracket-col.mod-2 {
  padding-top: 50px;
}

.bracket-container.mod-upper .bracket-col.mod-2 .bracket-item {
  margin-bottom: 132px;
}

.bracket-container.mod-upper .bracket-col.mod-2 .bracket-item-line {
  height: 83px;
}

.bracket-container.mod-upper .bracket-col.mod-2 .bracket-item-line.mod-up {
  top: -49px;
}

/* Lower bracket specific */
.bracket-container.mod-lower .bracket-col.mod-2 .bracket-item {
  margin-bottom: 32px;
}
'''


def generate_bracket_html(bracket_data):
    html = '''
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            ''' + VLR_CSS + '''
        </style>
    </head>
    <body>
        <div class="drag">
            <div class="event-brackets-container mod-locked">
    '''

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
        html += f'''
        <div class="bracket-col mod-{col_idx + 1}">
            <div class="bracket-col-label">
                {round_data["round"]}
            </div>
        '''
        if col_idx == 0:  # Add spacing for first column
            html += '''
            <div class="bracket-row mod-spacing">
                <div class="bracket-item mod-empty"></div>
            </div>
            '''
        for match_idx, match in enumerate(round_data["matches"]):
            team1 = match["team1"]
            team2 = match["team2"]
            winner = match["winner"]
            points = match.get("points", "? / 0")
            mod_last = "mod-last" if match_idx == len(round_data["matches"]) - 1 else ""
            mod_line = "mod-up" if col_idx == 0 or match_idx == 1 else "mod-down"

            nav = match_navigation["upper"].get(col_idx, {}).get(match_idx, {})
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

            match_id = f"9194{col_idx}{match_idx}"
            html += f'''
            <div class="bracket-row mod-{match_idx + 1}">
                <span class="bracket-item mod-pickem {mod_last}" title="{team1['name']} vs. {team2['name']}" 
                      data-curr-id="{curr_id}" data-next-id="{next_id}" data-next-pos="{next_pos}" 
                      data-next-id2="{next_id2}" data-next-pos2="{next_pos2}">
                    <div class="bracket-item-team {team1_class}" data-curr-pos="0">
                        <div class="bracket-item-team-name">
                            <img src="{team1['logo']}">
                            <span>{team1['name']}</span>
                        </div>
                        <div class="bracket-item-team-score">
                        </div>
                    </div>
                    <div class="bracket-item-team {team2_class}" data-curr-pos="1">
                        <div class="bracket-item-team-name">
                            <img src="{team2['logo']}">
                            <span>{team2['name']}</span>
                        </div>
                        <div class="bracket-item-team-score">
                        </div>
                    </div>
                    <div class="bracket-item-status">Points: {points}</div>
                    <div class="bracket-item-line {mod_line}"></div>
                    <input type="hidden" class="bracket-item-pick mod-winner" name="bracket-item-id-winner-{match_id}" value="">
                    <input type="hidden" class="bracket-item-pick mod-loser" name="bracket-item-id-loser-{match_id}" value="">
                </span>
            </div>
            '''
            if col_idx == 0 and match_idx == 0:  # Add spacing after first match
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
            points = match.get("points", "? / 0")
            mod_last = "mod-last" if match_idx == len(round_data["matches"]) - 1 else ""
            mod_line = "mod-up" if match_idx == 0 else "mod-down"

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

            match_id = f"9194{col_idx + 4}{match_idx}"
            html += f'''
            <div class="bracket-row mod-{match_idx + 1}">
                <span class="bracket-item mod-pickem {mod_last}" title="{team1['name']} vs. {team2['name']}"
                      data-curr-id="{curr_id}" data-next-id="{next_id}" data-next-pos="{next_pos}" 
                      data-next-id2="{next_id2}" data-next-pos2="{next_pos2}">
                    <div class="bracket-item-team {team1_class}" data-curr-pos="0">
                        <div class="bracket-item-team-name">
                            <img src="{team1['logo']}">
                            <span>{team1['name']}</span>
                        </div>
                        <div class="bracket-item-team-score">
                        </div>
                    </div>
                    <div class="bracket-item-team {team2_class}" data-curr-pos="1">
                        <div class="bracket-item-team-name">
                            <img src="{team2['logo']}">
                            <span>{team2['name']}</span>
                        </div>
                        <div class="bracket-item-team-score">
                        </div>
                    </div>
                    <div class="bracket-item-status">Points: {points}</div>
                    <div class="bracket-item-line {mod_line}"></div>
                    <input type="hidden" class="bracket-item-pick mod-winner" name="bracket-item-id-winner-{match_id}" value="">
                    <input type="hidden" class="bracket-item-pick mod-loser" name="bracket-item-id-loser-{match_id}" value="">
                </span>
            </div>
            '''
        html += '</div>'

    html += '</div>'

    html += '''
            </div>
        </div>
    </body>
    </html>
    '''
    return html

