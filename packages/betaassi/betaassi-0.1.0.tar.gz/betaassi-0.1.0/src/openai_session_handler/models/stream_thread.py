from .threads.basethread import BaseThread
from .messages.streammessage import StreamMessage

class StreamThread (BaseThread):

    def publish_message(self, content:str) :
        StreamMessage.publish_message(thread_id=self.id, content=content)


