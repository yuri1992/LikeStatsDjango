try:
    from urllib.parse import parse_qs, urlencode
except ImportError:
    from urlparse import parse_qs
    from urllib import urlencode

class GraphAPIRequest(object):
    """
        Graph Api Request Object
    """
    def __init__(self, access_token, path, args):
        self.path = path
        self.access_token = access_token
        self.args = args

    def get(self):
        """
            return the response from the request
        """
        return self._requset()

    def get_all(self):
        """
            Fetch All data, until there no more data to retrive form.
            Facebook have limiting the numbers of items you can retrive
            on each Request.
        """
        res = []
        self.response = self._requset(self.path)
        if 'data' in response:
            res = res + response['data']
        while self.next_page:
            self.response = self._requset(self.next_page)
            if 'data' in response:
                res = res + response['data']

        self.response = res
        return self.response

    def request(access_token, path, args=None,
                post_args=None, files=None, method=None, timeout=60):
        args = args or {}

        if post_args is not None:
            method = "POST"

        if access_token:
            if post_args is not None:
                post_args["access_token"] = access_token
            else:
                args["access_token"] = access_token

        if not path.startswith('https://'):
            path = "https://graph.facebook.com/" + path
        try:
            response = requests.request(method or "GET",
                                        path,
                                        timeout=timeout,
                                        params=args,
                                        data=post_args,
                                        files=files)
        except requests.HTTPError as e:
            response = json.loads(e.read())
            raise GraphAPIError(response)
        return result

class GraphReponse(object):
    def __init__(self, raw_reponse):
        self.raw_reponse = raw_reponse
        self._response = {}
        self.serialize_raw_response()

    def serialize_raw_response(self):
        """
        """
        response = self.raw_reponse
        headers = response.headers

        if 'json' in headers['content-type']:
            result = response.json()
        elif 'image/' in headers['content-type']:
            mimetype = headers['content-type']
            result = {"data": response.content,
                      "mime-type": mimetype,
                      "url": response.url}
        elif "access_token" in parse_qs(response.text):
            query_str = parse_qs(response.text)
            if "access_token" in query_str:
                result = {"access_token": query_str["access_token"][0]}
                if "expires" in query_str:
                    result["expires"] = query_str["expires"][0]
            else:
                pass
                raise GraphAPIError(response.json())
        else:
            raise GraphAPIError('Maintype was not text, image, or querystring')

        if result and isinstance(result, dict) and result.get("error"):
            pass
            raise GraphAPIError(result)

        self._response = result



    @property
    def response(self):
        return self._response
    

    @property
    def next_page(self):
        if 'paging' in self.response and 'next' in self.response['paging']:
            return self.response['paging']['next']
        return False

    @property
    def previous_page(self):
        if 'paging' in self.response and 'previous' in self.response:
            return self.response['paging']['previous']
        return False

    

class GraphAPIError(Exception):

    def __init__(self, result):
        self.result = result
        try:
            self.type = result["error_code"]
        except:
            self.type = ""

        # OAuth 2.0 Draft 10
        try:
            self.message = result["error_description"]
        except:
            # OAuth 2.0 Draft 00
            try:
                self.message = result["error"]["message"]
            except:
                # REST server style
                try:
                    self.message = result["error_msg"]
                except:
                    self.message = result

        Exception.__init__(self, self.message)