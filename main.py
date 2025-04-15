# pip install fastapi
from fastapi import FastAPI
import happybase
from pydantic import BaseModel
import uuid
from datetime import datetime

class ChatRoom(BaseModel):
    room_name: str

class Message(BaseModel):
    room_id: str # 데이터가 누구로부터 속해있는지
    content: str


connection = happybase.Connection('localhost', port=9090)
connection.open()

app = FastAPI()

# @app.get('/') # => urls.py(FastAPI에서는 분리되어있지 않고 하나로 존재)
# def index():  # => views.py
#     return {'hello':'world'}
    
@app.post('/chatrooms') # post방식으로 들어오면 chatrooms 생성
def create_chatroom(chatroom: ChatRoom):
    table = connection.table('chatrooms')
    chatroom_id = str(uuid.uuid4())

    table.put(chatroom_id, {'info:room_name': chatroom.room_name}) #chatroom.room_name >> "pythhon chatting room" (create 로직)

    return {'chatroom_id': chatroom_id,
            'room_name': chatroom.room_name
    }

@app.get('/chatrooms') # get방식으로 들어오면 chatrooms 조회
def get_chatrooms():
    table = connection.table('chatrooms')
    rows = table.scan()

    result = []

    for k, v in rows:
        result.append(
            {
                'chatroom_id': k,
                'room_name': v[b'info:room_name'], #bite 형식입니다
            }
        )

    return result

@app.post('/messages')
def create_message(message: Message): # type hint
    table = connection.table('messages')

    room_id = message.room_id # 변수
    timestamp = int(datetime.now().timestamp() * 1000)
    message_id = f'{room_id}-{timestamp}'

    table.put(message_id, {'info:content': message.content, 'info:room_id': room_id})

    return {
        'message_id': message_id,
        'room_id': room_id,
        'content': message.content
    }

@app.get('/chatrooms/{room_id}/messages') # room_id에 맞춰서 하위에 있는 메시지 가져오기
def get_messages(room_id: str):
    table = connection.table('messages')
    prefix = room_id.encode('utf-8')

    rows = table.scan(row_prefix=prefix, reverse=True)

    result = []
    for k, v in rows:
        result.append({
            'message_id': k,
            'room_id': v[b'info:room_id'], #binary
            'content': v[b'info:content'],
        })
        
    return result


