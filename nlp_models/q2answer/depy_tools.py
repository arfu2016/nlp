"""
@Project   : CubeGirl
@Module    : depy_tools.py
@Author    : Deco [deco@cubee.com]
@Created   : 1/24/18 11:56 AM
@Desc      : 
"""
import re
import string


def clean_sentence(st):
    """clean a single input sentence"""
    in_tab = '[' + string.punctuation + r'''。，“”‘’（）：；？·—《》、''' + ']'
    out_tab = ''
    clean = re.sub(in_tab, out_tab, st)
    return clean


def clean_templates(templates):
    """clean a group of templates or sentences"""
    return [clean_sentence(tpl) for tpl in templates]
