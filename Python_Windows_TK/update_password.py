import os
from dotenv import load_dotenv
import psycopg2
from auth_utils import hash_password

def update_user_password(username, plain_password):
    """Update user's password with bcrypt hash in the database.
    
    Args:
        username: The username to update
        plain_password: The plain text password to hash and store
    """
    load_dotenv()
    
    try:
        conn_params = {
            'host': os.environ['postgres_host'],
            'database': os.environ['postgres_db'],
            'user': os.environ['postgres_user'],
            'password': os.environ['postgres_password']
        }
        
        # Hash the password
        hashed_password = hash_password(plain_password)
        
        # Convert bytes to string for storage
        hashed_password_str = hashed_password.decode('utf-8')
        
        # Update the password in the database
        with psycopg2.connect(**conn_params) as conn:
            with conn.cursor() as cur:
                query = """
                UPDATE public.user_id_table 
                SET movie_user_pw = %s
                WHERE movie_user_id = %s;
                """
                cur.execute(query, (hashed_password_str, username))
                rows_affected = cur.rowcount
                
                if rows_affected > 0:
                    print(f"Successfully updated password for user: {username}")
                else:
                    print(f"No user found with username: {username}")
                
                conn.commit()
                
    except Exception as e:
        print(f"Error updating password: {e}")

if __name__ == "__main__":
    # Update password for user 'aaa'
    
    update_user_password("1234", "5678")
    update_user_password("bbb", "BBB")
    update_user_password("ccc", "CCC")