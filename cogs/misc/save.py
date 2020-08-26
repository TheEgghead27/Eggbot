import simplejson as json

from eggbot import scores
from cogs.commands.economy import stonks, warehouse
from cogs.commands.roles import roles, joinRoles


def write(eggCount):
    if eggCount[1]:  # check if the eggCount is legitimate
        print(eggCount)
        print(str(eggCount[2]))
        date = eggCount[2]
        date = [date.year, date.month, date.day, date.hour]
        print(date)
        # uhhh ill just make plans here
        # scores: {'str(score)': date}

    else:
        print('bastard')

    with open("roles.json", "w") as j:
        dick = {"reactions": roles, "join": joinRoles}
        json.dump(dick, j, encoding="utf-8")
    with open("stonks.json", "w") as j:
        dick = {"moneys": stonks, "amazon": warehouse, "scores": scores}
        json.dump(dick, j, encoding="utf-8")
