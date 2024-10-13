from flask import Flask, jsonify, request, abort
import uuid
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def index():
    return "SCIM Server is running!"

# In-memory storage for simplicity
users = {}
groups = {}

# SCIM User schema attributes
def format_user(user):
    return {
        "id": user["id"],
        "userName": user["userName"],
        "name": {
            "givenName": user["givenName"],
            "familyName": user["familyName"]
        },
        "emails": [{"value": user["email"], "primary": True}],
        "meta": {
            "resourceType": "User",
            "created": user["created"],
            "lastModified": user["lastModified"]
        }
    }

# 1. Create a user (SCIM POST /Users)
@app.route('/Users', methods=['POST'])
def create_user():
    data = request.get_json()

    # Validate required fields
    if 'userName' not in data or 'name' not in data or 'emails' not in data:
        abort(400, "Missing required fields")

    user_id = str(uuid.uuid4())
    now = datetime.utcnow().isoformat()

    user = {
        "id": user_id,
        "userName": data['userName'],
        "givenName": data['name'].get('givenName'),
        "familyName": data['name'].get('familyName'),
        "email": data['emails'][0]['value'],
        "created": now,
        "lastModified": now
    }
    
    users[user_id] = user
    return jsonify(format_user(user)), 201

# 2. Retrieve a user (SCIM GET /Users/{id})
@app.route('/Users/<user_id>', methods=['GET'])
def get_user(user_id):
    user = users.get(user_id)
    if not user:
        abort(404, "User not found")
    return jsonify(format_user(user))

# 3. List users (SCIM GET /Users)
@app.route('/Users', methods=['GET'])
def list_users():
    return jsonify({"Resources": [format_user(user) for user in users.values()]})

# 4. Update a user (SCIM PUT /Users/{id})
@app.route('/Users/<user_id>', methods=['PUT'])
def update_user(user_id):
    user = users.get(user_id)
    if not user:
        abort(404, "User not found")

    data = request.get_json()
    user['userName'] = data['userName']
    user['givenName'] = data['name'].get('givenName')
    user['familyName'] = data['name'].get('familyName')
    user['email'] = data['emails'][0]['value']
    user['lastModified'] = datetime.utcnow().isoformat()

    users[user_id] = user
    return jsonify(format_user(user))

# 5. Delete a user (SCIM DELETE /Users/{id})
@app.route('/Users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = users.pop(user_id, None)
    if not user:
        abort(404, "User not found")
    return '', 204

# 6. Group management (SCIM POST /Groups)
@app.route('/Groups', methods=['POST'])
def create_group():
    data = request.get_json()

    group_id = str(uuid.uuid4())
    group = {
        "id": group_id,
        "displayName": data['displayName'],
        "members": data.get('members', [])
    }

    groups[group_id] = group
    return jsonify(group), 201

@app.route('/Groups', methods=['GET'])
def get_groups():
    pass

@app.route('/Groups/<groups_id>', methods=['GET'])
def get_group(groups_id):
    pass

@app.route('/Groups', methods=['PUT'])
def update_group():
    pass

@app.route('/Groups', methods=['DELETE'])
def delete_group():
    pass

@app.route('/Assign_Groups_User', methods=['POST'])
def assign_group():
    pass

@app.route('/Unassign_Groups_User', methods=['POST'])
def unassign_group():
    pass

# Start the Flask app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
