select
    attacking_type,
    defending_type,
    count(*) as duplicate_count
from {{ ref('dim_type_effectiveness') }}
group by attacking_type, defending_type
having count(*) > 1
