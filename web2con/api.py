import urllib2

from exceptions import Exception

from .auth import NoAuth

def _py26OrGreater():
    import sys
    return sys.hexversion > 0x20600f0

if _py26OrGreater():
    import json
else:
    import simplejson as json

class Error(Exception):
    """
    Base Exception thrown by the Web2Connector object when there is a
    general error interacting with the API.
    """
    pass

class HttpError(Error):
    """
    Exception thrown by the Web2Connector object when there is an HTTP
    error interacting with the API.
    """
    def __init__(self, e, uri, suffix, uriparts):
      self.e = e
      self.uri = uri
      self.suffix = suffix
      self.uriparts = uriparts

    def __str__(self):
        return (
            "Received status %i for URL: %s.%s using parameters: "
            "(%s)\ndetails: %s" %(
                self.e.code, self.uri, self.suffix, self.uriparts,
                self.e.fp.read()))

class Response(object):
    """
    Response from a web API request. Behaves like a list or a string
    (depending on requested format) but it has a few other interesting
    attributes.

    `headers` gives you access to the response headers as an
    httplib.HTTPHeaders instance. You can do
    `response.headers.getheader('h')` to retrieve a header.
    """
    def __init__(self, headers):
        self.headers = headers


# Multiple inheritance makes my inner Java nerd cry. Why can't I just
# add arbitrary attributes to list or str objects?! Guido, we need to
# talk.
class JsonListResponse(Response, list):
    __doc__ = """JSON Response
    """ + Response.__doc__
    def __init__(self, lst, headers):
        Response.__init__(self, headers)
        list.__init__(self, lst)
class JsonDictResponse(Response, dict):
    __doc__ = """JSON Response
    """ + Response.__doc__
    def __init__(self, d, headers):
        Response.__init__(self, headers)
        dict.__init__(self, d)

class StrResponse(Response, str):
    __doc__ = """String Response
    """ + Response.__doc__


def handle_json(stream):
    res = json.loads(stream.read())
    response_cls = (
        JsonListResponse if type(res) is list
        else JsonDictResponse)
    return response_cls(res, stream.headers)


def handle_str(stream):
    r = StrResponse(stream.read())
    r.headers = stream.headers
    return r

class Descriptor(object):
    def __init__(
        self, auth, response_handler, domain,
        protocol, suffix, headers):
        self.auth = auth
        self.response_handler = response_handler
        self.domain = domain
        self.protocol = protocol
        self.suffix = suffix
        self.headers = headers

class Call(object):
    def __init__(self, descriptor, uriparts):
        self.d = descriptor
        self.uriparts = uriparts

    def __getattr__(self, k):
        try:
            return object.__getattr__(self, k)
        except AttributeError:
            return Call(self.d, self.uriparts + (k,))

    def __call__(self, **kwargs):
        # Build the uri.
        uriparts = []
        for uripart in self.uriparts:
            # If this part matches a keyword argument, use the
            # supplied value otherwise, just use the part.
            uriparts.append(unicode(kwargs.pop(uripart, uripart)))
        uri = u'/'.join(uriparts)

        method = "GET"
        #for action in POST_ACTIONS:
        #    if uri.endswith(action):
        #        method = "POST"
        #        break

        # If an id kwarg is present and there is no id to fill in in
        # the list of uriparts, assume the id goes at the end.
        id = kwargs.pop('id', None)
        if id:
            uri += "/%s" %(id)

        uriBase = "%s://%s/%s%s" %(
            self.d.protocol, self.d.domain, uri, self.d.suffix)

        headers = dict(self.d.headers)
        if self.d.auth:
            headers.update(self.d.auth.generate_headers(uriBase, method, kwargs))
            arg_data = self.d.auth.encode_params(uriBase, method, kwargs)
            if method == 'GET':
                if arg_data:
                    uriBase += '?' + arg_data
                body = None
            else:
                body = arg_data

        req = urllib2.Request(uriBase, body, headers)

        try:
            stream = urllib2.urlopen(req)
            return self.d.response_handler(stream)
        except urllib2.HTTPError, e:
            if (e.code == 304):
                return []
            else:
                raise HttpError(e, uri, self.d.suffix, arg_data)

class Web2Connector(Call):
    """
    The base of all Web API calls.
    """
    def __init__(self, domain, auth=None, response_handler=None, uriparts=None,
                 protocol='http', suffix="", headers=None):
        if not auth:
            auth = NoAuth()
        if not response_handler:
            response_handler = handle_str
        if not uriparts:
            uriparts = ()
        if not headers:
            headers = {}
        Call.__init__(
            self, Descriptor(
                auth, response_handler, domain, protocol,
                suffix, headers),
            uriparts)


__all__ = ["Web2Connector", "Error", "HttpError",
           "JsonListResponse", "JsonDictResponse",
           "StrResponse", "handle_json", "handle_str"]
