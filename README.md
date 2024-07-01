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

## Publicly accessible self-hosted link
[https://nasa.tisap.net/visualize](https://nasa.tisap.net/visualize)

Since I already had a personal website hosted on my LAN-linux box, I just added a 
config to my nginx and a CNAME record on Cloudflare for my personal tisap.net domain.

Briefly, the CNAME record (nasa.tisap.net) is proxied through Cloudflare for some protection, then hits my home router which VPS forwards the 443 port to my local Linux NUC. Then nginx locally handles the proxying between my other site (climaski.com) and this current dashboard which docker-compose is running on port 7860.

It can be available indefinitely at minimal additional cost to me.


## Trade-offs and Limitations
Most architecture trade-offs are discussed in the executive summary but very specific one-off thoughts were recorded below as development progressed

### Incremental vs Full-refresh
Normally incremental data refreshes (additive) would be desired both for efficiency and runtime reasons. However, given that these datasets reside mostly in memory, full refreshes should be adequate here.

### Zillow CSVs vs API
Normally Zillow's API would be the preferred download mechanism of the data, especially since Zillow itself directs developers to use that as opposed to the CSVs. However, when requesting a new API token, the service communicated it might take 10+ days to process which was outside the due date of the deliverable.

Plus, given that the /region endpoints equates to counties, there are ~3000 USA counties so it is more efficient to get the aggregate CSV data than query by county individually.

### CDC Data Pre-downloaded
The CDC SVI index data for 2022 is downloaded and pre-committed to the repo at `nasa_interview_project/data/SVI_2022_US_county.csv`. Ideally this file would be fetched on-demand, but the file is hidden behind a "Download" button and its GET path was not easily ascertained--even after time spent in the Chrome developer Network tab. Given more time, a brute-force approach of Selenium automation to click the button and download it would be one solution.
