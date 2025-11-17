# Author Name: Scoey Derus
# Purpose: Using Kaggle's 250 top IMDB movies, generate a graph using matplotlibs bar graph and pandas dataframe
# to find the datasets highest average rating decade  
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib.colors import LinearSegmentedColormap
import pandas as pd
import numpy as np

plt.figure(figsize=(10,8))

#pd.set_option('display.max_rows',None)         # commented out, pandas does not display full table by default must set option
#pd.set_option('display.max_columns',None)

imdb_table = pd.read_csv('./imdb_top_movies/imdb_top_movies.csv', index_col = 0)             # DataFrame created from .csv file
decade = imdb_table.loc[:,['Year','Rating']]                   # Drop columns we don't need (DataFrame type)
                                                                             # DataFrame supports slicing via loc and iloc
decade['Decade'] = (decade['Year'] // 10) * 10   # Create a decade column | (1992 // 10 = 199.2 rounded down) * 10 = 1990
# Another method to create a column
#decade['test'] = decade['Year'].map(lambda x: (x // 10) * 10)
avg_rating_per_decade = decade.groupby('Decade', as_index=False)['Rating'].mean().round(2)  # Find the mean rating per decade, round to two decimals

# Goal of chunk - weigh the decades by the number of movies they have for a trend line
counts = decade.groupby('Decade',as_index=False)['Rating'].count()                       # Find the count of movies  
avg_rating_per_decade['Weight'] = np.sqrt(counts['Rating'])                              # Scale down (EX: 46 movies vs 6 would show downward trend towards higher #)
avg_rating_per_decade['ColorMap'] = (
    (avg_rating_per_decade['Weight'] - avg_rating_per_decade['Weight'].min()) /          # Normalize our weight for a color map 
    (avg_rating_per_decade['Weight'].max() - avg_rating_per_decade['Weight'].min())      # 1) Min row = 0.00 #2) max row = 1.00, divide #1 by #2
)   

# Creation of ColorMap - used for bargraph and for colorbar
custom_colors = ["#4169e0","#509db5","#73b550","#b39934","#ba7e30","#d44235"]
custom_cmap = LinearSegmentedColormap.from_list("custom_hot_cool",custom_colors)
my_norm = cm.colors.Normalize(vmin=counts['Rating'].min(),vmax=counts['Rating'].max())

# Create a colorbar THIS DOES NOT HAVE TO DO WITH COLORS OF BARS
sm = cm.ScalarMappable(cmap=custom_cmap,norm=my_norm)  # Use above variables for custom colors
cbar = plt.colorbar(sm,orientation='horizontal',alpha=0.6)       # Create the colorbar using our custom ScalarMappable object
cbar.set_label("Number of Movies in Decade")           # Give colorbar a label

colors = custom_cmap(avg_rating_per_decade['ColorMap'])# Give bargraph colors based on normalized weight
bars = plt.bar(avg_rating_per_decade['Decade'],        # Plot bar graph, (decades,ratings) as (x,y)
               avg_rating_per_decade['Rating'],     
               width=8,                                # Width of bars set to 8 for visuals
               color=colors,                           # Set the colors of bars to custom colormap
               edgecolor='black',                      # Black border around bars
               alpha=0.6)

# Visual zooming
min_rating = min(avg_rating_per_decade['Rating'])
max_rating = max(avg_rating_per_decade['Rating'])
plt.ylim(min_rating - .15, max_rating + .05)

# Titles and axes labels
plt.title("Highest Rated Decade (Top 250 IMBD Movies)\n(Weighed by Number of Movies)")
plt.xlabel("Decade")
plt.ylabel("Average Rating (Bar Chart)")

# Creating a weighted trend line based off number of movies

# Coefficient is the numerical value that describes the relationship between variables -1 to 1
# Y = mx + b, m is the coefficient (slope), b is the y-intercept/constant (tells you Y when X is 0)
coeff_weighted = np.polyfit(avg_rating_per_decade['Decade'],   # X-Coord
                          avg_rating_per_decade['Rating'],     # Y-Coord
                          2,                                   # 1 = Linear (answers overall), 2 = Quadratic (overall but slight curvature) # Deg of polynomial
                          w=avg_rating_per_decade['Weight'])   # Add weight to the polynomial, pulls the trendline towards higher weights (1990s - 2010s)

coeff_unweighted = np.polyfit(avg_rating_per_decade['Decade'], # X-Coord
                              avg_rating_per_decade['Rating'], # Y-Coord
                              2)                               # 1 = Linear (answers overall), 2 = Quadratic (overall but slight curvature) # Deg of polynomial

weighted_trend_line = np.poly1d(coeff_weighted)     # Represents equation,TYPE = numpy.poly1d, weighted = 0.0004431 x + 7.43
                                                    # wtl(avg_rating_per_decade['Decade']) 0.0004431 (decade) + 7.43 = x
                                                    # 0.0004431(2000) + 7.43 = 8.3162

unweighted_trend_line = np.poly1d(coeff_unweighted) # 0.001145 x + 6.04
                                                    # 0.001145(2000) + 6.04 = 8.33

# NOTE: Because the unweighted trend line is SLIGHTLY greater than the weighted, it will have more of a slope which we see on the graph
# the weighted trend line is pulled more towards the higher number of movies 

# Plot the trend lines, red is weighted, green is unweighted
plt.plot(avg_rating_per_decade['Decade'], 
         unweighted_trend_line(avg_rating_per_decade['Decade']), # Pass in all the decades to the trend line 
         label='Unweighted', 
         color='red',
         linestyle='--',
         alpha=0.75)

plt.plot(avg_rating_per_decade['Decade'],
          weighted_trend_line(avg_rating_per_decade['Decade']),  # Pass in all the decades to the trend line
          label='Weighted', 
          color = 'blue',
          linestyle='--',
          alpha=0.75)

for bar in bars:                                 # in order to get text, we need to go through all bar objects (matplotlib.patches.Rectangle)
    plt.text(bar.get_x() + bar.get_width() / 2,  # X-coord of left edge of bar, get_width / 2 gives half width which is distance from left edge to center of bar
             bar.get_height(),            # Y-coord (Verticality)
             bar.get_height(),                   # What is displayed
             ha='center',
             fontweight='bold')                        # Center the text (horizontal alignment)

plt.legend(framealpha = 0.4, loc='upper left') # Give opacity to the legend 
plt.show()                                     # Show window