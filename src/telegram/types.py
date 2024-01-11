class User:
    def __init__(
        self,
        id: int,
        usename: str = None,
        first_name: str = None,
        last_name: str = None,
    ):
        self.id = id
        self.username = usename
        self.first_name = first_name
        self.last_name = last_name

    def __repr__(self):
        return f"User({self.id}, {self.usename}, {self.first_name}, {self.last_name})"


class Chat:
    def __init__(self, id: int):
        self.id = id

    def __repr__(self):
        return f"Chat({self.id})"


class Message:
    def __init__(self, id: int, date: int, chat: Chat, from_user: User, text: str):
        self.id = id
        self.date = date
        self.chat = chat
        self.from_user = from_user
        self.text = text

    def __repr__(self):
        return f"Message({self.id}, {self.date}, {self.chat}, {self.from_user}, {self.text})"

    @classmethod
    def from_json(cls, update):
        id = update["message"]["message_id"]
        date = update["message"]["date"]
        chat_id = update["message"]["chat"]["id"]
        user_id = update["message"]["from"]["id"]
        username = update["message"]["from"]["username"]

        if "first_name" in update["message"]["from"]:
            first_name = update["message"]["from"]["first_name"]
        else:
            first_name = None

        if "last_name" in update["message"]["from"]:
            last_name = update["message"]["from"]["last_name"]
        else:
            last_name = None

        text = update["message"]["text"]

        user = User(
            id=user_id, usename=username, first_name=first_name, last_name=last_name
        )
        chat = Chat(id=chat_id)

        return cls(id=id, date=date, chat=chat, from_user=user, text=text)
