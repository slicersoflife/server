from flask import request, jsonify, Blueprint, current_app
from sqlalchemy import select
from fuzzywuzzy import fuzz
from uuid import uuid4 as uuid

from .helpers import perform_fuzzy_search

# import uuid
from app.extensions import db
from .models import Friend, FriendRequest


def add_routes(bp: Blueprint):
    @bp.post("/friend_request")
    def friend_request():
        # add POST route to save a new entry in the friend request table, taking in the user id of the
        # person who sent the request and the user id of the person who received the request
        # I get an error, module' object is not callable, can you change the following code to fix this
        post_data = request.get_json()
        try:
            friend_request = FriendRequest(
                id=uuid(),
                from_user_id=post_data.get("from_user_id"),
                to_user_id=post_data.get("to_user_id"),
            )
            db.session.add(friend_request)
            db.session.commit()
            response_object = {
                "status": "success",
                "message": "Friend request sent",
            }
            db.session.close()
            return jsonify(response_object), 200
        except Exception as exception:
            print(exception)
            response_object = {"status": "fail", "message": str(exception)}
            return jsonify(response_object), 503

    @bp.post("/friend_request/accept")
    def accept_friend_request():
        # POST request to accept a friend request, removing it from the table and adding the friends to the friends table
        post_data = request.get_json()
        try:
            from_user_id = post_data.get("from_user_id")
            to_user_id = post_data.get("to_user_id")
            friend_request = db.session.scalars(
                select(FriendRequest).filter_by(
                    from_user_id=from_user_id, to_user_id=to_user_id
                )
            ).first()
            if friend_request is None:
                response_object = {
                    "status": "fail",
                    "message": "Friend request does not exist",
                }
                return jsonify(response_object), 401
            db.session.delete(friend_request)
            db.session.commit()
            friend = Friend(id=uuid(), user_a_id=from_user_id, user_b_id=to_user_id)
            db.session.add(friend)
            db.session.commit()
            response_object = {
                "status": "success",
                "message": "Friend request accepted",
            }
            return jsonify(response_object), 200
        except Exception as exception:
            print(exception)
            response_object = {"status": "fail", "message": str(exception)}
            return jsonify(response_object), 503

    @bp.post("/friend_request/decline")
    def decline_friend_request():
        # POST request to decline a friend request, removing it from the table
        post_data = request.get_json()
        try:
            from_user_id = post_data.get("from_user_id")
            to_user_id = post_data.get("to_user_id")
            friend_request = db.session.scalars(
                select(FriendRequest).filter_by(
                    from_user_id=from_user_id, to_user_id=to_user_id
                )
            ).first()
            if friend_request is None:
                response_object = {
                    "status": "fail",
                    "message": "Friend request does not exist",
                }
                return jsonify(response_object), 401
            db.session.delete(friend_request)
            db.session.commit()
            response_object = {
                "status": "success",
                "message": "Friend request declined",
            }
            return jsonify(response_object), 200
        except Exception as exception:
            print(exception)
            response_object = {"status": "fail", "message": str(exception)}
            return jsonify(response_object), 503

    # fuzzy search endpoint
    @bp.get("/friend/search")
    def fuzzy_search():
        query = request.args.get("query")
        from app.auth.models import User

        users = db.session.execute(select(User.username)).all()
        items = list(map(lambda u: u[0], users))
        results = perform_fuzzy_search(query, items)
        return jsonify(results)

    # mutual friends endpoint
    @bp.get("/friend/mutuals")
    def find_mutuals():
        from app.auth.models import User

        # Fetch user data from the database
        users_data = db.session.execute(
            select(User.id, User.username, User.friends)
        ).all()

        # Convert the data into a dictionary with user_id as keys
        users = {
            user.id: {"username": user.username, "friends": user.friends}
            for user in users_data
        }

        # Helper function to find friends intersection
        def find_mutual_friends(user_id1, user_id2):
            user1_friends = set(users[user_id1]["friends"])
            user2_friends = set(users[user_id2]["friends"])
            mutual_friends = user1_friends.intersection(user2_friends)
            return mutual_friends

        user_id1 = int(request.args.get("user_id1"))
        user_id2 = int(request.args.get("user_id2"))
        if user_id1 not in users or user_id2 not in users:
            return jsonify(error="One or both user IDs do not exist"), 404
        mutual_friends = find_mutual_friends(user_id1, user_id2)
        return jsonify(mutual_friends=list(mutual_friends))

    @bp.post("/friend/delete")
    def delete_friend():
        # GET request to remove a friend from the friends table
        post_data = request.get_json()
        try:
            from_user_id = post_data.get("user_a_id")
            to_user_id = post_data.get("user_b_id")
            friend = db.session.scalars(
                select(Friend).filter_by(user_a_id=from_user_id, user_b_id=to_user_id)
            ).first()
            if friend is None:
                friend = db.session.scalars(
                    select(Friend).filter_by(
                        user_a_id=to_user_id, user_b_id=from_user_id
                    )
                ).first()
                if friend is None:
                    response_object = {
                        "status": "fail",
                        "message": "Friend does not exist",
                    }
                    return jsonify(response_object), 401
            db.session.delete(friend)
            db.session.commit()
            response_object = {
                "status": "success",
                "message": "Removed friend",
            }
            return jsonify(response_object), 200
        except Exception as exception:
            print(exception)
            response_object = {"status": "fail", "message": str(exception)}
            return jsonify(response_object), 503

    pass
