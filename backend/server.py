from flask import Flask, request
from flask_cors import CORS
from compilerC import Code
import json

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['POST'])
def App():
    data = request.get_json(silent=True)
    computed = Code(data)
    respone = computed.run()
    # print(respone)
    #-----------------------#
    # free memmory
    computed = None
    del(computed)
    #-----------------------#
    print(respone)
    return json.dumps(respone)


if __name__ == "__main__":
    print('----------READY----------')
    app.run()
