# Analysis of MSCOCO images with nodes from VisualSem
# Using 2048D representations and l2

## Top-N Frequency Plots

### Top-1
![top1](images_analysis/2048D_l2_top1.png)

### Top-5
![top-5](images_analysis/2048D_l2_top5.png)

### Top-10
![top10](images_analysis/2048D_l2_top10.png)

### Top-50
![top50](images_analysis/2048D_l2_top50.png)

### Summary
As we can see from the above frequency plots, the more nodes we gather per image, the more the line becomes more horizontal instead of decreasing exponentially which is much more clearer here compared to cosine similarity. Seems to have correct concepts.

## Examples
To show whether the representations are useful and correct things can be recognized in an image, the MSCOCO images are shown with the recognized nodes in order.

### Example 1
![coco1](images_analysis/coco1.jpg)

COCO_train2014_000000046114.jpg

['calculator', 'home_computer', 'Commodore_International', 'netbook', 'Nokia', 'smartphone', 'e-reader', 'Computer_case', 'Sixth_generation_of_video_game_consoles', 'PDA', 'laptop', 'electric_meter', 'computer_keyboard', 'C64', 'Chromebook', 'typewriter', 'ink-jet_printer', 'microcomputer', 'Platform_display', 'tape_recorder', 'computer', 'VCR', 'desktop_computer', 'Handheld_game_console', 'computer_science', 'radio', 'Acer_Inc.', 'History_of_personal_computers', 'electric_organ', 'household_appliance', 'toaster', 'Music_sequencer', 'slide_projector', 'synthesizer', 'vending_machine', 'Fourth_generation_of_video_game_consoles', 'CD_drive', 'Amiga', 'Palm_(PDA)', 'Arduino', 'memory', 'air_conditioning', 'Nintendo', 'kitchen_stove', 'video_card', 'ATX_Power_Supply', 'oscilloscope', 'ghetto_blaster', 'central_processing_unit', 'Samsung']

### Example 2
![coco2](images_analysis/coco2.jpg)

COCO_train2014_000000211852.jpg

['Boston_Terrier', 'Shih-Tzu', 'Horse_markings', 'Cat_coat_genetics', 'spitz', 'canna', 'Equine_coat_color', 'calico_cat', 'chow_chow', 'Spaniel', 'Norwegian_Forest_cat', 'Alaskan_Klee_Kai', 'Siberian_tiger', 'Bicolor_cat', 'Hybrid_tea_rose', 'dahlia', 'buckskin', 'gelding', 'Rosa_odorata', 'Japanese_spaniel', 'epiphyllum', 'Flaxen_gene', 'sorrel', 'bulldog', 'guinea_pig', 'tack', 'petunia', 'Bactrian_camel', 'Laika_(dog_breed)', 'Manx_cat', 'Welsh_pony', 'begonia', 'Saint_Bernard', 'pansy', 'Spheniscus', 'Judgement_of_Paris', 'Erotic_art', 'The_Last_Judgment_(Michelangelo)', 'French_braid', 'Bernese_Mountain_Dog', 'Amaryllis_belladonna', 'yawn', 'hippeastrum', 'Arabian_horse', 'standard_poodle', 'puppy', 'Devon_Rex', 'monstera', 'peony', 'Brugmansia']

### Example 3
![coco3](images_analysis/coco3.jpg)

COCO_train2014_000000445140.jpg

['mutton', 'stuffing', 'European_cuisine', 'halva', 'gigot', 'ragout', 'spaghetti_and_meatballs', 'shrimp_sauce', 'schnitzel', 'mackerel', 'ramen', 'eel', 'shellfish', 'chop', 'pilaf', 'comfort_food', 'offal', 'burrito', 'pizza', 'steak', 'spaghetti', 'donburi', 'sub', 'hamburger', 'anglesite', 'shrimp', 'Vegetarian_cuisine', 'Bulgarian_cuisine', 'rhodonite', 'food_fish', 'lángos', 'Danish_cuisine', 'Soto_(food)', 'Panzanella', 'National_dish', 'fluorite', 'quiche', 'Moroccan_cuisine', 'laksa', 'Cheese_sandwich', 'meatball', 'Korean_cuisine', 'Castilian-Leonese_cuisine', 'steak_au_poivre', 'Palatschinke', 'Global_cuisine', 'Spanish_cuisine', 'salad', 'chalcedony', 'Rice_vermicelli']

### Example 4
![coco4](images_analysis/coco4.jpg)

COCO_train2014_000000574696.jpg

['zebra', 'quagga', 'Equus_grevyi', 'mountain_zebra', "Grant's_zebra", 'Equidae', "Burchell's_zebra", "Chapman's_zebra", 'Horse_gait', 'hinny', 'horse_breeding', "Burchell's_zebra", 'Equine_coat_color', 'Siberian_tiger', 'Equus', 'odd-toed_ungulate', 'shire_horse', 'Horse_markings', 'Ardennes_horse', 'Welsh_pony', 'purebred', 'Bengal_tiger', 'tack', 'American_saddle_horse', 'Appaloosa', 'Arabian_horse', 'rhinoceros', 'Friesian_horse', 'dun', "Hartmann's_mountain_zebra", 'White_tiger', 'okapi', 'Selle_Français', 'zebroid', 'Rollkur', 'horseback', 'buckskin', 'stallion', 'tiger', 'saddle_horse', 'Indian_rhinoceros', 'leucism', 'noseband', 'Trakehner', 'white_rhinoceros', 'stegosaurus', 'griffin', 'blue_wildebeest', 'Sumatran_tiger', 'Bactrian_camel']

### Summary
This clearly shows that things are recognized correctly for each of these images. This indicates that l2 does capture some details???????

## Cosine Similarities
To see how the cosine similarities relate to each other in the top-Ns, we show some mean, median, variance and both min and max statistics. F stands for gathering all the similarities for that top and applying the statistics, whereas P calculates these statistics per image top and then averaging this.

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Mean F</th>
      <th>Median F</th>
      <th>Variance F</th>
      <th>Mean P</th>
      <th>Median P</th>
      <th>Variance P</th>
      <th>Min F</th>
      <th>Max F</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>Top-1</th>
      <td>1.626358</td>
      <td>1.621211</td>
      <td>0.004775</td>
      <td>1.626358</td>
      <td>1.626358</td>
      <td>0.000000</td>
      <td>1.398103</td>
      <td>2.008661</td>
    </tr>
    <tr>
      <th>Top-5</th>
      <td>1.633222</td>
      <td>1.627742</td>
      <td>0.004950</td>
      <td>1.633222</td>
      <td>1.634248</td>
      <td>0.000026</td>
      <td>1.398103</td>
      <td>2.036203</td>
    </tr>
    <tr>
      <th>Top-10</th>
      <td>1.637157</td>
      <td>1.631503</td>
      <td>0.005052</td>
      <td>1.637157</td>
      <td>1.638478</td>
      <td>0.000034</td>
      <td>1.398103</td>
      <td>2.056323</td>
    </tr>
    <tr>
      <th>Top-50</th>
      <td>1.648302</td>
      <td>1.642217</td>
      <td>0.005338</td>
      <td>1.648302</td>
      <td>1.650180</td>
      <td>0.000055</td>
      <td>1.398103</td>
      <td>2.079260</td>
    </tr>
  </tbody>
</table>
### Summary
What we can see, is that for all the tops, both the mean and medians don't differ significantly, however, the variance does not grow as much, whereas the minimal value stays the same and the maximum grows.
