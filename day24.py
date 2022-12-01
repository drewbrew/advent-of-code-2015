import heapq

TEST_WEIGHTS = list(range(1, 6)) + list(range(7, 12))

def read_input(filename: str = 'day24.txt') -> list[int]:
    with open(filename) as infile:
        return sorted((int(line.strip()) for line in infile), reverse=True)
    

def get_target_weight(weights: list[int], part_two: bool = False) -> int:
    target = sum(weights) / (3 if not part_two else 4)
    assert target == int(target), target
    return int(target)



def part_one(weights: list[int], part_two: bool = False) -> int:
    """find the sum of weights which balances with the lowest quantum entanglement"""
    best_entanglement = 1
    for weight in weights:
        best_entanglement *= weight
    fewest_packages = len(weights)
    target_weight = get_target_weight(weights=weights, part_two=part_two)

    queue = []
    for index, value in enumerate(weights):
        heapq.heappush(queue, ([value], weights[index + 1:]))
    
    try:
        while (next_in_queue := heapq.heappop(queue)):
            package_list, remaining_weights = next_in_queue
            if len(package_list) > fewest_packages:
                continue
            total_weight = sum(package_list)
            if total_weight > target_weight:
                continue
            elif total_weight == target_weight:
                if len(package_list) > fewest_packages:
                    continue
                if len(package_list) == fewest_packages:
                    entanglement = 1
                    for pkg in package_list:
                        entanglement *= pkg
                    if entanglement >= best_entanglement:
                        continue
                    best_entanglement = entanglement
                    fewest_packages = len(package_list)
                    continue
                entanglement = 1
                for pkg in package_list:
                    entanglement *= pkg
                best_entanglement = entanglement
                fewest_packages = len(package_list)
                continue
            for index, next_pkg in enumerate(remaining_weights):
                heapq.heappush(queue, (package_list + [next_pkg], remaining_weights[index + 1:]))
    except IndexError:
        return best_entanglement

def main():
    assert part_one(TEST_WEIGHTS) == 99
    print(part_one(read_input()))
    assert part_one(TEST_WEIGHTS, True) == 44
    print(part_one(read_input(), True))


if __name__ == '__main__':
    main()