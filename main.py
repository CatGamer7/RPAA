import csv
from parser.parser import Extended_Reddit_RO
from parser.data_model import CSV_Model


if __name__ == "__main__":
    
    with open("name.csv", "w", newline="", encoding="UTF-8") as file:
        writer = csv.writer(file)

        parser = Extended_Reddit_RO(
            "abcFZ-aLBO94KN428uLX7A",
            "gesLnro3-NaqL_blXaHowIHRpfz3Hw",
            "english comment scraper (by u/Holiday_Scarcity_911)"
        )
        nodes = parser.parse_subreddit(
            "srilanka",
            ["Politics", "News", "Discussion", "Beaurocracy", "Rumour"],
            CSV_Model
        )

        writer.writerow(CSV_Model.TUPLE_HEADERS)
        for node in nodes:
            writer.writerow(node.export())
