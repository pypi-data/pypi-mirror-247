# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is regenerated.
# --------------------------------------------------------------------------

from abc import ABC
from typing import TYPE_CHECKING

from azure.core.pipeline.transport import HttpRequest

from ._configuration import DeviceUpdateMgmtClientConfiguration

if TYPE_CHECKING:
    # pylint: disable=unused-import,ungrouped-imports
    from azure.core import AsyncPipelineClient

    from .._serialization import Deserializer, Serializer


class DeviceUpdateMgmtClientMixinABC(ABC):
    """DO NOT use this class. It is for internal typing use only."""

    _client: "AsyncPipelineClient"
    _config: DeviceUpdateMgmtClientConfiguration
    _serialize: "Serializer"
    _deserialize: "Deserializer"
