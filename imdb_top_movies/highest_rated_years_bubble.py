# Author Name: Scoey Derus
# Purpose: Using Kaggle's 250 top IMDB movies, generate a graph using matplotlibs scatter plot and pandas dataframe
# to find the datasets highest rated year
import pandas as pd
import matplotlib.pyplot as plt

#pd.set_option('display.max_rows',None)         # commented out, pandas does not display full table by default must set option
#pd.set_option('display.max_columns',None)

imdb_table = pd.read_csv('./imdb_top_movies/imdb_top_movies.csv', index_col=0)                      # read in the pandas dataframe, col 0 will be the 'Rank'

cleaned_table = imdb_table.loc[:,['Year','Rating']]                                                 # clean the dataset for only what we need
average_rating_per_year = cleaned_table.groupby('Year', as_index=False)['Rating'].mean().round(2)   # filter further by grouping and getting average rating
                                                                                                    # as_index will make it so that 'Year' is a column and not the index

# NOTE: this 3 step process is essentially universal for scatters based on color or size (do not need step 3 if only wanting color)
# Transform values if needed (power, log, sqrt), normalize 0-1, scale to be visually meaningful

# Step 1) create separation by making the values much larger (if data is numerically TINY, this dataset is large enough)
weights = average_rating_per_year['Rating'] # gets the original ratings

# Step 2) normalize the numbers to fall into a 0-1 range - color maps need a 0-1 distribution to work well (c param in scatter)
weights = (weights - weights.min()) / (weights.max() - weights.min()) ** 4 # weights - weights.min = 0 for the first value (aka the 0 in the 0-1 range we want)
                                                                           # dividing by the max weight - the min weight will always mean the last value is 1
                                                                           # all values are then between 0 and 1, which means we get what we need for colormap 
                                                                           # 0 is darkest color, .5 is middle, 1 is brightest, CMAP MUST BE NORMALIZED

# Step 3) expand the range for s param in scatter
weights = 50 + (weights - weights.min()) / (weights.max() - weights.min()) * 450 # this step is not needed if we only want color, but if we want size, it is needed
                                                                                 # because 0-1 is not a visually meaningful enough scale

average_rating_per_year['Weight'] = weights             # Create a column for our weights section that we just calculated

min_rating = min(average_rating_per_year['Rating'])     # Used for ylim scaling (zooming in on the graph)
max_rating = max(average_rating_per_year['Rating'])     # Used for ylim scaling (zooming in on the graph)
      
highest_rating = max(average_rating_per_year['Rating']) # Used to answer our question
highest_rated_year = average_rating_per_year.loc[average_rating_per_year['Rating'] == highest_rating,'Year'].item()

plt.figure(figsize=(10,6))  # Create a decent sized graph for us to look at

# Create our scatter plot (x,y,size,color,colormap)
scatter = plt.scatter(
    average_rating_per_year['Year'],
    average_rating_per_year['Rating'],
    s=average_rating_per_year['Weight'],
    c=average_rating_per_year['Weight'],
    cmap='cool')

plt.ylim(min_rating - 0.05, max_rating + 0.4) # Used for our zooming
plt.xlabel('Year')                            # Setting x-axis label
plt.ylabel('Rating (Average)')                # Setting y-axis label
plt.title('Best Rated Year (IMDB Top 250) Scatter Version') # Setting the title of the scatter plot

# Create our text to answer the question "What was the highest rated year on average"
# (x,y,text,horizontal alignment)
plt.text(
    highest_rated_year,
    max_rating + 0.2,
    "The highest rated year is: " + str(highest_rated_year) + " at a rating of " + str(highest_rating), 
    ha='center')

# We want to add text to the bubbles that are of a certain size, cannot loop thru like a bar graph, must iterate over the DataFrame
for x,y,size in zip(average_rating_per_year['Year'],average_rating_per_year['Rating'],average_rating_per_year['Weight']): # zip() allows iteration over multiple sequences parallel
    if size > 150: # only after a certain size are we printing in the bubble, or else it looks bad
        plt.text(x, y ,str(round(y,1)), ha='center',va='center',fontsize=7)

plt.show() # show the graph