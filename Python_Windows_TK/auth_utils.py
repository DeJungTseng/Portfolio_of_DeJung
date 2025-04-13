import bcrypt
import datasource



def verify_password(plain_password, hashed_password):
    """Verify a stored password against one provided by user.
    
    Args:
        plain_password: The password provided by user
        hashed_password: The stored hashed password
        
    Returns:
        bool: True if passwords match, False otherwise
    """
    try:
        # Convert input password to bytes
        plain_password = plain_password.encode('utf-8')
        stored_hash = hashed_password.encode('utf-8') if isinstance(hashed_password, str) else hashed_password
        
        # Use bcrypt to check if the password matches the hash
        return bcrypt.checkpw(plain_password, stored_hash)
    except Exception as e:
        print(f"Error verifying password: {e}")
        return False

def validate_login(username, password):
    """驗證登入資訊
    
    Args:
        username: The username from LoginDialog's entry
        password: The password from LoginDialog's entry
        
    Returns:
        bool: True if credentials are valid, False otherwise
    """
    print(f"[validate_login] Validating credentials for username: {username}")
    
    # Query credentials from database using the provided username
    stored_username, stored_password_hash = datasource.get_user_id_pw(username)
    print(f"[validate_login] Database returned stored_username: {stored_username}")
    
    # Check if user exists
    if stored_username is None:
        print("[validate_login] User not found in database")
        return False
    
    # Verify the password
    password_match = verify_password(password, stored_password_hash)
    print(f"[validate_login] Password match result: {password_match}")
    
    return password_match
