#!/usr/bin/env python
# _*_coding:utf-8_*_

"""
@Time     : 2023/7/11 9:23
@Author   : ji hao ran
@File     : segmented.py
@Project  : StreamlitAntdComponents
@Software : PyCharm
"""

from ..utils import *


def segmented(
        items: List[Union[str, dict, SegmentedItem]],
        index: Union[int, None] = 0,
        format_func: Union[Label, Callable] = None,
        label: str = None,
        position: Position = 'top',
        align: Align = 'start',
        direction: Direction = 'horizontal',
        radius: MantineSize = 'md',
        size: MantineSize = 'md',
        color: MantineColor = None,
        bg_color: str = None,
        divider: bool = True,
        grow: bool = False,
        disabled: bool = False,
        readonly: bool = False,
        return_index: bool = False,
        on_change: Callable = None,
        args: Tuple[Any, ...] = None,
        kwargs: Dict[str, Any] = None,
        key=None,
) -> Union[str, int]:
    """mantine segmentedControl https://mantine.dev/core/segmented-control/

    :param items: segmented data
    :param index: default selected item index,if None,default not selected item.
    :param format_func: label formatter function,receive str and return str
    :param label: segmented label
    :param position: segmented label position
    :param align: segmented align
    :param direction: segmented direction
    :param radius: segmented radius
    :param size: segmented size
    :param color: segmented indicator background color,default streamlit primary color
    :param bg_color: segmented background color,default streamlit secondary background color
    :param divider: show segmented vertical divider
    :param grow: width 100%
    :param disabled: disable segmented
    :param readonly: readonly mode
    :param return_index: if True,return button index,default return label
    :param on_change: item change callback
    :param args: callback args
    :param kwargs: callback kwargs
    :param key: component unique identifier
    :return: selected segmented item value or index
    """
    # register callback
    register(key, on_change, args, kwargs)
    # parse items
    items, kv = ParseItems(items, format_func).single(key_field='value')
    # component params
    kw = update_kw(locals(), items=items)
    # component default
    default = get_default(index, return_index, kv)
    # pass component id and params to frontend
    return component(id=get_func_name(), kw=kw, default=default, key=key)
