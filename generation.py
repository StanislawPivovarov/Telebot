import json

import rstr

# with open('my_intent_catcher_data/train.json', encoding="utf-8") as f:
with open('supporting_train.json', encoding="utf-8") as f:
    templates = json.load(f)

for section, commands in templates.items():
    print(section)
    commands = '\n'.join(commands)
    commands = commands.split('\n')

    i = 0
    while i < len(commands):
        if commands[i] == '':
            i += 1
            continue
        a = []
        reg = commands[i]
        j = 0
        while j < 10000:
            s = rstr.xeger(reg)
            if a.count(s) == 0:
                a.append(s)
            j += 1
        j = 0
        while j < len(a):
            print("\"" + a[j] + "\",")
            j += 1
        i += 1
    print('\n\n')