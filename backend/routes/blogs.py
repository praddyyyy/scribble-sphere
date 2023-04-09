from routes import app, version, db, redis_cli
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
    blog_ids = redis_cli.keys('blog:*')
    blogs = []
    cache_output = []
    db_output = []
    if blog_ids:
        print('HIT REDIS CACHE')
        for blog_id in blog_ids:
            blog = json.loads(redis_cli.get(blog_id))

            blog_data = {}
            blog_data['blog_id'] = blog['blog_id']
            blog_data['caption'] = blog['caption']
            image_path = os.path.join('static', 'images', blog['image'])
            with open(image_path, 'rb') as f:
                image_data = f.read()
                base64_encoded_data = base64.b64encode(
                    image_data).decode('utf-8')
            blog_data['image'] = base64_encoded_data
            blog_data['author'] = blog['author']
            blog_data['created_at'] = blog['created_at']
            blog_data['author_id'] = blog['user_id']
            cache_output.append(blog_data)
    if not len(cache_output):
        print('HIT DATABASE')
        blogs = Blogs.query.order_by(Blogs.created_at.desc()).all()
        for blog in blogs:
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
            db_output.append(blog_data)

    if not len(cache_output) and not len(db_output):
        return Response(
            response=json.dumps({"message": "No Blogs Exists"}),
            status=401,
            mimetype="application/json"
        )
    return jsonify({'blogs': cache_output if len(cache_output) else db_output})


@app.route(version + '/blog', methods=['GET'])
@token_required
def get_blogs(current_user):
    blogs = []
    cache_output = []
    db_output = []
    blog_keys = redis_cli.keys(f'blog:*')
    if blog_keys:
        print('HIT REDIS CACHE')
       # Filter the blog keys to only include those belonging to the current user
        user_blog_keys = [key for key in blog_keys if json.loads(
            redis_cli.get(key))['user_id'] == current_user.id]

        # Use the Redis get() method to get the values of the filtered blog keys
        blog_values = [redis_cli.get(key) for key in user_blog_keys]

        # Deserialize the blog values from JSON to Python objects
        blogs = [json.loads(value) for value in blog_values]
        for blog in blogs:
            print(blog)
            blog_data = {}
            blog_data['blog_id'] = blog['blog_id']
            blog_data['caption'] = blog['caption']
            image_path = os.path.join('static', 'images', blog['image'])
            with open(image_path, 'rb') as f:
                image_data = f.read()
                base64_encoded_data = base64.b64encode(
                    image_data).decode('utf-8')
            blog_data['image'] = base64_encoded_data
            blog_data['author'] = blog['author']
            blog_data['created_at'] = blog['created_at']
            blog_data['author_id'] = blog['user_id']
            cache_output.append(blog_data)
    if not len(cache_output):
        print('HIT DATABASE')
        blogs = Blogs.query.all()
        for blog in blogs:
            if blog.user_id == current_user.id:
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
                db_output.append(blog_data)

    if not len(cache_output) and not len(db_output):
        return Response(
            response=json.dumps({"message": "No Blogs Exists"}),
            status=401,
            mimetype="application/json"
        )

    return jsonify({'blogs': cache_output if len(cache_output) else db_output})


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

    blog_data = {
        'blog_id': new_blog.id,
        'caption': caption,
        'author': author,
        'image': image,
        'user_id': user_id,
        'created_at': str(new_blog.created_at)
    }
    redis_cli.set(f'blog:{new_blog.id}', json.dumps(blog_data))

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
    blogs = []
    cache_output = []
    db_output = []
    blog_keys = redis_cli.keys(f'blog:*')
    if blog_keys:
        print('HIT REDIS CACHE')
       # Filter the blog keys to only include those belonging to the current user
        user_blog_keys = [key for key in blog_keys if json.loads(redis_cli.get(key))[
            'user_id'] == user_id]

        # Use the Redis get() method to get the values of the filtered blog keys
        blog_values = [redis_cli.get(key) for key in user_blog_keys]

        # Deserialize the blog values from JSON to Python objects
        blogs = [json.loads(value) for value in blog_values]
        for blog in blogs:
            blog_data = {}
            blog_data['blog_id'] = blog['blog_id']
            blog_data['caption'] = blog['caption']
            image_path = os.path.join('static', 'images', blog['image'])
            with open(image_path, 'rb') as f:
                image_data = f.read()
                base64_encoded_data = base64.b64encode(
                    image_data).decode('utf-8')
            blog_data['image'] = base64_encoded_data
            blog_data['author'] = blog['author']
            blog_data['created_at'] = blog['created_at']
            blog_data['author_id'] = blog['user_id']
            cache_output.append(blog_data)
    if not len(cache_output):
        print('HIT DATABASE')
        blogs = Blogs.query.filter_by(user_id=user_id).all()
        for blog in blogs:
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
            db_output.append(blog_data)
    if not len(cache_output) and not len(db_output):
        return Response(
            response=json.dumps({"message": "No Blogs Exists"}),
            status=401,
            mimetype="application/json"
        )
    return jsonify({'blogs': cache_output if len(cache_output) else db_output})


# Route for deleting a blog

@app.route(version + '/blog/<blog_id>', methods=['DELETE'])
def delete_blog(blog_id):
    # Check if the blog exists in Redis
    blog_key = f'blog:{blog_id}'
    if not redis_cli.exists(blog_key):
        return jsonify({'error': 'Blog not found'}), 404
    # Delete the blog from Redis
    redis_cli.delete(blog_key)
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
