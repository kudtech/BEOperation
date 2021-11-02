from aiohttp import web
import socketio

sio = socketio.AsyncServer()
app = web.Application()
sio.attach(app)


async def index(request):
    with open('templates/sockets/index.html') as f:
        return web.Response(text=f.read(), content_type='text/html')


@sio.on('message')
async def receive_message(sid, message):
    print("Socket ID: ", sid)
    print(message)
    server_message = "Server: " + message
    await sio.emit('message', server_message)

# if user.is_aunthenticated,connect else raise ConnectionRefusedError('Aunthentication Failed')
@sio.event
def connect(sid, environ):
    print(sid, ' is connected.')


@sio.event
def disconnect(sid):
    print(sid, 'has disconnected.')


app.router.add_get('/', index)

# Start server
if __name__ == '__main__':
    web.run_app(app)
