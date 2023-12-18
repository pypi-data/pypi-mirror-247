# pylint: disable=too-many-lines
# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is regenerated.
# --------------------------------------------------------------------------
from io import IOBase
from typing import Any, Callable, Dict, IO, Iterable, Optional, TypeVar, Union, cast, overload
import urllib.parse

from azure.core.exceptions import (
    ClientAuthenticationError,
    HttpResponseError,
    ResourceExistsError,
    ResourceNotFoundError,
    ResourceNotModifiedError,
    map_error,
)
from azure.core.paging import ItemPaged
from azure.core.pipeline import PipelineResponse
from azure.core.pipeline.transport import HttpResponse
from azure.core.polling import LROPoller, NoPolling, PollingMethod
from azure.core.rest import HttpRequest
from azure.core.tracing.decorator import distributed_trace
from azure.core.utils import case_insensitive_dict
from azure.mgmt.core.exceptions import ARMErrorFormat
from azure.mgmt.core.polling.arm_polling import ARMPolling

from .. import models as _models
from .._serialization import Serializer
from .._vendor import _convert_request

T = TypeVar("T")
ClsType = Optional[Callable[[PipelineResponse[HttpRequest, HttpResponse], T, Dict[str, Any]], Any]]

_SERIALIZER = Serializer()
_SERIALIZER.client_side_validation = False


def build_list_by_batch_account_request(
    resource_group_name: str,
    account_name: str,
    subscription_id: str,
    *,
    maxresults: Optional[int] = None,
    **kwargs: Any
) -> HttpRequest:
    _headers = case_insensitive_dict(kwargs.pop("headers", {}) or {})
    _params = case_insensitive_dict(kwargs.pop("params", {}) or {})

    api_version: str = kwargs.pop("api_version", _params.pop("api-version", "2023-11-01"))
    accept = _headers.pop("Accept", "application/json")

    # Construct URL
    _url = kwargs.pop(
        "template_url",
        "/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Batch/batchAccounts/{accountName}/privateEndpointConnections",
    )  # pylint: disable=line-too-long
    path_format_arguments = {
        "subscriptionId": _SERIALIZER.url("subscription_id", subscription_id, "str"),
        "resourceGroupName": _SERIALIZER.url("resource_group_name", resource_group_name, "str"),
        "accountName": _SERIALIZER.url(
            "account_name", account_name, "str", max_length=24, min_length=3, pattern=r"^[a-zA-Z0-9]+$"
        ),
    }

    _url: str = _url.format(**path_format_arguments)  # type: ignore

    # Construct parameters
    _params["api-version"] = _SERIALIZER.query("api_version", api_version, "str")
    if maxresults is not None:
        _params["maxresults"] = _SERIALIZER.query("maxresults", maxresults, "int")

    # Construct headers
    _headers["Accept"] = _SERIALIZER.header("accept", accept, "str")

    return HttpRequest(method="GET", url=_url, params=_params, headers=_headers, **kwargs)


def build_get_request(
    resource_group_name: str,
    account_name: str,
    private_endpoint_connection_name: str,
    subscription_id: str,
    **kwargs: Any
) -> HttpRequest:
    _headers = case_insensitive_dict(kwargs.pop("headers", {}) or {})
    _params = case_insensitive_dict(kwargs.pop("params", {}) or {})

    api_version: str = kwargs.pop("api_version", _params.pop("api-version", "2023-11-01"))
    accept = _headers.pop("Accept", "application/json")

    # Construct URL
    _url = kwargs.pop(
        "template_url",
        "/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Batch/batchAccounts/{accountName}/privateEndpointConnections/{privateEndpointConnectionName}",
    )  # pylint: disable=line-too-long
    path_format_arguments = {
        "subscriptionId": _SERIALIZER.url("subscription_id", subscription_id, "str"),
        "resourceGroupName": _SERIALIZER.url("resource_group_name", resource_group_name, "str"),
        "accountName": _SERIALIZER.url(
            "account_name", account_name, "str", max_length=24, min_length=3, pattern=r"^[a-zA-Z0-9]+$"
        ),
        "privateEndpointConnectionName": _SERIALIZER.url(
            "private_endpoint_connection_name",
            private_endpoint_connection_name,
            "str",
            max_length=101,
            min_length=1,
            pattern=r"^[a-zA-Z0-9_-]+\.?[a-fA-F0-9-]*$",
        ),
    }

    _url: str = _url.format(**path_format_arguments)  # type: ignore

    # Construct parameters
    _params["api-version"] = _SERIALIZER.query("api_version", api_version, "str")

    # Construct headers
    _headers["Accept"] = _SERIALIZER.header("accept", accept, "str")

    return HttpRequest(method="GET", url=_url, params=_params, headers=_headers, **kwargs)


def build_update_request(
    resource_group_name: str,
    account_name: str,
    private_endpoint_connection_name: str,
    subscription_id: str,
    *,
    if_match: Optional[str] = None,
    **kwargs: Any
) -> HttpRequest:
    _headers = case_insensitive_dict(kwargs.pop("headers", {}) or {})
    _params = case_insensitive_dict(kwargs.pop("params", {}) or {})

    api_version: str = kwargs.pop("api_version", _params.pop("api-version", "2023-11-01"))
    content_type: Optional[str] = kwargs.pop("content_type", _headers.pop("Content-Type", None))
    accept = _headers.pop("Accept", "application/json")

    # Construct URL
    _url = kwargs.pop(
        "template_url",
        "/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Batch/batchAccounts/{accountName}/privateEndpointConnections/{privateEndpointConnectionName}",
    )  # pylint: disable=line-too-long
    path_format_arguments = {
        "subscriptionId": _SERIALIZER.url("subscription_id", subscription_id, "str"),
        "resourceGroupName": _SERIALIZER.url("resource_group_name", resource_group_name, "str"),
        "accountName": _SERIALIZER.url(
            "account_name", account_name, "str", max_length=24, min_length=3, pattern=r"^[a-zA-Z0-9]+$"
        ),
        "privateEndpointConnectionName": _SERIALIZER.url(
            "private_endpoint_connection_name",
            private_endpoint_connection_name,
            "str",
            max_length=101,
            min_length=1,
            pattern=r"^[a-zA-Z0-9_-]+\.?[a-fA-F0-9-]*$",
        ),
    }

    _url: str = _url.format(**path_format_arguments)  # type: ignore

    # Construct parameters
    _params["api-version"] = _SERIALIZER.query("api_version", api_version, "str")

    # Construct headers
    if if_match is not None:
        _headers["If-Match"] = _SERIALIZER.header("if_match", if_match, "str")
    if content_type is not None:
        _headers["Content-Type"] = _SERIALIZER.header("content_type", content_type, "str")
    _headers["Accept"] = _SERIALIZER.header("accept", accept, "str")

    return HttpRequest(method="PATCH", url=_url, params=_params, headers=_headers, **kwargs)


def build_delete_request(
    resource_group_name: str,
    account_name: str,
    private_endpoint_connection_name: str,
    subscription_id: str,
    **kwargs: Any
) -> HttpRequest:
    _headers = case_insensitive_dict(kwargs.pop("headers", {}) or {})
    _params = case_insensitive_dict(kwargs.pop("params", {}) or {})

    api_version: str = kwargs.pop("api_version", _params.pop("api-version", "2023-11-01"))
    accept = _headers.pop("Accept", "application/json")

    # Construct URL
    _url = kwargs.pop(
        "template_url",
        "/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Batch/batchAccounts/{accountName}/privateEndpointConnections/{privateEndpointConnectionName}",
    )  # pylint: disable=line-too-long
    path_format_arguments = {
        "subscriptionId": _SERIALIZER.url("subscription_id", subscription_id, "str"),
        "resourceGroupName": _SERIALIZER.url("resource_group_name", resource_group_name, "str"),
        "accountName": _SERIALIZER.url(
            "account_name", account_name, "str", max_length=24, min_length=3, pattern=r"^[a-zA-Z0-9]+$"
        ),
        "privateEndpointConnectionName": _SERIALIZER.url(
            "private_endpoint_connection_name",
            private_endpoint_connection_name,
            "str",
            max_length=101,
            min_length=1,
            pattern=r"^[a-zA-Z0-9_-]+\.?[a-fA-F0-9-]*$",
        ),
    }

    _url: str = _url.format(**path_format_arguments)  # type: ignore

    # Construct parameters
    _params["api-version"] = _SERIALIZER.query("api_version", api_version, "str")

    # Construct headers
    _headers["Accept"] = _SERIALIZER.header("accept", accept, "str")

    return HttpRequest(method="DELETE", url=_url, params=_params, headers=_headers, **kwargs)


class PrivateEndpointConnectionOperations:
    """
    .. warning::
        **DO NOT** instantiate this class directly.

        Instead, you should access the following operations through
        :class:`~azure.mgmt.batch.BatchManagementClient`'s
        :attr:`private_endpoint_connection` attribute.
    """

    models = _models

    def __init__(self, *args, **kwargs):
        input_args = list(args)
        self._client = input_args.pop(0) if input_args else kwargs.pop("client")
        self._config = input_args.pop(0) if input_args else kwargs.pop("config")
        self._serialize = input_args.pop(0) if input_args else kwargs.pop("serializer")
        self._deserialize = input_args.pop(0) if input_args else kwargs.pop("deserializer")

    @distributed_trace
    def list_by_batch_account(
        self, resource_group_name: str, account_name: str, maxresults: Optional[int] = None, **kwargs: Any
    ) -> Iterable["_models.PrivateEndpointConnection"]:
        """Lists all of the private endpoint connections in the specified account.

        :param resource_group_name: The name of the resource group that contains the Batch account.
         Required.
        :type resource_group_name: str
        :param account_name: The name of the Batch account. Required.
        :type account_name: str
        :param maxresults: The maximum number of items to return in the response. Default value is
         None.
        :type maxresults: int
        :keyword callable cls: A custom type or function that will be passed the direct response
        :return: An iterator like instance of either PrivateEndpointConnection or the result of
         cls(response)
        :rtype: ~azure.core.paging.ItemPaged[~azure.mgmt.batch.models.PrivateEndpointConnection]
        :raises ~azure.core.exceptions.HttpResponseError:
        """
        _headers = kwargs.pop("headers", {}) or {}
        _params = case_insensitive_dict(kwargs.pop("params", {}) or {})

        api_version: str = kwargs.pop("api_version", _params.pop("api-version", self._config.api_version))
        cls: ClsType[_models.ListPrivateEndpointConnectionsResult] = kwargs.pop("cls", None)

        error_map = {
            401: ClientAuthenticationError,
            404: ResourceNotFoundError,
            409: ResourceExistsError,
            304: ResourceNotModifiedError,
        }
        error_map.update(kwargs.pop("error_map", {}) or {})

        def prepare_request(next_link=None):
            if not next_link:

                request = build_list_by_batch_account_request(
                    resource_group_name=resource_group_name,
                    account_name=account_name,
                    subscription_id=self._config.subscription_id,
                    maxresults=maxresults,
                    api_version=api_version,
                    template_url=self.list_by_batch_account.metadata["url"],
                    headers=_headers,
                    params=_params,
                )
                request = _convert_request(request)
                request.url = self._client.format_url(request.url)

            else:
                # make call to next link with the client's api-version
                _parsed_next_link = urllib.parse.urlparse(next_link)
                _next_request_params = case_insensitive_dict(
                    {
                        key: [urllib.parse.quote(v) for v in value]
                        for key, value in urllib.parse.parse_qs(_parsed_next_link.query).items()
                    }
                )
                _next_request_params["api-version"] = self._config.api_version
                request = HttpRequest(
                    "GET", urllib.parse.urljoin(next_link, _parsed_next_link.path), params=_next_request_params
                )
                request = _convert_request(request)
                request.url = self._client.format_url(request.url)
                request.method = "GET"
            return request

        def extract_data(pipeline_response):
            deserialized = self._deserialize("ListPrivateEndpointConnectionsResult", pipeline_response)
            list_of_elem = deserialized.value
            if cls:
                list_of_elem = cls(list_of_elem)  # type: ignore
            return deserialized.next_link or None, iter(list_of_elem)

        def get_next(next_link=None):
            request = prepare_request(next_link)

            _stream = False
            pipeline_response: PipelineResponse = self._client._pipeline.run(  # pylint: disable=protected-access
                request, stream=_stream, **kwargs
            )
            response = pipeline_response.http_response

            if response.status_code not in [200]:
                map_error(status_code=response.status_code, response=response, error_map=error_map)
                raise HttpResponseError(response=response, error_format=ARMErrorFormat)

            return pipeline_response

        return ItemPaged(get_next, extract_data)

    list_by_batch_account.metadata = {
        "url": "/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Batch/batchAccounts/{accountName}/privateEndpointConnections"
    }

    @distributed_trace
    def get(
        self, resource_group_name: str, account_name: str, private_endpoint_connection_name: str, **kwargs: Any
    ) -> _models.PrivateEndpointConnection:
        """Gets information about the specified private endpoint connection.

        :param resource_group_name: The name of the resource group that contains the Batch account.
         Required.
        :type resource_group_name: str
        :param account_name: The name of the Batch account. Required.
        :type account_name: str
        :param private_endpoint_connection_name: The private endpoint connection name. This must be
         unique within the account. Required.
        :type private_endpoint_connection_name: str
        :keyword callable cls: A custom type or function that will be passed the direct response
        :return: PrivateEndpointConnection or the result of cls(response)
        :rtype: ~azure.mgmt.batch.models.PrivateEndpointConnection
        :raises ~azure.core.exceptions.HttpResponseError:
        """
        error_map = {
            401: ClientAuthenticationError,
            404: ResourceNotFoundError,
            409: ResourceExistsError,
            304: ResourceNotModifiedError,
        }
        error_map.update(kwargs.pop("error_map", {}) or {})

        _headers = kwargs.pop("headers", {}) or {}
        _params = case_insensitive_dict(kwargs.pop("params", {}) or {})

        api_version: str = kwargs.pop("api_version", _params.pop("api-version", self._config.api_version))
        cls: ClsType[_models.PrivateEndpointConnection] = kwargs.pop("cls", None)

        request = build_get_request(
            resource_group_name=resource_group_name,
            account_name=account_name,
            private_endpoint_connection_name=private_endpoint_connection_name,
            subscription_id=self._config.subscription_id,
            api_version=api_version,
            template_url=self.get.metadata["url"],
            headers=_headers,
            params=_params,
        )
        request = _convert_request(request)
        request.url = self._client.format_url(request.url)

        _stream = False
        pipeline_response: PipelineResponse = self._client._pipeline.run(  # pylint: disable=protected-access
            request, stream=_stream, **kwargs
        )

        response = pipeline_response.http_response

        if response.status_code not in [200]:
            map_error(status_code=response.status_code, response=response, error_map=error_map)
            raise HttpResponseError(response=response, error_format=ARMErrorFormat)

        deserialized = self._deserialize("PrivateEndpointConnection", pipeline_response)

        if cls:
            return cls(pipeline_response, deserialized, {})

        return deserialized

    get.metadata = {
        "url": "/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Batch/batchAccounts/{accountName}/privateEndpointConnections/{privateEndpointConnectionName}"
    }

    def _update_initial(
        self,
        resource_group_name: str,
        account_name: str,
        private_endpoint_connection_name: str,
        parameters: Union[_models.PrivateEndpointConnection, IO],
        if_match: Optional[str] = None,
        **kwargs: Any
    ) -> Optional[_models.PrivateEndpointConnection]:
        error_map = {
            401: ClientAuthenticationError,
            404: ResourceNotFoundError,
            409: ResourceExistsError,
            304: ResourceNotModifiedError,
        }
        error_map.update(kwargs.pop("error_map", {}) or {})

        _headers = case_insensitive_dict(kwargs.pop("headers", {}) or {})
        _params = case_insensitive_dict(kwargs.pop("params", {}) or {})

        api_version: str = kwargs.pop("api_version", _params.pop("api-version", self._config.api_version))
        content_type: Optional[str] = kwargs.pop("content_type", _headers.pop("Content-Type", None))
        cls: ClsType[Optional[_models.PrivateEndpointConnection]] = kwargs.pop("cls", None)

        content_type = content_type or "application/json"
        _json = None
        _content = None
        if isinstance(parameters, (IOBase, bytes)):
            _content = parameters
        else:
            _json = self._serialize.body(parameters, "PrivateEndpointConnection")

        request = build_update_request(
            resource_group_name=resource_group_name,
            account_name=account_name,
            private_endpoint_connection_name=private_endpoint_connection_name,
            subscription_id=self._config.subscription_id,
            if_match=if_match,
            api_version=api_version,
            content_type=content_type,
            json=_json,
            content=_content,
            template_url=self._update_initial.metadata["url"],
            headers=_headers,
            params=_params,
        )
        request = _convert_request(request)
        request.url = self._client.format_url(request.url)

        _stream = False
        pipeline_response: PipelineResponse = self._client._pipeline.run(  # pylint: disable=protected-access
            request, stream=_stream, **kwargs
        )

        response = pipeline_response.http_response

        if response.status_code not in [200, 202]:
            map_error(status_code=response.status_code, response=response, error_map=error_map)
            raise HttpResponseError(response=response, error_format=ARMErrorFormat)

        deserialized = None
        response_headers = {}
        if response.status_code == 200:
            deserialized = self._deserialize("PrivateEndpointConnection", pipeline_response)

        if response.status_code == 202:
            response_headers["Location"] = self._deserialize("str", response.headers.get("Location"))
            response_headers["Retry-After"] = self._deserialize("int", response.headers.get("Retry-After"))

        if cls:
            return cls(pipeline_response, deserialized, response_headers)

        return deserialized

    _update_initial.metadata = {
        "url": "/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Batch/batchAccounts/{accountName}/privateEndpointConnections/{privateEndpointConnectionName}"
    }

    @overload
    def begin_update(
        self,
        resource_group_name: str,
        account_name: str,
        private_endpoint_connection_name: str,
        parameters: _models.PrivateEndpointConnection,
        if_match: Optional[str] = None,
        *,
        content_type: str = "application/json",
        **kwargs: Any
    ) -> LROPoller[_models.PrivateEndpointConnection]:
        """Updates the properties of an existing private endpoint connection.

        :param resource_group_name: The name of the resource group that contains the Batch account.
         Required.
        :type resource_group_name: str
        :param account_name: The name of the Batch account. Required.
        :type account_name: str
        :param private_endpoint_connection_name: The private endpoint connection name. This must be
         unique within the account. Required.
        :type private_endpoint_connection_name: str
        :param parameters: PrivateEndpointConnection properties that should be updated. Properties that
         are supplied will be updated, any property not supplied will be unchanged. Required.
        :type parameters: ~azure.mgmt.batch.models.PrivateEndpointConnection
        :param if_match: The state (ETag) version of the private endpoint connection to update. This
         value can be omitted or set to "*" to apply the operation unconditionally. Default value is
         None.
        :type if_match: str
        :keyword content_type: Body Parameter content-type. Content type parameter for JSON body.
         Default value is "application/json".
        :paramtype content_type: str
        :keyword callable cls: A custom type or function that will be passed the direct response
        :keyword str continuation_token: A continuation token to restart a poller from a saved state.
        :keyword polling: By default, your polling method will be ARMPolling. Pass in False for this
         operation to not poll, or pass in your own initialized polling object for a personal polling
         strategy.
        :paramtype polling: bool or ~azure.core.polling.PollingMethod
        :keyword int polling_interval: Default waiting time between two polls for LRO operations if no
         Retry-After header is present.
        :return: An instance of LROPoller that returns either PrivateEndpointConnection or the result
         of cls(response)
        :rtype: ~azure.core.polling.LROPoller[~azure.mgmt.batch.models.PrivateEndpointConnection]
        :raises ~azure.core.exceptions.HttpResponseError:
        """

    @overload
    def begin_update(
        self,
        resource_group_name: str,
        account_name: str,
        private_endpoint_connection_name: str,
        parameters: IO,
        if_match: Optional[str] = None,
        *,
        content_type: str = "application/json",
        **kwargs: Any
    ) -> LROPoller[_models.PrivateEndpointConnection]:
        """Updates the properties of an existing private endpoint connection.

        :param resource_group_name: The name of the resource group that contains the Batch account.
         Required.
        :type resource_group_name: str
        :param account_name: The name of the Batch account. Required.
        :type account_name: str
        :param private_endpoint_connection_name: The private endpoint connection name. This must be
         unique within the account. Required.
        :type private_endpoint_connection_name: str
        :param parameters: PrivateEndpointConnection properties that should be updated. Properties that
         are supplied will be updated, any property not supplied will be unchanged. Required.
        :type parameters: IO
        :param if_match: The state (ETag) version of the private endpoint connection to update. This
         value can be omitted or set to "*" to apply the operation unconditionally. Default value is
         None.
        :type if_match: str
        :keyword content_type: Body Parameter content-type. Content type parameter for binary body.
         Default value is "application/json".
        :paramtype content_type: str
        :keyword callable cls: A custom type or function that will be passed the direct response
        :keyword str continuation_token: A continuation token to restart a poller from a saved state.
        :keyword polling: By default, your polling method will be ARMPolling. Pass in False for this
         operation to not poll, or pass in your own initialized polling object for a personal polling
         strategy.
        :paramtype polling: bool or ~azure.core.polling.PollingMethod
        :keyword int polling_interval: Default waiting time between two polls for LRO operations if no
         Retry-After header is present.
        :return: An instance of LROPoller that returns either PrivateEndpointConnection or the result
         of cls(response)
        :rtype: ~azure.core.polling.LROPoller[~azure.mgmt.batch.models.PrivateEndpointConnection]
        :raises ~azure.core.exceptions.HttpResponseError:
        """

    @distributed_trace
    def begin_update(
        self,
        resource_group_name: str,
        account_name: str,
        private_endpoint_connection_name: str,
        parameters: Union[_models.PrivateEndpointConnection, IO],
        if_match: Optional[str] = None,
        **kwargs: Any
    ) -> LROPoller[_models.PrivateEndpointConnection]:
        """Updates the properties of an existing private endpoint connection.

        :param resource_group_name: The name of the resource group that contains the Batch account.
         Required.
        :type resource_group_name: str
        :param account_name: The name of the Batch account. Required.
        :type account_name: str
        :param private_endpoint_connection_name: The private endpoint connection name. This must be
         unique within the account. Required.
        :type private_endpoint_connection_name: str
        :param parameters: PrivateEndpointConnection properties that should be updated. Properties that
         are supplied will be updated, any property not supplied will be unchanged. Is either a
         PrivateEndpointConnection type or a IO type. Required.
        :type parameters: ~azure.mgmt.batch.models.PrivateEndpointConnection or IO
        :param if_match: The state (ETag) version of the private endpoint connection to update. This
         value can be omitted or set to "*" to apply the operation unconditionally. Default value is
         None.
        :type if_match: str
        :keyword content_type: Body Parameter content-type. Known values are: 'application/json'.
         Default value is None.
        :paramtype content_type: str
        :keyword callable cls: A custom type or function that will be passed the direct response
        :keyword str continuation_token: A continuation token to restart a poller from a saved state.
        :keyword polling: By default, your polling method will be ARMPolling. Pass in False for this
         operation to not poll, or pass in your own initialized polling object for a personal polling
         strategy.
        :paramtype polling: bool or ~azure.core.polling.PollingMethod
        :keyword int polling_interval: Default waiting time between two polls for LRO operations if no
         Retry-After header is present.
        :return: An instance of LROPoller that returns either PrivateEndpointConnection or the result
         of cls(response)
        :rtype: ~azure.core.polling.LROPoller[~azure.mgmt.batch.models.PrivateEndpointConnection]
        :raises ~azure.core.exceptions.HttpResponseError:
        """
        _headers = case_insensitive_dict(kwargs.pop("headers", {}) or {})
        _params = case_insensitive_dict(kwargs.pop("params", {}) or {})

        api_version: str = kwargs.pop("api_version", _params.pop("api-version", self._config.api_version))
        content_type: Optional[str] = kwargs.pop("content_type", _headers.pop("Content-Type", None))
        cls: ClsType[_models.PrivateEndpointConnection] = kwargs.pop("cls", None)
        polling: Union[bool, PollingMethod] = kwargs.pop("polling", True)
        lro_delay = kwargs.pop("polling_interval", self._config.polling_interval)
        cont_token: Optional[str] = kwargs.pop("continuation_token", None)
        if cont_token is None:
            raw_result = self._update_initial(
                resource_group_name=resource_group_name,
                account_name=account_name,
                private_endpoint_connection_name=private_endpoint_connection_name,
                parameters=parameters,
                if_match=if_match,
                api_version=api_version,
                content_type=content_type,
                cls=lambda x, y, z: x,
                headers=_headers,
                params=_params,
                **kwargs
            )
        kwargs.pop("error_map", None)

        def get_long_running_output(pipeline_response):
            deserialized = self._deserialize("PrivateEndpointConnection", pipeline_response)
            if cls:
                return cls(pipeline_response, deserialized, {})
            return deserialized

        if polling is True:
            polling_method: PollingMethod = cast(
                PollingMethod, ARMPolling(lro_delay, lro_options={"final-state-via": "azure-async-operation"}, **kwargs)
            )
        elif polling is False:
            polling_method = cast(PollingMethod, NoPolling())
        else:
            polling_method = polling
        if cont_token:
            return LROPoller.from_continuation_token(
                polling_method=polling_method,
                continuation_token=cont_token,
                client=self._client,
                deserialization_callback=get_long_running_output,
            )
        return LROPoller(self._client, raw_result, get_long_running_output, polling_method)  # type: ignore

    begin_update.metadata = {
        "url": "/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Batch/batchAccounts/{accountName}/privateEndpointConnections/{privateEndpointConnectionName}"
    }

    def _delete_initial(  # pylint: disable=inconsistent-return-statements
        self, resource_group_name: str, account_name: str, private_endpoint_connection_name: str, **kwargs: Any
    ) -> None:
        error_map = {
            401: ClientAuthenticationError,
            404: ResourceNotFoundError,
            409: ResourceExistsError,
            304: ResourceNotModifiedError,
        }
        error_map.update(kwargs.pop("error_map", {}) or {})

        _headers = kwargs.pop("headers", {}) or {}
        _params = case_insensitive_dict(kwargs.pop("params", {}) or {})

        api_version: str = kwargs.pop("api_version", _params.pop("api-version", self._config.api_version))
        cls: ClsType[None] = kwargs.pop("cls", None)

        request = build_delete_request(
            resource_group_name=resource_group_name,
            account_name=account_name,
            private_endpoint_connection_name=private_endpoint_connection_name,
            subscription_id=self._config.subscription_id,
            api_version=api_version,
            template_url=self._delete_initial.metadata["url"],
            headers=_headers,
            params=_params,
        )
        request = _convert_request(request)
        request.url = self._client.format_url(request.url)

        _stream = False
        pipeline_response: PipelineResponse = self._client._pipeline.run(  # pylint: disable=protected-access
            request, stream=_stream, **kwargs
        )

        response = pipeline_response.http_response

        if response.status_code not in [202, 204]:
            map_error(status_code=response.status_code, response=response, error_map=error_map)
            raise HttpResponseError(response=response, error_format=ARMErrorFormat)

        response_headers = {}
        if response.status_code == 202:
            response_headers["Location"] = self._deserialize("str", response.headers.get("Location"))
            response_headers["Retry-After"] = self._deserialize("int", response.headers.get("Retry-After"))

        if cls:
            return cls(pipeline_response, None, response_headers)

    _delete_initial.metadata = {
        "url": "/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Batch/batchAccounts/{accountName}/privateEndpointConnections/{privateEndpointConnectionName}"
    }

    @distributed_trace
    def begin_delete(
        self, resource_group_name: str, account_name: str, private_endpoint_connection_name: str, **kwargs: Any
    ) -> LROPoller[None]:
        """Deletes the specified private endpoint connection.

        :param resource_group_name: The name of the resource group that contains the Batch account.
         Required.
        :type resource_group_name: str
        :param account_name: The name of the Batch account. Required.
        :type account_name: str
        :param private_endpoint_connection_name: The private endpoint connection name. This must be
         unique within the account. Required.
        :type private_endpoint_connection_name: str
        :keyword callable cls: A custom type or function that will be passed the direct response
        :keyword str continuation_token: A continuation token to restart a poller from a saved state.
        :keyword polling: By default, your polling method will be ARMPolling. Pass in False for this
         operation to not poll, or pass in your own initialized polling object for a personal polling
         strategy.
        :paramtype polling: bool or ~azure.core.polling.PollingMethod
        :keyword int polling_interval: Default waiting time between two polls for LRO operations if no
         Retry-After header is present.
        :return: An instance of LROPoller that returns either None or the result of cls(response)
        :rtype: ~azure.core.polling.LROPoller[None]
        :raises ~azure.core.exceptions.HttpResponseError:
        """
        _headers = kwargs.pop("headers", {}) or {}
        _params = case_insensitive_dict(kwargs.pop("params", {}) or {})

        api_version: str = kwargs.pop("api_version", _params.pop("api-version", self._config.api_version))
        cls: ClsType[None] = kwargs.pop("cls", None)
        polling: Union[bool, PollingMethod] = kwargs.pop("polling", True)
        lro_delay = kwargs.pop("polling_interval", self._config.polling_interval)
        cont_token: Optional[str] = kwargs.pop("continuation_token", None)
        if cont_token is None:
            raw_result = self._delete_initial(  # type: ignore
                resource_group_name=resource_group_name,
                account_name=account_name,
                private_endpoint_connection_name=private_endpoint_connection_name,
                api_version=api_version,
                cls=lambda x, y, z: x,
                headers=_headers,
                params=_params,
                **kwargs
            )
        kwargs.pop("error_map", None)

        def get_long_running_output(pipeline_response):  # pylint: disable=inconsistent-return-statements
            if cls:
                return cls(pipeline_response, None, {})

        if polling is True:
            polling_method: PollingMethod = cast(
                PollingMethod, ARMPolling(lro_delay, lro_options={"final-state-via": "azure-async-operation"}, **kwargs)
            )
        elif polling is False:
            polling_method = cast(PollingMethod, NoPolling())
        else:
            polling_method = polling
        if cont_token:
            return LROPoller.from_continuation_token(
                polling_method=polling_method,
                continuation_token=cont_token,
                client=self._client,
                deserialization_callback=get_long_running_output,
            )
        return LROPoller(self._client, raw_result, get_long_running_output, polling_method)  # type: ignore

    begin_delete.metadata = {
        "url": "/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Batch/batchAccounts/{accountName}/privateEndpointConnections/{privateEndpointConnectionName}"
    }
