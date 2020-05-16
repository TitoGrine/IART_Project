import re
from tweet import Tweet


def process_valence(valence):
    if valence < 0:
        return 0
    elif valence > 0:
        return 1
    else:
        return 2


def process_dataset(url):
    file = open(url, 'r')
    dataset = file.read()
    splitted_data = re.split("\n|\t", dataset)
    prepared_data = [splitted_data[i: i + 4] for i in range(0, len(splitted_data), 4)]
    prepared_data.pop(0)
    prepared_data.pop()

    return list(map(lambda x: Tweet(x[0], x[1], x[2], process_valence(int(x[3].split(":")[0])), x[3].split(":")[1]),
                    prepared_data))


def get_dataset(data):
    x = []
    y = []

    for tweet in data:
        x.append(tweet.tweet)
        y.append(tweet.intensity)
    return x, y
