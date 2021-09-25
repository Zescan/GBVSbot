def ncgr (charname):
    charname = charname.strip()
    if charname.startswith('그'):
        charname = "gran"
    elif charname.startswith('퍼'):
        charname = "percival"
    elif charname.startswith('샤') or charname.startswith('감'):
        charname = "charlotta"
    elif charname.startswith('파'):
        charname = "ladiva"
    elif charname.startswith('카'):
        charname = "katalina"
    elif charname.startswith('페'):
        charname = "ferry"
    elif charname.startswith('로'):
        charname = "lowain"
    elif charname.startswith('랜') or charname.startswith('란'):
        charname = "lancelot"
    elif charname.startswith('제'):
        charname = "zeta"
    elif charname.startswith('메'):
        charname = "metera"
    elif charname.startswith('바'):
        charname = "vaseraga"
    elif charname.endswith('붑'):
        charname = "beelzebub"
    elif charname.startswith('벨'):
        charname = "belial"
    elif charname.startswith('지'):
        charname = "djeeta"
    elif charname.startswith('우'):
        charname = "anre"
    elif charname.startswith('나'):
        charname = "narmaya"
    elif charname.startswith('조'):
        charname = "zooey"
    elif charname.startswith('소'):
        charname = "soriz"
    elif charname.startswith('칼'):
        charname = "cagliostro"
    elif charname == '유엘':
        charname = "yuel"
    elif charname.startswith('유스'):
        charname = "Eustace"
    return charname

def rncgr (charname):
    if charname == 'gran':
        charname = "그랑"
    elif charname == 'percival':
        charname = "퍼시벌"
    elif charname == 'charlotta':
        charname = "샤를로테"
    elif charname == 'ladiva':
        charname = "파스티바"
    elif charname == 'katalina':
        charname = "카타리나"
    elif charname == 'ferry':
        charname = "페리"
    elif charname == 'lowain':
        charname = "로아인"
    elif charname == 'lancelot':
        charname = "랜슬롯"
    elif charname == 'zeta':
        charname = "제타"
    elif charname == 'metera':
        charname = "메테라"
    elif charname == 'vaseraga':
        charname = "바자라가"
    elif charname == 'beelzebub':
        charname = "벨제붑"
    elif charname == 'belial':
        charname = "벨리알"
    elif charname == 'djeeta':
        charname = "지타"
    elif charname == 'anre':
        charname = "우노"
    elif charname == 'narmaya':
        charname = "나루메아"
    elif charname == 'zooey':
        charname = "조이"
    elif charname == 'soriz':
        charname = "소리즈"
    elif charname == 'cagliostro':
        charname = "칼리오스트로"
    elif charname == 'yuel':
        charname = "유엘"
    elif charname == 'Eustace':
        charname = "유스테스"
    return charname
