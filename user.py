import hashlib
from post import Post
from sql import connection_required


class User:
    @classmethod
    def objects(cls):
        entries = cls.__get()
        return [User(entry['first_name'], entry['last_name'], entry['username'], entry['email']) for entry in entries]

    @classmethod
    def get(cls, id_):
        entry = cls.__get(id_=id_)
        if entry:
            return User(entry[0]['first_name'], entry[0]['last_name'], entry[0]['username'], entry[0]['email'])
        return None

    @classmethod
    def create(cls, first_name, last_name, username, email):
        user = User(first_name, last_name, username, email)
        user.__create()
        return user

    def delete(self):
        # TODO: cascade delete (all of this user's posts and votes should also be deleted)
        self.__delete()

    def post(self, title, content):
        Post.create(self, title, content)

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


if __name__ == "__main__":
    user = User.create('Andrew', 'Lynn', 'arlynn813', 'arlynn813@gmail.com')
    user.post('Title 1', 'test')
    user.post('Title 2', 'test')

    user2 = User.create('First', 'Last', 'username', 'test@test.com')
    user2.post('Title 1', 'test')

    print('\nuser posts')
    for p in user.posts:
        print(p)

    print('\nuser2 posts')
    for p in user2.posts:
        print(p)

    print('\nuser2 feed')
    for p in user2.feed:
        print(p)
