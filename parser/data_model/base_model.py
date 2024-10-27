from abc import ABC, abstractmethod
import time


class Base_Model(ABC):

    def __init__(
            self, full_name: str, text_body: str, author_name: str | None, votes: int,
            reply_name: str | None, parent_submission_name: str | None,
            submission_flair: str, timestamp: int, controversiality: bool | None
        ) -> None:

        self.full_name = full_name
        self.text_body = text_body
        self.author_name = author_name
        self.votes = votes
        self.responds_to = reply_name
        self.parent_submission_name = parent_submission_name
        self.created_timestamp = timestamp
        self.submission_flair = submission_flair
        self.parsed_timestamp = int(time.time())
        self.controversiality = bool(controversiality)
        
    @abstractmethod
    def export(self) -> object:
        """Exports object to default format."""
        pass
