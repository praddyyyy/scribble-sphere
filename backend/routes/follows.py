from routes import app, version, db
from flask import request, jsonify, Response
from models.user_model import Users
from models.follow_model import FollowRequest
# Route for sending follow requests


@app.route(version + '/follow', methods=['POST'])
def send_follow_request():
    sender_id = request.json['sender_id']
    receiver_id = request.json['receiver_id']
    follow_request = FollowRequest(
        sender_id=sender_id, receiver_id=receiver_id, status='pending')
    db.session.add(follow_request)
    db.session.commit()
    return jsonify({'message': 'Follow request sent successfully', 'success': True})

# Route for displaying follow requests


@app.route(version + '/follow-requests/<int:user_id>', methods=['GET'])
def get_follow_requests(user_id):
    follow_requests = FollowRequest.query.filter_by(
        receiver_id=user_id, status='pending').all()
    return jsonify([request.serialize() for request in follow_requests])


# Route for displaying followers
@app.route(version + '/followers/<int:user_id>', methods=['GET'])
def get_followers(user_id):
    followers = FollowRequest.query.filter_by(
        receiver_id=user_id, status='accepted').all()
    data = []
    for follower in followers:
        temp = {}
        temp['follower_id'] = follower.sender_id
        data.append(temp)
    return jsonify({'data': data, 'success': True})

# Route for displaying following


@app.route(version + '/following/<int:user_id>', methods=['GET'])
def get_following(user_id):
    following = FollowRequest.query.filter_by(
        sender_id=user_id, status='accepted').all()
    data = []
    for follow in following:
        temp = {}
        temp['following_id'] = follow.receiver_id
        data.append(temp)
    return jsonify({'data': data, 'success': True})

# Route to accept a follow request


@app.route(version + '/follow-requests/<int:sender_id>/<int:receiver_id>/accept', methods=['PUT'])
def accept_follow_request(sender_id, receiver_id):
    follow_request = FollowRequest.query.filter_by(
        sender_id=sender_id, receiver_id=receiver_id, status='pending').all()

    if not follow_request:
        return jsonify({'message': 'Follow request not found.'})

    for request in follow_request:
        request.status = 'accepted'
        db.session.commit()

    return jsonify({'message': 'Follow request accepted.'})

# Route to deny a follow request


@app.route(version + '/follow-requests/<int:sender_id>/<int:receiver_id>/deny', methods=['DELETE'])
def deny_follow_request(sender_id, receiver_id):
    follow_request = FollowRequest.query.filter_by(
        sender_id=sender_id, receiver_id=receiver_id, status='pending').all()

    if not follow_request:
        return jsonify({'message': 'Follow request not found.'})

    for request in follow_request:
        db.session.delete(request)
        db.session.commit()

    return jsonify({'message': 'Follow request denied.', 'success': True})

# Route to unfollow a user


@app.route(version + '/unfollow/<int:sender_id>/<int:receiver_id>', methods=['DELETE'])
def unfollow_user(sender_id, receiver_id):
    follow_request = FollowRequest.query.filter_by(
        sender_id=sender_id, receiver_id=receiver_id, status='accepted').all()

    if not follow_request:
        return jsonify({'message': 'Follow request not found.'})

    for request in follow_request:
        db.session.delete(request)
        db.session.commit()

    return jsonify({'message': 'Unfollowed successfully.', 'success': True})


# Check if a user is following another user


@app.route(version + '/is-following/<int:sender_id>/<int:receiver_id>', methods=['GET'])
def is_following(sender_id, receiver_id):
    follow_request = FollowRequest.query.filter_by(
        sender_id=sender_id, receiver_id=receiver_id, status='accepted').all()

    if not follow_request:
        return jsonify({'message': 'Not following', 'success': False})

    return jsonify({'message': 'Following', 'success': True})

# Check if a user has sent a follow request to another user


@app.route(version + '/follow-request-sent/<int:sender_id>/<int:receiver_id>', methods=['GET'])
def follow_request_sent(sender_id, receiver_id):
    follow_request = FollowRequest.query.filter_by(
        sender_id=sender_id, receiver_id=receiver_id, status='pending').all()

    if not follow_request:
        return jsonify({'message': 'Follow request not sent', 'success': False})

    return jsonify({'message': 'Follow request sent', 'success': True})