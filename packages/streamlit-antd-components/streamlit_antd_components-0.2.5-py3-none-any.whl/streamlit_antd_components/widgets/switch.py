#!/usr/bin/env python
# _*_coding:utf-8_*_

"""
@Time     : 2023/6/12 16:28
@Author   : ji hao ran
@File     : switch.py
@Project  : StreamlitAntdComponents
@Software : PyCharm
"""
from ..utils import *


def switch(
        label: str = None,
        value: bool = False,
        description: str = None,
        on_label: Union[str, BsIcon] = None,
        off_label: Union[str, BsIcon] = None,
        align: Align = 'start',
        position: MantinePosition = 'right',
        size: MantineSize = 'sm',
        radius: MantineSize = 'xl',
        on_color: MantineColor = None,
        off_color: MantineColor = None,
        disabled: bool = False,
        on_change: Callable = None,
        args: Tuple[Any, ...] = None,
        kwargs: Dict[str, Any] = None,
        key=None
) -> bool:
    """mantine switch  https://v6.mantine.dev/core/switch/

    :param label: switch label,markdown and html with bootstrap available
    :param value: default value
    :param description: switch description
    :param on_label: switch on status label,str or BsIcon
    :param off_label: switch off status label,str or BsIcon
    :param align: switch align
    :param position: switch label position
    :param size: switch size
    :param radius: switch radius
    :param on_color: switch on status color,default streamlit primary color
    :param off_color: switch off status color,default gray
    :param disabled: disabled status
    :param on_change: switch change callback
    :param args: callback args
    :param kwargs: callback kwargs
    :param key: component unique identifier
    :return: True when open,False when close
    """
    # register callback
    register(key, on_change, args, kwargs)
    # parse icon
    kw = dict(locals())
    kw.update(on_label={'bs': on_label.__dict__.get('name')} if isinstance(on_label, BsIcon) else on_label)
    kw.update(off_label={'bs': off_label.__dict__.get('name')} if isinstance(off_label, BsIcon) else off_label)
    kw = update_kw(kw)
    # pass component id and params to frontend
    return component(id=get_func_name(), kw=kw, default=value, key=key)
