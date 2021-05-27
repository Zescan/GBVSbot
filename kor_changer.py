def nor_cgr (command):
    if command == '근약':
        command = "c.L"
    elif command == '원약':
        command = "f.L"
    elif command == '근중':
        command = "c.M"
    elif command == '원중':
        command = "f.M"
    elif command == '근강':
        command = "c.H"
    elif command == '원강':
        command = "f.H"
    elif command == '앉약':
        command = "2L"
    elif command == '앉중':
        command = "2M"
    elif command == '앉강':
        command = "2H"
    elif command == '앉특':
        command = "2U"
    elif command == '점약':
        command = "j.L"
    elif command == '점중':
        command = "j.M"
    elif command == '점강':
        command = "j.H"
    elif command == '점특':
        command = "j.U"
    elif command == '5특':
        command = "5U"
    elif command == '잡기':
        command = "TR"
    elif command == '공중잡기':
        command = "j.TR"
    elif command == '오버헤드':
        command = "MH"
    elif command == '오의':
        command = "236236H"
    elif command == '해방오의':
        command = "236236U"
    return command

def com_cgr (command):
    if '약' in command:
        command = command.replace('약', 'L')
    elif '중' in command:
        command = command.replace('중', 'M')
    elif '강' in command:
        command = command.replace('강', 'H')
    elif '특' in command:
        command = command.replace('특', 'U')
    elif '평' in command:
        command = command.replace('평', 'X')
    return command

def sknm_cgr (command):
    cmd = ""
    surfix = ""
    btns = ["L", "M", "H", "U", "X"]
    jumps = ["공중", "점프", "공", "점"]
    # "장풍"은 236 외의 커맨드에 대한 경우, 한 캐릭이 다양한 종류의 장풍을 가진 경우가 존재하므로 제외합니다.
    # FIXME 기라성(하단)에 대한 약칭 표기를 찾아야 합니다.
    # FIXME 블랙플라이(붑 장풍)의 약칭 표기를 찾아야 합니다.
    # FIXME 마이티라이드(카타 장풍)의 약칭 표기를 찾아야 합니다. 
    cmd236 = ["파동"
              , "레긴"
              , "찰나", "경화"
              , "보겐"
              , "엘쓰", "친구"
              , "기라"
              , "게티"
              , "플라"
              , "너클"
              , "레긴", "리시"
              , "나찰"
              , "야천", "야텐"
              , "인피"
              , "와이", "이모", "스러", "브레", "스위"
              , "마이"
              , "메헨", "함정"
              , "헤드", "박"
              , "안츤"
              , "게슈"
              ]
    if not "MH" in command:
        for j in jumps:
            if j in command:
                cmd += "j."
                break 
        for btn in btns:
            if btn in command:
                surfix = btn
                break
        for c in cmd236:
            if c in command:
                cmd += "236"
                break
        if cmd != "" and surfix != "":
            command = cmd + surfix
    return command
    
