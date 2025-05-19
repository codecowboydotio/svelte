from flask import Flask, jsonify, request
import requests

# Initialize Flask application
app = Flask(__name__)

# Define the /foo endpoint
@app.route('/foo', methods=['GET','POST'])
def foo():
    return jsonify({
        "status": "success",
        "message": "Here is your answer!",
        "data": {
            "answer": 42,
            "description": "The Answer to the Ultimate Question of Life, the Universe, and Everything"
            "data": request.json
        }
    })

# Run the application
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
