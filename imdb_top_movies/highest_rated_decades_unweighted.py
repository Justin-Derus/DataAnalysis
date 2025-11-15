# Author Name: Scoey Derus
# Purpose: Using Kaggle's 250 top IMDB movies, generate a graph using matplotlibs bar graph and pandas dataframe
# to find the datasets highest average rating decade  
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

imdb_table = pd.read_csv('./imdb_top_movies.csv', index_col = 0)     # DataFrame created off .csv file
decade_highest_rated = imdb_table.loc[:,['Year','Rating']]                         # Drop columns we don't need (DataFrame type)
                                                                                   # DataFrame supports slicing via loc and iloc
decade_highest_rated['Decade'] = (decade_highest_rated['Year'] // 10) * 10         # Create a decade column | (1992 // 10 = 199.2 rounded down) * 10 = 1990

avg_rating_per_decade = decade_highest_rated.groupby('Decade', as_index=False)[['Rating']].mean().round(2)  # Find the mean rating per decade, round to two decimals

min_rating = min(avg_rating_per_decade['Rating'])   # Find min rating for the y axis to "zoom in"
max_rating = max(avg_rating_per_decade['Rating'])   # Find max rating for the y axis to "zoom in"

bars = plt.bar(avg_rating_per_decade['Decade'], avg_rating_per_decade['Rating'], color="#88db9e", width=7)   # plot the bar graph based on the decade (index) and rating
plt.ylim(min_rating - .25, max_rating + .1)                                                # zoom in on the graph to make it more visually distinguishable
plt.title("Highest Rated Decade (Top 250 IMBD Movies)\n(Unweighted)")     # Add the titles and lables
plt.xlabel("Decade")
plt.ylabel("Average Rating")

#NOTE: This does not account for decades with more movies having more impact on the overall trend
coefficients = np.polyfit(avg_rating_per_decade['Decade'],avg_rating_per_decade['Rating'],1) # 1 linear
trend_line = np.poly1d(coefficients)
plt.plot(avg_rating_per_decade['Decade'], trend_line(avg_rating_per_decade['Decade']),label='Rating Trend',color='#7591c9')

for bar in bars:                                 # in order to get text, we need to go through all objects 
    plt.text(bar.get_x() + bar.get_width() / 2,   # x coords ( left edge xcoord + (width of bar/2) )
             bar.get_height() + -.03,            # y coords (vertical height)
             bar.get_height(),                   # this is the actual text argument (average ratings)
             ha='center')                        # center the text (horizontal alignment)

plt.legend()
plt.show()  # Show window