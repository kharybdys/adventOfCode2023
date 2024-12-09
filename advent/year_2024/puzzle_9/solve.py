from dataclasses import dataclass
from typing import Self

from registry import register_solver


def get_file_id(index: int) -> int:
    return index // 2


@register_solver(year="2024", key="9", variation="a")
def solve_a(puzzle_input: list[str], example: bool) -> None:
    print(puzzle_input)
    assert len(puzzle_input) == 1, "Day 9 can only work with a single line of input"

    disk_map = [int(char) for char in puzzle_input[0]]
    assert len(disk_map) % 2 == 1, "Day 9 expects an input of odd length"

    start_index = 0
    start_items_done = 0
    back_index = len(disk_map) - 1
    back_items_done = 0
    solution = 0
    result_index = 0
    while start_index < back_index or (start_index == back_index and back_items_done + start_items_done < disk_map[back_index]):
        print(f"{result_index=}, {start_index=}, {start_items_done=}, {back_index=}, {back_items_done=}, {disk_map[start_index]=}, {disk_map[back_index]=}")
        free = start_index % 2 != 0
        file_id = get_file_id(back_index if free else start_index)

        print(f"Current file_id: {file_id}, free: {free}")
        solution += result_index * file_id

        if free:
            back_items_done += 1
            start_items_done += 1
            while start_items_done >= disk_map[start_index]:
                start_index += 1
                start_items_done = 0
            while back_items_done >= disk_map[back_index]:
                back_index -= 2
                back_items_done = 0

        else:
            start_items_done += 1
            while start_items_done >= disk_map[start_index]:
                start_index += 1
                start_items_done = 0
        result_index += 1

    print(f"Solution is {solution}")


@dataclass
class DiskMapItem:
    free: bool
    file_id: int
    size: int

    next: Self | None = None
    previous: Self | None = None

    @classmethod
    def from_index_and_char(cls, index: int, char: str) -> Self:
        free = index % 2 != 0
        return cls(
            free=free,
            file_id=-1 if free else index // 2,
            size=int(char),
        )


def sum_disk_map(start_item: DiskMapItem) -> int:
    position = 0
    result = 0
    map_item = start_item
    while map_item is not None:
        if not map_item.free:
            result += sum(map_item.file_id * (position + index) for index in range(map_item.size))
        position += map_item.size
        map_item = map_item.next
    return result


def repr_disk_map(start_item: DiskMapItem) -> str:
    position = 0
    result = []
    map_item = start_item
    while map_item is not None:
        if not map_item.free:
            result.extend(str(map_item.file_id) * map_item.size)
        else:
            result.extend("." * map_item.size)
        position += map_item.size
        map_item = map_item.next
    return "".join(result)


def find_free_space_for(start_item: DiskMapItem, size: int, file_id: int) -> DiskMapItem | None:
    map_item = start_item
    print(f"Trying to find free space for {size=}, {file_id=}")
    while map_item is not None:
        if map_item.file_id == file_id:
            return None
        if map_item.free and map_item.size >= size:
            return map_item
        map_item = map_item.next
    return None


@register_solver(year="2024", key="9", variation="b")
def solve_b(puzzle_input: list[str], example: bool) -> None:
    print(puzzle_input)
    assert len(puzzle_input) == 1, "Day 9 can only work with a single line of input"

    disk_map = [DiskMapItem.from_index_and_char(index, char) for index, char in enumerate(puzzle_input[0])]
    assert len(disk_map) % 2 == 1, "Day 9 expects an input of odd length"

    # Turn into a doubly-linked list
    for index in range(len(disk_map)):
        map_item = disk_map[index]
        if index != 0:
            map_item.previous = disk_map[index - 1]
        if index < len(disk_map) - 1:
            map_item.next = disk_map[index + 1]

    start_item = disk_map[0]
    map_item = disk_map[-1]
    while map_item is not None:
        print(f"Progress: {repr_disk_map(start_item)}")
        file_item = map_item
        map_item = map_item.previous
        if not file_item.free:
            free_space = find_free_space_for(start_item, file_item.size, file_item.file_id)
            if free_space:
                new_free_space = DiskMapItem(free=True, file_id=-1, size=file_item.size)
                remaining_free_space = DiskMapItem(free=True, file_id=-1, size=free_space.size - file_item.size)

                # Insert new_free_space on the location of map_item
                new_free_space.previous = file_item.previous
                new_free_space.previous.next = new_free_space
                new_free_space.next = file_item.next
                if new_free_space.next:
                    new_free_space.next.previous = new_free_space

                # Insert map_item on the location of free_space, possibly padding with remaining_free_space
                file_item.previous = free_space.previous
                file_item.previous.next = file_item

                if remaining_free_space.size > 0:
                    file_item.next = remaining_free_space
                    file_item.next.previous = file_item
                    remaining_free_space.next = free_space.next
                    remaining_free_space.next.previous = remaining_free_space
                else:
                    file_item.next = free_space.next
                    file_item.next.previous = file_item

    print(f"Solution is {sum_disk_map(start_item)}")
