from model import User
import bcrypt

username = input("Enter username: ")

User.create(
    username = username,
    name = "User Userson",
    lang = "fa",
    color = "light",
    is_male = True,
    quota = 10000,
    age = 24,
    password = bcrypt.hashpw(username.encode(), bcrypt.gensalt())
)

print("Created")

