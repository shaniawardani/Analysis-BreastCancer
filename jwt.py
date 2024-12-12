#jwt.py
import secrets  

# Generate a JWT secret  
jwt_secret = secrets.token_hex(32)  # Generates a 64-character hexadecimal string  
print(jwt_secret)