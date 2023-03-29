from routes import app, version, db
from flask import request, jsonify, Response
from flask_cors import CORS
from models.blogs_model import Blogs
from routes import photos
from helpers import token_required
import json
import os
import base64


@app.route(version + '/all-blogs', methods=['GET'])
@token_required
def get_all_blogs(current_user):
    blogs = Blogs.query.order_by(Blogs.created_at.desc()).all()
    output = []
    for blog in blogs:
        blog_data = {}
        blog_data['blog_id'] = blog.id
        blog_data['caption'] = blog.caption
        image_path = os.path.join('static', 'images', blog.image)
        with open(image_path, 'rb') as f:
            image_data = f.read()
            base64_encoded_data = base64.b64encode(image_data).decode('utf-8')
        blog_data['image'] = base64_encoded_data
        blog_data['author'] = blog.author
        blog_data['created_at'] = blog.created_at
        blog_data['author_id'] = blog.user_id
        output.append(blog_data)
    if not len(output):
        return Response(
            response=json.dumps({"message": "No Blogs Exists"}),
            status=401,
            mimetype="application/json"
        )
    return jsonify({'blogs': output})


@app.route(version + '/blog', methods=['GET'])
@token_required
def get_blogs(current_user):
    blogs = Blogs.query.all()
    output = []
    for blog in blogs:
        if blog.id == current_user.id:
            blog_data = {}
            blog_data['blog_id'] = blog.id
            blog_data['caption'] = blog.caption
            image_path = os.path.join('static', 'images', blog.image)
            with open(image_path, 'rb') as f:
                image_data = f.read()
                base64_encoded_data = base64.b64encode(
                    image_data).decode('utf-8')
            blog_data['image'] = base64_encoded_data
            blog_data['author'] = blog.author
            blog_data['created_at'] = blog.created_at
            blog_data['author_id'] = blog.user_id
            output.append(blog_data)
        else:
            return Response(
                response=json.dumps({"message": "No Blogs Exists"}),
                status=401,
                mimetype="application/json")
    if not len(output):
        return Response(
            response=json.dumps({"message": "No Blogs Exists"}),
            status=401,
            mimetype="application/json"
        )
    return jsonify({'blogs': output})


@app.route(version + '/blog', methods=['POST'])
@token_required
def create_blog(current_user):
    caption = request.form['caption']
    author = current_user.username
    user_id = current_user.id
    image = photos.save(request.files['image'])
    new_blog = Blogs(caption=caption,
                     author=author, image=image, user_id=user_id)
    db.session.add(new_blog)
    db.session.commit()
    return jsonify({'message': 'Blog created'})


@app.route(version + '/blog/<blog_id>', methods=['GET'])
@token_required
def get_blog(current_user, blog_id):
    blog = Blogs.query.filter_by(id=blog_id).first()
    if not blog:
        return jsonify({'message': 'No blog found!'})
    blog_data = {}
    blog_data['blog_id'] = blog.id
    blog_data['caption'] = blog.caption
    image_path = os.path.join('static', 'images', blog.image)
    with open(image_path, 'rb') as f:
        image_data = f.read()
        base64_encoded_data = base64.b64encode(image_data).decode('utf-8')
    blog_data['image'] = base64_encoded_data
    blog_data['author'] = blog.author
    blog_data['created_at'] = blog.created_at
    blog_data['author_id'] = blog.user_id
    return jsonify({'blog': blog_data})


# Route to get all blogs of a user
@app.route(version + '/user-blogs/<user_id>', methods=['GET'])
@token_required
def get_user_blogs(current_user, user_id):
    blogs = Blogs.query.filter_by(user_id=user_id).all()
    output = []
    for blog in blogs:
        blog_data = {}
        blog_data['blog_id'] = blog.id
        blog_data['caption'] = blog.caption
        image_path = os.path.join('static', 'images', blog.image)
        with open(image_path, 'rb') as f:
            image_data = f.read()
            base64_encoded_data = base64.b64encode(image_data).decode('utf-8')
        blog_data['image'] = base64_encoded_data
        blog_data['author'] = blog.author
        blog_data['created_at'] = blog.created_at
        blog_data['author_id'] = blog.user_id
        output.append(blog_data)
    if not len(output):
        return Response(
            response=json.dumps({"message": "No Blogs Exists"}),
            status=401,
            mimetype="application/json"
        )
    return jsonify({'blogs': output})


# Route for deleting a blog

@app.route(version + '/blog/<blog_id>', methods=['DELETE'])
def delete_blog(blog_id):
    blog = Blogs.query.filter_by(id=blog_id).first()
    if not blog:
        return jsonify({'message': 'No blog found!'})
    db.session.delete(blog)
    db.session.commit()
    return jsonify({'message': 'Blog deleted'})

# Route for updating caption of a blog


@app.route(version + '/blog/update-caption/<blog_id>', methods=['PUT'])
def update_blog(blog_id):
    blog = Blogs.query.filter_by(id=blog_id).first()
    if not blog:
        return jsonify({'message': 'No blog found!'})
    caption = request.form['caption']
    blog.caption = caption
    db.session.commit()
    return jsonify({'message': 'Blog updated'})
