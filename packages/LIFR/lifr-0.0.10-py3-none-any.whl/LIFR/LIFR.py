import asyncio
import websockets
import json
print("hello")

async def send(content):
    async with websockets.connect('ws://quoi29.ddns.net:8765') as websocket:
        # Send a message to the server
       
        await websocket.send(str(content))

        # Receive and print the server's response
        response = await websocket.recv()
       
        return response

def generate(content):
	if(type(content["data"])==str):
		split_text=content["data"].split("\n")
		text=[]
		for el in split_text:
			text.append([el])
		print(text)
		content["data"]=text
	content["type"]="generate"
	text=asyncio.get_event_loop().run_until_complete(send(str(content)))
	return json.loads(text)
def search(content):
	content["type"]="search"
	text=asyncio.get_event_loop().run_until_complete(send(json.dumps(content)))
	return text