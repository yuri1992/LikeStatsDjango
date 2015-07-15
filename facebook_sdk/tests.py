from django.test import TestCase
from .facebook_request import GraphReponse, GraphAPIError, GraphAPIRequest


class MockGraphResponse(object):

    def __init__(self, d):
        self.__dict__.update(d)

    def __getattr__(self, key):
        if key in self.__dict__:
            return self.__dict__[key]

    def __setattr__(self, key, value):
        self.__dict__[key] = value

    def json(self):
        return self.__dict__['response']


class TestGraphResponse(TestCase):

    def setUp(self):
        pass

    def test_json_response(self):
        mock = MockGraphResponse({
            'headers': {
                'content-type': 'application/json; charset=UTF-8'
            },
            'response': {
                'bla': 'bla'
            }
        })
        res = GraphReponse(mock)
        self.assertDictEqual({'bla': 'bla'}, res.response)

        self.assertFalse(res.next_page)
        self.assertFalse(res.previous_page)

    def test_image_response(self):
        mock = MockGraphResponse({
            'headers': {
                'content-type': 'image/jpeg/isdsf'
            },
            'response': {

            },
            'content': {
                'bla': 'asdasdasd'
            },
            'url': 'http://check.com'
        })
        res = GraphReponse(mock)

        self.assertDictEqual({
            'mime-type': 'image/jpeg/isdsf',
            'data': {
                'bla': 'asdasdasd'
            },
            'url': 'http://check.com'
        }, res.response)

        self.assertFalse(res.next_page)
        self.assertFalse(res.previous_page)

    def test_access_token_response(self):
        mock = MockGraphResponse({
            'headers': {
                'content-type': 'html/text'
            },
            'text': "access_token=test_arg&expires=123",
        })
        res = GraphReponse(mock)
        self.assertDictEqual({
            'access_token': 'test_arg',
            'expires': '123',
        }, res.response)
        self.assertFalse(res.next_page)
        self.assertFalse(res.previous_page)

        mock = MockGraphResponse({
            'headers': {
                'content-type': 'html/text'
            },
            'text': "no_token=test_arg&expires=123",
        })
        self.assertRaises(GraphAPIError, lambda: GraphReponse(mock))

    def test_paging(self):
        mock = MockGraphResponse({
            'headers': {
                'content-type': 'application/json; charset=UTF-8'
            },
            'response': {
                'paging': {
                    'next': 'link'
                }
            }
        })
        res = GraphReponse(mock)

        self.assertTrue(res.next_page)
        self.assertEqual('link', res.next_page)
        self.assertFalse(res.previous_page)

        mock = MockGraphResponse({
            'headers': {
                'content-type': 'application/json; charset=UTF-8'
            },
            'response': {
                'paging': {
                    'previous': 'link'
                }
            }
        })
        res = GraphReponse(mock)
        self.assertFalse(res.next_page)
        self.assertTrue(res.previous_page)
        self.assertEqual('link', res.previous_page)


class TestRequestGraph(TestCase):

    def setUp(self):
        self.req = GraphAPIRequest(
            "access_token",
            "/me",
            {}
        )

    def test_initial_request_obj(self):
        self.assertEqual("access_token", self.req.access_token)
        self.assertEqual("/me", self.req.path)
        self.assertEqual({}, self.req.args)
        self.assertEqual({}, self.req.response)

    def test_get_request_no_access(self):
        res = self.req.get()
        self.assertEqual(
            {u'error': {u'message': u'Invalid OAuth access token.',
                        u'code': 190, u'type': u'OAuthException'}},
            res.response
        )
        self.assertFalse(res.previous_page)
        self.assertFalse(res.next_page)
