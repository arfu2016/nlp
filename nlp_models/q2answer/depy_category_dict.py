"""
@Project   : CubeGirl
@Module    : depy_category_dict.py
@Author    : Deco [deco@cubee.com]
@Created   : 1/26/18 2:09 PM
@Desc      : 
"""
import inspect

from . import (class0_convert, class2_general, class1_strict, class3_sparql)
from . import (tpl0_convert, tpl1_strict_natural, tpl2_general,
               tpl01_yesorno, tpl3_words, tpl4_sparql)


class Category:

    @staticmethod
    def list_construct(tpl_list):
        only_templates = [class0_convert, class2_general, class3_sparql,
                          class1_strict]
        for A in only_templates:
            for x in dir(A):
                the_class = getattr(A, x)
                if inspect.isclass(the_class):
                    tpl_list.append(x)

    @staticmethod
    def dict_construct(tpl_dict0, tpl_dict1, tpl_list):
        only_templates = {10: tpl0_convert, 0: tpl1_strict_natural,
                          1: tpl2_general, 11: tpl01_yesorno,
                          20: tpl3_words, 4: tpl4_sparql}
        remove_classes = ['OneTerm', 'OneTermForTpl']
        remove_classes.extend(tpl_list)
        for index, A in only_templates.items():
            temp = []
            for x in dir(A):
                the_class = getattr(A, x)
                if inspect.isclass(the_class) and x not in remove_classes:
                    tpl_dict0.update({x: the_class})
                    temp.append(the_class)
            tpl_dict1.update({index: temp})

    def __init__(self):
        self.tpl_dict = {}
        self.category_dict = {}
        self.remove_list = []
        self.list_construct(self.remove_list)
        self.dict_construct(self.tpl_dict, self.category_dict,
                            self.remove_list)


ca_dict = Category()
