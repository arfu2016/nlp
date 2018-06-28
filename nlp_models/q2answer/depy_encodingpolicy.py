"""
@Project   : CubeGirl
@Module    : depy_encodingpolicy.py
@Author    : Deco [deco@cubee.com]
@Created   : 12/21/17 11:17 AM
@Desc      : 对字符串格式的检验
"""
import logging

from . import depy_settings as settings

logger = logging.getLogger("quepy.encodingpolicy")


def encoding_flexible_conversion(string, complain=False):
    """
    Converts string to the proper encoding if it's possible
    and if it's not raises a ValueError exception.

    If complain it's True, it will emit a logging warning about
    converting a string that had to be on the right encoding.
    """

    if isinstance(string, str):
        return string
    try:
        ustring = string.decode(settings.DEFAULT_ENCODING)
    except Exception:
        # except SyntaxError, AttributeError:
        message = "Argument must be string or bytes corresponding to {}"
        raise ValueError(message.format(settings.DEFAULT_ENCODING))
    if complain:
        logger.warning("Please provide str format for {}".format(string))
    return ustring


def assert_valid_encoding(string):
    """
    If not str it raises a
    ValueError exception.
    """

    if not isinstance(string, str):
        raise ValueError("Argument must be string")
