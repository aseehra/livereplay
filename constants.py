from collections import namedtuple

TWITTER_API_BASE = 'https://api.twitter.com/1.1/'

HttpErrorCodes = namedtuple(
        'HttpErrorCodes',
        [
            'OK',
            'NOT_MODIFIED',
            'BAD_REQUEST',
            'UNAUTHORIZED',
            'FORBIDDEN',
            'NOT_FOUND',
            'NOT_ACCEPTABLE',
            'GONE',
            'ENHANCE_CALM',
            'UNPROCESSABLE_ENTRY',
            'TOO_MANY_REQUESTS',
            'INTERNAL_SERVER_ERROR',
            'BAD_GATEWAY',
            'SERVICE_UNAVAILABLE',
            'GATEWAY_TIMEOUT'])
TWITTER_STATUS = HttpErrorCodes(
        200,
        304,
        400,
        401,
        403,
        404,
        406,
        410,
        420,
        422,
        420,
        500,
        502,
        503,
        504)
