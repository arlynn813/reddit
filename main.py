import hashlib
from flask import Flask, jsonify, redirect, request, render_template, session, url_for
from models import Post, User, Vote


app = Flask(__name__, static_folder='')
app.secret_key = '8e55e0f12a92a2a38a084ef464f68415'  # generated from secrets.token_hex(16) in python console


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user_id = hashlib.sha1(request.form['username'].encode('utf-8')).hexdigest()
        user = User.get(user_id)
        if not user:
            user = User.create(request.form['first_name'], request.form['last_name'], request.form['username'],
                               request.form['email'])
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
    return render_template('post.html', post=Post.get(post_id))


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
