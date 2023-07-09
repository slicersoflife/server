import datetime, time, random, os
from flask import request, jsonify, Blueprint, current_app

from app.extensions import db
from app.auth.models import Friend, FriendRequest, User

from dotenv import load_dotenv
import boto3, botocore


def lambda_handler(event, context):
    # Perform your scheduled task logic here
    # Match friends, schedule calls, and send notifications

    # Get the list of users from the database
    users = get_users()

    # Iterate over users and match friends
    matched_friends = []
    for user in users:
        friend = match_friend(user, matched_friends)
        if friend:
            matched_friends.append((user, friend))

    # Schedule calls for matched friend pairs
    for friend_pair in matched_friends:
        user1, user2 = friend_pair
        call_time = generate_random_call_time()
        initiate_call(user1, user2, call_time)

    return {"statusCode": 200, "body": "Scheduled task executed successfully."}


def generate_random_call_time():
    # Generate a random time between 12 PM and 8 PM
    start_time = datetime.time(hour=12)
    end_time = datetime.time(hour=20)
    call_time = datetime.datetime.combine(
        datetime.date.today(), start_time
    ) + datetime.timedelta(minutes=random.randint(0, 480))
    return call_time


def get_users():
    # Retrieve the list of users from your database
    # Perform the necessary query to get all users
    # Return the list of users
    # Example implementation:
    users = User.query.all()
    return users


def match_friend(user, matched_friends):
    # Match a friend for the given user
    # You can implement your own logic to find an available friend
    # based on your table relationships and any additional criteria
    # Example implementation:
    for friend in user.friends_a:
        if friend not in matched_friends:
            return friend
    for friend in user.friends_b:
        if friend not in matched_friends:
            return friend
    return None


def initiate_call(user1, user2, call_time):
    # Perform the necessary actions to initiate a call between user1 and user2
    # Example implementation:
    # Send notification using SNS or any other messaging service
    send_notification(user1, user2, call_time)


def send_notification(user1, user2, call_time):
    # Send notification to user1 and user2 about the scheduled call
    # Example implementation:
    sns_client = boto3.client("sns")
    message = f"You have a scheduled call with {user2.username} at {call_time}."
    sns_client.publish(TopicArn="your-sns-topic-arn", Message=message)


# make a script that combs through our users
