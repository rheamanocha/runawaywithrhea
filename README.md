# run away with rhea

Static site served by GitHub Pages at runawaywithrhea.com.

## Hero images and tiles

Each page's hero photo is also the thumbnail on its Guides card and map card. After adding or changing a hero image, run `python3 tools/sync-tiles.py` to refresh the tiles, then commit. Pages without a hero photo keep the gradient placeholder.

## Analytics

Google Analytics 4 loads from `analytics.js` (the Measurement ID lives in that one file). Every page includes `<script src="/analytics.js" defer></script>` in its head. For a page not built from the templates, run `python3 tools/add-analytics.py` to add the tag, then commit. It only reports from runawaywithrhea.com and skips visitors with Do Not Track on.
