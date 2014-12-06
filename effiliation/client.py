#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2


class Client:
    """ Client for the Effiliation API

    The Effiliation API is described here
    http://apiv2.effiliation.com/apiv2/doc/home.htm
    """

    api_key = None

    service_url = "http://apiv2.effiliation.com/apiv2"
    protocol = "json"

    mandatories_params = {
        'filter': ['commercialtrades', 'links', 'productfeeds', 'programs'],
        'session_id': ['counter'],
        'link_id': ['counter'],
    }

    allowed_params_values = {
        'filter': {
            '_' : ['mines', 'recommendation', 'active', 'inactive', ],
            'programs': ['mines', 'recommendation', 'active', 'inactive','pending', 'unregistered', 'closed', 'refused', ]
        }
    }

    params_default_values = {
        'filter': {
            '_': 'mines',
        }
    }


    def __init__(self, api_key=None, protocol=None):
        """Init a Client

        Keyword arguments:
        api_key -- the Publisher api key
        protocol -- the protocol for returns. Available protocols are csv, xml
        and json. Default to json

        >>> c = Client()
        >>> print c.api_key
        None
        >>> print c.protocol
        json

        >>> c = Client('foo', 'bar')
        >>> print c.api_key
        foo
        >>> print c.protocol
        json

        >>> c = Client('foo', 'xml')
        >>> print c.protocol
        xml

        >>> c = Client('foo', 'csv')
        >>> print c.protocol
        csv

        >>> c = Client('foo', 'json')
        >>> print c.protocol
        json
        """
        if api_key is not None:
            self.api_key = api_key

        if protocol is not None and protocol in ['xml', 'json', 'csv']:
            self.protocol = protocol


    def do_request(self, resource, params={}):
        """ Sends the request and returns the results

        Keyword arguments:
        resource -- The resource
        params -- The request parameters
        """
        url = "/".join([self.service_url, "%s.%s" % (resource, self.protocol)])
        query_parameters = ['key=' + self.api_key]

        params = self.check_params(resource, params)

        for key in params:
            if params[key] != None:
                query_parameters.append("%s=%s" % (key, params[key]))

        url += "?" + "&".join(query_parameters)

        request = urllib2.Request(url)
        opener = urllib2.build_opener(HttpErrorHandler())

        datastream = opener.open(request)
        return datastream.read()


    def check_params(self, resource, params):
        """Checks parameters are valid for the resource

        Tries to use default values for missing parameters before to raise
        errors

        Keyword arguments:
        resource -- the resource
        params -- the parameters
        """
        for param in self.mandatories_params:
            if param not in params and resource in self.mandatories_params[param]:
                # A mandatory parameter is missing, try to set the default value...
                if param in self.params_default_values and resource in self.params_default_values[param]:
                    # ... using the resource name
                    params[param] = self.params_default_values[param][resource]
                elif param in self.params_default_values and '_' in self.params_default_values[param]:
                    # ... or using the global _ value
                    params[param] = self.params_default_values[param]['_']
                else:
                    raise Exception("Parameter '%s' is missing" % param)

        for param in self.allowed_params_values:
            if param not in params:
                continue

            r = resource
            if r not in self.allowed_params_values[param]:
                # not values specified for the resource, check the global _ value
                r = '_'

                if r not in self.allowed_params_values[param]:
                    # no values limitation for the param
                    continue

            if params[param] not in self.allowed_params_values[param][r]:
                raise Exception("Parameter '%s' is improperly filled (one of the following value is required: %s)" % (param, ", ".join(self.allowed_params_values[param][r])))

        return params


    def get_promotional_offers(self, params={}):
        """ Shortcut to gets the commercialtrades resource"""
        return self.do_request('commercialtrades', params)


    def get_links(self, params={}):
        """ Shortcut to gets the links resource"""
        return self.do_request('links', params)


    def get_product_feeds(self, params={}):
        """ Shortcut to gets the productfeeds resource"""
        return self.do_request('productfeeds', params)


    def get_programs(self, params={}):
        """ Shortcut to gets the programs resource"""
        return self.do_request('programs', params)


    def get_categories(self, params={}):
        """ Shortcut to gets the categories resource"""
        return self.do_request('categories', params)


    def get_counter(self, params={}):
        """ Shortcut to gets the counter resource"""
        return self.do_request('counter', params)


    def get_transactions(self, params={}):
        """ Shortcut to gets the transaction resource"""
        return self.do_request('transaction', params)


    def get_reporting(self, params={}):
        """ Shortcut to gets the reporting resource"""
        return self.do_request('reporting', params)


class HttpErrorHandler(urllib2.HTTPDefaultErrorHandler):
    """ Http error handler for urllib2"""

    def http_error_default(self, req, fp, code, msg, headers):
        result = urllib2.HTTPError(
                req.get_full_url(), code, msg, headers, fp)
        result.status = code
        return result


if __name__ == '__main__':
    import doctest
    doctest.testmod()
