select First.Year, Second.Year, Country.Name, ((1.0 * (Second.Rate - First.Rate)) / (Second.Year - First.Year)) from Country
inner join LiteracyRate First on (Country.Code = First.CountryCode)
inner join LiteracyRate Second on (Country.Code = Second.CountryCode)
where (First.Year < Second.Year)
group by Country.Name, First.Year, Second.Year having (Second.Year - First.Year = min(Second.Year - First.Year))
order by ((1.0 * (Second.Rate - First.Rate)) / (Second.Year - First.Year)) desc;
