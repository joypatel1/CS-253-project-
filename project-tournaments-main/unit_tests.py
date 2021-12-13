import unittest
import os
import app as flaskr
import tempfile
# docs.python.org/3.10/library/unittest.html used as a reference to set up unit testing. Create a class for the login methods' unit tests


class FlaskrTestCase(unittest.TestCase):
    # --- Test if the hashing function hashed the password.
    def setUp(self):
        self.db_fd, flaskr.app.config['DATABASE'] = tempfile.mkstemp()
        flaskr.app.testing = True
        self.app = flaskr.app.test_client()
        with flaskr.app.app_context():
            flaskr.init_db()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(flaskr.app.config['DATABASE'])

    def test_empty_db(self):
        rv = self.app.get('/')
        assert b'No entries here so far' in rv.data

    def login(self, username, password):
        return self.app.post('/login', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)

    def logout(self):
        return self.app.get('/logout', follow_redirects=True)

    def show_bracket4(self):
        data = self.app.post('/new-bracket4', data=dict(
                            name='2k Tournament',
                            player_name='Kyle',
                            game_name='NBA 2k22',
                            description='This is an NBA 2k22 Tournament for fun'),
                            follow_redirects=True)
        assert '2k Tournament' in data
        assert 'Kyle' in data
        assert 'NBA 2k22' in data
        assert 'This is an NBA 2k22 Tournament for fun' in data

    def show_bracket8(self):
        data = self.app.post('/new-bracket8', data=dict(
            name='Massive Tournament',
            player_name='Ian',
            game_name='Fortnite',
            description='Intense Fortnite tournament'),
                             follow_redirects=True)
        assert 'Massive Tournament' in data
        assert 'Ian' in data
        assert 'Fortnite' in data
        assert 'Intense Fortnite tournament' in data

    def show_bracket16(self):
        data = self.app.post('/new-bracket16', data=dict(
            name='Biggest Bracket Ever',
            player_name='Joy',
            game_name='Dota',
            description='Dota tournament for money'),
                             follow_redirects=True)
        assert 'Biggest Bracket Ever' in data
        assert 'Joy' in data
        assert 'Dota' in data
        assert 'Dota tournament for money' in data

    if __name__ == '__main__':
        unittest.main()


