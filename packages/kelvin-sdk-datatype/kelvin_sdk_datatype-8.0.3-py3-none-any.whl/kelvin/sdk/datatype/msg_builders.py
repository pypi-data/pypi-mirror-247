from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Union

from pydantic import StrictBool, StrictFloat, StrictInt, StrictStr
from pydantic.dataclasses import dataclass
from pydantic.fields import Field

from kelvin.sdk.datatype import KRNAppVersion, KRNAsset, KRNAssetParameter, Message
from kelvin.sdk.datatype.base_messages import (
    EdgeParameter,
    ParametersMsg,
    ParametersPayload,
    ResourceParameters,
)


class MessageBuilder(ABC):
    @abstractmethod
    def to_message(self) -> Message:
        pass


@dataclass
class AssetParameter:
    """Asset Parameter Helper.

    Args:
        resource (KRNAssetParameter): Kelvin Resource name for the target Asset Parameter
        value (Union[bool, int, float, string]): parameter value
        comment (Optional[str]): optional comment for parameter change
    """

    resource: KRNAssetParameter
    value: Union[StrictBool, StrictInt, StrictFloat, StrictStr]
    comment: Optional[str] = None


@dataclass
class AssetParameters(MessageBuilder):
    """Parameters Builder. Set application parameters in bulk.

    Args:
        resource (Optional[KRNAppVersion]): Optional Kelvin Resource name for the target App Version.
            Defaults to current app.
        parameters (List[AssetParameters]): list of single asset parameters
    """

    parameters: List[AssetParameter]
    resource: Optional[KRNAppVersion] = None

    def to_message(self) -> ParametersMsg:
        asset_params: Dict[str, List[EdgeParameter]] = {}
        for asset_param in self.parameters:
            asset_params.setdefault(asset_param.resource.asset, []).append(
                EdgeParameter(name=asset_param.resource.parameter, value=asset_param.value, comment=asset_param.comment)
            )

        param_models = [
            ResourceParameters(resource=KRNAsset(asset), parameters=params) for asset, params in asset_params.items()
        ]

        return ParametersMsg(resource=self.resource, payload=ParametersPayload(resource_parameters=param_models))
