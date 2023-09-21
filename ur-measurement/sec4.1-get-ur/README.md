# Section 4.1: Response collection
## Preparation
- Install python3
- Install python packages: `python3 -m pip install -r requirement.txt`
- Download and compile ZDNS (https://github.com/zmap/zdns) to `./zdns`
- Download Maxmind GeoLite2 data to `./data/GeoLite2-City.mmdb` and `./data/GeoLite2-ASN.mmdb`
- Download the top domain list (https://tranco-list.eu/) to `./data/tranco-1m.csv`
- (Optional) Replace our list of stable open resolvers at `./data/stable_ipv4.txt` with yours

## Running the collection
- At `./main.sh`, you can switch to debug mode, which measures fewer domains.
```
test='test' # run as test mode
# test=''   # run as normal mode
```
- Run `./main.sh`

## Result
- Save at `./middle/` and `./result/`