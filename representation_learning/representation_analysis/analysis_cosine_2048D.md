# Analysis of MSCOCO images with nodes from VisualSem
# Using 2048D representations and cosine similarity

## Top-N Frequency Plots

### Top-1
![top1](images_analysis/top1.png)

### Top-5
![top-5](images_analysis/top5.png)

### Top-10
![top10](images_analysis/top10.png)

### Top-50
![top50](images_analysis/top50.png)

### Summary
As we can see from the above frequency plots, the more nodes we gather per image, the more the line becomes more horizontal instead of decreasing exponentially. Moreover, using the top-1 shows much more what can be expected in the MSCOCO images (bicycles, skating etc.) compared to the top-50 that becomes slightly more random due to more abstract recognized nodes.  

## Examples
To show whether the representations are useful and correct things can be recognized in an image, the MSCOCO images are shown with the recognized nodes in order.

### Example 1
![coco1](images_analysis/coco1.jpg)

COCO_train2014_000000046114.jpg

['Nokia', 'laptop', 'microcomputer', 'Sixth_generation_of_video_game_consoles', 'home_computer', 'video_game_console', 'Handheld_game_console', 'smartphone', 'Fifth_generation_of_video_game_consoles', 'Nintendo', 'netbook', 'Computer_case', 'Apple_Inc.', 'digital_camera', 'Still_camera', 'computer', 'Seventh_generation_of_video_game_consoles', 'fixed_disk', 'Kabushiki-gaisha_Nikon', 'phone', 'calculator', 'computer_monitor', 'slide_projector', 'Global_Positioning_System', 'Fourth_generation_of_video_game_consoles', 'television_set', 'kitchen_stove', 'History_of_personal_computers', 'Single-lens_reflex_camera', 'hard_drive', 'PlayStation_2', 'typewriter', 'mobile_phone', 'electric_meter', 'Nikon_F-mount', 'Nokia_Nseries', 'PlayStation_3', 'Nintendo_64', 'Xbox_360', 'tape_recorder', 'PDA', 'Nikon_Coolpix_series', 'LCD', 'VCR', 'Dell', 'Acer_Inc.', 'Power_supply', 'microwave_oven', 'ink-jet_printer', 'desktop_computer']

### Example 2
![coco2](images_analysis/coco2.jpg)

COCO_train2014_000000211852.jpg

['still_life', 'Nepenthes', 'coconut', 'animal_art', 'dragon', 'kebab', 'food_fish', 'mineral', 'crab', 'meat', 'bread', 'aloe', 'tulip', 'cabbage', 'Euphorbiaceae', 'cone', 'fungus', 'Gesneriaceae', 'cycad', 'begonia', 'Ernst_Ludwig_Kirchner', 'blazon', 'Descent_from_the_Cross', 'psittacosaurus', 'Edible_mushroom', 'Lamiaceae', 'Rubiaceae', 'Greek_mythology', 'spinach', 'Bromeliaceae', 'The_Last_Judgment_(Michelangelo)', 'poinsettia', 'salad', 'iris', 'carnivorous_plant', 'Proteaceae', 'Easter', 'spice', 'Allium', 'anemone_fish', 'cactus', 'seafood', 'fruiting_body', 'legume', 'Ericaceae', 'vegetarianism', 'vegetable', 'cayenne_pepper', 'goldfish', 'barbecue']

### Example 3
![coco3](images_analysis/coco3.jpg)

COCO_train2014_000000445140.jpg

['National_dish', 'pizza', 'ramen', 'salad', 'Vietnamese_cuisine', 'Thai_cuisine', 'torte', 'European_cuisine', 'kebab', 'Saint_George', 'pie', 'gingerbread', 'fried_rice', 'bezant', 'blazon', 'Assumption', 'ragout', 'Spanish_cuisine', 'Dormition', 'Vegetarian_cuisine', 'pasta', 'begonia', 'American_food', 'mutton', 'food', 'Korean_cuisine', 'Italian_cuisine', 'pilaf', 'Cantonese_cuisine', 'meat', 'Nativity_of_Jesus_in_art', 'Danish_cuisine', 'Saxifraga', 'stuffed_cabbage', 'Chinese_cuisine', 'shellfish', 'International_Gothic', 'Global_cuisine', 'skewer', 'steak', 'Arab_cuisine', 'Ernst_Ludwig_Kirchner', 'rhododendron', 'burrito', 'offal', 'succulent', 'Wassily_Kandinsky', 'bouquet', 'sandwich', 'bread']

### Example 4
![coco4](images_analysis/coco4.jpg)

COCO_train2014_000000574696.jpg

['zebra', 'Equus_grevyi', 'quagga', 'mountain_zebra', 'Equidae', 'horsemanship', "Burchell's_zebra", 'horseback', 'Horse_markings', 'horseback_riding', 'Horse_gait', 'dressage', 'polo_mallet', 'horse', 'falconry', 'saddle_horse', 'Equus', 'American_football', 'Gypsy_Cob', 'Arabian_horse', 'purebred', 'Blackfoot', 'Bactrian_camel', 'blue_wildebeest', 'okapi', 'horseman', 'official', 'reenactment', 'Equine_coat_color', 'National_personification', 'hackamore', 'Tuareg', 'donkey', 'Lipizzan', 'Aristide_Maillol', 'pony', 'hussar', 'Cossack', 'Folk_hero', 'odd-toed_ungulate', 'cavalry', 'Folk_costume', 'equestrian_sport', 'horse_breeding', 'pieta', 'trooper', 'Appaloosa', 'cowboy', 'bridle', 'cattle']

### Summary
Some things are recognized well, but there are still some mistakes. Here, we can also see that in the first few comparisons, we can see that those are mostly the most accurate.

## Cosine Similarities
To see how the cosine similarities relate to each other in the top-Ns, we show some mean, median, variance and both min and max statistics. F stands for gathering all the similarities for that top and applying the statistics, whereas P calculates these statistics per image top and then averaging this.

|        |  Mean F |  Median F |  Variance F x 10^-8 |  Mean P |  Median P |  Variance P x 10^-10 |  Min F |  Max F |
|--------|---------|-----------|---------------------|---------|-----------|----------------------|--------|--------|
| Top-1  | 0.997   | 0.997     | 5.026               | 0.997   | 0.997     | 0                    | 0.996  | 0.998  |
| Top-5  | 0.997   | 0.997     | 5.239               | 0.997   | 0.997     | 2.780                | 0.996  | 0.998  |
| Top-10 | 0.997   | 0.997     | 5.370               | 0.997   | 0.997     | 3.773                | 0.996  | 0.998  |
| Top-50 | 0.997   | 0.997     | 5.764               | 0.997   | 0.997     | 6.165                | 0.995  | 0.998  |

### Summary
What we can see, is that for all the tops, both the mean and medians don't differ significantly, however, we can see a growing variance as soon as more nodes are introduced as well as lower possible values.
