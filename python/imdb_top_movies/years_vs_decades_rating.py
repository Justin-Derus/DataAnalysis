# Author Name: Scoey Derus
# Purpose: Using Kaggle's 250 top IMDB movies to compare highest rated decades_table vs years,
# are they the same? 
import pandas as pd
import matplotlib.pyplot as plt

#pd.set_option('display.max_rows',None)         # commented out, pandas does not display full table by default must set option
#pd.set_option('display.max_columns',None)

imdb_table = pd.read_csv('./imdb_top_movies/imdb_top_movies.csv', index_col=0)   # read in the pandas dataframe, col 0 will be the 'Rank'

cleaned_table = imdb_table.loc[:,['Year','Rating']]   # clean the dataset for only what we need
cleaned_table['Decade'] = (cleaned_table['Year'] // 10) * 10    # Create a decade column | (1992 // 10 = 199.2 rounded down) * 10 = 1990

fig,ax = plt.subplots(2,1,figsize=(8,8))  # This is the figure we will be using, 2 rows of 1 column so 2 graphs to compare

##############################
# Begin ax[0] "Decades"      #
##############################

avg_rating_per_decade = cleaned_table.groupby('Decade', as_index=False)[['Rating']].mean().round(2)  # Find the mean rating per decade, round to two decimals

min_rating_d = min(avg_rating_per_decade['Rating'])   # Find min rating for the y axis to "zoom in"
max_rating_d = max(avg_rating_per_decade['Rating'])   # Find max rating for the y axis to "zoom in"

max_rated_d = avg_rating_per_decade.loc[avg_rating_per_decade['Rating'] == max_rating_d, 'Decade'].item() # used for text display of highest decade
middle_decade = (min(avg_rating_per_decade['Decade']) + max(avg_rating_per_decade['Decade'])) / 2         # used for text display of highest decade

bars = ax[0].bar(avg_rating_per_decade['Decade'], avg_rating_per_decade['Rating'], color="#88db9e", width=7)   # plot the bar graph based on the decade (index) and rating
ax[0].set_ylim(min_rating_d - .25, max_rating_d + .1)             # zoom in on the graph to make it more visually distinguishable
ax[0].set_title("Highest Rated Decade (Top 250 IMBD Movies)")     # Add the titles and lables
ax[0].set_xlabel("Decade")                                        # set the x label
ax[0].set_ylabel("Rating (Average)")                              # set the y label
ax[0].set_xticks(avg_rating_per_decade['Decade'])                 # set the ticks on x-axis
ax[0].set_xticklabels(str(decade) + "s" for decade in avg_rating_per_decade['Decade'])  # add an "s" character to the x-axis for readability
ax[0].text(middle_decade,max_rating_d + .025,"The highest rated decade was " + str(max_rated_d) + " at a rating of " + str(max_rating_d), ha='center')  # display best

for bar in bars:                                 # in order to get text, we need to go through all objects 
    ax[0].text(bar.get_x() + bar.get_width() / 2,# x coords ( left edge xcoord + (width of bar/2) )
             bar.get_height() + -.03,            # y coords (vertical height)
             bar.get_height(),                   # this is the actual text argument (average ratings)
             ha='center')                        # center the text (horizontal alignment)
    
##############################
# Begin ax[1] "Years"        #
##############################

# We will not be adding a new column like we did in ax[0]
average_rating_per_year = cleaned_table.groupby('Year', as_index=False)['Rating'].mean().round(2)   # filter further by grouping and getting average rating
                                                                                                    # as_index will make it so that 'Year' is a column and not the index

# NOTE: this 3 step process is essentially universal for scatters based on color or size (do not need step 3 if only wanting color)
# Transform values if needed (power, log, sqrt), normalize 0-1, scale to be visually meaningful

# Step 1) create separation by making the values much larger (if data is numerically TINY, this dataset is large enough)
weights = average_rating_per_year['Rating'] # gets the original ratings

# Step 2) normalize the numbers to fall into a 0-1 range - color maps need a 0-1 distribution to work well (c param in scatter)
weights = (weights - weights.min()) / (weights.max() - weights.min())      # weights - weights.min = 0 for the first value (aka the 0 in the 0-1 range we want)
                                                                           # dividing by the max weight - the min weight will always mean the last value is 1
                                                                           # all values are then between 0 and 1, which means we get what we need for colormap 
                                                                           # 0 is darkest color, .5 is middle, 1 is brightest, CMAP MUST BE NORMALIZED

# Step 3) expand the range for s param in scatter
weights = 50 + (weights - weights.min()) / (weights.max() - weights.min()) * 450 # this step is not needed if we only want color, but if we want size, it is needed
                                                                                 # because 0-1 is not a visually meaningful enough scale

average_rating_per_year['Weight'] = weights             # Create a column for  weights section that we just calculated (DO NOT DO IN CLEANED_TABLE, MORE TIMELY)

min_rating = min(average_rating_per_year['Rating'])     # Used for ylim scaling (zooming in on the graph)
max_rating = max(average_rating_per_year['Rating'])     # Used for ylim scaling (zooming in on the graph)
      
highest_rating = max(average_rating_per_year['Rating']) # Used to answer question
highest_rated_year = average_rating_per_year.loc[average_rating_per_year['Rating'] == highest_rating,'Year'].item() # get the highest rated year

# Create scatter plot (x,y,size,color,colormap)
ax[1].scatter(
    average_rating_per_year['Year'],
    average_rating_per_year['Rating'],
    s=average_rating_per_year['Weight'],
    c=average_rating_per_year['Weight'],
    cmap='cool')

ax[1].set_ylim(min_rating - 0.05, max_rating + 0.4)  # Used for zooming
ax[1].set_xlabel('Year')                             # Setting x-axis label
ax[1].set_ylabel('Rating (Average)')                 # Setting y-axis label
ax[1].set_title('Highest Rated Year (IMDB Top 250)') # Setting the title of the scatter plot

# Create text to answer the question "What was the highest rated year on average"
# (x,y,text,horizontal alignment)
ax[1].text(
    highest_rated_year,
    max_rating + 0.2,
    "The highest rated year is: " + str(highest_rated_year) + " at a rating of " + str(highest_rating), 
    ha='center')

# We want to add text to the bubbles that are of a certain size, cannot loop thru like a bar graph, must iterate over the DataFrame
for x,y,size in zip(average_rating_per_year['Year'],average_rating_per_year['Rating'],average_rating_per_year['Weight']): # zip() allows iteration over multsequences parallel
    if size > 150: # only after a certain size are we printing in the bubble, or else it looks bad
        ax[1].text(x, y ,str(round(y,1)), ha='center',va='center',fontsize=7)

plt.tight_layout()
plt.show() # show the graph