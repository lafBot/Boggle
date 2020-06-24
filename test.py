from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle

app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

class FlaskTests(TestCase):

    def test_homepage(self):
        """Ensure home HTML is displayed and session values are set"""
        with app.test_client() as client:
            res = client.get('/')
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('High Score:', html)
            self.assertNotEqual(len(session['board']), 0)
            self.assertIsNone(session.get('highscore'))
            self.assertIsNone(session.get('nplays'))

    def test_valid_word(self):
        """Make sure valid word within board passes"""
        with app.test_client() as client:

            # set board in session for testing
            with client.session_transaction() as alt_session:
                alt_session['board'] = [['B', 'O', 'A', 'R', 'D'],
                                        ['B', 'O', 'A', 'R', 'D'],
                                        ['B', 'O', 'A', 'R', 'D'],
                                        ['B', 'O', 'A', 'R', 'D'],
                                        ['B', 'O', 'A', 'R', 'D']]
            res = client.get('/check-word?word=board')
            self.assertEqual(res.json['result'], 'ok')
    
    def test_real_word(self):
        """Check if word is within dictionary"""
        with app.test_client() as client:
            client.get('/')
            result = client.get('/check-word?word=asdasd')

            self.assertEqual(result.json['result'], 'not-word')

    def test_not_on_board(self):
        """Check words not within board fail"""
        with app.test_client() as client:
            client.get('/')
            result = client.get('/check-word?word=exuberant')
            self.assertEqual(result.json['result'], 'not-on-board')