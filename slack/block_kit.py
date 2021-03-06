from django.conf import settings
from slackclient import SlackClient


slack_token = settings.SLACK_TOKEN
slack_client = SlackClient(slack_token)


class Message:
    def __init__(self):
        self.blocks = []

    def add_block(self, block):
        self.blocks.append(block)

    def serialize(self):
        serialized = []
        for block in self.blocks:
            serialized.append(block.serialize())
        return serialized

    def send(self, channel, ts=None):
        """
        Build and send the message to the required channel
        """
        api_call = "chat.postMessage" if not ts else "chat.update"

        response = slack_client.api_call(
            api_call,
            channel=channel,
            ts=ts,
            blocks=self.serialize(),
        )
        return response


class Block:
    def __init__(self, block_id=None):
        self.block_id = block_id

    def serialize(self):
        raise NotImplementedError


class Section(Block):
    def __init__(self, block_id=None, text=None, fields=None):
        super().__init__(block_id=block_id)
        self.text = text
        self.fields = fields

    def add_field(self, field):
        if not self.fields:
            self.fields = []
        self.fields.append(field)

    def serialize(self):
        block = {
            "type": "section",
        }

        if self.block_id:
            block['block_id'] = self.block_id

        if self.text:
            block['text'] = self.text.serialize()
        elif self.fields:
            block['fields'] = [t.serialize() for t in self.fields]
        else:
            raise ValueError

        return block


class Actions(Block):
    def __init__(self, block_id=None, elements=None):
        super().__init__(block_id=block_id)
        self.elements = elements

    def add_element(self, element):
        if not self.elements:
            self.elements = []

        self.elements.append(element)

    def serialize(self):
        block = {
            "type": "actions",
            "block_id": self.block_id
        }

        block['elements'] = [e.serialize() for e in self.elements]

        return block


class Divider(Block):
    def serialize(self):
        return {
            "type": "divider"
        }


class Button:
    def __init__(self, text, action_id, value=None):
        self.text = Text(text=text, text_type="plain_text")
        self.action_id = action_id
        self.value = value

    def serialize(self):
        button = {
            "type": "button",
            "text": self.text.serialize(),
            "action_id": self.action_id,
        }

        if self.value:
            button['value'] = str(self.value)

        return button


class Text:
    def __init__(self, text, title=None, text_type="mrkdwn", add_new_line=False):
        self.text_type = text_type
        self.text = text
        self.title = title
        self.add_new_line = add_new_line

    def serialize(self):
        text = f"{self.text}\n\u00A0" if self.add_new_line else self.text

        return {
            "type": self.text_type,
            "text": self.text if not self.title else f"*{self.title}*\n{text}"
        }
