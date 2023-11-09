import numpy as np
from scipy import stats
import xarray as xr
def data_sub(data,lon_min,lon_max,lat_min,lat_max):
    
    '''Define a box between lon_min lon_max lat_min and lat_max and 
    extract the data in the box and drop everything else.
    
    
    Parameters
    ----------
    
    data : xarray_like
    Data to be subdomained. 
    
    lon_min : integer
    Longitude minimum of the subdomain
    
    lon_max : integer
    Longitude maximum of the subdomain
    
    lat_min : integer
    Latitude minimum of the subdomain
    
    lat_max : integer
    Latitude maximum of the subdomain
    
    Returns
    ---------
    
    data_sub : xarray_like
    Subdomain. 
    '''
    
    try:
        data_sub = data.where((  data.lon>=lon_min) & (data.lon<=lon_max) & (data.lat<=lat_max) & (data.lat>=lat_min),
                                                                          drop=True)
    except AttributeError:
        try:
            data_sub = data.where((  data.nav_lon>=lon_min) & (data.nav_lon<=lon_max) & (data.nav_lat<=lat_max) & (data.nav_lat>=lat_min),drop=True)
        except AttributeError:
            try:
                data_sub = data.where((  data.longitude>=lon_min) & (data.longitude<=lon_max) & (data.latitude<=lat_max) & (data.latitude>=lat_min),drop=True)
            except AttributeError:
                try:
                    data_sub = data.where((  data.x>=lon_min) & (data.x<=lon_max) & (data.y<=lat_max) &
                                      (data.y>=lat_min),drop=True)
                except AttributeError:
                    data_sub = data.where((  data.LON>=lon_min) & (data.LON<=lon_max) & (data.LAT<=lat_max) &
                                      (data.LAT>=lat_min),drop=True)
            
    

 
    
    return data_sub



def nandetrend(y):
    ''' Remove the linear trend from the data '''
    
    x = np.arange(0,y.shape[0],1)
    m, b, r_val, p_val, std_err = stats.linregress(x,np.array(y))
    y_detrended= np.array(y) - m*x
    return y_detrended



def ano_norm_t(ds):
    
    '''Compute the anomalies by removing the monthly means. 
    The anomalies are normalized by their corresponding month.
    
    Parameters
    ----------
    
    ds : xarray_like
    Timeserie or 3d field.
    
    Returns
    -----------
    
    ano : xarray_like
    Returns the anomalies of var relative the climatology.
    
    ano_norm : xarray_like
    Returns the anomalies of var relative the climatology normalized by the standard deviation.
    
    '''    
    
    clim     = ds.groupby('time.month').mean('time')
    clim_std = ds.groupby('time.month').std('time')
    ano      = ds.groupby('time.month') - clim
    ano_norm = xr.apply_ufunc(lambda x, m, s: (x - m) / s,
                                    ds.groupby('time.month'),
                                    clim, clim_std)
    
    return ano, ano_norm