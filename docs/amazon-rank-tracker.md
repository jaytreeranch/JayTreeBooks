# JayTree Books Amazon Rank Tracker

This tracker uses the Canopy Amazon Search API to check where a target Amazon ASIN appears for selected shopper search phrases.

## Target

- Book: The Hollow Bell: A Millbrook Falls Mystery
- Kindle ASIN: `B0HD52HGGZ`
- Marketplace: US

## Default keywords

- cold case mystery
- small town mystery
- small town cold case mystery
- missing sister mystery
- missing person mystery
- police procedural mystery
- women sleuth mystery
- atmospheric mystery
- supernatural mystery
- family secrets mystery

## API budget

The Canopy Hobby plan includes 100 requests per billing period. The scheduled workflow therefore defaults to one result page per keyword and runs twice monthly: 10 keywords × 1 page × 2 runs = about 20 search requests per month, leaving most of the quota available for deeper manual audits.

For a deeper manual run, use the workflow's `max_pages` input. Example: 5 keywords × 5 pages = up to 25 requests.

## Secret

The workflow expects the repository Actions secret `CANOPY_API_KEY`.

## Outputs

Each successful run writes:

- `reports/amazon-rank/latest.md`
- `reports/amazon-rank/amazon-rank-YYYY-MM-DD.csv`

The same report directory is uploaded as a GitHub Actions artifact.
