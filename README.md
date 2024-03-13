# rgani_scraper
Webscraper for the online catalogue of the Russian State Archive of Contemporary History (RGANI)

Writes the archival data into CSV and JSON files

run with:

```python3 parse_rgani.py```

Due to problems with the TLS certificate of the catalogues website the certificate verification has been deactivated. 
This produces warnings when running the script.
