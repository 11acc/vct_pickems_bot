
import pycountry


class EventYears:
    VALID_YEARS = [
        2025
    ]

    @classmethod
    def validate(self, year: int) -> int:
        if year in self.VALID_YEARS:
            return True
        else:
            return False


class EventTypes:
    VALID_EVENTS = {
        "KICKOFF": "KICKOFF"
        , "SPLIT 1": "SPLIT 1"
        , "SPLIT 2": "SPLIT 2"
        , "MASTERS": "MASTERS"
        , "CHAMPIONS": "CHAMPIONS"
        , "CHAMPS": "CHAMPIONS"
    }
    
    @classmethod
    def validate(self, region: str) -> str:
        region_upper = region.upper()
        if region_upper in self.VALID_EVENTS:
            return True
        else:
            return False

REGION_EMOJIS = {
    "EMEA": "<:vct_emea:1332393237507346462>"
    , "AMERICAS": "<:vct_amer:1332393264526921808>"
    , "PACIFIC": "<:vct_pacf:1332393245489238057>"
    , "CHINA": "<:vct_chna:1332393256004354068>"
    , "MASTERS": "<:vct_masters:1332393227101143083>"
    , "CHAMPIONS": "<:vct_champs:1332393272378921000>"
    , "LOGO": "<:vct_logo:1333491883007021086>"
}


def local_to_emoji(local: str) -> str:
    country = pycountry.countries.search_fuzzy(local)[0].alpha_2
    return f":flag_{country.lower()}:"

def get_vct_emoji(region: str) -> str:
    return REGION_EMOJIS.get(region.upper(), "❓")