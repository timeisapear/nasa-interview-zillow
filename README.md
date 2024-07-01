## Run instructions
1. Clone repo:
```sh
git clone https://github.com/timeisapear/nasa-interview-zillow
```

2. Enter folder:
```sh
cd nasa-interview-zillow
```

3. Execute docker-compose (Ideally using Rancher)
```sh
docker-compose -f docker/docker-compose.yml up
```

4. Navigate to dashboard on browser
```sh
open http://[local-machine-ip]:7860/visualize
```


## Trade-offs and Limitations
Most architecture trade-offs are discussed in executive summary, but below are very specific one-off thoughts as development progressed

### Incremental vs Full-refresh
Normally incremental refresh (additive) would be desired for data refreshes, both for efficiency and runtime reasons. However, given that these datasets reside mostly in memory, full refreshes should be adequate in this analysis.

### Zillow CSVs vs API
Normally Zillow's API would be the preferred download mechanism of the data, especially since Zillow itself directs developers to use that as opposed to the CSVs. However, the requesting the API token mechanism communicated it might take 10+ days to proces, outside the due date of the deliverable.

Plus, given the /region endpoints that equate to counties, there are ~3000 USA counties so it is more efficient to get the aggregate CSV data than query by county individually.


### CDC Data pre-downloaded
The CDC SVI index data for 2022 is downloaded and pre-committed to the repo. Ideally this would be fetched dynamically, but the file is hidden behind a "Download" button and its GET path was not easily ascertained even after time spent in the Chrome developer window. Given more time, a brute-force approach of Selenium automation to click the button and download it would be one solution.
