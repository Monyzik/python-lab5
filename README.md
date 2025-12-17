from src.models.game_entity import GameEntity

## Лабораторная работа №4 (Казино)

В лабораторной работе реализован простой CLI интерфейс,
для его запуска необходимо запустить команду:

```shell
python -m src.main
```

После чего надо ввести количество шагов (положительное число),
а также сид (либо None при его отсутствии)

### Архитектура:
```
.
├── collections
│   ├── casino_balance.py
│   ├── chip_collection.py
│   ├── goose_collection.py
│   └── player_collection.py
├── common
│   ├── config.py
│   ├── constants.py
│   └── exceptions.py
├── models
│   ├── collection.py
│   ├── dict_entity.py
│   ├── game_entity.py
│   └── list_entity.py
├── objects
│   ├── casino.py
│   ├── chip.py
│   ├── goose.py
│   └── player.py
├── main.py
└── simulation.py
```

### Описание:

#### Реализованные сущности:

##### Гуси:

В качестве сущностей реализованны гуси, ниже приведены основной функционал:

Самый обычный гусь - умеет издавать различные звуки

```python
class Goose(GameEntity):
    def __call__(self, *args, **kwargs):
        ...

    def honk(self) -> None:
        ...
```

Агрессивный гусь - может атаковать и воровать фишки у игрока

```python
class WarGoose(Goose):
    def attack(self, player: Player, casino_balances: CasinoBalances, unregister_func: Callable) -> None:
        ...

    def steal_chip(self, player: Player, index: int) -> None:
        ...
```

Громкий гусь - может использовать свою суперспособность

```python
class HonkGoose(Goose):
    def superpower(self, players: PlayerCollection, casino_balances: CasinoBalances,
                   unregister_func: Callable) -> None:
        ...
```

Для них реализована коллекция GooseCollection,
в ней реализованы методы эволюции и начала дискотеки:

```python
class GooseCollection(ListEntity[Goose]):
    expected_type = Goose

    def disco(self) -> None:
        ...

    def evolution(self, power: int = 1) -> None:
        ...

```

##### Игроки:

Реализованы игроки, которые умеют крутить рулетку:

```python
class Player(GameEntity):
    def spin(self, bet: int | Chip, casino_balances: CasinoBalances, unregister_func: Callable) -> None: ...
```

Реализованна коллекция игроков,
которая поддерживает игру в покер и начало дискотеки игроков:

```python
class PlayerCollection(ListEntity[Player]):
    expected_type = Player

    def disco(self) -> None:
        ...

    def play_pocker(self, bet: int | Chip, casino_balances: CasinoBalances, unregister_func: Callable) -> None:
        ...
```

##### Фишки:

Реализованны фишки, а также их коллекция, с ними можно производить различные операции:
вычитать, складывать, сравнивать.

Сущности в казино имеют свой баланс, то есть ChipCollection

