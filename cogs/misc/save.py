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

        scores[str(eggCount[0])] = date
        scoresSorted = []
        for i in scores:  # wait can i sort a dict? no
            scoresSorted.append(int(i))
            print(scores[i] == date)
        scoresSorted.sort()
        if len(scores) == 6:
            print(scores[str(scoresSorted[0])])
            del scores[str(scoresSorted[0])]
        elif len(scores) != 5:
            print('Dude WTF')

    with open("roles.json", "w") as j:
        dick = {"reactions": roles, "join": joinRoles}
        json.dump(dick, j, encoding="utf-8")
    with open("stonks.json", "w") as j:
        dick = {"moneys": stonks, "amazon": warehouse, "scores": scores}
        json.dump(dick, j, encoding="utf-8")
