
import argparse
import json
import os
from PIL import Image, ImageDraw, ImageFont
import textwrap
import urllib.request
from io import BytesIO


class TournamentBracketGenerator:
    """Generate tournament brackets as PNG images without external dependencies."""

    def __init__(self, config):
        self.config = config
        self.teams = config.get('teams', {})
        self.bracket_type = config.get('bracket_type', 'double_elimination')
        self.num_teams = config.get('num_teams', 8)
        self.logo_cache = {}  # Cache for downloaded logos

        # Dimensions and styling
        self.match_width = 200
        self.match_height = 64
        self.team_height = 32
        self.margin_x = 80
        self.margin_y = 30
        self.round_header_height = 30
        self.logo_size = (24, 24)

        # Calculate bracket dimensions based on number of teams
        self.rounds = self._calculate_rounds()

        # Colors
        self.colors = {
            'background': (250, 250, 250),
            'text': (68, 68, 68),
            'border': (170, 170, 170),
            'winner_bg': (206, 233, 211),
            'match_bg': (255, 255, 255),
            'line': (170, 170, 170)
        }

        # Attempt to load fonts
        try:
            self.title_font = ImageFont.truetype("Arial.ttf", 11)
            self.team_font = ImageFont.truetype("Arial.ttf", 12)
            self.score_font = ImageFont.truetype("Arial.ttf", 12)
            self.points_font = ImageFont.truetype("Arial.ttf", 10)
        except IOError:
            # Fallback to default font
            self.title_font = ImageFont.load_default()
            self.team_font = ImageFont.load_default()
            self.score_font = ImageFont.load_default()
            self.points_font = ImageFont.load_default()

    def _calculate_rounds(self):
        """Calculate the number of rounds needed based on team count."""
        rounds = 0
        teams = self.num_teams
        while teams > 1:
            teams = teams // 2
            rounds += 1
        return rounds

    def _get_match_data(self, bracket, round_idx, match_idx):
        """Get match data for a specific position in the bracket."""
        position1 = f"{bracket}-{round_idx}-{match_idx}-1"
        position2 = f"{bracket}-{round_idx}-{match_idx}-2"

        team1 = self.teams.get(position1, {
            'id': '',
            'name': 'TBD',
            'logo': '',
            'score': '',
            'is_winner': False
        })
        team2 = self.teams.get(position2, {
            'id': '',
            'name': 'TBD',
            'logo': '',
            'score': '',
            'is_winner': False
        })

        # Calculate points based on the round (increases with later rounds)
        points = 5 * round_idx if bracket == 'upper' else 10 * round_idx

        return {'team1': team1, 'team2': team2, 'points': points}

    def _get_logo(self, logo_url):
        """Fetch or retrieve cached logo image."""
        if not logo_url:
            # Return a default blank logo
            return Image.new('RGBA', self.logo_size, (0, 0, 0, 0))

        if logo_url in self.logo_cache:
            return self.logo_cache[logo_url]

        try:
            # Check if it's a local file
            if os.path.isfile(logo_url):
                img = Image.open(logo_url)
            else:
                # Handle URLs, adding https: prefix if needed
                if logo_url.startswith('//'):
                    logo_url = 'https:' + logo_url

                response = urllib.request.urlopen(logo_url)
                img = Image.open(BytesIO(response.read()))

            # Resize and convert to RGBA
            img = img.convert('RGBA')
            img = img.resize(self.logo_size, Image.LANCZOS)

            self.logo_cache[logo_url] = img
            return img
        except Exception as e:
            print(f"Could not load logo {logo_url}: {e}")
            return Image.new('RGBA', self.logo_size, (0, 0, 0, 0))

    def _draw_team(self, draw, x, y, team, is_top=True):
        """Draw a team box with logo, name and score."""
        # Box background
        background_color = self.colors['winner_bg'] if team[
            'is_winner'] else self.colors['match_bg']
        draw.rectangle([(x, y), (x + self.match_width, y + self.team_height)],
                       fill=background_color,
                       outline=self.colors['border'])

        # Divider for score
        score_width = 32
        draw.line([(x + self.match_width - score_width, y),
                   (x + self.match_width - score_width, y + self.team_height)],
                  fill=self.colors['border'],
                  width=1)

        # Team logo
        # if team['logo']:
            # logo = self._get_logo(team['logo'])
            # logo_pos = (x + 5, y + (self.team_height - self.logo_size[1]) // 2)
            # img.paste(logo, logo_pos, logo)

        # Team name (truncate if too long)
        name = team['name'] if team['name'] else 'TBD'
        name_width = self.match_width - score_width - 40  # space for logo + margin
        if draw.textlength(name, font=self.team_font) > name_width:
            # Truncate with ellipsis
            while draw.textlength(
                    name + "...",
                    font=self.team_font) > name_width and len(name) > 0:
                name = name[:-1]
            name += "..." if name else ""

        draw.text(
            (x + 35, y +
             (self.team_height - draw.textlength("Aj", font=self.team_font)) //
             2),
            name,
            fill=self.colors['text'],
            font=self.team_font)

        # Score
        if team['score']:
            score_x = x + self.match_width - score_width // 2 - draw.textlength(
                str(team['score']), font=self.score_font) // 2
            score_y = y + (self.team_height -
                           draw.textlength("0", font=self.score_font)) // 2
            draw.text((score_x, score_y),
                      str(team['score']),
                      fill=self.colors['text'],
                      font=self.score_font)

    def _draw_match(self, draw, x, y, match_data, round_idx, match_idx,
                    total_matches_in_round):
        """Draw a complete match with connecting lines."""
        # Draw team boxes
        self._draw_team(draw, x, y, match_data['team1'], is_top=True)
        self._draw_team(draw,
                        x,
                        y + self.team_height,
                        match_data['team2'],
                        is_top=False)

        # Draw points text
        points_text = f"Points: ? / {match_data['points']}"
        draw.text((x + 5, y + self.team_height * 2 + 5),
                  points_text,
                  fill=self.colors['text'],
                  font=self.points_font)

        # Draw connecting lines to next round if not the final round
        if round_idx < self.rounds:
            # Calculate next match position
            next_round_matches = 2**(self.rounds - round_idx - 1)
            next_match_idx = (match_idx - 1) // 2 + 1

            line_start_x = x + self.match_width
            line_start_y = y + self.team_height

            # Horizontal line
            line_length = self.margin_x // 2
            draw.line([(line_start_x, line_start_y),
                       (line_start_x + line_length, line_start_y)],
                      fill=self.colors['line'],
                      width=1)

            # Only draw the vertical connecting line from every 2 matches
            if match_idx % 2 == 1:
                # Calculate where the next match will be
                next_y = (match_idx -
                          1) // 2 * (self.match_height + self.margin_y *
                                     (2**round_idx)) + self.round_header_height

                # Vertical line going down
                if match_idx < total_matches_in_round:
                    draw.line([(line_start_x + line_length, line_start_y),
                               (line_start_x + line_length, line_start_y +
                                self.margin_y * (2**(round_idx - 1)))],
                              fill=self.colors['line'],
                              width=1)
            else:
                # Vertical line going up
                next_y = ((match_idx - 2) //
                          2) * (self.match_height + self.margin_y *
                                (2**round_idx)) + self.round_header_height

                # Draw vertical line going up
                draw.line([(line_start_x + line_length,
                            line_start_y - self.team_height),
                           (line_start_x + line_length,
                            line_start_y - self.team_height - self.margin_y *
                            (2**(round_idx - 1)))],
                          fill=self.colors['line'],
                          width=1)

    def _draw_round_header(self, draw, x, y, round_idx, bracket='upper'):
        """Draw round header text."""
        if bracket == 'upper':
            if round_idx == self.rounds:
                header_text = "Grand Final"
            elif round_idx == self.rounds - 1:
                header_text = "Upper Final"
            else:
                header_text = f"Upper Round {round_idx}"
        else:
            if round_idx == self.rounds * 2 - 1:
                header_text = "Lower Final"
            else:
                header_text = f"Lower Round {round_idx}"

        text_width = draw.textlength(header_text, font=self.title_font)
        draw.text((x + (self.match_width - text_width) // 2, y),
                  header_text,
                  fill=self.colors['text'],
                  font=self.title_font)

    def generate_bracket(self, output_path):
        """Generate the tournament bracket image."""
        # Calculate total image dimensions based on bracket type and team count
        total_width = self.rounds * (self.match_width + self.margin_x)

        # For upper bracket
        matches_in_first_round_upper = 2**(self.rounds - 1)
        upper_height = (matches_in_first_round_upper * self.match_height) + (
            (matches_in_first_round_upper - 1) *
            self.margin_y) + self.round_header_height * 2

        if self.bracket_type == 'double_elimination':
            # For lower bracket (roughly the same height as upper)
            lower_height = upper_height
            total_height = upper_height + lower_height
        else:
            total_height = upper_height

        # Create the image
        img = Image.new('RGB', (total_width, total_height),
                        self.colors['background'])
        draw = ImageDraw.Draw(img)

        # Draw upper bracket
        self._draw_upper_bracket(draw, 0, 0)

        # Draw lower bracket if needed
        if self.bracket_type == 'double_elimination':
            self._draw_lower_bracket(draw, 0, upper_height)

        # Save the image
        img.save(output_path)
        print(f"Bracket saved to {output_path}")

        # Also return the image for possible further processing
        return img

    def _draw_upper_bracket(self, draw, start_x, start_y):
        """Draw the upper bracket section."""
        for round_idx in range(1, self.rounds + 1):
            matches_in_round = 2**(self.rounds - round_idx)

            # Round header
            round_x = start_x + (round_idx - 1) * (self.match_width +
                                                   self.margin_x)
            self._draw_round_header(draw, round_x, start_y, round_idx, 'upper')

            # Draw matches
            for match_idx in range(1, matches_in_round + 1):
                match_data = self._get_match_data('upper', round_idx,
                                                  match_idx)

                # Calculate match position
                match_spacing = self.margin_y * (2**(round_idx - 1))
                match_y = start_y + self.round_header_height + (
                    match_idx - 1) * (self.match_height + match_spacing)

                self._draw_match(draw, round_x, match_y, match_data, round_idx,
                                 match_idx, matches_in_round)

    def _draw_lower_bracket(self, draw, start_x, start_y):
        """Draw the lower bracket section."""
        lower_rounds = self.rounds * 2 - 1

        # For each round in lower bracket
        for round_idx in range(1, lower_rounds + 1):
            # In lower bracket, the number of matches changes in a different pattern
            if round_idx % 2 == 1:  # Odd rounds
                matches_in_round = 2**(self.rounds - (round_idx // 2) - 1)
            else:  # Even rounds
                matches_in_round = 2**(self.rounds - (round_idx // 2) - 1)

            # Skip the round if no matches
            if matches_in_round <= 0:
                continue

            # Round header
            visual_round = (round_idx - 1) // 2 + 1  # Adjust round visually
            round_x = start_x + (visual_round - 1) * (self.match_width +
                                                      self.margin_x)
            self._draw_round_header(draw, round_x, start_y, round_idx, 'lower')

            # Draw matches
            for match_idx in range(1, matches_in_round + 1):
                match_data = self._get_match_data('lower', round_idx,
                                                  match_idx)

                # Calculate match position
                match_spacing = self.margin_y
                match_y = start_y + self.round_header_height + (
                    match_idx - 1) * (self.match_height + match_spacing)

                self._draw_match(draw, round_x, match_y, match_data, round_idx,
                                 match_idx, matches_in_round)


def main():
    parser = argparse.ArgumentParser(
        description='Generate a tournament bracket image')
    parser.add_argument('--config',
                        type=str,
                        required=True,
                        help='Path to JSON configuration file')
    parser.add_argument('--output',
                        type=str,
                        default='bracket.png',
                        help='Output PNG file path')
    args = parser.parse_args()

    # Load configuration
    with open(args.config, 'r') as f:
        config = json.load(f)

    # Generate the bracket
    generator = TournamentBracketGenerator(config)
    generator.generate_bracket(args.output)


if __name__ == "__main__":
    main()
