import argparse
import csv
from parser.parser import Extended_Reddit_RO
from parser.data_model import CSV_Model


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("-o", "--output", help="Output file name")
    parser.add_argument("-cid", "--client_id", help="Client id of reddit app", required=True)
    parser.add_argument("-cs", "--client_secret", help="Client secret of reddit app", required=True)
    parser.add_argument("-u", "--user_agent", help="User agent of reddit app", required=True)
    parser.add_argument("-s", "--subreddit", help="Subreddit display name to parse", required=True)
    parser.add_argument("-f", "--flairs", nargs='+', help="Space separated flair names")
    parser.add_argument("-l", "--limit", help="Parse limit on number of submissions", default=10000)

    args = parser.parse_args()

    filename = args.output if args.output else "output.csv"

    with open(filename, "w", newline="", encoding="UTF-8") as file:
        writer = csv.writer(file)

        parser = Extended_Reddit_RO(
            args.client_id,
            args.client_secret,
            args.user_agent
        )
        nodes = parser.parse_subreddit(
            args.subreddit,
            args.flairs,
            CSV_Model,
            int(args.limit)
        )

        writer.writerow(CSV_Model.TUPLE_HEADERS)
        for node in nodes:
            writer.writerow(node.export())

if __name__ == "__main__":
    main()    
