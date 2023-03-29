from routes import app, version, db
from flask import request, jsonify, Response
from models.likes_model import Likes
from models.user_model import Users
from models.blogs_model import Blogs
from helpers import token_required

# Route for liking a blog


@app.route(version + '/like', methods=['POST'])
def like_blog():
    user_id = request.json['user_id']
    blog_id = request.json['blog_id']
    like = Likes(liked_by=user_id, liked_post=blog_id)
    db.session.add(like)
    db.session.commit()
    return jsonify({'message': 'Liked successfully', 'success': True})

# Route for displaying likes


@app.route(version + '/likes/<int:blog_id>', methods=['GET'])
def get_likes(blog_id):
    likes = Likes.query.filter_by(liked_post=blog_id).all()
    return jsonify([like.serialize() for like in likes])

# Route for displaying liked blogs


@app.route(version + '/liked-blogs', methods=['GET'])
@token_required
def get_liked_blogs(current_user):
    likes = Likes.query.filter_by(liked_by=current_user.id).all()
    data = []
    for like in likes:
        temp = {}
        temp['blog_id'] = like.liked_post
        data.append(temp)
    return jsonify({'data': data, 'success': True})

# Route for disliking a blog


@app.route(version + '/like/<int:user_id>/<int:blog_id>/dislike', methods=['PUT'])
def dislike_blog(user_id, blog_id):
    like = Likes.query.filter_by(liked_by=user_id, liked_post=blog_id).all()
    for l in like:
        db.session.delete(l)
    db.session.commit()
    return jsonify({'message': 'Disliked successfully', 'success': True})

# Route for checking if a blog is liked by a user


@app.route(version + '/like/<int:user_id>/<int:blog_id>/check', methods=['GET'])
def check_like(user_id, blog_id):
    like = Likes.query.filter_by(liked_by=user_id, liked_post=blog_id).all()
    if len(like) > 0:
        return jsonify({'message': 'Liked', 'success': True})
    else:
        return jsonify({'message': 'Not liked', 'success': False})


# Route for displaying likes count


@app.route(version + '/likes-count/<int:blog_id>', methods=['GET'])
def get_likes_count(blog_id):
    likes = Likes.query.filter_by(liked_post=blog_id).all()
    return jsonify({'count': len(likes), 'success': True})


# Route for displaying like count of all blogs of a user


@app.route(version + '/likes-count/all-blogs', methods=['GET'])
@token_required
def get_likes_count_all(current_user):
    blogs = Blogs.query.filter_by(user_id=current_user.id).all()
    data = []
    for blog in blogs:
        temp = {}
        temp['blog_id'] = blog.id
        temp['likes_count'] = len(
            Likes.query.filter_by(liked_post=blog.id).all())
        data.append(temp)
    return jsonify({'data': data, 'success': True})
