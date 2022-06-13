from datetime import datetime
import pydantic
from pydantic import BaseModel
from typing import Any

POST_PREFIX = "#POST#"
OWNER_PREFIX = "#OWNER#"


class Blog_Item(BaseModel):
    PK: str = ""
    SK: str = ""
    post_id: str
    publish_date: str = ""
    owner_id: str
    title: str = ""
    description: str = ""

    def __init__(self, **data: Any) -> None:
        super().__init__(**data)
        if self.publish_date == "":
            self.publish_date = str(datetime.now().strftime("%Y-%m-%d"))
            # print(publish_date)
        self.PK = f"{POST_PREFIX}{self.post_id}"
        self.SK = f"{OWNER_PREFIX}{self.owner_id}"


def display():
    test_BlogItem = Blog_Item(
        post_id="1235",
        publish_date="",
        owner_id="123",
        title="testTitle",
        description="This is a test blog",
    )

    print(f"test_Model: {test_BlogItem}")


if __name__ == "__main__":
    display()
