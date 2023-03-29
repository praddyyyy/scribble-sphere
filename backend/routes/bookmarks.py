from routes import app, version, db
from flask import request, jsonify, Response
from models.bookmark_model import Bookmarks
from models.user_model import Users
from models.blogs_model import Blogs


# Route for bookmarking a blog


@app.route(version + '/bookmark/<int:blog_id>/<int:user_id>', methods=['POST'])
def bookmark_blog(blog_id, user_id):
    bookmark = Bookmarks(bookmarked_by=user_id,
                         bookmarked_post=blog_id)
    db.session.add(bookmark)
    db.session.commit()
    return jsonify({'message': 'Bookmarked successfully', 'success': True})


# Route for displaying bookmarks by a user


@app.route(version + '/bookmarks/<int:user_id>', methods=['GET'])
def get_bookmarks(user_id):
    bookmarks = Bookmarks.query.filter_by(bookmarked_by=user_id).all()
    if len(bookmarks) == 0:
        return jsonify({'message': 'No bookmarks found', 'success': False})
    data = []
    for bookmark in bookmarks:
        temp = {}
        temp['blog_id'] = bookmark.bookmarked_post
        data.append(temp)
    return jsonify({"bookmarks": data, "success": True})


# Route for deleting a bookmark


@app.route(version + '/bookmark/<int:blog_id>/<int:user_id>/delete', methods=['DELETE'])
def delete_bookmark(blog_id, user_id):
    bookmark = Bookmarks.query.filter_by(
        bookmarked_by=user_id, bookmarked_post=blog_id).first()
    if not bookmark:
        return jsonify({'message': 'No bookmark found', 'success': False})

    db.session.delete(bookmark)
    db.session.commit()
    return jsonify({'message': 'Bookmark deleted successfully', 'success': True})


# Route for checking if a blog is bookmarked by a user


@app.route(version + '/bookmark/<int:blog_id>/<int:user_id>/check', methods=['GET'])
def check_bookmark(user_id, blog_id):
    bookmark = Bookmarks.query.filter_by(
        bookmarked_by=user_id, bookmarked_post=blog_id).first()
    if bookmark:
        return jsonify({'message': 'Bookmarked', 'success': True})
    return jsonify({'message': 'Not bookmarked', 'success': False})
