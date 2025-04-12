
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

messages = []

@app.route('/')
def index():
    return render_template('index.html', messages=messages)

@app.route('/send', methods=['POST'])
def send():
    data = request.get_json()
    message = data.get('message')
    if message:
        messages.append(message)
        return jsonify({"status": "success"})
    return jsonify({"status": "error", "message": "No message provided"})

if __name__ == '__main__':
    app.run(debug=True)
