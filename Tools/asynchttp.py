import httpx


from typing import Dict,Optional,Any,Union,Tuple,AsyncIterator

async def get(url:str,
              *,
              headers: Optional[Dict[str,str]] =None,
              params: Optional[Dict[str,Any]] =None,
              timeout: Optional[int] = 20,
              **kwargs
              ) -> httpx.Response:
    '''
    说明：
        对httpx的get请求进行异步封装

    参数：
    :param url: url
    :param headers:请求头
    :param params: 参数
    :param timeout: 超时时长
    '''
    async with httpx.AsyncClient() as Client:
        return await Client.get(url,
                                headers=headers,
                                params=params,
                                timeout=timeout,
                                **kwargs
                                )

async def post(url:str,
               *,
               headers: Optional[Dict[str,str]] =None,
               params: Optional[Dict[str,Any]] =None,
               data: Optional[Dict[str,Any]]=None,
               json: Optional[Dict[str,Union[Any,str]]]=None,
               timeout:Optional[int]=20,
               **kwargs)->httpx.Response:
    '''
    说明：
        对httpx的post请求进行异步封装

    参数：
    :param url: url
    :param headers:请求头
    :param params: 参数
    :param data: data
    :param json: json
    :param timeout: 超时时间
    '''
    async with httpx.AsyncClient() as Clint:
        return await Clint.post(url,
                                headers=headers,
                                params=params,
                                data=data,
                                json=json,
                                timeout=timeout,
                                **kwargs)