select
    cast(moves.id as integer) as move_id,
    cast(moves.name as {{ dbt.type_string() }}) as move_name,
    cast(moves.power as integer) as power,
    cast(moves.accuracy as integer) as accuracy,
    cast(moves.pp as integer) as pp,
    cast(moves.priority as integer) as priority,
    cast(moves.type__name as {{ dbt.type_string() }}) as move_type,
    cast(moves.damage_class__name as {{ dbt.type_string() }}) as damage_class,
    cast(moves.generation__name as {{ dbt.type_string() }}) as generation_name,
    loads.inserted_at as _loaded_at
from {{ source('raw', 'moves') }} as moves
left join {{ source('raw', '_dlt_loads') }} as loads
    on moves._dlt_load_id = loads.load_id
