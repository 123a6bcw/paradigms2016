select Country.Name from Country
left outer join City on (Country.Code = City.CountryCode)
group by Country.Code having (Country.Population > 2 * sum(City.Population));
