import simplejson as json


def write(bot):
    with open("roles.json", "w") as j:
        dick = {"reactions": bot.roles, "join": bot.joinRoles}
        json.dump(dick, j, encoding="utf-8")
    with open("stonks.json", "w") as j:
        print(bot.stonks['users']["474328006588891157"])
        dick = {"moneys": bot.stonks, "amazon": bot.warehouse, "scores": sortScores(bot)}
        json.dump(dick, j, encoding="utf-8")


def sortScores(bot):
    current = bot.eggCount
    data = bot.scores
    Scores = data
    if current[1]:  # check if the eggCount is legitimate
        date = current[2]
        hour = date.hour
        if hour + 5 < 24:
            hour += 5
        date = [date.year, date.month, date.day, hour]

        marked = []
        scoresSorted = []
        for i in data:  # wait can i sort a dict? no
            if data[i][:3] == date[:3]:  # check if the data is from today
                marked.append(i)  # avoid iteration during while error
            scoresSorted.append(int(i))

        for i in marked:
            if int(i) > bot.eggCount[0]:
                current[0] = int(i)
                bot.eggCount = current
            del data[i]
        data[current[0]] = date

        scoresSorted.sort()

        Scores = purgeDuplicates(jsonSanitize(data))

        if len(Scores) > 5:
            del Scores[str(scoresSorted[0])]
        elif len(Scores) < 5:
            p = -1
            while len(Scores) < 5:
                Scores[p] = [1980, 1, 1, 0]
                p -= 1
    return Scores


def purgeDuplicates(dic: dict):
    registered = []
    for i in dic:
        if i in registered:
            del dic[i]
        else:
            registered.append(i)
    return dic


def jsonSanitize(dic: dict):
    queued = []
    for i in dic:
        if type(i) != str:
            queued.append(i)
    for i in queued:
        dic[str(i)] = dic[i]
        del dic[i]
    return dic
