select
    pokemon_name,
    move_name,
    power,
    is_stab,
    stab_adjusted_power
from {{ ref('fct_competitive_moves') }}
where power is not null
  and (
    (is_stab and stab_adjusted_power != power * 1.5)
    or (not is_stab and stab_adjusted_power != power)
  )
