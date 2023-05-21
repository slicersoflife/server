from flask import request, jsonify, Blueprint, current_app
from sqlalchemy import select
import uuid

from app.extensions import db
from .models import Friend, FriendRequest


def add_routes(bp: Blueprint):
    @bp.post("/friend_request")
    def friend_request():
        # add POST route to save a new entry in the friend request table, taking in the user id of the person who sent the request and the user id of the person who received the request
        post_data = request.get_json()
        try:
            from_user_id = post_data.get("from_user_id")
            to_user_id = post_data.get("to_user_id")

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
            friend_request = FriendRequest.query.filter_by(
                from_user_id=from_user_id, to_user_id=to_user_id
            ).first()
            db.session.delete(friend_request)
            db.session.commit()
            friend = Friend(id=uuid(), from_user_id=from_user_id, to_user_id=to_user_id)
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
            friend_request = FriendRequest.query.filter_by(
                from_user_id=from_user_id, to_user_id=to_user_id
            ).first()
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

    @bp.get("/friend/delete")
    def delete_friend():
        # GET request to remove a friend from the friends table
        try:
            from_user_id = request.args.get("user_a")
            to_user_id = request.args.get("user_b")
            friend = Friend.query.filter_by(
                from_user_id=from_user_id, to_user_id=to_user_id
            ).first()
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
