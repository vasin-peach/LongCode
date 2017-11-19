from flask import Flask, request
from flask_cors import CORS
from compiler import Code

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['POST'])
def App():
    data = request.get_json(silent=True)
    computed = Code(data)
    respone = computed.run()
    print(respone)
    #-----------------------#
    # free memmory
    computed = None
    del(computed)
    #-----------------------#
    return respone


if __name__ == "__main__":
    print('----------READY----------')
    app.run()
