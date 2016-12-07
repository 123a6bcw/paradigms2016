select Country.Name, count(City.Name) from Country
left outer join City on (Country.Code = City.CountryCode and City.Population >= 1000000)
group by Country.Code
order by count(City.Name) desc, Country.Name;
