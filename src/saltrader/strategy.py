'''Strategy definition logic.

    Strategy is defined by a set of actions and constraints, if constraints a, b, c ... 
    are met, actions x, y, z ... are fired.

'''
from    saltools.common import  EasyObj     , MY_CLASS
from    collections     import  OrderedDict
from    dateutil.parser import  parser
from    datetime        import  datetime
from    decimal         import  Decimal
from    enum            import  Enum 
from    .data           import  Resource, Provider

class Displayable   (EasyObj):
    EasyObj_PARAMS  = OrderedDict((
        ('_id'          , {}            ),
        ('name'         , {
            'default'   : None          }),
        ('description'  , {
            'default'   : None          }),))
    
    def _on_init(
        self    ):
        if not self.name    :
            self.name   = self._id

class Parameter         (Displayable):
    pass
class ParameterDate     (Parameter  ):
    '''Date parameter.
    '''
    EasyObj_PARAMS  = OrderedDict((
        ('value'        , {
            'type'      : datetime  ,
            'parser'    : parser    ,
            'default'   : None      }),))
class ParameterInt      (Parameter  ):
    '''Int parameter.
    '''
    EasyObj_PARAMS  = OrderedDict((
        ('value'        , {
            'type'      : int       ,
            'parser'    : int       ,
            'default'   : None      }),))
class ParameterFloat    (Parameter  ):
    '''Int parameter.
    '''
    EasyObj_PARAMS  = OrderedDict((
        ('value'        , {
            'type'      : float     ,
            'parser'    : float     ,
            'default'   : None      }),))
class ParameterDecimal  (Parameter  ):
    '''Decimal parameter.
    '''
    EasyObj_PARAMS  = OrderedDict((
        ('value'        , {
            'type'      : Decimal   ,
            'parser'    : Decimal   ,
            'default'   : None      }),))
class ParameterStr      (Parameter  ):
    '''Str parameter.
    '''
    EasyObj_PARAMS  = OrderedDict((
        ('value'        , {
            'type'      : str   ,
            'default'   : None  }),))

class Constraint    (Displayable):
    '''Constraint

        Define a constraint based on data type and custom logic.
        A constraint can also contain a list of constraint that will be used 
        when evaluating its state.

        Args:
            constraints     (List, Constraint   ): Sub constraints.
            parameters      (List, Parameter    ): Constraint parameters.
    '''
    EasyObj_PARAMS  = OrderedDict((
        ('constraints'  , {
            'type'      : MY_CLASS  ,
            'default'   : []        }),
        ('parameters'   , {
            'type'      : Parameter ,
            'default'   : []        }),
        ('data_provider', {
            'type'  : Provider  }),
        ('logic'        , { }),))
    
    def process(
        self            ,
        siblings_output ):

        children_output = {}
        for constraint in self.constraints  :
            children_output[constraint._id] = constraint.process(children_output)
        
        return self.logic(
            siblings_output                             ,
            children_output                             ,
            {x._id: x.value for x in self.parameters }  ,
            self.data_provider                          )

class Strategy(EasyObj):
    pass

    