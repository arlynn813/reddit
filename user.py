from sql import connection_required


class User:
    @classmethod
    def objects(cls):
        entries = cls.__get()
        return [User(entry['first_name'], entry['last_name'], entry['username'], entry['email']) for entry in entries]

    @classmethod
    def get(cls, id_):
        entry = cls.__get(id_=id_)[0]
        return User(entry['first_name'], entry['last_name'], entry['username'], entry['email'])

    @classmethod
    def create(cls, first_name, last_name, username, email):
        user = User(first_name, last_name, username, email)
        user.__create()
        return user

    def delete(self):
        # TODO: cascade delete (all of this user's posts and votes should also be deleted)
        self.__delete()

    # Do not explicitly call the below methods. These are used internally by the above methods.
    # For example, calling init will not store the object in the database.
    def __init__(self, first_name, last_name, username, email):
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.email = email
        self.id = hash(username)

    # SQL methods
    @classmethod
    @connection_required()
    def __get(cls, id_=None):
        if id_:
            return f'SELECT * FROM user WHERE id={id_};'
        return f'SELECT * FROM user;'

    @connection_required(commit=True)
    def __create(self):
        return f'INSERT INTO user VALUES("{self.first_name}", "{self.last_name}", "{self.username}", "{self.email}", "{self.id}");'

    @connection_required(commit=True)
    def __delete(self):
        return f'DELETE FROM user WHERE id={self.id};'


if __name__ == "__main__":
    test_user = User.create('Andrew', 'Lynn', 'arlynn813', 'arlynn813@gmail.com')  # creates a new entry in the user table and returns user object
    users = User.objects()  # returns a list of user objects from all entries stored in user table
    print([u.username for u in users])
    user = User.get(id_=test_user.id)  # returns a single user object given by id from user table
    print(user.username)
    user.delete()
    print(User.objects())
