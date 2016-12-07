select GovernmentForm, sum(SurfaceArea) from Country
group by GovernmentForm
order by sum(SurfaceArea) desc
limit 1;
