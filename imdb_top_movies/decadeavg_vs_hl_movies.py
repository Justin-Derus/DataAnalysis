# Author Name: Scoey Derus
# Purpose: Using Kaggle's 250 top IMDB movies, I have generated 3 (Really 1) bar graph depciting the average rating of the top 250
# movies by per decade, along with the decades single highest, and lowest rated best movie out of the top 250 movies

import pandas as pd                         # Using dataframe
import matplotlib.pyplot as plt             # Used for visual graphs
from matplotlib.colors import Normalize     # Used for creating color map
from matplotlib.cm import ScalarMappable    # Used for creating color bar
from matplotlib.patches import Patch        # Used to remove certain elements from the legend that added nothing of importance

imdb_table = pd.read_csv('./imdb_top_movies/imdb_top_movies.csv',index_col=0)   # Read in the csv file for data

plt.figure(figsize=(11,7))  # Set size of window

cleaned_table = imdb_table.loc[:,['Year', 'Rating']]    # Clean data for whats needed

cleaned_table['Decade'] = cleaned_table['Year'].map(lambda x: (x // 10) * 10) # Create decade column

max_rating_in_decade = cleaned_table.groupby('Decade')['Rating'].max()  # Get a series of the highest rated movie in each decade
min_rating_in_decade = cleaned_table.groupby('Decade')['Rating'].min()  # Get a series of the lowest best rated movie in each decade
count_of_movies = cleaned_table.groupby('Decade')['Rating'].count()     # Get a series of the counts of movies per decade  

cleaned_table = cleaned_table.groupby('Decade',as_index=False)['Rating'].mean().round(2)    # Get rid of year, replace w/ decade and mean rating
cleaned_table['HRM'] = cleaned_table['Decade'].map(max_rating_in_decade)                    # Create highest rated movie column
cleaned_table['LRM'] = cleaned_table['Decade'].map(min_rating_in_decade)                    # Create lowest rated movie column
cleaned_table['MovieCount'] = cleaned_table['Decade'].map(count_of_movies)                  # Create count column

min_rating = min(cleaned_table['LRM'])      # Used for zooming
max_rating = max(cleaned_table['HRM'])      # Used for zooming

# Coloring Using normalized versions of ratings
cmap = plt.get_cmap('magma')    # Choose color map

my_norm = Normalize(vmin=cleaned_table['MovieCount'].min(),
                              vmax=cleaned_table['MovieCount'].max()) # Normalize 0-1, lowest is 0.000, max is 1.000 all fall between

colors=cmap(my_norm(cleaned_table['MovieCount'])) # Normalize movie count and make a cmap of the normalization, cmap used for bar colors

# Make a color bar - need a scalarmapable under matplotlibs color
sm = ScalarMappable(cmap=cmap,norm=my_norm)         # Create ScalarMappable object based on cmap and norms created above
cbar = plt.colorbar(sm, orientation='horizontal',alpha=0.8)   # Pass in ScalarMappable object to pyplots colorbar, put it below graph for readability
cbar.set_label('Amount of Movies in Decade')        # Give label to color bar to know what it means

# NOTE: NOT stacking bars, putting them in front of each other because the average is in the middle and the highest and lowest will 
# ALWAYS be behind and infront of the average respectively
highest_movie_bar = plt.bar(cleaned_table['Decade'],                # Decade (X-Coord)
                            cleaned_table['HRM'],                   # Highest Rated Movie (Y-Coord)
                            color=colors,                           # Colors set to normalized cmap
                            width=8,                                # 10 decades, 8 width is visually appealing
                            zorder=0,                               # In back
                            alpha = 0.3,                            # lowest alpha in back for visual
                            edgecolor='black',                      # Black edge around the bars
                            label='Highest Rated Movie in Decade')  # Label for legend

avg_decade_bar = plt.bar(cleaned_table['Decade'],
                         cleaned_table['Rating'],
                         color=colors,
                         width=8,
                         zorder=1,                          # In middle
                         alpha=0.3,                         # Medium alpha in middle for visual
                         edgecolor='black',
                         label='Average Rating of Decade')

lowest_movie_bar = plt.bar(cleaned_table['Decade'],
                           cleaned_table['LRM'],
                           color=colors,
                           width=8,
                           zorder=2,                             # In front
                           alpha=0.5,                            # Highest alpha in front to show colorbar
                           edgecolor='black',
                           label='Lowest Rated Movie in Decade')

# Add text to display value/height of bars
for bar in avg_decade_bar:
    height = bar.get_height()               
    plt.text(
        bar.get_x() + bar.get_width() / 2,  # 1) Get x gives leftmost edge, adding bar width / 2 puts it towards middle
        height,                             # 2) Y coordinate for text
        height,                             # 3) Actual text being displayed
        ha='center'                         # Horizontal alignment to match middle of bar
    )

for bar in highest_movie_bar:
    height = bar.get_height()
    plt.text(
        bar.get_x() + bar.get_width() / 2,
        height,
        height,
        ha='center'
    )

for bar in lowest_movie_bar:
    height = bar.get_height()
    plt.text(
        bar.get_x() + bar.get_width() / 2,
        height,
        height,
        ha='center'
    )

plt.ylim(min_rating - .25, max_rating + .05)    # Zooming done here, want lowest of low bars, highest of high bars

plt.ylabel('Rating')    # Label Axes
plt.xlabel('Decade')

# Uses matplotlibs.patches to remove color bar from legend, text is visually simple and understandable
legend_elements = [
    Patch(facecolor='none', edgecolor='none', label='Highest Rated Movie in Decade'), # Remove edge of color box and the color itself, keep label
    Patch(facecolor='none', edgecolor='none', label='Average Rating of Decade'),
    Patch(facecolor='none', edgecolor='none', label='Lowest Rated Movie in Decade')
]

plt.legend(handles=legend_elements, # Tell legend to not show colorbox at all
           loc='upper left',        # Moves to upper left of graph
           handlelength=0,          # Without these 4 **Kwarggs set, color box is gone but padding is still visible, remove it
           handleheight=0,
           handletextpad=0,
           borderaxespad=0,
           edgecolor='black',
           )

plt.title("Comparing Highest & Lowest Rated Movie \nof a Decade to Decade Averages")

plt.show()