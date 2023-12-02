from flask import request, jsonify, Blueprint, current_app
from sqlalchemy import select

from app.extensions import db
from .helpers import perform_fuzzy_search
from .models import Friendship, FriendRequest


def add_routes(bp: Blueprint):
    @bp.post("/friend_request")
    def send_friend_request():
        post_data = request.get_json()
        try:
            friend_request = FriendRequest(
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
            friendship = Friendship(user_a_id=from_user_id, user_b_id=to_user_id)
            db.session.add(friendship)
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

    @bp.get("/friend/search")
    def search_friend():
        query = request.args.get("query")
        from app.auth.models import User

        users = db.session.execute(select(User.username)).all()
        items = list(map(lambda u: u[0], users))
        results = perform_fuzzy_search(query, items)
        return jsonify(results)

    @bp.post("/friend/delete")
    def delete_friend():
        # GET request to remove a friend from the friends table
        post_data = request.get_json()
        try:
            from_user_id = post_data.get("user_a_id")
            to_user_id = post_data.get("user_b_id")
            friend = db.session.scalars(
                select(Friendship).filter_by(
                    user_a_id=from_user_id, user_b_id=to_user_id
                )
            ).first()
            if friend is None:
                friend = db.session.scalars(
                    select(Friendship).filter_by(
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
