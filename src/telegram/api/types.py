from ..models import User


class Chat:
    def __init__(self, id: int):
        self.id = id

    def __repr__(self):
        return f"Chat({self.id})"


class Message:
    def __init__(
        self,
        id: int,
        date: int,
        chat: Chat,
        from_user: User,
        text: str,
    ):
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

        if "text" in update["message"]:
            text = update["message"]["text"]
        else:
            text = None

        if "contact" in update["message"]:
            if "phone_number" in update["message"]["contact"]:
                phone_number = update["message"]["contact"]["phone_number"]
            else:
                phone_number = None
        else:
            phone_number = None

        user, _ = User.objects.get_or_create(telegram_id=user_id)
        if first_name and user.first_name != first_name:
            user.first_name = first_name
        if last_name and user.last_name != last_name:
            user.last_name = last_name
        if username and user.username != username:
            user.username = username
        if phone_number and user.phone_number != phone_number:
            user.phone_number = phone_number
        user.save()

        chat = Chat(id=chat_id)

        return cls(
            id=id,
            date=date,
            chat=chat,
            from_user=user,
            text=text,
        )
