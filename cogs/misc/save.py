import simplejson as json
from cogs.commands.economy import stonks, warehouse
from cogs.commands.roles import roles, joinRoles


def write(eggCount):
    if eggCount[1]:
        print(eggCount)
        print(str(eggCount[2]))
        print(str(eggCount[2]) == '2020-08-26')  # ok this is the right str format
        # uhhh ill just make plans here
        # scores: {'str(score)': date}
        # date formatting (because this is bad ux)
        # split str by "-"
        # pop split()[0] to the end
        # join args with /
        # fuck euros
    else:
        print('bastard')
    with open("roles.json", "w") as j:
        dick = {"reactions": roles, "join": joinRoles}
        json.dump(dick, j, encoding="utf-8")
    with open("stonks.json", "w") as j:
        dick = {"moneys": stonks, "amazon": warehouse}
        json.dump(dick, j, encoding="utf-8")
