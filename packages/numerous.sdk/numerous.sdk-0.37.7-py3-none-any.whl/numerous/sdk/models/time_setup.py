from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Optional


class RunMode(Enum):
    CONTINUOUS = "continuous"
    DURATION = "duration"


@dataclass
class TimeSetup:
    run_mode: RunMode
    start: datetime
    end: Optional[datetime]
    duration: Optional[timedelta]

    @staticmethod
    def from_document(job_data: dict[str, Any]) -> "TimeSetup":
        run_settings: dict[str, Any] = job_data["runSettings"]
        run_mode = RunMode(run_settings["runMode"])
        start = datetime.fromisoformat(run_settings["startDate"])
        end = (
            datetime.fromisoformat(run_settings["endDate"])
            if run_settings.get("endDate") is not None
            else None
        )
        return TimeSetup(
            run_mode=run_mode,
            start=start,
            end=end,
            duration=None if end is None else end - start,
        )
