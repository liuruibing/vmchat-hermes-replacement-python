from typing import Callable, Optional


class RunLimiter:
    def __init__(self, capacity: int = 4) -> None:
        self.capacity = capacity
        self.activeCount = 0

    def get_capacity(self) -> int:
        return self.capacity

    getCapacity = get_capacity

    def get_active_count(self) -> int:
        return self.activeCount

    getActiveCount = get_active_count

    def try_acquire(self) -> Optional[Callable[[], None]]:
        if self.activeCount >= self.capacity:
            return None

        self.activeCount += 1
        released = False

        def release() -> None:
            nonlocal released
            if not released:
                released = True
                self.activeCount = max(0, self.activeCount - 1)

        return release

    tryAcquire = try_acquire
