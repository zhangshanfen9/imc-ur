# Section 4.2: Determining suspicious record
## Preparation
- Move the results from section 4.1: 
  - `sec4.1-get-ur/middle -> sec4.2-get-sus-ur/output/middle`
  - `sec4.1-get-ur/result -> sec4.2-get-sus-ur/output/result`
- Download and compile ZDNS (https://github.com/zmap/zdns) to `./zdns`
- At `./detect_protecting_records/detect.sh`, configure your testing domains
  - Configure testing records for your domain, for example:
  - `your_domain.com A 66.66.66.66`
  - `your_domain.com TXT TEST_TXT`
  - Revise the `detect.sh` according to your configuration


## Running the determination
- At `./prepare.sh`, you can switch to debug mode, if you use debug mode in Sec4.1.
```
test='test' # run as test mode
# test=''   # run as normal mode
```
- Prepare data and detect protecting records: `./prepare.sh`
- Run `a_record_analyze.ipynb` for outputting suspicious A URs
- Run `txt_record_analyze.ipynb` for outputting suspicious TXT URs

## Result
- `output/analyze/`