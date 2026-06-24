import os
import pytest
import responses
import duckdb
from ingestion.pipeline import run_pipeline

@pytest.fixture
def test_db_path():
    path = "data/test_pokedex.db"
    if os.path.exists(path):
        os.remove(path)
    yield path
    if os.path.exists(path):
        os.remove(path)

@pytest.fixture
def mock_pokeapi():
    with responses.RequestsMock(assert_all_requests_are_fired=False) as rsps:
        rsps.add(
            responses.GET,
            "https://pokeapi.co/api/v2/type/?limit=100",
            json={
                "results": [
                    {"name": "normal", "url": "https://pokeapi.co/api/v2/type/1/"},
                    {"name": "fire", "url": "https://pokeapi.co/api/v2/type/2/"}
                ],
                "next": None
            },
            status=200
        )
        rsps.add(
            responses.GET,
            "https://pokeapi.co/api/v2/type/1/",
            json={
                "id": 1,
                "name": "normal",
                "damage_relations": {
                    "double_damage_from": [],
                    "half_damage_from": [],
                    "no_damage_from": [],
                    "double_damage_to": [],
                    "half_damage_to": [],
                    "no_damage_to": []
                }
            },
            status=200
        )
        rsps.add(
            responses.GET,
            "https://pokeapi.co/api/v2/type/2/",
            json={
                "id": 2,
                "name": "fire",
                "damage_relations": {
                    "double_damage_from": [],
                    "half_damage_from": [],
                    "no_damage_from": [],
                    "double_damage_to": [],
                    "half_damage_to": [],
                    "no_damage_to": []
                }
            },
            status=200
        )

        rsps.add(
            responses.GET,
            "https://pokeapi.co/api/v2/ability/?limit=100",
            json={
                "results": [
                    {"name": "stench", "url": "https://pokeapi.co/api/v2/ability/1/"}
                ],
                "next": None
            },
            status=200
        )
        rsps.add(
            responses.GET,
            "https://pokeapi.co/api/v2/ability/1/",
            json={
                "id": 1,
                "name": "stench",
                "effect_entries": []
            },
            status=200
        )

        rsps.add(
            responses.GET,
            "https://pokeapi.co/api/v2/move/?limit=100",
            json={
                "results": [
                    {"name": "pound", "url": "https://pokeapi.co/api/v2/move/1/"}
                ],
                "next": None
            },
            status=200
        )
        rsps.add(
            responses.GET,
            "https://pokeapi.co/api/v2/move/1/",
            json={
                "id": 1,
                "name": "pound",
                "power": 40,
                "accuracy": 100,
                "type": {"name": "normal"},
                "damage_class": {"name": "physical"}
            },
            status=200
        )

        rsps.add(
            responses.GET,
            "https://pokeapi.co/api/v2/stat/?limit=100",
            json={
                "results": [
                    {"name": "hp", "url": "https://pokeapi.co/api/v2/stat/1/"}
                ],
                "next": None
            },
            status=200
        )
        rsps.add(
            responses.GET,
            "https://pokeapi.co/api/v2/stat/1/",
            json={
                "id": 1,
                "name": "hp",
                "game_index": 1
            },
            status=200
        )

        rsps.add(
            responses.GET,
            "https://pokeapi.co/api/v2/pokemon/?limit=100",
            json={
                "results": [
                    {"name": "bulbasaur", "url": "https://pokeapi.co/api/v2/pokemon/1/"},
                    {"name": "ivysaur", "url": "https://pokeapi.co/api/v2/pokemon/2/"}
                ],
                "next": None
            },
            status=200
        )
        rsps.add(
            responses.GET,
            "https://pokeapi.co/api/v2/pokemon/1/",
            json={
                "id": 1,
                "name": "bulbasaur",
                "height": 7,
                "weight": 69,
                "stats": [
                    {"base_stat": 45, "effort": 0, "stat": {"name": "hp", "url": "https://pokeapi.co/api/v2/stat/1/"}}
                ],
                "types": [
                    {"slot": 1, "type": {"name": "grass", "url": "https://pokeapi.co/api/v2/type/12/"}}
                ],
                "moves": [
                    {"move": {"name": "tackle", "url": "https://pokeapi.co/api/v2/move/33/"}}
                ]
            },
            status=200
        )
        rsps.add(
            responses.GET,
            "https://pokeapi.co/api/v2/pokemon/2/",
            json={
                "id": 2,
                "name": "ivysaur",
                "height": 10,
                "weight": 130,
                "stats": [
                    {"base_stat": 60, "effort": 0, "stat": {"name": "hp", "url": "https://pokeapi.co/api/v2/stat/1/"}}
                ],
                "types": [
                    {"slot": 1, "type": {"name": "grass", "url": "https://pokeapi.co/api/v2/type/12/"}}
                ],
                "moves": [
                    {"move": {"name": "tackle", "url": "https://pokeapi.co/api/v2/move/33/"}}
                ]
            },
            status=200
        )
        yield rsps

def test_pipeline_ingestion(test_db_path, mock_pokeapi):
    run_pipeline(db_path=test_db_path, pokemon_limit=0)
    
    conn = duckdb.connect(test_db_path)
    tables = [row[0] for row in conn.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'raw'").fetchall()]
    conn.close()
    
    expected_tables = ["pokemon", "types", "abilities", "moves", "stats", "pokemon__stats", "pokemon__types", "pokemon__moves"]
    for table in expected_tables:
        assert table in tables, f"Expected table '{table}' to be created in schema 'raw', but it was not. Found tables: {tables}"
        
    conn = duckdb.connect(test_db_path)
    
    pkmn_count = conn.execute("SELECT COUNT(*) FROM raw.pokemon").fetchone()[0]
    assert pkmn_count == 2, f"Expected 2 pokemon rows in raw.pokemon, but got {pkmn_count}"
    
    types_count = conn.execute("SELECT COUNT(*) FROM raw.types").fetchone()[0]
    assert types_count == 2, f"Expected 2 types rows in raw.types, but got {types_count}"
    
    moves_count = conn.execute("SELECT COUNT(*) FROM raw.moves").fetchone()[0]
    assert moves_count == 1, f"Expected 1 move row in raw.moves, but got {moves_count}"
    
    abilities_count = conn.execute("SELECT COUNT(*) FROM raw.abilities").fetchone()[0]
    assert abilities_count == 1, f"Expected 1 ability row in raw.abilities, but got {abilities_count}"
    
    stats_count = conn.execute("SELECT COUNT(*) FROM raw.stats").fetchone()[0]
    assert stats_count == 1, f"Expected 1 stat row in raw.stats, but got {stats_count}"
    
    pkmn_stats_count = conn.execute("SELECT COUNT(*) FROM raw.pokemon__stats").fetchone()[0]
    assert pkmn_stats_count == 2, f"Expected 2 nested pokemon__stats rows, but got {pkmn_stats_count}"
    
    conn.close()

def test_pipeline_pokemon_limit(test_db_path, mock_pokeapi):
    run_pipeline(db_path=test_db_path, pokemon_limit=1)
    
    conn = duckdb.connect(test_db_path)
    pkmn_count = conn.execute("SELECT COUNT(*) FROM raw.pokemon").fetchone()[0]
    types_count = conn.execute("SELECT COUNT(*) FROM raw.types").fetchone()[0]
    conn.close()
    
    assert pkmn_count == 1, f"Expected POKEMON_LIMIT=1 to restrict raw.pokemon rows to 1, but got {pkmn_count}"
    assert types_count == 2, f"Expected POKEMON_LIMIT=1 to NOT affect types lookup table, which should still have 2 rows, but got {types_count}"

def test_pipeline_retry_429_backoff(test_db_path):
    with responses.RequestsMock() as rsps:
        rsps.add(
            responses.GET,
            "https://pokeapi.co/api/v2/type/?limit=100",
            json={"results": [{"name": "normal", "url": "https://pokeapi.co/api/v2/type/1/"}], "next": None},
            status=200
        )
        rsps.add(
            responses.GET,
            "https://pokeapi.co/api/v2/type/1/",
            status=429
        )
        rsps.add(
            responses.GET,
            "https://pokeapi.co/api/v2/type/1/",
            json={"id": 1, "name": "normal", "damage_relations": {}},
            status=200
        )
        
        rsps.add(
            responses.GET,
            "https://pokeapi.co/api/v2/ability/?limit=100",
            json={"results": [], "next": None},
            status=200
        )
        rsps.add(
            responses.GET,
            "https://pokeapi.co/api/v2/move/?limit=100",
            json={"results": [], "next": None},
            status=200
        )
        rsps.add(
            responses.GET,
            "https://pokeapi.co/api/v2/stat/?limit=100",
            json={"results": [], "next": None},
            status=200
        )
        rsps.add(
            responses.GET,
            "https://pokeapi.co/api/v2/pokemon/?limit=100",
            json={"results": [], "next": None},
            status=200
        )
        
        run_pipeline(db_path=test_db_path, pokemon_limit=0)
        
        conn = duckdb.connect(test_db_path)
        types_count = conn.execute("SELECT COUNT(*) FROM raw.types").fetchone()[0]
        conn.close()
        
        assert types_count == 1, f"Expected types table to contain 1 row after successful retry, but got {types_count}"
