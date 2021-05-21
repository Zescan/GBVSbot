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
    return command

# a='236약214중'
# print(a)
# for i in a:
#     if '약' in a:
#         a = a.replace('약', 'L')
#     elif '중' in a:
#         a = a.replace('중', 'M')
# print(a)

# command = '236약214중'
# stlen = len(command)
# print(stlen)
# for stlen in command:
#     if '약' in command:
#         command = command.replace('약' , 'L')
#     elif '중' in command:
#         command = command.replace('중' , 'M')
# print(command)