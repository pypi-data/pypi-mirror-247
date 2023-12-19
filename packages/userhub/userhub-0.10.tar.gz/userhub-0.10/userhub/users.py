"""
Functionality of working with users
"""

from ._req import fetch


LINK = 'https://chill.services/api/'


async def get(
    token: str,
    data: dict = None,
):
    """ Get """

    if data is None:
        data = {}

    req = {
        'token': token,
        **data,
    }

    res = await fetch(LINK + 'users/get/', req)
    if isinstance(res, str):
        print(res)
        return res
    return res
