import hashlib
from flask import Flask, redirect, request, render_template, url_for
from models import Post, User


# TODO: Fix static_folder argument. Currently waiting on instructor answer on piazza...
# Fixing this argument also entails resolving file paths in index.html
app = Flask(__name__, static_folder='scripts')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user_id = hashlib.sha1(request.form['username'].encode('utf-8')).hexdigest()
        user = User.get(user_id)
        if not user:
            user = User.create(request.form['first_name'], request.form['last_name'], request.form['username'],
                               request.form['email'])
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
    post = Post.get(post_id)
    post.delete()
    return {}


if __name__ == '__main__':
    app.run(host='localhost', port=8000, debug=True)
