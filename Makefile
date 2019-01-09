wards.geojson :
	wget -O $@ "https://data.cityofchicago.org/api/geospatial/sp34-6z76?method=export&format=GeoJSON"

wards.csv : wards.geojson
	cat $< | python scripts/demo.py > $@
