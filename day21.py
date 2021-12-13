"""Day 21: RPG simulator"""
from itertools import permutations

# Puzzle input
BOSS_HIT = 104
BOSS_DAMAGE = 8
BOSS_ARMOR = 1


class Fighter:
    def __init__(self, hit_points: int, damage: int, armor: int) -> None:
        self.hit_points = hit_points
        self.damage = damage
        self.armor = armor

    def receive_attack(self, damage) -> bool:
        damage_dealt = max([1, damage - self.armor])
        self.hit_points -= damage_dealt
        return self.is_alive()

    def is_alive(self) -> bool:
        return self.hit_points > 0


WEAPON_OPTIONS = [
    (8, 4),  # dagger
    (10, 5),  # shortsword
    (25, 6),  # warhammer
    (40, 7),  # longsword
    (74, 8),  # great axe
]

ARMOR_OPTIONS = [
    (0, 0),  # nothing
    (13, 1),  # leather
    (31, 2),  # chain mail
    (53, 3),  # splint mail
    (75, 4),  # banded
    (102, 5),  # plate
]

RING_OPTIONS = list(
    permutations(
        [
            (0, 0, 0),  # nothing - 1
            (0, 0, 0),  # nothing - 2
            (25, 1, 0),  # +1 damage
            (50, 2, 0),  # +2 dmg
            (100, 3, 0),  # +3
            (20, 0, 1),  # +1 armor
            (40, 0, 2),  # +2
            (80, 0, 3),  # +3
        ],
        2,
    )
)


def part_one(your_hit_points: int = 100) -> int:
    """Part 1: fewest gold spent while winning"""
    best_cost = int(1e9)
    for weapon_cost, weapon_damage in WEAPON_OPTIONS:
        for armor_cost, armor_boost in ARMOR_OPTIONS:
            for (ring1_cost, ring_1_damage, ring_1_armor), (
                ring2_cost,
                ring2_damage,
                ring2_armor,
            ) in RING_OPTIONS:
                player = Fighter(
                    hit_points=your_hit_points,
                    damage=weapon_damage + ring_1_damage + ring2_damage,
                    armor=armor_boost + ring_1_armor + ring2_armor,
                )
                boss = Fighter(
                    hit_points=BOSS_HIT, damage=BOSS_DAMAGE, armor=BOSS_ARMOR
                )
                while player.is_alive():
                    boss.receive_attack(player.damage)
                    if not boss.is_alive():
                        cost = weapon_cost + armor_cost + ring1_cost + ring2_cost
                        if cost < best_cost:
                            best_cost = cost
                        break
                    player.receive_attack(boss.damage)
    return best_cost


def part_two(your_hit_points: int = 100) -> int:
    """Part 2: most gold spent while losing"""
    best_cost = 0
    for weapon_cost, weapon_damage in WEAPON_OPTIONS:
        for armor_cost, armor_boost in ARMOR_OPTIONS:
            for (ring1_cost, ring_1_damage, ring_1_armor), (
                ring2_cost,
                ring2_damage,
                ring2_armor,
            ) in RING_OPTIONS:
                player = Fighter(
                    hit_points=your_hit_points,
                    damage=weapon_damage + ring_1_damage + ring2_damage,
                    armor=armor_boost + ring_1_armor + ring2_armor,
                )
                boss = Fighter(
                    hit_points=BOSS_HIT, damage=BOSS_DAMAGE, armor=BOSS_ARMOR
                )
                while boss.is_alive():
                    boss.receive_attack(player.damage)
                    if not boss.is_alive():
                        break
                    player.receive_attack(boss.damage)
                    if not player.is_alive():
                        cost = weapon_cost + armor_cost + ring1_cost + ring2_cost
                        if cost > best_cost:
                            best_cost = cost
                        break

    return best_cost


def main():
    print(part_one())
    print(part_two())


if __name__ == "__main__":
    main()
