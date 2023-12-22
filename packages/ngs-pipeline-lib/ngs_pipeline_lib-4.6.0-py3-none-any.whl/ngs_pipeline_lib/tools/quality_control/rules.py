from operator import attrgetter

from pydantic import BaseModel, conlist

from ngs_pipeline_lib.tools.quality_control.operators import Operator


class Rule(BaseModel):
    key: str
    operator: Operator
    value: conlist(
        item_type=float | int, min_items=2, max_items=2
    ) | float | int | str | None

    def apply(self, observations: dict[str, str | float | int]) -> bool:
        return self.operator.function(observations[self.key], self.value)

    class Config:
        json_encoders = {
            Operator: attrgetter("description"),
        }
