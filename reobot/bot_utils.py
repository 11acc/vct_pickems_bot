
import pycountry
from fuzzywuzzy import process


VCT_EMOJIS = {
    "100t": "<:100t:1337076165209131354>"
    , "c9": "<:c9:1337076157856749792>"
    , "eg": "<:eg:1337076144789038999>"
    , "fur": "<:fur:1337076130044470288>"
    , "kru": "<:kru:1337076116068162588>"
    , "lev": "<:lev:1337076108281805894>"
    , "loud": "<:loud:1337076103675154538>"
    , "mibr": "<:mibr:1337076095341569398>"
    , "nrg": "<:nrg:1337076086919802988>"
    , "sen": "<:sen:1337076073099427840>"
    , "g2": "<:g2:1337076065448886315>"
    , "2g": "<:2g:1337076058301661344>"

    , "xlg": "<:xlg:1339300595844845953>"
    , "wol": "<:wol:1339300580035792997>"
    , "tyl": "<:tyl:1339300561148837989>"
    , "tec": "<:tec:1339300546355658793>"
    , "te": "<:te:1339300527858516059>"
    , "nova": "<:nova:1339300516932489300>"
    , "jdg": "<:jdg:1339300506278957127>"
    , "fpx": "<:fpx:1339300492811046953>"
    , "drg": "<:drg:1339300476608319549>"
    , "edg": "<:edg:1339300424846540822>"
    , "blg": "<:blg:1339300405682634853>"
    , "ag": "<:ag:1339300389320971708>"

    , "bbl": "<:bbl:1337075651680689898>"
    , "fnc": "<:fnc:1337075648114863888>"
    , "fut": "<:fut:1337075627036329247>"
    , "gx": "<:gx:1337075525208951696>"
    , "kc": "<:kc:1337075514158817284>"
    , "navi": "<:navi:1337075489734520994>"
    , "th": "<:th:1337075481692835446>"
    , "koi": "<:koi:1337075472458322023>"
    , "tl": "<:tl:1337075462444383104>"
    , "vit": "<:vit:1337075454355705906>"
    , "m8": "<:m8:1337075444444299356>"
    , "apk": "<:apk:1337075436097487656>"

    , "dfm": "<:dfm:1337075049198522481>"
    , "drx": "<:drx:1337075036892430511>"
    , "gen": "<:gen:1337075022363234395>"
    , "ge": "<:ge:1337075011864887326>"
    , "prx": "<:prx:1337075004382122084>"
    , "rrq": "<:rrq:1337074997553791118>"
    , "t1": "<:t1:1337074991501572619>"
    , "talon": "<:talon:1337074985470132315>"
    , "secret": "<:secret:1337074976674680843>"
    , "zeta": "<:zeta:1337074968110043239>"
    , "noodles": "<:noodles:1337074958840369233>"
    , "boom": "<:boom:1337074947581194144>"

    , "vct_logo": "<:vct_logo:1333491883007021086>"
    , "vct_champs": "<:vct_champs:1332393227387921000>"
    , "vct_americas": "<:vct_americas:1332393264526921808>"
    , "vct_china": "<:vct_china:1332393256004354068>"
    , "vct_pacific": "<:vct_pacific:1332393245489238057>"
    , "vct_emea": "<:vct_emea:1332393237507346462>"
    , "vct_masters": "<:vct_masters:1332393227101143083>"
}

def get_vct_emoji(input_name):
    best_match, score = process.extractOne(input_name, VCT_EMOJIS.keys())
    if score >= 80:
        matched_emoji = VCT_EMOJIS[best_match]
        return matched_emoji
    return "❓"

def local_to_emoji(local: str) -> str:
    try:
        country = pycountry.countries.search_fuzzy(local)[0].alpha_2
        return f":flag_{country.lower()}:"
    except (LookupError, AttributeError) as e:
        print(f"Something went wrong when converting local to emoji -> {e}")
        return None