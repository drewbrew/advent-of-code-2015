"""Day 21: Wizard simulator"""
from copy import deepcopy
from dataclasses import dataclass
from typing import Optional, Self
import heapq

# Puzzle input
BOSS_HIT = 58
BOSS_DAMAGE = 9
# givens
BOSS_ARMOR = 0
START_MANA = 500
HIT_POINTS = 50


@dataclass
class Spell:
    name: str
    mana_used: int
    instant_damage: int = 0
    instant_health: int = 0
    effect_turns: int = 0
    armor_boost: int = 0
    lingering_damage: int = 0
    mana_boost: int = 0
    effect_name: str = ""


@dataclass
class Fighter:
    hit_points: int
    armor: int
    mana: int
    damage: int
    active_effects: list[Spell]

    def receive_attack(self, damage) -> int:
        damage_dealt = damage - self.armor
        return damage_dealt

    def is_alive(self) -> bool:
        return self.hit_points > 0

    def apply_effects(self):
        added_effect = []
        for spell in list(self.active_effects) + added_effect:
            # print('applying effect', spell, spell.effect_turns)
            if spell.lingering_damage:
                self.hit_points -= spell.lingering_damage
            if spell.mana_boost:
                self.mana += spell.mana_boost
            if spell.armor_boost:
                self.armor = spell.armor_boost
            spell.effect_turns -= 1
            if spell.effect_turns <= 0:
                self.active_effects.remove(spell)
                # print(f'{spell.effect_name} wears off, {self.active_effects}')

    @property
    def shield_active(self) -> bool:
        return SHIELD.effect_name in {effect.name for effect in self.active_effects}


class Game:
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(\n\tplayer={self.player!r}, \n\topponent={self.opponent!r}, \n\tmana_used={self.mana_used},\n\tspells_used={', '.join(spell.name for spell in self.spells_used)}\n)"

    def __init__(
        self,
        player: Optional[Fighter] = None,
        opponent: Optional[Fighter] = None,
        mana_used: int = 0,
        spells_used: Optional[list[Spell]] = None,
    ) -> None:
        self.player = player or Fighter(
            hit_points=HIT_POINTS, armor=0, damage=0, mana=START_MANA, active_effects=[]
        )
        assert all(
            effect.effect_turns > 0 for effect in self.player.active_effects
        ), self.player.active_effects
        armor_boost_active = self.player.shield_active
        if armor_boost_active:
            self.player.armor = SHIELD.armor_boost
        else:
            self.player.armor = 0
        self.opponent = opponent or Fighter(
            hit_points=BOSS_HIT,
            damage=BOSS_DAMAGE,
            armor=BOSS_ARMOR,
            mana=0,
            active_effects=[],
        )
        self.mana_used = mana_used
        self.spells_used = spells_used or []

    def __lt__(self, other):
        if isinstance(other, Game):
            return self.mana_used < other.mana_used
        raise NotImplemented

    def apply_spell(self, spell: Spell) -> Self:
        spell = deepcopy(spell)
        if spell.effect_name == "Recharge":
            assert spell.effect_turns == 5, spell.effect_turns
        mana_used = self.mana_used + spell.mana_used
        player_mana = self.player.mana - spell.mana_used
        boss_hp = self.opponent.hit_points - spell.instant_damage
        player_hp = self.player.hit_points + spell.instant_health
        player_active_effects = self.player.active_effects[:]
        opponent_active_effects = self.opponent.active_effects[:]
        if spell.effect_turns > 0:
            if spell.mana_boost or spell.armor_boost:
                player_active_effects.append(spell)
            elif spell.lingering_damage:
                opponent_active_effects.append(spell)
            else:
                raise ValueError(f"Don't know how to apply {spell} to")
        assert all(
            effect.effect_turns > 0 for effect in player_active_effects
        ), self.player.active_effects
        return self.__class__(
            player=Fighter(
                hit_points=player_hp,
                armor=SHIELD.armor_boost
                if spell == SHIELD or self.player.shield_active
                else 0,
                mana=player_mana,
                damage=0,
                active_effects=player_active_effects,
            ),
            opponent=Fighter(
                hit_points=boss_hp,
                armor=0,
                mana=0,
                damage=self.opponent.damage,
                active_effects=opponent_active_effects,
            ),
            mana_used=mana_used,
            spells_used=self.spells_used + [spell],
        )

    def apply_boss_turn(self) -> Self:
        self.player.apply_effects()
        self.opponent.apply_effects()
        if not self.player.is_alive():
            raise GameOver(mana_used=self.mana_used, player_dead=True)
        if not self.opponent.is_alive():
            raise GameOver(mana_used=self.mana_used)
        damage_received = self.player.receive_attack(self.opponent.damage)
        player_hp = self.player.hit_points
        player_hp -= damage_received
        if player_hp <= 0:
            raise GameOver(mana_used=self.mana_used, player_dead=True)
        return self.__class__(
            player=Fighter(
                hit_points=player_hp,
                mana=self.player.mana,
                armor=self.player.armor,
                damage=0,
                active_effects=self.player.active_effects,
            ),
            opponent=Fighter(
                hit_points=self.opponent.hit_points,
                armor=self.opponent.armor,
                mana=0,
                damage=self.opponent.damage,
                active_effects=self.opponent.active_effects,
            ),
            mana_used=self.mana_used,
            spells_used=self.spells_used,
        )

    def take_turn(self) -> list[Self]:
        new_game_states = []
        self.player.apply_effects()
        self.opponent.apply_effects()
        assert all(
            effect.effect_turns > 0 for effect in self.player.active_effects
        ), self.player.active_effects
        if not self.player.is_alive():
            raise GameOver(self.mana_used, player_dead=True)
        if not self.opponent.is_alive():
            raise GameOver(self.mana_used)

        active_effects = {
            effect.effect_name
            for effect in self.player.active_effects + self.opponent.active_effects
        }
        for spell in SPELL_OPTIONS:
            new_game = deepcopy(self)
            if spell.effect_name and spell.effect_name in active_effects:
                continue
            if spell.mana_used > self.player.mana:
                # can't use it
                continue
            # print(f'applying spell {spell.effect_name} to {self}')
            new_game = new_game.apply_spell(spell)
            if not new_game.opponent.is_alive():
                new_game_states.append(new_game)
                continue

            # now boss attacks
            try:
                new_game = new_game.apply_boss_turn()
            except GameOver as exc:
                if exc.player_dead:
                    continue
            new_game_states.append(new_game)

        return new_game_states


class PartTwoGame(Game):
    def take_turn(self) -> list[Self]:
        self.player.hit_points -= 1
        if self.player.hit_points <= 0:
            raise GameOver(self.mana_used, player_dead=True)
        return super().take_turn()

    def apply_boss_turn(self) -> Self:
        self.player.hit_points -= 1
        if self.player.hit_points <= 0:
            raise GameOver(self.mana_used, player_dead=True)
        return super().apply_boss_turn()


class GameOver(Exception):
    def __init__(
        self, mana_used: int, player_dead: bool = False, *args: object
    ) -> None:
        self.mana_used = mana_used
        self.player_dead = player_dead
        super().__init__(*args)


MAGIC_MISSILE = Spell(name="Magic Missile", mana_used=53, instant_damage=4)
DRAIN = Spell(name="Drain", mana_used=73, instant_damage=2, instant_health=2)
SHIELD = Spell(
    name="Shield", mana_used=113, effect_turns=6, armor_boost=7, effect_name="shield"
)
POISON = Spell(
    name="Poison",
    mana_used=173,
    effect_turns=6,
    lingering_damage=3,
    effect_name="poison",
)
RECHARGE = Spell(
    name="Recharge",
    mana_used=229,
    effect_turns=5,
    mana_boost=101,
    effect_name="recharge",
)

SPELL_OPTIONS = [MAGIC_MISSILE, DRAIN, SHIELD, POISON, RECHARGE]

ARMOR_OPTIONS = [
    (0, 0),  # nothing
]


def part_one(
    player_mana: int = 500,
    player_hp: int = 50,
    boss_hp: int = BOSS_HIT,
    boss_damage: int = BOSS_DAMAGE,
) -> int:
    """Part 1: fewest mana spent while winning"""
    best_cost = int(1e9)
    games: list[Game] = [
        Game(
            player=Fighter(
                hit_points=player_hp,
                armor=0,
                mana=player_mana,
                damage=0,
                active_effects=[],
            ),
            opponent=Fighter(
                hit_points=boss_hp,
                armor=0,
                damage=boss_damage,
                active_effects=[],
                mana=0,
            ),
            mana_used=0,
            spells_used=[],
        )
    ]
    while games:
        try:
            next_game = games.pop(0)
        except IndexError:
            break
        mana_used = next_game.mana_used
        if not next_game.player.is_alive():
            # print(f"player dead, {next_game.opponent.hit_points=}, {mana_used=}")
            continue
        if not next_game.opponent.is_alive():
            # print(f"Opponent dead! {mana_used=}, {next_game}")
            best_cost = min(mana_used, best_cost)
            continue
        if mana_used >= best_cost:
            # print(f"too much {mana_used=}, {len(games)=}", end="\r")
            continue
        try:
            next_states = next_game.take_turn()
        except GameOver as exc:
            if not exc.player_dead and exc.mana_used < best_cost:
                # print(f"opponent dead during turn!  {exc.mana_used=}")
                best_cost = min(exc.mana_used, best_cost)
            continue
        games.extend(next_states)
        # print(next_states, len(games))
    return best_cost


def part_two(
    player_mana: int = 500,
    player_hp: int = 50,
    boss_hp: int = BOSS_HIT,
    boss_damage: int = BOSS_DAMAGE,
) -> int:
    """Part 1: fewest mana spent while winning"""
    best_cost = int(1e9)
    games: list[PartTwoGame] = [
        PartTwoGame(
            player=Fighter(
                hit_points=player_hp,
                armor=0,
                mana=player_mana,
                damage=0,
                active_effects=[],
            ),
            opponent=Fighter(
                hit_points=boss_hp,
                armor=0,
                damage=boss_damage,
                active_effects=[],
                mana=0,
            ),
            mana_used=0,
            spells_used=[],
        )
    ]
    while games:
        try:
            next_game = games.pop(0)
        except IndexError:
            break
        mana_used = next_game.mana_used
        if not next_game.player.is_alive():
            # print(f"player dead, {next_game.opponent.hit_points=}, {mana_used=}")
            continue
        if not next_game.opponent.is_alive():
            # print(f"Opponent dead! {mana_used=}, {next_game}")
            best_cost = min(mana_used, best_cost)
            continue
        if mana_used >= best_cost:
            # print(f"too much {mana_used=}, {len(games)=}", end="\r")
            continue
        try:
            next_states = next_game.take_turn()
        except GameOver as exc:
            if not exc.player_dead and exc.mana_used < best_cost:
                # print(f"opponent dead during turn!  {exc.mana_used=}")
                best_cost = min(exc.mana_used, best_cost)
            continue
        games.extend(next_states)
        # print(next_states, len(games))
    return best_cost


def main():
    test_1 = part_one(player_hp=10, player_mana=250, boss_damage=8, boss_hp=13)
    assert test_1 == (POISON.mana_used + MAGIC_MISSILE.mana_used), test_1
    test_2 = part_one(player_hp=10, player_mana=250, boss_damage=8, boss_hp=14)
    assert test_2 == (
        RECHARGE.mana_used
        + SHIELD.mana_used
        + DRAIN.mana_used
        + POISON.mana_used
        + MAGIC_MISSILE.mana_used
    ), test_2
    print("tests passed, on to part 1")
    print(part_one())
    print(part_two())


if __name__ == "__main__":
    main()
