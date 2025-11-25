# Author Name: Scoey Derus
# Purpose: Using Kaggle's 250 top IMDB movies, generate a graph using matplotlibs bar graph and pandas dataframe
# to find the datasets highest rated year
import pandas as p
import matplotlib.pyplot as plt

imdb_table = p.read_csv('./imdb_top_movies/imdb_top_movies.csv', index_col=0) # read file and give the row #'s "Rank"
cleaned_table = imdb_table.loc[:,['Year','Rating']]                           # for this purpose we only need these columns

# Need to get all years, and average rating for those years
avg_rating_per_year = cleaned_table.groupby('Year')[['Rating']].mean().round(2) # create a new dataframe with the years grouped and the ratings for them

min_rating = min(avg_rating_per_year['Rating'])             # find the minimum rating (for zooming purposes)
max_rating = max(avg_rating_per_year['Rating'])             # find the maximum rating (for zooming purposes)
highest_rated_year = avg_rating_per_year['Rating'].idxmax() # find out what the highest rated year is for our text purposes, the idxmax is going to give us the year
highest_rating = avg_rating_per_year['Rating'].max()        # find out what the rating was for that highest year, max on rating gives highest rating

plt.figure(figsize=(15,7))                                  # set the size of our new figure, we have a lot of x-axis and we do not want to miss any

bars = plt.bar(avg_rating_per_year.index.astype(str),avg_rating_per_year['Rating']) # creation of bar graph, x axis is the 'Year' index of the dataframe, y is 'Rating' column
plt.xlabel("Years")                                     # label for axes and title
plt.ylabel("Rating (Average)")
plt.title("Highest Rated Year (Top 250 IMBD Movies)")

plt.ylim(min_rating -.25, max_rating + .1)                      # using out previous min and max calculation for zooming
plt.xticks(avg_rating_per_year.index.astype(str),rotation=90)   # our x axis uses dates (a lot) so we want to rotate the dates for no overlap, our axis is the index from the DF

for bar in bars:                # for every bar we want to add the value it is to the top of it
    height = bar.get_height()   
    plt.text(bar.get_x() + bar.get_width()/2, height + 0.02,  height, ha='center',fontsize=6) # f"{height:.1f}" for rounding

    # first param = x coord -> want to get the left side of the bar, then find the width and divide by two to get center
    # second param is the y coord, want the height of the bar (the value) and adding a little value to get it right above the bar
    # third param is the actual thing to be printed, commented to the right is a format string for rounding if wanted
    # fourth param centers the text (horizontal alignment)
    # fifth param is to change the size of the text because our sample size is way to big

plt.text(str(1921),9,"The highest rated year is: " + str(highest_rated_year) + " at a rating of " + str(highest_rating) ,ha="left") 
# add some text to answer the Q: "What was the highest rated year?"

plt.show() # show the bar chart