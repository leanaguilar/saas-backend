from flask import Flask, jsonify
from flask_cors import CORS
import firebase_admin
from firebase_admin import auth, credentials
from flask import Flask, request, jsonify


app = Flask(__name__)
CORS(app)  # Allow CORS for all routes

# Test route
@app.route('/hello', methods=['GET'])
def hello():
    return jsonify(message="Hello from Flask!")


# Initialize Firebase Admin SDK
cred = credentials.Certificate("./firebase-sdk.json")  # Update the path
firebase_admin.initialize_app(cred)


@app.route('/verify-token', methods=['GET'])
def verify_token():
    # Get the token from the Authorization header
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return jsonify({'error': 'No token provided'}), 401

    token = auth_header.split(' ')[1]

    try:
        # Verify the token using Firebase Admin
        decoded_token = auth.verify_id_token(token)
        uid = decoded_token['uid']  # You can also access other fields if needed
        return jsonify({'message': 'Token is valid', 'uid': uid}), 200

    except Exception as e:
        print(f"Error verifying token: {e}")
        return jsonify({'error': 'Invalid token'}), 401

if __name__ == '__main__':
    app.run(debug=True)
