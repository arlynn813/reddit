from datetime import datetime
from sql import connection_required


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

    def delete(self):
        # TODO: cascade delete (all votes on this post should also be deleted)
        self.__delete()

    @property
    def user(self):
        from user import User  # putting this at the top causes circular import error...
        return User.get(self.user_id)

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
    def objects(cls, post=None):
        entries = cls.__get(post=post)
        return [Vote(entry['value'], entry['user_id'], entry['post_id'], id_=entry['id']) for entry in entries]

    @classmethod
    def get(cls, id_):
        try:
            entry = cls.__get(id_=id_)[0]
        except IndexError:
            return None
        return Vote(entry['value'], entry['user_id'], entry['post_id'], id_=entry['id'])

    @classmethod
    def create(cls, post, value):
        vote = Vote(value, post.user.id, post.id)
        vote.__create()
        return vote  # note: this object does not contain the sql auto generated primary key...

    def delete(self):
        self.__delete()

    def __init__(self, value, user_id, post_id, id_=None):
        self.value = value
        self.user_id = user_id
        self.post_id = post_id
        self.id = id_

    # SQL methods
    @classmethod
    @connection_required()
    def __get(cls, id_=None, post=None):
        if id_:
            return f'SELECT * FROM vote WHERE id={id_};'
        elif post:
            return f'SELECT * FROM vote WHERE post_id={post.id};'
        return 'SELECT * FROM vote;'

    @connection_required(commit=True)
    def __create(self):
        return f'INSERT INTO vote (value, user_id, post_id) VALUES({self.value}, "{self.user_id}", {self.post_id});'

    @connection_required(commit=True)
    def __delete(self):
        return f'DELETE FROM vote WHERE id={self.id};'


if __name__ == '__main__':
    """
    from user import User
    user1 = User.create('Andrew', 'Lynn', 'arlynn813', 'arlynn813@gmail.com')
    user2 = User.create('First', 'Last', 'test_username', 'test@test.com')
    Post.create(user1, 'Title 1', 'This is the content of the first post.')
    Post.create(user1, 'Title 2', 'This is the content of the second post.')
    Post.create(user2, 'Test Title', 'This is test content.')

    print('testing posts from user1 query')
    for p in user1.posts:
        print(p)

    print('testing posts from user2 query')
    for p in user2.posts:
        print(p)

    print('testing all posts query')
    all_posts = Post.objects()
    for p in all_posts:
        print(p)

    print('testing delete')
    for p in all_posts:
        p.delete()
    print(Post.objects())
    """
    from user import User
    from post import Post, Vote

    vote = Vote.get(1)
    print('VOTE: ', vote)
    vote.delete()
    print(Vote.objects())

