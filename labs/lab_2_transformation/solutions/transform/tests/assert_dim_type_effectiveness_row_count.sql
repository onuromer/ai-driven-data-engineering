select count(*) as invalid_row_count
from {{ ref('dim_type_effectiveness') }}
having count(*) != 324
