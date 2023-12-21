from __future__ import annotations
from typing import Any, BinaryIO, Dict, NoReturn, Optional, Union, overload
from httpx import AsyncClient as HClient
from json_minify import json_minify
from ujson import dumps
from .exception import check_exceptions
from .headers import Headers
from .util import api, webApi

__all__ = ('AsyncSession',)


class AsyncSession(Headers):
    """Base class for client sessions.

    Parameters
    ----------
    client : Client
        The global client object.
    proxies : dict[str, str], optional
        Proxies for HTTP requests supported by the httpx library (https://www.python-httpx.org/advanced/#routing)
    deviceId : str, optional
        The device of the client.

    """

    def __init__(self, client: Optional[AsyncSession] = None, proxies: Optional[Dict[str, str]] = None, deviceId: Optional[str] = None) -> None:
        self.proxies = (proxies or client.proxies) if client else proxies
        self.sid = client.sid if client else None
        self.uid = client.uid if client else None
        self.secret = client.secret if client else None
        Headers.__init__(self, deviceId=deviceId)
        self.session = HClient(proxies=self.proxies, timeout=20)  # type: ignore
        self.sidInit()

    def sidInit(self) -> None:
        """Set the instance session ID."""
        if self.sid:
            self.updateHeaders(sid=self.sid)

    @overload
    def settings(self, *, sid: Optional[str] = None) -> None:
        ...

    @overload
    def settings(self, *, sid: Optional[str] = None, uid: Optional[str]) -> None:
        ...

    @overload
    def settings(self, *, sid: Optional[str] = None, uid: Optional[str] = None, secret: Optional[str] = None) -> None:
        ...

    def settings(self, **kwargs: Any) -> None:
        """Update the instance settings.

        Parameters
        ----------
        sid : str, optional
            The new session ID. If not provided, the current value will be used
        uid : str, optional
            The new user ID. If not provided, the current value will be used
        secret : str, optional
            The new secret password. If not provided, the current value will be used

        """
        self.sid = kwargs.pop('sid', self.sid)
        self.uid = kwargs.pop('uid', self.uid)
        self.secret = kwargs.pop('secret', self.secret)
        self.sidInit()

    async def postRequest(self, url: str, data: Union[str, Dict[str, Any], BinaryIO, None] = None, newHeaders: Optional[Dict[str, str]] = None, webRequest: bool = False, minify: bool = False) -> Union[Dict[str, Any], NoReturn]:
        """Make a POST request to the amino API.

        Parameters
        ----------
        url : str
            The API url/path.
        data : str, dict, BinaryIO, optional
            The raw data to send. Default is None.
        newHeaders : dict, optional
            The HTTP headers to include in request. Default is None.
        webRequest : bool, optional
            Make web request. Default is False.
        minify : bool, optional
            Json minify the data. Default is False.

        Returns
        -------
        dict
            The response from the API.

        Raises
        ------
        AminoBaseException
            If the request fails.

        """
        if isinstance(data, dict):
            data = json_minify(dumps(data)) if minify else dumps(data)
        # no file support in the signature message
        self.updateHeaders(data=data if isinstance(data, str) else None, sid=self.sid)
        if newHeaders:
            self.app_headers.update(newHeaders)
        async with HClient(proxies=self.proxies, timeout=20) as session:  # type: ignore
            req = await session.post(
                url=webApi(url) if webRequest else api(url),
                data=data if isinstance(data, str) else None,  # type: ignore
                files={"file": data} if isinstance(data, BinaryIO) else None,
                headers=self.web_headers if webRequest else self.app_headers
            )
        return check_exceptions(req.json()) if req.status_code != 200 else req.json()

    async def getRequest(self, url: str) -> Union[Dict[str, Any], NoReturn]:
        """Make a GET request to the amino API.

        Parameters
        ----------
        url : str
            The API url/path.

        Returns
        -------
        dict
            The response from the API.

        Raises
        ------
        AminoBaseException
            If the request fails.

        """
        async with HClient(proxies=self.proxies, timeout=20) as session:  # type: ignore
            req = await session.get(url=api(url), headers=self.updateHeaders())
        return check_exceptions(req.json()) if req.status_code != 200 else req.json()

    async def deleteRequest(self, url: str) -> Union[Dict[str, Any], NoReturn]:
        """Make a DELETE request to the amino API.

        Parameters
        ----------
        url : str
            The API url/path.

        Returns
        -------
        dict
            The response from the API.

        Raises
        ------
        AminoBaseException
            If the request fails.

        """
        async with HClient(proxies=self.proxies, timeout=20) as session:  # type: ignore
            req = await session.delete(url=api(url), headers=self.updateHeaders())
        return check_exceptions(req.json()) if req.status_code != 200 else req.json()
