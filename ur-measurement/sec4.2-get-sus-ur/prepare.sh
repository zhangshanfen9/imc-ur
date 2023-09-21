#! /bin/sh

test='test' # run as test mode
# test=''   # run as normal mode
chmod +x ./zdns
chmod +x ./*.sh
cd output/middle/
pwd

for zip_file in *.zip; do
  if [ -f "$zip_file" ]; then
    unzip -o "$zip_file"
  fi
done

cd ../result/
pwd

for zip_file in *.zip; do
  if [ -f "$zip_file" ]; then
    unzip -o "$zip_file"
  fi
done

cd ../../
pwd
rm -rf ./output/middle/*.zip && rm -rf ./output/result/*.zip

python3 ./detect_protecting_records/get_list.py $test
chmod +x ./detect_protecting_records/detect.sh && ./detect_protecting_records/detect.sh