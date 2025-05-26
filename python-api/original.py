from flask import Flask, jsonify, request
from flask_cors import CORS

# Initialize Flask application
app = Flask(__name__)

# Enable CORS for all routes
CORS(app, resources={r"/*": {"origins": "*", "allow_headers": ["Content-Type", "Authorization"]}})

# Alternatively, for more specific CORS configuration:
# CORS(app, resources={r"/foo": {"origins": ["http://localhost:3000", "https://yourdomain.com"]}})

# Define the /foo endpoint that accepts both GET and POST
@app.route('/foo', methods=['GET', 'POST', 'OPTIONS'])
def foo():
    # Handle preflight OPTIONS request
    if request.method == 'OPTIONS':
        return build_cors_preflight_response()
    
    # Process the actual request
    elif request.method == 'POST':
        # For POST requests, return the data that was sent
        received_data = request.get_json(force=True)
        response = jsonify({
            "status": "success",
            "message": "Data received successfully",
            "received_data": received_data,
            "data_type": str(type(received_data)),
            #"test": received_data['foo']
        })
        return response
    
    else:
        # For GET requests, return the original response
        response = jsonify({
            "status": "success",
            "message": "Here is your answer!",
            "data": {
                "answer": 42,
                "description": "The Answer to the Ultimate Question of Life, the Universe, and Everything"
            }
        })
        return response

# Helper function for preflight response
def build_cors_preflight_response():
    response = jsonify({})
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "Content-Type,Authorization")
    response.headers.add("Access-Control-Allow-Methods", "GET,POST,OPTIONS")
    return response

# Run the application
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
