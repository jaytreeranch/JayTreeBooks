# JayTree Books Amazon Rank Tracker

This tracker uses Canopy's GraphQL Amazon search data to check where a target Amazon ASIN appears for selected shopper search phrases.

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

The Canopy Hobby plan includes 100 requests per billing period. The tracker now uses one GraphQL request per keyword and requests multiple Amazon result pages inside that request. With the default 10-keyword set, one audit uses up to about 10 Canopy API requests rather than one request for every page.

The scheduled workflow runs twice monthly, so the normal baseline is about 20 requests per month, leaving most of the Hobby allowance available for additional targeted checks.

## Secret

The workflow expects the repository Actions secret `CANOPY_API_KEY`.

## Outputs

Each successful run writes:

- `reports/amazon-rank/latest.md`
- `reports/amazon-rank/amazon-rank-YYYY-MM-DD.csv`

The same report directory is uploaded as a GitHub Actions artifact.

## Notes

Canopy search data can differ somewhat from a signed-out manual Amazon search because Amazon results can vary by shopper context, marketplace behavior, and search surface. Use this tracker for consistent trend measurement and periodic manual checks for spot validation.
