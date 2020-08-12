import simplejson as json
from cogs.commands.economy import stonks, warehouse
# TODO Update this for roles when that is cogged
from eggbot import roles, joinRoles


def write():
    with open("roles.json", "w") as j:
        dick = {"reactions": roles, "join": joinRoles}
        json.dump(dick, j, encoding="utf-8")
    with open("stonks.json", "w") as j:
        dick = {"moneys": stonks, "amazon": warehouse}
        json.dump(dick, j, encoding="utf-8")
