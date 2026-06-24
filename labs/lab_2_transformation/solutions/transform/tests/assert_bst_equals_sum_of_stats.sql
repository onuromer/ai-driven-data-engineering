select
    pokemon_id,
    pokemon_name,
    base_stat_total,
    hp + attack + defense + sp_attack + sp_defense + speed as calculated_bst
from {{ ref('fct_pokemon_stats') }}
where base_stat_total != hp + attack + defense + sp_attack + sp_defense + speed
