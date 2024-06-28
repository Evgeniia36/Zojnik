import os
from dotenv import load_dotenv

load_dotenv()

admin_username = os.getenv('admin_username')
admin_password = os.getenv('admin_password')
valid_refresh_token = os.getenv('valid_refresh_token')
valid_access_token = os.getenv('valid_access_token')

user_id = os.getenv('user_id')
valid_email = os.getenv('valid_email')
valid_password = os.getenv('valid_password')
new_valid_password = os.getenv('new_valid_password')

valid_email_2 = os.getenv('valid_email_2')
valid_password_2 = os.getenv('valid_password_2')


