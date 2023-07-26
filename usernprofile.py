import csv
import hashlib

class User:
    def __init__(self, username, password, id):
        self.id = id
        self.username = username
        self.password = password

    def to_dict(self):
        return {"UserID": self.id, "Username": self.username, "Password": self.password}

    @classmethod
    def from_dict(cls, data):
        return cls(data["Username"], data["Password"], data["UserID"])
    
def write_user_to_csv(users):
    with open('Users.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["UserID", "Username", "Password"])
        for user in users:
            writer.writerow([user.id, user.username, user.password])

def is_username_taken(username):
    try:
        with open('Users.csv', 'r') as file:
            reader = csv.reader(file)
            next(reader)  # skip header
            for row in reader:
                if row[1] == username:
                    return True
    except FileNotFoundError:
        pass #if the file doesn't exist, no usernames have been taken yet
    return False

def add_user(username, password):
    if is_username_taken(username):
        return False  # username is already taken, user was not created
    users = read_users_from_csv()
    id = len(users) + 1  # assign the next id
    user = User(username, password, id)
    users.append(user)
    write_user_to_csv(users)  # pass the list of users, not a single user
    return True  # user was successfully created

def read_users_from_csv():
    users = []
    try:
        with open('Users.csv', 'r') as file:
            reader = csv.reader(file)
            next(reader)  # skip header
            for row in reader:
                user = User(row[1], row[2], row[0])  # username, password, id
                users.append(user)
    except FileNotFoundError:
        pass  # If the file doesn't exist, no users have been created yet
    return users

def authenticate_user(username, password):
    users = read_users_from_csv()
    for user in users:
        if user.username == username and user.password == password:
            return True  # User was found and password matched
    return False  # No matching user was found

def register(username, password):
    return add_user(username, password)

def login(username, password):
    return authenticate_user(username, password)


#Profile - will hold progress and previous responses

class UserProfile:
    def __init__(self, user_id, depression_score, stress_score, anxiety_score):
        self.user_id = user_id
        self.depression_score = depression_score
        self.stress_score = stress_score
        self.anxiety_score = anxiety_score

def write_profile_to_csv(profile):
    with open('Profiles.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        # writer.writerow(["UserID", "DepressionScore", "StressScore", "AnxietyScore"]) # remove this line to avoid writing headers multiple times
        writer.writerow([profile.user_id, profile.depression_score, profile.stress_score, profile.anxiety_score])


def add_profile(user_id, depression_score, stress_score, anxiety_score):
    profile = UserProfile(user_id, depression_score, stress_score, anxiety_score)
    write_profile_to_csv(profile)

def read_profile_from_csv(user_id):
    print(f"Trying to read profile for user_id {user_id}")
    try:
        with open('Profiles.csv', 'r') as file:
            reader = csv.reader(file)
            next(reader)  # skip header
            for row in reader:
                print(f"Read row from CSV: {row}")
                if int(row[0]) == user_id:
                    return UserProfile(int(row[0]), float(row[1]), float(row[2]), float(row[3]))
    except FileNotFoundError:
        print("File not found. Creating default profile.")
    # return a default profile if no profile found for this user_id
    return UserProfile(user_id, 0.0, 0.0, 0.0)

def update_profile(user_id, depression_score=None, stress_score=None, anxiety_score=None):
    profiles = []
    updated = False
    try:
        with open('Profiles.csv', 'r') as file:
            reader = csv.reader(file)
            next(reader)  # skip header
            for row in reader:
                if int(row[0]) == user_id:
                    # update the scores if a new value was given, otherwise keep the old value
                    depression_score = depression_score if depression_score is not None else float(row[1])
                    stress_score = stress_score if stress_score is not None else float(row[2])
                    anxiety_score = anxiety_score if anxiety_score is not None else float(row[3])
                    profiles.append(UserProfile(user_id, depression_score, stress_score, anxiety_score))
                    updated = True
                else:
                    profiles.append(UserProfile(int(row[0]), float(row[1]), float(row[2]), float(row[3])))
    except FileNotFoundError:
        pass  # If the file doesn't exist, no profiles have been created yet
    # If the profile was not found in the file, create a new one
    if not updated and depression_score is not None and stress_score is not None and anxiety_score is not None:
        profiles.append(UserProfile(user_id, depression_score, stress_score, anxiety_score))

    # write the updated profiles back to the CSV file
    with open('Profiles.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["UserID", "DepressionScore", "StressScore", "AnxietyScore"])
        for profile in profiles:
            writer.writerow([profile.user_id, profile.depression_score, profile.stress_score, profile.anxiety_score])


#Personalizing responses based on user's profile
#this needs to be updated after we have a final questionnaire in place
def give_feedback(user_id):
    profile = read_profile_from_csv(user_id)
    if profile is None:
        print("No profile found for this user ID")
        return
    if profile.depression_score > 8:
        print("You've been scoring high on depression lately. Do you want to talk about it?")
    elif profile.stress_score > 7:
        print("Your stress levels seem to be rising. Have you tried any relaxation techniques?")
    else:
        print("Your scores look normal. Keep taking care of your mental health!")
