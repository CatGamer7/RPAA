from .base_model import Base_Model


class CSV_Model(Base_Model):

    TUPLE_HEADERS = ("full_name", "text_body", "author_name", "votes",
                     "responds_to", "parent_submission_name", "submission flair",
                     "created_timestamp", "parsed_timestamp", "controversiality"
    )
    
    TUPLE_HEADER_DESCRIPTIONS = {
        "full_name": "Node reddit name (id)",
        "text_body": "Node content",
        "author_name": "Node author's reddit name (author id)",
        "votes" : "Total voting rating of Node",
        "responds_to": "Node, that is being replied",
        "parent_submission_name": "submission of a comment (blank for submisson node)",
        "submission flair": "Visible text of submission flair",
        "created_timestamp": "UNIX timestamp of reddit-reported creation time",
        "parsed_timestamp": "UNIX timestamp of time of parsing",
        "controversiality": "Reddit-reported controversiality value (either 0 or 1) represented as bool"
    }

    def export_tuple(self) -> tuple:
        return (self.full_name, self.text_body, self.author_name, self.votes,
                self.responds_to, self.parent_submission_name, self.submission_flair,
                self.created_timestamp, self.parsed_timestamp, self.controversiality)
    
    def export(self) -> object:
        return self.export_tuple()