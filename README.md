# What

Inspect Zillow data for correlations in conjunction with CDC data to determine whether Social Vulnerability Index informs negative outcomes across Zillow datasets

Some thoughts on questions:

Does SVR correlate with more vulnerable type of housing that does worse in natural disasters? (Would need tornado/hurricane data etc.)
Are new construction sales concentrated more in 

# Why

To provide a project to display skills in software development, data engineering and communication. Any derived insights would be also be interesting in and of themselves.

# How

Use requests to get data from
- Zillow
- CDC
- crosswalk? use geosync API?

Save to CSV?/sqlite if time

Use pandas to join the data, bucket Zillow geocodes with SVI data

Visualize it
- Seaborn/Plotly?


# Trade-offs
## Incremental vs Full-refresh
Normally incremental refresh (additive) would be desired for data refreshes, both for efficiency and runtime reasons. However, given that these datasets reside mostly in memory, full refreshes should be adequate in this analysis.

## Zillow CSVs vs API
Normally would use API, especially as that is the direction of the Zillow data page. However, given constraints, let's start with the CSV. 
Plus, with the /region endpoints that equate to counties, there are ~3000 counties so more efficient to get the aggregate data than query by county.
