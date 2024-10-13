import requests

BASE_URL = "http://server:5000/Users"

# Helper function to pretty-print responses
def print_response(response):
    print(f"Status Code: {response.status_code}")
    if response.status_code in [200, 201]:
        print(response.json())
    else:
        print(response.text)

# 1. Create a user
def create_user():
    user_data = {
        "userName": "jdoe",
        "name": {
            "givenName": "John",
            "familyName": "Doe"
        },
        "emails": [
            {
                "value": "jdoe@example.com",
                "primary": True
            }
        ]
    }
    response = requests.post(BASE_URL, json=user_data)
    print_response(response)
    if response.status_code in [200, 201]:
        return response.json().get('id')  # Return the created user's ID

# 2. Get a user
def get_user(user_id):
    response = requests.get(f"{BASE_URL}/{user_id}")
    print_response(response)

# 3. List users
def list_users():
    response = requests.get(BASE_URL)
    print_response(response)

# 4. Update a user
def update_user(user_id):
    update_data = {
        "userName": "johndoe",
        "name": {
            "givenName": "John",
            "familyName": "Doe"
        },
        "emails": [
            {
                "value": "john.doe@newexample.com",
                "primary": True
            }
        ]
    }
    response = requests.put(f"{BASE_URL}/{user_id}", json=update_data)
    print_response(response)

# 5. Delete a user
def delete_user(user_id):
    response = requests.delete(f"{BASE_URL}/{user_id}")
    print_response(response)

# Example usage
if __name__ == "__main__":
    user_id = create_user()  # Step 1: Create user and get the user ID
    if user_id:
        print(f"User ID from the create response: {user_id}")
        get_user(user_id)  # Step 2: Retrieve user
        list_users()  # Step 3: List all users
        update_user(user_id)  # Step 4: Update user
        delete_user(user_id)  # Step 5: Delete user
