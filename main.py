import argparse
import csv
from parser.parser import Extended_Reddit_RO
from parser.data_model import CSV_Model


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("-o", "--output", help="Output file name")
    parser.add_argument("-m", "--mode", help="Parsing mode: 'fl' to include flairs, 'ex' to exclude 'no' to use keywords only", required=True)
    parser.add_argument("-cid", "--client_id", help="Client id of reddit app", required=True)
    parser.add_argument("-cs", "--client_secret", help="Client secret of reddit app", required=True)
    parser.add_argument("-u", "--user_agent", help="User agent of reddit app", required=True)
    parser.add_argument("-s", "--subreddit", help="Subreddit display name to parse", required=True)
    parser.add_argument("-f", "--flairs", nargs='+', help="Space separated flair names")
    parser.add_argument("-k", "--keywords", nargs='+', help="Keywords used as search terms")
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

        nodes = None
        match args.mode:

            case "fl":
                nodes = parser.parse_subreddit_by_flair(
                    args.subreddit,
                    args.flairs,
                    CSV_Model,
                    args.keywords,
                    int(args.limit)
                )

            case "ex":
                nodes = parser.parse_subreddit_ex_flair(
                    args.subreddit,
                    args.flairs,
                    CSV_Model,
                    args.keywords,
                    int(args.limit)
                )


            case "no":
                nodes = parser.parse_subreddit_no_flair(
                    args.subreddit,
                    args.flairs,
                    CSV_Model,
                    args.keywords,
                    int(args.limit)
                )

            case _:
                nodes = parser.parse_subreddit_no_flair(
                    args.subreddit,
                    args.flairs,
                    CSV_Model,
                    args.keywords,
                    int(args.limit)
                )

        writer.writerow(CSV_Model.TUPLE_HEADERS)
        for node in nodes:
            writer.writerow(node.export())

if __name__ == "__main__":
    main()    
