-- script which lists all bands with glam rock
select band_name, 
  case 
  When split is NULL then 2022 - formed
  Else split - formed
  end as lifespan
  from metal_bands
  where style like '%Glam rock%'
  order by lifespan desc
