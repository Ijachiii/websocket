import json
from channels.generic.websocket import AsyncWebsocketConsumer
from blog.models import BlogPost, Comment
from channels.db import database_sync_to_async


class CommentConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.blog_id = self.scope["url_route"]["kwargs"]["blog_id"]
        self.blog_group_id = f"chat_{self.blog_id}"

        # Join room group
        await self.channel_layer.group_add(
            self.blog_group_id,
            self.channel_name
        )

        await self.accept()

        await self.send_previous_messages()


    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.blog_group_id,
            self.channel_name
        )


    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        sender = text_data_json["sender"]
        message = text_data_json["message"]

        blog = await self.get_blog(self.blog_id)
        # Save to database
        await self.save_messages(sender, message, blog)

        # Send message to room group
        await self.channel_layer.group_send(
            self.blog_group_id,
            {
                "type": "chat.message",
                "sender": sender,
                "message": message,
            }
        )

    @database_sync_to_async
    def get_blog(self, blog_id):
        return BlogPost.objects.get(id=blog_id)


    @database_sync_to_async
    def save_messages(self, sender, message, blog):
        message = Comment(sender=sender, message=message, blog=blog)
        message.save()


    # Receive message from room group
    async def chat_message(self, event):
        sender = event["sender"]
        message = event["message"]

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            "sender": sender,
            "message": message
        }))


    async def send_previous_messages(self):
        previous_messages = await self.get_previous_messages(self.blog_id)

        if previous_messages:
            formatted_messages = []
            for message in previous_messages:
                formatted_message = {
                    "sender": message["sender"],
                    "message": message["message"],
                    "timestamp": message["timestamp"].strftime("%Y-%m-%d %H:%M:%S")
                }
                formatted_messages.append(formatted_message)


            await self.send(text_data=json.dumps({
                "messages": formatted_messages
            }))


    @database_sync_to_async
    def get_previous_messages(self, blog_id):
        # Implement your logic to fetch previous messages for the specified blog
        previous_messages = Comment.objects.filter(blog_id=blog_id).values("sender", "message", "timestamp" )
        # Return the list of messages
        return list(previous_messages)

# class ChatConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         await self.accept()

#     async def disconnect(self, close_code):
#         pass

#     async def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         email = text_data_json["email"]
#         message = text_data_json['message']

#         print(text_data_json)

#         await self.send(text_data=json.dumps({
#             "email": email,
#             "message": message
#         }))

# class ChatConsumer(WebsocketConsumer):
#     def connect(self):
#         self.accept()

#     def disconnect(self, close_code):
#         pass

#     def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         message = text_data_json["message"]

#         self.send(text_data=json.dumps({"message": message}))