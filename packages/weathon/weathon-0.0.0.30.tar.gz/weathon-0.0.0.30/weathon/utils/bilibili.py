import json

def generate_subtitles(json_data) ->str:
    contents = json_data["body"]

    subtitles = []
    for subtitle in contents:
        subtitles.append(subtitle["content"])
    return ",".join(subtitles)