from flask import Flask, jsonify, request

# Initialize Flask application
app = Flask(__name__)

# Define the /foo endpoint that accepts both GET and POST
@app.route('/foo', methods=['GET', 'POST'])
def foo():
    if request.method == 'POST':
        # For POST requests, return the data that was sent
        received_data = request.get_json(force=True, silent=True) or {}
        
        return jsonify({
            "status": "success",
            "message": "Data received successfully",
            "received_data": received_data,
            "data_type": str(type(received_data))
        })
    else:
        # For GET requests, return the original response
        return jsonify({
            "status": "success",
            "message": "Here is your answer!",
            "data": {
                "answer": 42,
                "description": "The Answer to the Ultimate Question of Life, the Universe, and Everything"
            }
        })

# Run the application
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)