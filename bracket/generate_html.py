
# :: Method to render the vlr bracket with any input data

VLR_CSS = '''
*, *:before, *:after {
    box-sizing: inherit;
}

html, body, div, span, applet, object, iframe, h1, h2, h3, h4, h5, h6, p, blockquote, pre, a, abbr, acronym, address, big, cite, code, del, dfn, em, img, ins, kbd, q, s, samp, small, strike, strong, sub, sup, tt, var, center, dl, dt, dd, ol, ul, li, fieldset, form, label, legend, table, caption, tbody, tfoot, thead, tr, th, td, article, aside, canvas, details, embed, figure, figcaption, footer, header, hgroup, menu, nav, output, ruby, section, summary, time, mark, audio, video {
    margin: 0;
    padding: 0;
    border: 0;
    font-size: 100%;
    font: inherit;
    vertical-align: baseline;
    text-decoration: none;
}

div {
    display: block;
    unicode-bidi: isolate;
}

img {
    border: 0;
}

input {
    line-height: normal;
}

button, input, optgroup, select, textarea {
    color: inherit;
    font: inherit;
    margin: 0;
}

html,
body {
    display: block;
    font-family: 'Roboto', sans-serif;
    font-size: 12px;
    color: #333;
    background-color: #c6c6c6;
    text-rendering: optimizeLegibility;
    -webkit-font-smoothing: antialiased;
    /* overflow-y: hidden; */
    -webkit-text-size-adjust: 100%;
    box-sizing: border-box;
}

body {
    line-height: 1;
    margin: 0;
}

.wrapper {
    width: auto;
    min-width: 320px;
    max-width: 1160px;
    position: relative;
    padding: 0 22px;
    padding-top: 24px;
    padding-bottom: 60px;
    margin: 0 auto;
    background: #dadadc;
    box-shadow: 0 0 2px rgba(0, 0, 0, 0.22);
    min-height: calc(100vh - 55px - 44px - 1px);
}

.col-container {
    display: flex;
    flex-wrap: wrap;
}
.col {
    flex-basis: 0;
    flex-grow: 1;
    min-width: 0;
}

.event-container {
    position: relative;
    display: flex;
}
@media (max-width: 1080px) {
    .event-container {
        display: block;
    }
}
.event-content {
    min-width: 0;
    flex: 0 0 794px;
}

.wf-card {
    background: #fafafa;
    overflow: hidden;
    margin-bottom: 22px;
    position: relative;
    border: 0 !important;
    box-shadow: 0 1px 3px -1px rgba(0, 0, 0, 0.4);
    display: block;
}

.event-bracket-wrapper {
    width: 100%;
    height: 100%;
    margin: auto;
    overflow: hidden;
}
.event-brackets-container {
    padding: 15px 20px;
    padding-bottom: 25px;
    padding-right: 150px;
    overflow-x: auto;
}
.bracket-container {
    display: flex;
    padding: 10px 0;
}
.bracket-col {
    margin-right: 56px;
}

/* /// LABELS , SPACING */
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
.bracket-item.mod-empty {
    border: 2px solid transparent;
    height: 70px;
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
.bracket-item.mod-last {
    margin-bottom: 0 !important;
}

/* /// BRACKET */
.bracket-container.mod-compact .bracket-col {
    margin-right: 23px;
}
.bracket-container.mod-compact .bracket-col {
    margin-right: 23px;
}
/* /// // UPPER BRACKET */
.bracket-container.mod-upper .bracket-col.mod-2 {
    padding-top: 50px;
}
.bracket-container.mod-upper .bracket-col.mod-2 .bracket-item {
    margin-bottom: 132px;
}
.bracket-container.mod-upper .bracket-col.mod-3 {
    padding-top: 150px;
}
.bracket-container.mod-upper .bracket-col.mod-3 .bracket-item {
    margin-bottom: 334px;
}
/* /// // LOWER BRACKET */
.bracket-container.mod-lower .bracket-col.mod-1 {
    padding-top: 49px;
}
.bracket-container.mod-lower .bracket-col.mod-2 {
    padding-top: 0;
}
.bracket-container.mod-lower .bracket-col.mod-2 .bracket-item {
    margin-bottom: 32px;
}
.bracket-container.mod-lower .bracket-col.mod-3 {
    padding-top: 50px;
}
.bracket-container.mod-lower .bracket-col.mod-3 .bracket-item {
    margin-bottom: 132px;
}
.bracket-container.mod-lower .bracket-col.mod-4 .bracket-item {
    margin-bottom: 133px;
}

/* /// BRACKET ITEM WITHIN */
.bracket-item-team {
    display: flex;
    justify-content: space-between;
    width: 140px;
    border-top: 1px solid #ccc;
}
.bracket-item-team.mod-first {
    border-bottom: 1px solid #ccc;
    border-top: 0;
}
.bracket-item-team.mod-winner {
    background: #cee9d3;
    font-weight: 700;
}
.bracket-item.mod-pickem .bracket-item-team.mod-winner {
    background: none;
    font-weight: 400;
}
/* /// // TEAM STUFF */
.bracket-item-team-name {
    height: 32px;
    display: flex;
    align-items: center;
}
.bracket-item-team-score {
    flex: 0 0 32px;
    height: 32px;
    justify-content: center;
    border-left: 1px solid #ccc;
    align-items: center;
    display: flex;
}
.bracket-item img {
    width: 20px;
    height: 20px;
    margin: 0 5px;
    image-rendering: -webkit-optimize-contrast;
}
.bracket-item-team-name span {
    width: 75px;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
    padding: 5px 0;
}
/* /// // STATUS */
.bracket-item.mod-pickem .bracket-item-status {
    display: block;
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

/* /// LINES */
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
.bracket-container.mod-compact .bracket-item-line {
    width: 13px;
    right: -13px;
}
.bracket-container.mod-compact .bracket-item-line:after {
    right: -15px;
    width: 15px;
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
.bracket-container.mod-upper .bracket-col.mod-2 .bracket-item-line {
    height: 83px;
}
.bracket-container.mod-upper .bracket-col.mod-2 .bracket-item-line.mod-up {
    top: -49px;
}
'''


def generate_bracket_html(bracket_data) -> str | None:
    html = '''
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            ''' + VLR_CSS + '''
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
            <div class="bracket-col-label">
                {round_data["round"]}
            </div>
        '''
        # Add spacing for Upper Round 1 (first column)
        if col_idx == 0:
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
            points = match.get("points", "? / 0")
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

