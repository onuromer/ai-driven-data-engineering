import os
import subprocess

import duckdb
import pytest

from ingestion.pipeline import run_pipeline

TRANSFORM_DIR = os.path.join(os.path.dirname(__file__), "..", "transform")


@pytest.fixture
def transform_test_db_path():
    path = "data/test_pokedex.db"
    if os.path.exists(path):
        os.remove(path)
    yield path
    if os.path.exists(path):
        os.remove(path)


@pytest.fixture
def mock_pokeapi():
    import responses

    with responses.RequestsMock(assert_all_requests_are_fired=False) as rsps:
        rsps.add(
            responses.GET,
            "https://pokeapi.co/api/v2/type/?limit=100",
            json={
                "results": [
                    {"name": "normal", "url": "https://pokeapi.co/api/v2/type/1/"},
                    {"name": "fire", "url": "https://pokeapi.co/api/v2/type/10/"},
                    {"name": "electric", "url": "https://pokeapi.co/api/v2/type/13/"},
                ],
                "next": None,
            },
            status=200,
        )
        rsps.add(
            responses.GET,
            "https://pokeapi.co/api/v2/type/1/",
            json={
                "id": 1,
                "name": "normal",
                "generation": {"name": "generation-i", "url": "https://pokeapi.co/api/v2/generation/1/"},
                "move_damage_class": {"name": "physical", "url": "https://pokeapi.co/api/v2/move-damage-class/2/"},
                "damage_relations": {
                    "double_damage_from": [],
                    "half_damage_from": [{"name": "fighting", "url": "https://pokeapi.co/api/v2/type/2/"}],
                    "no_damage_from": [],
                    "double_damage_to": [],
                    "half_damage_to": [{"name": "rock", "url": "https://pokeapi.co/api/v2/type/13/"}],
                    "no_damage_to": [],
                },
            },
            status=200,
        )
        rsps.add(
            responses.GET,
            "https://pokeapi.co/api/v2/type/10/",
            json={
                "id": 10,
                "name": "fire",
                "generation": {"name": "generation-i", "url": "https://pokeapi.co/api/v2/generation/1/"},
                "move_damage_class": {"name": "special", "url": "https://pokeapi.co/api/v2/move-damage-class/3/"},
                "damage_relations": {
                    "double_damage_from": [{"name": "water", "url": "https://pokeapi.co/api/v2/type/11/"}],
                    "half_damage_from": [{"name": "fire", "url": "https://pokeapi.co/api/v2/type/10/"}],
                    "no_damage_from": [],
                    "double_damage_to": [{"name": "grass", "url": "https://pokeapi.co/api/v2/type/12/"}],
                    "half_damage_to": [{"name": "fire", "url": "https://pokeapi.co/api/v2/type/10/"}],
                    "no_damage_to": [],
                },
            },
            status=200,
        )
        rsps.add(
            responses.GET,
            "https://pokeapi.co/api/v2/type/13/",
            json={
                "id": 13,
                "name": "electric",
                "generation": {"name": "generation-i", "url": "https://pokeapi.co/api/v2/generation/1/"},
                "move_damage_class": {"name": "special", "url": "https://pokeapi.co/api/v2/move-damage-class/3/"},
                "damage_relations": {
                    "double_damage_from": [{"name": "ground", "url": "https://pokeapi.co/api/v2/type/5/"}],
                    "half_damage_from": [],
                    "no_damage_from": [],
                    "double_damage_to": [{"name": "water", "url": "https://pokeapi.co/api/v2/type/11/"}],
                    "half_damage_to": [{"name": "grass", "url": "https://pokeapi.co/api/v2/type/12/"}],
                    "no_damage_to": [{"name": "ground", "url": "https://pokeapi.co/api/v2/type/5/"}],
                },
            },
            status=200,
        )

        rsps.add(
            responses.GET,
            "https://pokeapi.co/api/v2/ability/?limit=100",
            json={"results": [{"name": "static", "url": "https://pokeapi.co/api/v2/ability/9/"}], "next": None},
            status=200,
        )
        rsps.add(
            responses.GET,
            "https://pokeapi.co/api/v2/ability/9/",
            json={
                "id": 9,
                "name": "static",
                "is_main_series": True,
                "generation": {"name": "generation-iii", "url": "https://pokeapi.co/api/v2/generation/3/"},
                "effect_entries": [],
            },
            status=200,
        )

        rsps.add(
            responses.GET,
            "https://pokeapi.co/api/v2/move/?limit=100",
            json={
                "results": [
                    {"name": "thunder-shock", "url": "https://pokeapi.co/api/v2/move/84/"},
                    {"name": "tackle", "url": "https://pokeapi.co/api/v2/move/33/"},
                ],
                "next": None,
            },
            status=200,
        )
        rsps.add(
            responses.GET,
            "https://pokeapi.co/api/v2/move/84/",
            json={
                "id": 84,
                "name": "thunder-shock",
                "power": 40,
                "accuracy": 100,
                "pp": 30,
                "priority": 0,
                "type": {"name": "electric", "url": "https://pokeapi.co/api/v2/type/13/"},
                "damage_class": {"name": "special", "url": "https://pokeapi.co/api/v2/move-damage-class/3/"},
                "generation": {"name": "generation-i", "url": "https://pokeapi.co/api/v2/generation/1/"},
            },
            status=200,
        )
        rsps.add(
            responses.GET,
            "https://pokeapi.co/api/v2/move/33/",
            json={
                "id": 33,
                "name": "tackle",
                "power": 40,
                "accuracy": 100,
                "pp": 35,
                "priority": 0,
                "type": {"name": "normal", "url": "https://pokeapi.co/api/v2/type/1/"},
                "damage_class": {"name": "physical", "url": "https://pokeapi.co/api/v2/move-damage-class/2/"},
                "generation": {"name": "generation-i", "url": "https://pokeapi.co/api/v2/generation/1/"},
            },
            status=200,
        )

        rsps.add(
            responses.GET,
            "https://pokeapi.co/api/v2/stat/?limit=100",
            json={
                "results": [
                    {"name": "hp", "url": "https://pokeapi.co/api/v2/stat/1/"},
                    {"name": "attack", "url": "https://pokeapi.co/api/v2/stat/2/"},
                    {"name": "defense", "url": "https://pokeapi.co/api/v2/stat/3/"},
                    {"name": "special-attack", "url": "https://pokeapi.co/api/v2/stat/4/"},
                    {"name": "special-defense", "url": "https://pokeapi.co/api/v2/stat/5/"},
                    {"name": "speed", "url": "https://pokeapi.co/api/v2/stat/6/"},
                ],
                "next": None,
            },
            status=200,
        )
        for stat_id, stat_name in [
            (1, "hp"),
            (2, "attack"),
            (3, "defense"),
            (4, "special-attack"),
            (5, "special-defense"),
            (6, "speed"),
        ]:
            rsps.add(
                responses.GET,
                f"https://pokeapi.co/api/v2/stat/{stat_id}/",
                json={"id": stat_id, "name": stat_name, "game_index": stat_id, "is_battle_only": False},
                status=200,
            )

        rsps.add(
            responses.GET,
            "https://pokeapi.co/api/v2/pokemon/?limit=100",
            json={
                "results": [{"name": "pikachu", "url": "https://pokeapi.co/api/v2/pokemon/25/"}],
                "next": None,
            },
            status=200,
        )
        rsps.add(
            responses.GET,
            "https://pokeapi.co/api/v2/pokemon/25/",
            json={
                "id": 25,
                "name": "pikachu",
                "base_experience": 112,
                "height": 4,
                "weight": 60,
                "is_default": True,
                "order": 25,
                "species": {"name": "pikachu", "url": "https://pokeapi.co/api/v2/pokemon-species/25/"},
                "stats": [
                    {"base_stat": 35, "effort": 0, "stat": {"name": "hp", "url": "https://pokeapi.co/api/v2/stat/1/"}},
                    {"base_stat": 55, "effort": 0, "stat": {"name": "attack", "url": "https://pokeapi.co/api/v2/stat/2/"}},
                    {"base_stat": 40, "effort": 0, "stat": {"name": "defense", "url": "https://pokeapi.co/api/v2/stat/3/"}},
                    {"base_stat": 50, "effort": 0, "stat": {"name": "special-attack", "url": "https://pokeapi.co/api/v2/stat/4/"}},
                    {"base_stat": 50, "effort": 0, "stat": {"name": "special-defense", "url": "https://pokeapi.co/api/v2/stat/5/"}},
                    {"base_stat": 90, "effort": 0, "stat": {"name": "speed", "url": "https://pokeapi.co/api/v2/stat/6/"}},
                ],
                "types": [
                    {"slot": 1, "type": {"name": "electric", "url": "https://pokeapi.co/api/v2/type/13/"}},
                ],
                "moves": [
                    {"move": {"name": "thunder-shock", "url": "https://pokeapi.co/api/v2/move/84/"}},
                    {"move": {"name": "tackle", "url": "https://pokeapi.co/api/v2/move/33/"}},
                ],
            },
            status=200,
        )
        yield rsps


@pytest.fixture
def built_transform_db(transform_test_db_path, mock_pokeapi):
    run_pipeline(db_path=transform_test_db_path, pokemon_limit=1)
    result = subprocess.run(
        ["uv", "run", "dbt", "run", "--profiles-dir", ".", "--target", "test"],
        cwd=TRANSFORM_DIR,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, (
        f"dbt run failed with exit code {result.returncode}.\n"
        f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
    )
    return transform_test_db_path


def test_dbt_staging_models_have_data(built_transform_db):
    conn = duckdb.connect(built_transform_db)
    staging_models = ["stg_pokemon", "stg_types", "stg_moves", "stg_abilities", "stg_stats"]
    for model in staging_models:
        count = conn.execute(f"SELECT COUNT(*) FROM staging.{model}").fetchone()[0]
        assert count > 0, f"Expected staging.{model} to have rows after dbt build, but got {count}"
    conn.close()


def test_dbt_mart_models_have_data(built_transform_db):
    conn = duckdb.connect(built_transform_db)
    mart_models = ["fct_pokemon_stats", "dim_type_effectiveness", "fct_competitive_moves"]
    for model in mart_models:
        count = conn.execute(f"SELECT COUNT(*) FROM marts.{model}").fetchone()[0]
        assert count > 0, f"Expected marts.{model} to have rows after dbt build, but got {count}"
    conn.close()


def test_fct_pokemon_stats_bst_and_type_comparison(built_transform_db):
    conn = duckdb.connect(built_transform_db)
    row = conn.execute(
        """
        SELECT pokemon_name, hp, attack, defense, sp_attack, sp_defense, speed,
               base_stat_total, primary_type, speed_vs_type_avg
        FROM marts.fct_pokemon_stats
        WHERE pokemon_name = 'pikachu'
        """
    ).fetchone()
    conn.close()

    assert row is not None, "Expected Pikachu in marts.fct_pokemon_stats but found no row"
    pokemon_name, hp, attack, defense, sp_attack, sp_defense, speed, bst, primary_type, speed_vs_type_avg = row
    assert pokemon_name == "pikachu", f"Expected pokemon_name 'pikachu' but got {pokemon_name!r}"
    assert primary_type == "electric", f"Expected primary_type 'electric' but got {primary_type!r}"
    expected_bst = hp + attack + defense + sp_attack + sp_defense + speed
    assert bst == expected_bst, f"Expected BST {expected_bst} but got {bst}"
    assert speed_vs_type_avg == 0, (
        f"Expected Pikachu speed_vs_type_avg to be 0 as the only electric-type Pokemon, but got {speed_vs_type_avg}"
    )


def test_fct_competitive_moves_stab_power(built_transform_db):
    conn = duckdb.connect(built_transform_db)
    rows = {
        row[0]: row[1:]
        for row in conn.execute(
            """
            SELECT move_name, is_stab, power, stab_adjusted_power
            FROM marts.fct_competitive_moves
            WHERE pokemon_name = 'pikachu'
            ORDER BY move_name
            """
        ).fetchall()
    }
    conn.close()

    assert "thunder-shock" in rows, "Expected Pikachu to learn thunder-shock in fct_competitive_moves"
    assert "tackle" in rows, "Expected Pikachu to learn tackle in fct_competitive_moves"

    thunder_stab, thunder_power, thunder_adjusted = rows["thunder-shock"]
    tackle_stab, tackle_power, tackle_adjusted = rows["tackle"]

    assert thunder_stab is True, f"Expected thunder-shock to have STAB for Pikachu, got is_stab={thunder_stab}"
    assert thunder_adjusted == thunder_power * 1.5, (
        f"Expected STAB-adjusted power {thunder_power * 1.5} for thunder-shock but got {thunder_adjusted}"
    )
    assert tackle_stab is False, f"Expected tackle to not have STAB for Pikachu, got is_stab={tackle_stab}"
    assert tackle_adjusted == tackle_power, (
        f"Expected non-STAB adjusted power {tackle_power} for tackle but got {tackle_adjusted}"
    )


def test_dim_type_effectiveness_matrix_size(built_transform_db):
    conn = duckdb.connect(built_transform_db)
    type_count = conn.execute(
        "SELECT COUNT(*) FROM staging.stg_types WHERE type_name IN ('normal', 'fire', 'electric')"
    ).fetchone()[0]
    matrix_count = conn.execute("SELECT COUNT(*) FROM marts.dim_type_effectiveness").fetchone()[0]
    conn.close()

    expected_count = type_count * type_count
    assert matrix_count == expected_count, (
        f"Expected {expected_count} type effectiveness rows ({type_count}x{type_count}) but got {matrix_count}"
    )


def test_dbt_build_fails_without_raw_data(transform_test_db_path):
    result = subprocess.run(
        ["uv", "run", "dbt", "build", "--profiles-dir", ".", "--target", "test"],
        cwd=TRANSFORM_DIR,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode != 0, (
        "Expected dbt build to fail when raw tables are missing, but it succeeded"
    )
