from    saltools.common import  EasyObj
from    .strategy       import  Strategy, Displayable
from    collections     import  OrderedDict


class Project(Displayable):
    EasyObj_PARAMS  = OrderedDict((
        ('strategies'    , {
            'type'  : Strategy  }),))