import datetime
import time
from dataclasses import dataclass

from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams
from qdrant_client.http.models import CollectionStatus
from qdrant_client.http.models import PointStruct
from qdrant_client.http.models import UpdateStatus
from qdrant_client.http.models import Filter, FieldCondition, MatchValue




@dataclass
class timer:
    _start = None
    _end = None

    def __enter__(self) -> 'timer':
        if self._start is None:
            self._start = time.time_ns()
        else:
            raise ValueError("Cannot restart a timer!")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._start is None:
            raise ValueError("Must start a timer before ending it!")
        if self._end is not None:
            raise ValueError("TImer has already stopped!")
        self._end = time.time_ns()

    def duration(self) -> datetime.timedelta:
        if self._start is None or self._end is None:
            raise ValueError("Cannot calculate duration if timer has not run!")







def sep(n: int = 20) -> None:
    print("-" * n)


client = QdrantClient("localhost", port=6333)

create_response = client.recreate_collection(
    collection_name="test_collection",
    vectors_config=VectorParams(size=4, distance=Distance.DOT),
)
print(f"{create_response=}")
sep()

collection_info = client.get_collection(collection_name="test_collection")
print(f"{collection_info=}")
assert collection_info.status == CollectionStatus.GREEN
assert collection_info.vectors_count == 0
sep()


operation_info = client.upsert(
    collection_name="test_collection",
    wait=True,
    points=[
        PointStruct(id=1, vector=[0.05, 0.61, 0.76, 0.74], payload={"city": "Berlin"}),
        PointStruct(id=2, vector=[0.19, 0.81, 0.75, 0.11], payload={"city": ["Berlin", "London"]}),
        PointStruct(id=3, vector=[0.36, 0.55, 0.47, 0.94], payload={"city": ["Berlin", "Moscow"]}),
        PointStruct(id=4, vector=[0.18, 0.01, 0.85, 0.80], payload={"city": ["London", "Moscow"]}),
        PointStruct(id=5, vector=[0.24, 0.18, 0.22, 0.44], payload={"count": [0]}),
        PointStruct(id=6, vector=[0.35, 0.08, 0.11, 0.44]),
    ],
)
print(f"{operation_info=}")
assert operation_info.status == UpdateStatus.COMPLETED
sep()


search_result = client.search(collection_name="test_collection", query_vector=[0.2, 0.1, 0.9, 0.7], limit=3)
print(f"{search_result=}")
sep(2)
assert len(search_result) == 3
print(f"{search_result[0]=}")
# ScoredPoint(id=4, score=1.362, ...)
print(f"{search_result[1]=}")
# ScoredPoint(id=1, score=1.273, ...)
print(f"{search_result[2]=}")
# ScoredPoint(id=3, score=1.208, ...)
sep()


filtered_search_result = client.search(
    collection_name="test_collection",
    query_vector=[0.2, 0.1, 0.9, 0.7],
    query_filter=Filter(must=[FieldCondition(key="city", match=MatchValue(value="London"))]),
    limit=3,
)
assert len(filtered_search_result) == 2
print(f"{filtered_search_result=}")
sep(2)
print(f"{filtered_search_result[0]=}")
# ScoredPoint(id=4, score=1.362, ...)
print(f"{filtered_search_result[1]=}")
# ScoredPoint(id=2, score=0.871, ...)
sep()
