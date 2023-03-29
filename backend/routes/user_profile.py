from routes import app, version, db
from flask import request, jsonify, Response
from models.user_profile_model import UserProfile

from helpers import token_required, token_generate

# Route to get current user profile


@app.route(version + '/user-profile', methods=['GET'])
@token_required
def get_user_profile(current_user):
    user_profile = UserProfile.query.filter_by(user=current_user.id).first()
    if not user_profile:
        return jsonify({'message': 'No profile found!', 'success': False}), 200
    user_profile_data = {}
    user_profile_data['user_id'] = user_profile.user
    user_profile_data['description'] = user_profile.description
    user_profile_data['current_location'] = user_profile.current_location
    user_profile_data['profession'] = user_profile.profession
    user_profile_data['current_company'] = user_profile.current_company
    user_profile_data['primary_link'] = user_profile.primary_link

    return jsonify({'user_profile': user_profile_data})

# Route to get user profile by user id


@app.route(version + '/user-profile/<int:user_id>', methods=['GET'])
@token_required
def get_user_profile_by_id(current_user, user_id):
    user_profile = UserProfile.query.filter_by(user=user_id).first()
    if not user_profile:
        return jsonify({'message': 'No profile found!', 'success': False}), 200
    user_profile_data = {}
    user_profile_data['user_id'] = user_profile.user
    user_profile_data['description'] = user_profile.description
    user_profile_data['current_location'] = user_profile.current_location
    user_profile_data['profession'] = user_profile.profession
    user_profile_data['current_company'] = user_profile.current_company
    user_profile_data['primary_link'] = user_profile.primary_link

    return jsonify({'user_profile': user_profile_data})


# @app.route(version + '/user-profile', methods=['POST'])
# @token_required
# def create_user_profile(current_user):
#     description = request.form['description']
#     current_location = request.form['current_location']
#     profession = request.form['profession']
#     current_company = request.form['current_company']
#     primary_link = request.form['primary_link']
#     user_id = current_user.id
#     new_user_profile = UserProfile(description=description, current_location=current_location, profession=profession,
#                                    current_company=current_company, primary_link=primary_link, user=user_id)
#     db.session.add(new_user_profile)
#     db.session.commit()
#     return jsonify({'message': 'User Profile created'})

# Route to update user profile
@app.route(version + '/user-profile', methods=['POST'])
@token_required
def update_user_profile(current_user):
    user_profile = UserProfile.query.filter_by(user=current_user.id).first()
    if not user_profile:
        if 'description' in request.form and request.form['description'] == 'null':
            description = None
        elif 'description' in request.form and request.form['description'] != '':
            description = request.form['description']
        else:
            description = None

        if 'current_location' in request.form and request.form['current_location'] == 'null':
            current_location = None
        elif 'current_location' in request.form and request.form['current_location'] != '':
            current_location = request.form['current_location']
        else:
            current_location = None

        if 'profession' in request.form and request.form['profession'] == 'null':
            profession = None
        elif 'profession' in request.form and request.form['profession'] != '':
            profession = request.form['profession']
        else:
            profession = None

        if 'current_company' in request.form and request.form['current_company'] == 'null':
            current_company = None
        elif 'current_company' in request.form and request.form['current_company'] != '':
            current_company = request.form['current_company']
        else:
            current_company = None

        if 'primary_link' in request.form and request.form['primary_link'] == 'null':
            primary_link = None
        elif 'primary_link' in request.form and request.form['primary_link'] != '':
            primary_link = request.form['primary_link']
        else:
            primary_link = None

        new_user_profile = UserProfile(description=description, current_location=current_location, profession=profession,
                                       current_company=current_company, primary_link=primary_link, user=current_user.id)
        db.session.add(new_user_profile)
        db.session.commit()
        return jsonify({'message': 'User Profile created', "success": True,
                        "user_profile": {"description": description, "current_location": current_location, "profession": profession, "current_company": current_company, "primary_link": primary_link}})

    if user_profile.user != current_user.id:
        return jsonify({'message': 'You are not authorized to update this profile', 'success': False}), 200
    # print(request.form['description'])
    if 'description' in request.form and request.form['description'] == 'null':
        user_profile.description = None
    elif 'description' in request.form and request.form['description'] != '':
        user_profile.description = request.form['description']
    else:
        user_profile.description = None

    if 'current_location' in request.form and request.form['current_location'] == 'null':
        user_profile.current_location = None
    elif 'current_location' in request.form and request.form['current_location'] != '':
        user_profile.current_location = request.form['current_location']
    else:
        user_profile.current_location = None

    if 'profession' in request.form and request.form['profession'] == 'null':
        user_profile.profession = None
    elif 'profession' in request.form and request.form['profession'] != '':
        user_profile.profession = request.form['profession']
    else:
        user_profile.profession = None

    if 'current_company' in request.form and request.form['current_company'] == 'null':
        user_profile.current_company = None
    elif 'current_company' in request.form and request.form['current_company'] != '':
        user_profile.current_company = request.form['current_company']
    else:
        user_profile.current_company = None

    if 'primary_link' in request.form and request.form['primary_link'] == 'null':
        user_profile.primary_link = None
    elif 'primary_link' in request.form and request.form['primary_link'] != '':
        user_profile.primary_link = request.form['primary_link']
    else:
        user_profile.primary_link = None
    db.session.commit()
    return jsonify({'message': 'User Profile updated', 'success': True, "user_profile": {"description": user_profile.description, "current_location": user_profile.current_location, "profession": user_profile.profession, "current_company": user_profile.current_company, "primary_link": user_profile.primary_link}})
