import hashlib
from datetime import datetime
from sql import connection_required


class User:
    @classmethod
    def objects(cls):
        entries = cls.__get()
        return [User(entry['first_name'], entry['last_name'], entry['username'], entry['email']) for entry in entries]

    @classmethod
    def get(cls, id_):
        try:
            entry = cls.__get(id_=id_)[0]
        except IndexError:
            return None
        return User(entry['first_name'], entry['last_name'], entry['username'], entry['email'])

    @classmethod
    def create(cls, first_name, last_name, username, email):
        user = User(first_name, last_name, username, email)
        user.__create()
        return user

    @classmethod
    def generate_tsv(cls):
        with open('data/user.tsv', 'w') as fp:
            fp.write('\t'.join(['first_name', 'last_name', 'username', 'email', 'id']) + '\n')
            for u in User.objects():
                fp.write('\t'.join([u.first_name, u.last_name, u.username, u.email, u.id]) + '\n')

    def delete(self):
        # TODO: Test cascade delete...
        for vote in self.votes:
            vote.delete()
        for post in self.posts:
            post.delete()
        self.__delete()

    def post(self, title, content):
        Post.create(self, title, content)

    @property
    def votes(self):
        return Vote.objects(user=self)

    @property
    def posts(self):
        return Post.objects(user=self)

    @property
    def feed(self):
        return Post.objects(user=self, exclude=True)

    # Do not explicitly call the below methods. These are used internally by the above methods.
    # For example, calling init will not store the object in the database.
    def __init__(self, first_name, last_name, username, email):
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.email = email
        self.id = hashlib.sha1(username.encode('utf-8')).hexdigest()

    def __str__(self):
        return self.username

    # SQL methods
    @classmethod
    @connection_required()
    def __get(cls, id_=None):
        if id_:
            return f'SELECT * FROM user WHERE id="{id_}";'
        return f'SELECT * FROM user;'

    @connection_required(commit=True)
    def __create(self):
        return f'INSERT INTO user VALUES("{self.first_name}", "{self.last_name}", "{self.username}", "{self.email}", "{self.id}");'

    @connection_required(commit=True)
    def __delete(self):
        return f'DELETE FROM user WHERE id="{self.id}";'


class Post:
    @classmethod
    def objects(cls, user=None, exclude=False):
        entries = cls.__get(user=user, exclude=exclude)
        posts = [Post(entry['title'], entry['content'], entry['created_at'], entry['user_id'], id_=entry['id']
                      ) for entry in entries]
        return sorted(posts, key=lambda x:x.created_at, reverse=True)

    @classmethod
    def get(cls, id_):
        try:
            entry = cls.__get(id_=id_)[0]
        except IndexError:
            return None
        return Post(entry['title'], entry['content'], entry['created_at'], entry['user_id'], id_=entry['id'])

    @classmethod
    def create(cls, user, title, content):
        post = Post(title, content, datetime.now(), user.id)
        post.__create()
        return post  # note: this object does not contain the sql auto generated primary key...

    @classmethod
    def generate_tsv(cls):
        with open('data/post.tsv', 'w') as fp:
            fp.write('\t'.join(['title', 'content', 'id', 'created_at', 'user_id']) + '\n')
            for p in Post.objects():
                fp.write('\t'.join([p.title, p.content, str(p.id), p.created_at, p.user_id]) + '\n')

    def delete(self):
        # TODO: Test cascade delete
        for vote in self.votes:
            vote.delete()
        self.__delete()

    def vote(self, user, value):
        v = Vote.get(post=self, user=user)
        if v:
            v.update(value)
        else:
            v = Vote.create(self, value, user)
        return v

    @property
    def user(self):
        return User.get(self.user_id)

    @property
    def vote_count(self):
        return sum([vote.value for vote in Vote.objects(post=self)])

    @property
    def votes(self):
        return Vote.objects(post=self)

    # Do not explicitly call the below methods. These are used internally by the above methods.
    # For example, calling init will not store the object in the database.
    def __init__(self, title, content, created_at, user_id, id_=None):
        self.title = title
        self.content = content
        self.created_at = created_at
        self.id = id_
        self.user_id = user_id

    def __str__(self):
        return f'{self.title} - {self.user.username}'

    # SQL methods
    @classmethod
    @connection_required()
    def __get(cls, id_=None, user=None, exclude=False):
        if id_:
            return f'SELECT * FROM post WHERE id={id_};'
        elif user:
            if exclude:
                return f'SELECT * FROM post WHERE user_id!="{user.id}";'
            return f'SELECT * FROM post WHERE user_id="{user.id}";'
        return 'SELECT * FROM post;'

    @connection_required(commit=True)
    def __create(self):
        return f'INSERT INTO post (title, content, user_id) VALUES("{self.title}", "{self.content}", "{self.user_id}");'

    @connection_required(commit=True)
    def __delete(self):
        return f'DELETE FROM post WHERE id={self.id};'


class Vote:
    @classmethod
    def objects(cls, post=None, user=None):
        entries = cls.__get(post=post, user=user)
        return [Vote(entry['value'], entry['user_id'], entry['post_id'], id_=entry['id']) for entry in entries]

    @classmethod
    def get(cls, id_=None, post=None, user=None):
        try:
            entry = cls.__get(id_=id_, post=post, user=user)[0]
        except IndexError:
            return None
        return Vote(entry['value'], entry['user_id'], entry['post_id'], id_=entry['id'])

    @classmethod
    def create(cls, post, value, user):
        vote = Vote(value, user.id, post.id)
        vote.__create()
        return vote  # note: this object does not contain the sql auto generated primary key...

    @classmethod
    def generate_tsv(cls):
        with open('data/vote.tsv', 'w') as fp:
            fp.write('\t'.join(['value', 'user_id', 'post_id', 'id']) + '\n')
            for v in Vote.objects():
                fp.write('\t'.join([v.value, v.user_id, str(v.post_id), str(v.id)]) + '\n')

    def delete(self):
        self.__delete()

    def update(self, value):
        self.value = value
        self.__update()

    def __init__(self, value, user_id, post_id, id_=None):
        self.value = value
        self.user_id = user_id
        self.post_id = post_id
        self.id = id_

    # SQL methods
    @classmethod
    @connection_required()
    def __get(cls, id_=None, post=None, user=None):
        if id_:
            return f'SELECT * FROM vote WHERE id={id_};'
        elif post and user:
            return f'SELECT * FROM vote WHERE post_id={post.id} AND user_id="{user.id}";'
        elif post:
            return f'SELECT * FROM vote WHERE post_id={post.id};'
        elif user:
            return f'SELECT * FROM vote WHERE user_id={user.id};'
        return 'SELECT * FROM vote;'

    @connection_required(commit=True)
    def __create(self):
        return f'INSERT INTO vote (value, user_id, post_id) VALUES({self.value}, "{self.user_id}", {self.post_id});'

    @connection_required(commit=True)
    def __delete(self):
        return f'DELETE FROM vote WHERE id={self.id};'

    @connection_required(commit=True)
    def __update(self):
        return f'UPDATE vote SET value={self.value} WHERE id={self.id};'
