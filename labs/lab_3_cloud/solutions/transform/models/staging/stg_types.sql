select
    cast(types.id as integer) as type_id,
    cast(types.name as {{ dbt.type_string() }}) as type_name,
    cast(types.generation__name as {{ dbt.type_string() }}) as generation_name,
    cast(types.move_damage_class__name as {{ dbt.type_string() }}) as move_damage_class_name,
    cast(types._dlt_id as {{ dbt.type_string() }}) as dlt_id,
    loads.inserted_at as _loaded_at
from {{ source('raw', 'types') }} as types
left join {{ source('raw', '_dlt_loads') }} as loads
    on types._dlt_load_id = loads.load_id
