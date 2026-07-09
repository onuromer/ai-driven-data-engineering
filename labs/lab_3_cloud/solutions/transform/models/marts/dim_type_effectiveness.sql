with standard_types as (
    select
        type_id,
        type_name,
        dlt_id
    from {{ ref('stg_types') }}
    where type_name in {{ standard_type_names() }}
),

type_pairs as (
    select
        attacking.type_name as attacking_type,
        defending.type_name as defending_type
    from standard_types as attacking
    cross join standard_types as defending
),

damage_relations as (
    select
        attacking.type_name as attacking_type,
        double_damage.name as defending_type,
        cast(2.0 as {{ dbt.type_float() }}) as damage_multiplier
    from standard_types as attacking
    inner join {{ source('raw', 'types__damage_relations__double_damage_to') }} as double_damage
        on attacking.dlt_id = double_damage._dlt_root_id

    union all

    select
        attacking.type_name as attacking_type,
        half_damage.name as defending_type,
        cast(0.5 as {{ dbt.type_float() }}) as damage_multiplier
    from standard_types as attacking
    inner join {{ source('raw', 'types__damage_relations__half_damage_to') }} as half_damage
        on attacking.dlt_id = half_damage._dlt_root_id

    union all

    select
        attacking.type_name as attacking_type,
        no_damage.name as defending_type,
        cast(0.0 as {{ dbt.type_float() }}) as damage_multiplier
    from standard_types as attacking
    inner join {{ source('raw', 'types__damage_relations__no_damage_to') }} as no_damage
        on attacking.dlt_id = no_damage._dlt_root_id
)

select
    type_pairs.attacking_type,
    type_pairs.defending_type,
    coalesce(damage_relations.damage_multiplier, cast(1.0 as {{ dbt.type_float() }})) as damage_multiplier
from type_pairs
left join damage_relations
    on type_pairs.attacking_type = damage_relations.attacking_type
    and type_pairs.defending_type = damage_relations.defending_type
