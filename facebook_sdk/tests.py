from django.test import TestCase
from .facebook_request import GraphReponse


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
    			'content-type' : 'json'
    		},
    		'response': {
    			'bla':'bla'
    		}
    	})
    	res = GraphReponse(mock)
    	self.assertDictEqual({'bla':'bla'},res.response)

    	self.assertFalse(res.next_page)
    	self.assertFalse(res.previous_page)

    def test_image_response(self):
    	mock = MockGraphResponse({
    		'headers': {
    			'content-type' : 'image/jpeg/isdsf'
    		},
    		'response': {
    			'bla':'bla'
    		}
    		'url':'http'
    	})
    	res = GraphReponse(mock)
    	self.assertDictEqual({'bla':'bla'},res.response)
    	
    	self.assertFalse(res.next_page)
    	self.assertFalse(res.previous_page)
