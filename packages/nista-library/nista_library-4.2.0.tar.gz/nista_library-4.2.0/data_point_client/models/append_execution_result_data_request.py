from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.sub_series_request import SubSeriesRequest


T = TypeVar("T", bound="AppendExecutionResultDataRequest")


@attr.s(auto_attribs=True)
class AppendExecutionResultDataRequest:
    """
    Attributes:
        sub_series (List['SubSeriesRequest']):
        unit (Union[Unset, None, str]):
        execution_id (Union[Unset, str]):
        time_zone (Union[Unset, None, str]):
        finished (Union[Unset, bool]):
        is_major_change (Union[Unset, bool]):
    """

    sub_series: List["SubSeriesRequest"]
    unit: Union[Unset, None, str] = UNSET
    execution_id: Union[Unset, str] = UNSET
    time_zone: Union[Unset, None, str] = UNSET
    finished: Union[Unset, bool] = UNSET
    is_major_change: Union[Unset, bool] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        sub_series = []
        for sub_series_item_data in self.sub_series:
            sub_series_item = sub_series_item_data.to_dict()

            sub_series.append(sub_series_item)

        unit = self.unit
        execution_id = self.execution_id
        time_zone = self.time_zone
        finished = self.finished
        is_major_change = self.is_major_change

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "subSeries": sub_series,
            }
        )
        if unit is not UNSET:
            field_dict["unit"] = unit
        if execution_id is not UNSET:
            field_dict["executionId"] = execution_id
        if time_zone is not UNSET:
            field_dict["timeZone"] = time_zone
        if finished is not UNSET:
            field_dict["finished"] = finished
        if is_major_change is not UNSET:
            field_dict["isMajorChange"] = is_major_change

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.sub_series_request import SubSeriesRequest

        d = src_dict.copy()
        sub_series = []
        _sub_series = d.pop("subSeries")
        for sub_series_item_data in _sub_series:
            sub_series_item = SubSeriesRequest.from_dict(sub_series_item_data)

            sub_series.append(sub_series_item)

        unit = d.pop("unit", UNSET)

        execution_id = d.pop("executionId", UNSET)

        time_zone = d.pop("timeZone", UNSET)

        finished = d.pop("finished", UNSET)

        is_major_change = d.pop("isMajorChange", UNSET)

        append_execution_result_data_request = cls(
            sub_series=sub_series,
            unit=unit,
            execution_id=execution_id,
            time_zone=time_zone,
            finished=finished,
            is_major_change=is_major_change,
        )

        return append_execution_result_data_request
