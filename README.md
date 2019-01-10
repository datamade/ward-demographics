# ward-demographics
Census Demographics of Chicago's Wards

# Methodology

The U.S. Census Bureau provides data at various level of
geographies. For the American Community Survey, the smallest units are
called "block groups." Block groups typically include between 600 and
3,000 people, with an optimum size of 1,500 people.

Data from block groups can be combined to estimate the demographics
for geographical units that the U.S. Census does not directly report,
like Chicago ward boundaries.

Let's take population as an example. For a given ward, we could find
all the block groups that fall within the ward boundaries, and then
add up the population of all those block groups to get an estimate of
the ward.

However, some block groups cross ward boundaries. In these cases, we
calculate the proportion of the area of block group that is in a ward,
and assign that proportion of the population of the block group to the
ward. For example, if half of the area of a block group is in the 5th
ward, we would assign half the population of that block group to the
5th ward.

For the variables on total population, and population broken down by
race and ethnity this is the procedure we follow.

For certain variable, the U.S. Census Bureau does not report data at
the smallest geographies in order to maintain the privacy of
individuals. Information on household income is one of these variables
and the smallest geographical unit that the data is reported at is the
the "tract" level. There are about 3 to 4 block groups in a tract.

To calculate mean household income, we find all the tracts that fall
within a ward. For these tracts, we sum up a variable for total
household income and a variable for total households. Finally, we
divide the total household income by the number of households. We use
a proportional assignment similar to what we do with block
groups. Additionally, household income is still occasionally
suppressed at the tract level for privacy levels. When household
income is missing at the tract level, we also treat the number of
households as missing.

There are three sources of error in the ward level aggregations.

1. The underlying block group or tract level data from the U.S. Census can have error 
2. The proportial assignment of values based upon areal overlap makes an assumption that the block groups and tracts are completely homogenous.
3. Missing income data at the tract level can introduce error

Given these sources of error, I advise not reporting with only a few
significant digits. For example, the 5th ward has a calculated total
population of 45,853. I'd report that as 46,000.


## Technical details


- Census data was pulled fro the U.S. Census's API. Particularly the 2017 vintage of the 5-year American Community Survey https://www.census.gov/data/developers/data-sets/acs-5year.2017.html
- The shapes of the census block groups and tracts come from the U.S. Census TigerWeb https://tigerweb.geo.census.gov/tigerwebmain/TIGERweb_main.html
- the shapes of the wards come from the City of Chicago's Open Data Portal https://data.cityofchicago.org/Facilities-Geographic-Boundaries/Boundaries-Wards-2015-/sp34-6z76

