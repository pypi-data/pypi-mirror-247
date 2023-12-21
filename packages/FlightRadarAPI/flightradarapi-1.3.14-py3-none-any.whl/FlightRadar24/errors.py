# -*- coding: utf-8 -*-

class CloudflareError(Exception):
    def __init__(self, message, response):
        self.message = message
        self.response = response

    def __str__(self):
        return self.message


class LoginError(Exception):
    pass
