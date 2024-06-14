import asyncio
from flask import Flask, jsonify
import random

app = Flask(__name__)


ERROR_RATE = 0.1

async def random_status():
    await asyncio.sleep(1)
    if random.random() < ERROR_RATE:
    	return {'data':'failed', 'status':503}
    
    return {'data':'success', 'status':200}


@app.route("/", methods=["POST"])
async def simple_request():
    data = await random_status()
    return jsonify(data)



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8010)

