# Raw Data

Place raw LISS-3 scene folders here (not tracked in git):

```
data/raw/scene_049/BAND2.tif ... BAND5.tif, BAND_META.txt
data/raw/scene_050/BAND2.tif ... BAND5.tif, BAND_META.txt
data/raw/Dehradun.zip  (Dehradun boundary shapefile archive)
```

Update `BASE` in `src/01_data_preparation.py` to point here if not
using the original Google Drive paths.
