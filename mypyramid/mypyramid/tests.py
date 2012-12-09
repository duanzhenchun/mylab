import unittest
import transaction

from pyramid import testing

from .models import DBSession

TEST_NAME = 'douban_123'
TEST_TOKEN = 'token=abc&secret=edf'

class TestMyView(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()
        from sqlalchemy import create_engine
        engine = create_engine('sqlite://')
        from .models import (
            Base,
            OauthUser,
            )
        DBSession.configure(bind=engine)
        Base.metadata.create_all(engine)
        with transaction.manager:
            user = OauthUser(name=TEST_NAME, token=TEST_TOKEN)
            DBSession.add(user)

    def tearDown(self):
        DBSession.remove()
        testing.tearDown()

    def test_oauthuser_list(self):
        from mypyramid.views.oauthuser import user_list
        request = testing.DummyRequest()
        info = user_list(request)
        self.assertEqual(len(info['users']), 1)
        self.assertEqual(info['users'][0].name, TEST_NAME)
        self.assertEqual(info['users'][0].token, TEST_TOKEN)
