
import pycountry
from fuzzywuzzy import process


VCT_EMOJIS = {
    "100t": "<:100t:1337076165269131354>"
    , "c9": "<:c9:1337076155785674792>"
    , "eg": "<:eg:1337076141478903899>"
    , "fur": "<:fur:1337076131064447028>"
    , "kru": "<:kru:1337076116606816258>"
    , "lev": "<:lev:1337076110281805884>"
    , "loud": "<:loud:1337076103667515453>"
    , "mibr": "<:mibr:1337076095341563935>"
    , "nrg": "<:nrg:1337076086931980298>"
    , "sen": "<:sen:1337076073099427840>"
    , "g2": "<:g2:1337076065448886315>"
    , "2g": "<:2g:1337076058301661344>"

    , "ag": "<:ag:1339300389320917108>"
    , "blg": "<:blg:1339300405682634853>"
    , "edg": "<:edg:1339300424846540822>"
    , "fpx": "<:fpx:1339300492811046953>"
    , "jdg": "<:jdg:1339300506278957127>"
    , "nova": "<:nova:1339300516932489300>"
    , "te": "<:te:1339300527858516059>"
    , "tec": "<:tec:1339300546355658793>"
    , "tyl": "<:tyl:1339300561148837989>"
    , "wol": "<:wol:1339300580035792997>"
    , "drg": "<:drg:1339300476608319549>"
    , "xlg": "<:xlg:1339300595848445953>"

    , "bbl": "<:bbl:1337075651680669898>"
    , "fnc": "<:fnc:1337075641811468368>"
    , "fut": "<:fut:1337075629736329247>"
    , "gx": "<:gx:1337075522508951696>"
    , "kc": "<:kc:1337075514115887124>"
    , "navi": "<:navi:1337075489734529094>"
    , "th": "<:th:1337075481698238544>"
    , "mkoi": "<:mkoi:1337075472458322023>"
    , "tl": "<:tl:1337075462446383104>"
    , "vit": "<:vit:1337075454355705906>"
    , "m8": "<:m8:1337075444444299356>"
    , "apk": "<:apk:1337075436693487656>"

    , "dfm": "<:dfm:1337075049198522481>"
    , "drx": "<:drx:1337075036892430511>"
    , "gen": "<:gen:1337075022363234395>"
    , "ge": "<:ge:1337075011864887326>"
    , "prx": "<:prx:1337075004382122084>"
    , "rrq": "<:rrq:1337074997553791118>"
    , "t1": "<:t1:1337074991501672619>"
    , "tln": "<:tln:1337074985470132315>"
    , "ts": "<:ts:1337074976674680843>"
    , "zeta": "<:zeta:1337074968110043239>"
    , "ns": "<:ns:1337074958840369233>"
    , "bme": "<:bme:1337074947583119414>"

    , "vct_logo": "<:vct_logo:1333491883007021086>"
    , "vct_champs": "<:vct_champs:1332393272378921000>"
    , "vct_americas": "<:vct_americas:1332393264526921808>"
    , "vct_china": "<:vct_china:1332393256004354068>"
    , "vct_pacific": "<:vct_pacific:1332393245489238057>"
    , "vct_emea": "<:vct_emea:1332393237507346462>"
    , "vct_masters": "<:vct_masters:1332393227101143083>"

    , "regular_sparkle_1": "<:sparkle_1:1342206404760567989>"
    , "regular_sparkle_2": "<:sparkle_2:1342206411974901800>"
    , "regular_sparkle_3": "<:sparkle_3:1342206418232545380>"
    , "regular_sparkle_4": "<:sparkle_4:1342206425388027954>"
    , "regular_sparkle_5": "<:sparkle_5:1342206434007318629>"
    , "regular_sparkle_6": "<:sparkle_6:1342206445533401279>"
    , "masters_sparkle_1": "<:masters_sparkle_1:1342206382698397787>"
    , "masters_sparkle_2": "<:masters_sparkle_2:1342206390403600405>"
    , "masters_sparkle_3": "<:masters_sparkle_3:1342206396808171562>"
    , "champs_sparkle_1": "<a:champs_sparkle_1:1342202573498880115>"
    , "champs_sparkle_2": "<a:champs_sparkle_2:1342202584936747111>"
    , "champs_sparkle_3": "<a:champs_sparkle_3_6:1342202595640610997>"

    , "who": "<a:who:1349559640836407458>"
    , "miku": "<a:miku_leek:1342190731313287238>"
}
ALIASES = {
    'Team Vitality': 'vit'
    , 'G2 Esports': 'g2'
    , 'Sentinels': 'sen'
    , 'Trace Esports': 'te'
    , 'EDward Gaming': 'edg'
    , 'T1': 't1'
    , 'DRX': 'drx'
    , 'Team Liquid': 'tl'
    , 'All Gamers': 'ag'
    , 'Bilibili Gaming': 'blg'
    , 'FunPlus Phoenix': 'fpx'
    , 'JDG Esports': 'jdg'
    , 'Nova Esports': 'nova'
    , 'Titan Esports Club': 'tec'
    , 'TYLOO': 'tyl'
    , 'Wolves Esports': 'wol'
    , 'Dragon Ranger Gaming': 'drg'
    , 'Xi Lai Gaming': 'xlg'
    , '100 Thieves': '100t'
    , 'Cloud9': 'c9'
    , 'Evil Geniuses': 'eg'
    , 'FURIA': 'fur'
    , 'KRÜ Esports': 'kru'
    , 'LEVIATÁN': 'lev'
    , 'LOUD': 'loud'
    , 'MIBR': 'mibr'
    , 'NRG Esports': 'nrg'
    , '2Game Esports': '2g'
    , 'DetonatioN FocusMe': 'dfm'
    , 'Gen.G': 'gen'
    , 'Global Esports': 'ge'
    , 'Paper Rex': 'prx'
    , 'Rex Regum Qeon': 'rrq'
    , 'TALON': 'tln'
    , 'Team Secret': 'ts'
    , 'ZETA DIVISION': 'zeta'
    , 'Nongshim RedForce': 'ns'
    , 'BOOM Esports': 'bme'
    , 'BBL Esports': 'bbl'
    , 'FNATIC': 'fnc'
    , 'FUT Esports': 'fut'
    , 'GIANTX': 'gx'
    , 'Karmine Corp': 'kc'
    , 'Natus Vincere': 'navi'
    , 'Team Heretics': 'th'
    , 'KOI': 'mkoi'
    , 'Gentle Mates': 'm8'
    , 'Apeks': 'apk'
}


def get_vct_emoji(input_name):
    # First try to look up a direct match, if not try aliases
    res_key = input_name if input_name in VCT_EMOJIS else ALIASES.get(input_name)
    if res_key:
        return VCT_EMOJIS.get(res_key)

    # If both fail, try fuzzy matching on aliases
    best_match, score = process.extractOne(input_name, ALIASES.keys())
    if score >= 80:
        matched_emoji = VCT_EMOJIS.get(ALIASES.get(best_match))
        print(f"/// END")
        return matched_emoji

    # and fuzzy on the whole VCT_EMOJIS list
    best_match, score = process.extractOne(input_name, VCT_EMOJIS.keys())
    if score >= 80:
        matched_emoji = VCT_EMOJIS.get(best_match)
        return matched_emoji

    return "❓"

def local_to_emoji(local: str) -> str:
    try:
        country = pycountry.countries.search_fuzzy(local)[0].alpha_2
        return f":flag_{country.lower()}:"
    except (LookupError, AttributeError) as e:
        print(f"Something went wrong when converting local to emoji -> {e}")
        return None