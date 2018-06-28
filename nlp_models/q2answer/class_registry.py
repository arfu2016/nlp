"""
@Project   : CubeGirl
@Module    : class_registry.py
@Author    : Deco [deco@cubee.com]
@Created   : 3/13/18 3:11 PM
@Desc      : Register classes
"""

registered_classes = dict()


def register_class(cls):
    """输入是问法类，输出还是完全相同的问法类"""
    registered_classes.update({cls.template_name: cls})
    return cls


def register_syntac(syntac_dict):
    """输入是问法类以及想要注册到的字典，输出还是完全相同的问法类"""

    def register_tpl(cls):
        syntac_dict.update({cls.template_name: cls})
        return cls

    return register_tpl
