'''Data providing logic for trading strategies.

    Implements data providers, these providers will be used to feed data
    to the trading strategies.

    Custom data provider must implement ``DataProvider`` and override and ``g_data``.

    Notes:
        * For data types definition, when dealing with the names of the columns in csvs or a databse, all must be 
          in lower case
        * data in storage must be ordered from oldest or recent.

    Data types defintion:
        * OHLCV: date(index), open, high, low, close, volume.
'''

from    enum            import  Enum
from    saltools.common import  EasyObj
from    collections     import  OrderedDict
from    saltools        import  logging
from    datetime        import  datetime
from    dateutil.parser import  parse

import  saltools.files  as      stf
import  pandas          as      pd

import  os

class ResourceType  (Enum):
    OHLCV   = 0
class TimeFrame     (Enum):
    MINUTE          = 0
    HOUR            = 1
    DAY             = 2
    WEEK            = 3
    MONTH           = 4
    YEAR            = 5

class Resource      (EasyObj):
    EasyObj_PARAMS  = OrderedDict((
        ('type'         , {
                'default'   : 'OHLCV'       ,
                'type'      : ResourceType  ,
            }),
        ('pair'         , {
                'type'      : str
            }),
        ('frame'        , {
                'type'      : TimeFrame ,
            }),
        ('interval'     , {
                'type'      : int   ,
                'default'   : 1     ,
            }),
        ('start_date'   , {
                'type'      : datetime  ,
                'default'   : None      ,
            }),
        ('limit'        , {
                'type'      : int   ,
                'default'   : None  ,
            }),
        ('end_date'     , {
                'type'      : datetime  ,
                'default'   : None      ,
            }),))
class Provider      (EasyObj):
    '''Data provider base.

        An interface for all data providers.

        Args:
            source_id   (str    ): The data source id, broker or exchange the data is collected from. 
    '''
    EasyObj_PARAMS = OrderedDict((
        ('source_id', {
            'type'  : str}),))

    @logging.handle_exception()
    def g_data(
        self                ,
        resource            ):
        '''Get the resource.

            Gets a dataframe containing the data specified by the arguments.
            Must be overridden by all derived classes. 

            Args:
                resource    (Resource   ): The resource to get.
            
            Returns:
                (pandas.DataFrame)  : A dataframe with the requested resource. 
        '''
        raise NotImplementedError

class ProviderCSV(Provider):
    '''Fetches  data from csv files.

        Notes:
            * All pairs must be in the format `BASE-QUOTE` in upper case.
            * CSV files must have follow the correct data structure for the given data type.
            * The separator for the csv files must be `,`.
            * Time series must be saved in CSVs from oldest to latest.

        Args:
            root    (str    ): The root to the csv files root folder.
    '''
    EasyObj_PARAMS = OrderedDict((
        ('root'     , {
            'type'  : str}),))
    
    @logging.handle_exception   ()
    def _g_resource_paths       (
        self    ,
        *args   ):
        '''Gets path to the requested resource.

            Gets path to the requested resource.

            Args:
                resource_type       (ResourceType       ): The resource type.
                pair                (str                ): The pair or symbol.   
                time_frame          (TimeFrame          ): The time frame of the resource.
                time_frame_interval (int                ): The interval of the time frame.

            Returns:
                str : Path to the resource csv file. 
        '''
        regex       = '_'.join(['(?:{})'.format(x if x else '[^_]+?') for x in args])+ '.csv'
        root        = os.path.join(self.root, self.source_id)
        paths       = stf.g_filders(root, regex, True, folders= False, sub_dirs= False)
        paths_dict  = {}
        for path in paths:
            resource_args = os.path.basename(path).split('.')[0].split('_')
            paths_dict[Resource(*resource_args)] = path
        return paths_dict

    @logging.handle_exception   ()
    def g_all_resources         (
        self ):
        return self._g_resource_paths(None, None, None, None).keys()
    @logging.handle_exception   ()
    def g_data                  (
        self        ,
        resource    ):
        paths       = self._g_resource_paths(
            resource.type.name  if resource.type  else None     ,
            resource.pair                                       ,
            resource.frame.name if resource.frame else None     ,
            resource.interval                                   )
            
        dfs         = {n_resource: pd.read_csv(paths[n_resource], index_col=0) 
            for n_resource in paths}
        for n_resource in dfs   :
            n_resource.start_date   = resource.start_date
            n_resource.end_date     = resource.end_date
            n_resource.limit        = resource.limit
            dfs[n_resource].index   = dfs[n_resource].index.astype('datetime64[ns]')
            dfs[n_resource]         = dfs[n_resource][n_resource.start_date: n_resource.end_date][:n_resource.limit]
        
        return      dfs