# Author Name: Scoey Derus
# Purpose: Using Kaggle's 250 top IMDB movies, generate a graph using matplotlibs bar graph and pandas dataframe
# to find the datasets highest average rating decade  
import matplotlib.pyplot as plt
import pandas as pd

imdb_table = pd.read_csv('imdb_top_movies/imdb_top_movies.csv', index_col = 0)     # DataFrame created off .csv file
decade_highest_rated = imdb_table.loc[:,['Year','Rating']]                         # Drop columns we don't need (DataFrame type)
                                                                                   # DataFrame supports slicing via loc and iloc
decade_highest_rated['Decade'] = (decade_highest_rated['Year'] // 10) * 10         # Create a decade column | (1992 // 10 = 199.2 rounded down) * 10 = 1990

avg_rating_per_decade = decade_highest_rated.groupby('Decade')[['Rating']].mean().round(2)  # Find the mean rating per decade, round to two decimals

min_rating = min(avg_rating_per_decade['Rating'])   # Find min rating for the y axis to "zoom in"
max_rating = max(avg_rating_per_decade['Rating'])   # Find max rating for the y axis to "zoom in"

fig, ax = plt.subplots()        # set the subplots, fig is the figure (container) of the plotting area
ax.set_facecolor("#cbcfca")     # ax is the Axes - the actual graph itself 
fig.set_facecolor("#cbcfca")

bars = ax.bar(avg_rating_per_decade.index.astype(str), avg_rating_per_decade['Rating'], color="#88db9e")   # plot the bar graph based on the decade (index) and rating
ax.set_ylim(min_rating - .25, max_rating + .1)                                                # zoom in on the graph to make it more visually distinguishable
ax.set_title("Highest Rated Decade (Top 250 IMBD Movies)")     # Add the titles and lables
ax.set_xlabel("Decade")
ax.set_ylabel("Average Rating")


for bar in bars:                                 # in order to get text, we need to go through all objects 
    ax.text(bar.get_x() + bar.get_width() / 2,   # x coords ( left edge xcoord + (width of bar/2) )
             bar.get_height() + -.03,            # y coords (vertical height)
             bar.get_height(),                   # this is the actual text argument (average ratings)
             ha='center')                        # center the text (horizontal alignment)

plt.show()  # Show window