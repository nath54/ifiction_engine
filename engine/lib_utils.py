#
from typing import Any, Optional
#
import heapq
#
from . import engine_classes_time as ect


#
### Function to convert a string from a str(list) to a JSON compatible version. ###
#
def str_list_to_json(txt: str) -> str:
    #
    replacements: dict[str, str] = {
        "None": "null",
        "False": "false",
        "True": "true",
        "'": "\""
    }
    #
    for r, v in replacements.items():
        #
        txt = txt.replace(r, v)
    #
    return txt


#
### Function to get the class name ###
#
def get_class_name(a: Any) -> str:
    #
    b = str(a.__class__)
    #
    l = "'"
    #
    d = b.find(l) + len(l)
    #
    dd = b.find("'", d)
    #
    c = b[d:dd]
    #
    return c


#
### Priority Queue class. ###
#
class PriorityQueue:

    #
    def __init__(self, initial_values: list[tuple[Any, ect.GameTime]] = []) -> None:
        # The heap will store tuples of (priority, item)
        # heapq is a min-heap, so lower priority values will be retrieved first.
        self._queue: list[tuple[ect.GameTime, int, Any]] = []
        # A counter to ensure stable ordering for items with the same priority
        # (useful if you want FIFO for equal-priority items)
        self._counter: int = 0

    #
    def insert_with_priority(self, item: Any, priority: ect.GameTime) -> None:
        """
        Inserts an item into the priority queue with a given priority.
        Lower priority values are considered higher priority (min-heap behavior).
        """
        # We negate the priority because heapq is a min-heap, and we want
        # higher "priority" (lower number) items to come out first.
        # The counter ensures that if priorities are equal, items inserted
        # earlier are retrieved earlier (FIFO).
        entry: tuple[ect.GameTime, int, Any] = (priority, self._counter, item)
        #
        heapq.heappush(self._queue, entry)
        #
        self._counter += 1

    #
    def pop_top(self) -> Optional[tuple[Any, ect.GameTime]]:
        """
        Retrieves and removes the item with the highest priority (lowest priority value).
        Returns None if the queue is empty.
        """

        #
        if not self._queue:
            #
            return None

        #
        ### The item is the last element of the tuple. ###
        #
        priority: ect.GameTime
        _count: int
        item: Any
        #
        priority, _count, item = heapq.heappop(self._queue)

        #
        ### Return the value. ###
        #
        return (item, priority)

    #
    def shift_all_times(self, time_shift: ect.GameTime) -> None:
        #
        for i, elt_tuple in enumerate(self._queue):
            #
            self._queue[i] = (elt_tuple[0] - time_shift, elt_tuple[1], elt_tuple[2])

    #
    def is_empty(self) -> bool:
        """
        Checks if the priority queue is empty.
        """
        #
        return not self._queue

    #
    def __len__(self) -> int:
        """
        Returns the number of items in the priority queue.
        """
        #
        return len(self._queue)


#
class PQ_Entity_and_EventsSystem:

    #
    def __init__(
        self,
        elt_type: str,
        elt_id: str,
        current_action: Optional[Any],
        current_action_time: ect.GameTime,
        can_be_interrupted: bool = True,
        repetitive: bool = False,
    ) -> None:

        #
        self.elt_type: str = elt_type
        self.elt_id: str = elt_id
        self.current_action: Optional[Any] = current_action
        self.current_action_time: ect.GameTime = current_action_time
        self.can_be_interrupted: bool = can_be_interrupted
        self.repetitive: bool = repetitive

