from collections.abc import Generator
from praw import Reddit
from praw.models import Comment
from .data_model import CSV_Model, Base_Model


class Extended_Reddit_RO(Reddit):
    """Class that encapsulates logic of structural retrieval of public
     objects through Reddit API"""

    def __init__(self, client_id: str, client_secret: str, user_agent: str,
                 username: str | None = None, password: str | None = None,
                 ratelimit_seconds: int = 3600
        ):

        """Parameters:
            client_id - client id of registered Reddit app;\n
            client_secret - client secret of registered Reddit app;\n
            user_agent - unique user agent;\n
            username - provide to access private content of user;\n
            password - provide to access private content of user;\n
            ratelimit_seconds - maximum number of seconds to wait out following Reddit's "Too many requests" response;\n
            """

        if username and password:
            super().__init__(
                client_id = client_id,
                client_secret = client_secret,
                user_agent = user_agent,
                username = username,
                password = password,
                ratelimit_seconds = ratelimit_seconds
            )
        else:
            super().__init__(
                client_id = client_id,
                client_secret = client_secret,
                user_agent = user_agent,
                ratelimit_seconds = ratelimit_seconds
            )


    def parse_subreddit_no_flair(
            self,
            subreddit_display_name: str,
            flairs: list[str],
            model: type[Base_Model] = CSV_Model,
            search_terms: list[str] = None,
            parse_limit: int = 10000,
            replace_limit: int = None
    ) -> Generator[Base_Model]:
        
        return self._parse_subreddit(
            subreddit_display_name,
            search_terms,
            model,
            parse_limit,
            replace_limit
        )


    def parse_subreddit_ex_flair(
            self,
            subreddit_display_name: str,
            flairs: list[str],
            model: type[Base_Model] = CSV_Model,
            search_terms: list[str] = None,
            parse_limit: int = 10000,
            replace_limit: int = None
    ) -> Generator[Base_Model]:
        
        prefix_flairs = map(
            lambda x: "flair:" + x,
            flairs
        )
        flairs_set = " OR ".join(prefix_flairs)
        flairs_negated = f"NOT ({flairs_set})"

        query_list = []
        for term in search_terms:
            combined_query = f"{flairs_negated} AND {term}"
            query_list.append(combined_query)

        return self._parse_subreddit(
            subreddit_display_name,
            query_list,
            model,
            parse_limit,
            replace_limit
        )


    def parse_subreddit_by_flair(
            self,
            subreddit_display_name: str,
            flairs: list[str],
            model: type[Base_Model] = CSV_Model,
            search_terms: list[str] = None,
            parse_limit: int = 10000,
            replace_limit: int = None
        ) -> Generator[Base_Model]:

        prefix_flairs = map(
            lambda x: "flair:" + x,
            flairs
        )
        search_terms_query = " OR ".join(search_terms)

        query_list = []
        for flair in prefix_flairs:
            combined_query = f"{flair} AND ({search_terms_query})"
            query_list.append(combined_query)

        return self._parse_subreddit(
            subreddit_display_name,
            query_list,
            model,
            parse_limit,
            replace_limit
        )


    def _parse_subreddit(
            self,
            subreddit_display_name: str,
            queries: list[str],
            model: type[Base_Model] = CSV_Model,
            parse_limit: int = 10000,
            replace_limit: int = None
        ) -> Generator[Base_Model]:

        if not subreddit_display_name:
            raise AttributeError("must provide subreddit name")
        
        subreddit = self.subreddit(subreddit_display_name)

        for query in queries:
            submissions = subreddit.search(query, limit=parse_limit)

            for submission in submissions:

                submission_node = model(
                    submission.fullname,
                    submission.title,
                    submission.author_fullname,
                    submission.score,
                    None,
                    submission.fullname,
                    submission.link_flair_text,
                    submission.created,
                    None
                )

                yield submission_node

                submission.comments.replace_more(limit=replace_limit)
                queue = Extended_Reddit_RO._pack_parent(
                    submission.comments[:], 
                    submission.fullname
                )

                while queue:
                    comment, parent = queue.pop(0)

                    if not ("author_fullname" in vars(comment)):
                        comment.author_fullname = None

                    if comment.body == "[deleted]":
                        comment.body = None

                    comment_node = model(
                        comment.fullname,
                        comment.body,
                        comment.author_fullname,
                        comment.score,
                        parent,
                        submission.fullname,
                        submission.link_flair_text,
                        submission.created,
                        comment.controversiality
                    )

                    yield comment_node

                    queue.extend(
                        Extended_Reddit_RO._pack_parent(
                            comment.replies, 
                            comment.fullname
                        )
                    )


    @staticmethod
    def _pack_parent(comments: iter, parent: str) -> list[tuple[Comment, str]]:

        return list(map(
            lambda x: (x, parent),
            comments
        ))