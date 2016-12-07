select Country.Name, Country.Population, Country.SurfaceArea from Country
inner join Capital on Country.Code = Capital.CountryCode
inner join City on Country.Code = City.CountryCode
group by Country.Code having (City.Population = max(City.Population) and City.Id <> Capital.CityId)
order by (Country.Population / Country.SurfaceArea) desc, Country.Name;
