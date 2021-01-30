import dataclasses
import json
import logging
import sys
from collections import defaultdict, Counter
from typing import Callable, Dict, List

logger = logging.getLogger('data validator')
logger.setLevel(logging.INFO)

#
# Validator Configuration
#
DATA_PATH = "src/data/tracks.json"

#
# Class Definition
#


@dataclasses.dataclass
class Track:  # pylint: disable=too-many-instance-attributes
    id: int
    title: str
    singer: str
    artist: str
    videoid: str
    publishedAt: str
    tags: List[str]
    start: int
    end: int


@dataclasses.dataclass
class ValidationResult:
    is_valid: bool
    message: str


Task = Callable[[List[Track]], ValidationResult]


class Validator:
    def __init__(self):
        self._tasks: Dict[str, Task] = {}

    def add(self, name: str):
        def decorator(task: Task):
            assert name not in self._tasks
            self._tasks[name] = task

        return decorator

    def run(self, tracks: List[Track]) -> bool:
        success = True
        for name, task in self._tasks.items():
            result = task(tracks)

            if result.is_valid:
                logger.info("%s : %s", name, result.message)
            else:
                logger.error("%s : %s", name, result.message)
                success = False
        return success


#
# Validation Tasks
#

validator = Validator()


@validator.add("validate id duplication")
def validate_ids(tracks: List[Track]) -> ValidationResult:
    track_ids = [track.id for track in tracks]
    if len(track_ids) != len(set(track_ids)):
        duplicated_ids = [
            track_id for track_id, count in Counter(track_ids).items()
            if count > 1
        ]
        return ValidationResult(
            is_valid=False,
            message=f"Duplicated IDs: {duplicated_ids}",
        )
    return ValidationResult(True, "OK")


@validator.add("validate published date")
def validate_published_at(tracks: List[Track]) -> ValidationResult:
    videoToTracks: Dict[str, List[Track]] = defaultdict(list)
    for track in tracks:
        videoToTracks[track.videoid].append(track)

    invalid_videoids: List[str] = []
    for videoid, target_tracks in videoToTracks.items():
        dates = [track.publishedAt for track in target_tracks]

        if len(set(dates)) > 1:
            invalid_videoids.append(videoid)

    if invalid_videoids:
        return ValidationResult(
            is_valid=False,
            message=f"Published date not matched: {invalid_videoids}")

    return ValidationResult(True, "OK")


@validator.add("validate start / end time")
def validate_start_end_time(tracks: List[Track]) -> ValidationResult:
    invalid_ids: List[int] = []
    for track in tracks:
        if track.start > track.end:
            invalid_ids.append(track.id)

    if invalid_ids:
        return ValidationResult(
            is_valid=False,
            message=f"Start time must be less than end time: {invalid_ids}")

    return ValidationResult(True, "OK")


def main():
    logger.info("Data path: %s", DATA_PATH)

    with open(DATA_PATH, "r") as fp:
        tracks = [Track(**trackJson) for trackJson in json.load(fp)]

    success = validator.run(tracks)
    if not success:
        sys.exit(1)


if __name__ == "__main__":
    main()
