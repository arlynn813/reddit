import hashlib
import os
from flask import Flask, jsonify, redirect, request, render_template, session, url_for
from models import Post, User, Vote
from werkzeug.utils import secure_filename


app = Flask(__name__, static_folder='')
app.config['IMG_FOLDER'] = os.path.join(app.root_path, 'img')
# We would normally hide the secret in an environment variable or dev_secret.py (outside of VCS).
# Although, I am just letting it sit here since we are not deploying this project to a live server.
app.secret_key = '8e55e0f12a92a2a38a084ef464f68415'  # generated from secrets.token_hex(16) in python console


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user_id = hashlib.sha1(request.form['username'].encode('utf-8')).hexdigest()
        user = User.get(user_id)
        if not user:
            picture = request.files['picture']
            picture_filename = picture.filename
            if picture_filename:
                os.mkdir(os.path.join(app.config['IMG_FOLDER'], user_id))
                picture.save(os.path.join(app.config['IMG_FOLDER'], user_id, picture_filename))
            user = User.create(request.form['username'], request.form['email'], picture_filename)
        session['user_id'] = user.id
        return redirect(url_for('feed', user_id=user.id))
    return render_template('register.html')


@app.route('/<user_id>/feed', methods=['GET'])
def feed(user_id):
    return render_template('feed.html', user=User.get(user_id))


@app.route('/<user_id>/profile', methods=['GET'])
def profile(user_id):
    return render_template('profile.html', user=User.get(user_id))


@app.route('/<user_id>/create', methods=['GET', 'POST'])
def create(user_id):
    user = User.get(user_id)
    if request.method == 'POST':
        user.post(request.form['title'], request.form['content'])
        return redirect(url_for('profile', user_id=user_id))
    return render_template('create.html', user=user)


@app.route('/posts/<post_id>', methods=['GET'])
def post(post_id):
    p = Post.get(post_id)
    v = Vote.get(post=p, user=User.get(session['user_id']))
    return render_template('post.html', post=p, vote=v, user=User.get(session['user_id']))


@app.route('/getTSVdump', methods=['GET'])
def tsv():
    User.generate_tsv()
    Post.generate_tsv()
    Vote.generate_tsv()
    return render_template('tsv.html')


# AJAX routes - Do not directly render these functions.
# AJAX routes are used internally in scripts
@app.route('/<user_id>/profile/<post_id>/delete', methods=['GET'])
def delete_post(user_id, post_id):
    if session['user_id'] == user_id:
        p = Post.get(post_id)
        p.delete()
        return 'success', 200
    return 'failure', 500


@app.route('/posts/<post_id>/vote', methods=['POST'])
def vote(post_id):
    p = Post.get(post_id)
    user = User.get(session['user_id'])
    p.vote(user, request.form['value'])
    return jsonify(vote_value=p.vote_count)


if __name__ == '__main__':
    app.run(host='localhost', port=8000, debug=True)
