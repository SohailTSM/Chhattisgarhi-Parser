from flask import Flask, request
import main


app = Flask(__name__)

@app.route('/api', methods=['POST', 'GET'])
def api():
    if request.method == 'POST':
        text = request.form['text']
        response = main.main(text)
        
        return {
            'status' : 1 if type(response) is dict else 0,
            'response' : response
        }

    return {
        'error' : 'No text input. Use POST method'
    }

if __name__ == '__main__':
    app.run(threaded=True)