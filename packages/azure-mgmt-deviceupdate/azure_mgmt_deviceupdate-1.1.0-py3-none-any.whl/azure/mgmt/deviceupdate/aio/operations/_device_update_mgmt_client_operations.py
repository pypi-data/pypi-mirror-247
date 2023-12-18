# pylint: disable=too-many-lines
# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is regenerated.
# --------------------------------------------------------------------------
from io import IOBase
from typing import Any, Callable, Dict, IO, Optional, TypeVar, Union, overload

from azure.core.exceptions import (
    ClientAuthenticationError,
    HttpResponseError,
    ResourceExistsError,
    ResourceNotFoundError,
    ResourceNotModifiedError,
    map_error,
)
from azure.core.pipeline import PipelineResponse
from azure.core.pipeline.transport import AsyncHttpResponse
from azure.core.rest import HttpRequest
from azure.core.tracing.decorator_async import distributed_trace_async
from azure.core.utils import case_insensitive_dict
from azure.mgmt.core.exceptions import ARMErrorFormat

from ... import models as _models
from ..._vendor import _convert_request
from ...operations._device_update_mgmt_client_operations import build_check_name_availability_request
from .._vendor import DeviceUpdateMgmtClientMixinABC

T = TypeVar("T")
ClsType = Optional[Callable[[PipelineResponse[HttpRequest, AsyncHttpResponse], T, Dict[str, Any]], Any]]


class DeviceUpdateMgmtClientOperationsMixin(DeviceUpdateMgmtClientMixinABC):
    @overload
    async def check_name_availability(
        self, request: _models.CheckNameAvailabilityRequest, *, content_type: str = "application/json", **kwargs: Any
    ) -> _models.CheckNameAvailabilityResponse:
        """Checks ADU resource name availability.

        :param request: Check Name Availability Request. Required.
        :type request: ~azure.mgmt.deviceupdate.models.CheckNameAvailabilityRequest
        :keyword content_type: Body Parameter content-type. Content type parameter for JSON body.
         Default value is "application/json".
        :paramtype content_type: str
        :keyword callable cls: A custom type or function that will be passed the direct response
        :return: CheckNameAvailabilityResponse or the result of cls(response)
        :rtype: ~azure.mgmt.deviceupdate.models.CheckNameAvailabilityResponse
        :raises ~azure.core.exceptions.HttpResponseError:
        """

    @overload
    async def check_name_availability(
        self, request: IO, *, content_type: str = "application/json", **kwargs: Any
    ) -> _models.CheckNameAvailabilityResponse:
        """Checks ADU resource name availability.

        :param request: Check Name Availability Request. Required.
        :type request: IO
        :keyword content_type: Body Parameter content-type. Content type parameter for binary body.
         Default value is "application/json".
        :paramtype content_type: str
        :keyword callable cls: A custom type or function that will be passed the direct response
        :return: CheckNameAvailabilityResponse or the result of cls(response)
        :rtype: ~azure.mgmt.deviceupdate.models.CheckNameAvailabilityResponse
        :raises ~azure.core.exceptions.HttpResponseError:
        """

    @distributed_trace_async
    async def check_name_availability(
        self, request: Union[_models.CheckNameAvailabilityRequest, IO], **kwargs: Any
    ) -> _models.CheckNameAvailabilityResponse:
        """Checks ADU resource name availability.

        :param request: Check Name Availability Request. Is either a CheckNameAvailabilityRequest type
         or a IO type. Required.
        :type request: ~azure.mgmt.deviceupdate.models.CheckNameAvailabilityRequest or IO
        :keyword content_type: Body Parameter content-type. Known values are: 'application/json'.
         Default value is None.
        :paramtype content_type: str
        :keyword callable cls: A custom type or function that will be passed the direct response
        :return: CheckNameAvailabilityResponse or the result of cls(response)
        :rtype: ~azure.mgmt.deviceupdate.models.CheckNameAvailabilityResponse
        :raises ~azure.core.exceptions.HttpResponseError:
        """
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
        cls: ClsType[_models.CheckNameAvailabilityResponse] = kwargs.pop("cls", None)

        content_type = content_type or "application/json"
        _json = None
        _content = None
        if isinstance(request, (IOBase, bytes)):
            _content = request
        else:
            _json = self._serialize.body(request, "CheckNameAvailabilityRequest")

        request = build_check_name_availability_request(
            subscription_id=self._config.subscription_id,
            api_version=api_version,
            content_type=content_type,
            json=_json,
            content=_content,
            template_url=self.check_name_availability.metadata["url"],
            headers=_headers,
            params=_params,
        )
        request = _convert_request(request)
        request.url = self._client.format_url(request.url)

        _stream = False
        pipeline_response: PipelineResponse = await self._client._pipeline.run(  # type: ignore # pylint: disable=protected-access
            request, stream=_stream, **kwargs
        )

        response = pipeline_response.http_response

        if response.status_code not in [200]:
            map_error(status_code=response.status_code, response=response, error_map=error_map)
            error = self._deserialize.failsafe_deserialize(_models.ErrorResponse, pipeline_response)
            raise HttpResponseError(response=response, model=error, error_format=ARMErrorFormat)

        deserialized = self._deserialize("CheckNameAvailabilityResponse", pipeline_response)

        if cls:
            return cls(pipeline_response, deserialized, {})

        return deserialized

    check_name_availability.metadata = {
        "url": "/subscriptions/{subscriptionId}/providers/Microsoft.DeviceUpdate/checknameavailability"
    }
