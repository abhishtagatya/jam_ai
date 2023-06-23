import re


def search_mention(message: str):
    mentions = re.findall(
        r"(?<=^|(?<=[^a-zA-Z0-9-_\.]))@([A-Za-z]+[A-Za-z0-9_]+)",
        message
    )
    return mentions
