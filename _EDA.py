#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')


# In[3]:


df = pd.read_csv("C:\\Users\\LENOVO\\OneDrive\\Documents\\Good_Reads_Book_Awards_Crawl_2023_12_27_11_14.csv")


# In[4]:


df


# In[5]:


df.info()


# In[6]:


df.describe()


# In[7]:


numeric_columns = ['Number of Ratings','Number of Reviews']

#Remove the character comma from those columns and convert to Int32
for column in numeric_columns:
    df[column] = df[column].replace(',', '', regex=True).astype('int32')


# In[8]:


df[column]


# In[9]:


#Convert the rest of the columns to correct data types
convert_dict = {'Readers Choice Votes': 'int32',
                'Readers Choice Category': 'category',
                'Title': 'string',
                'Author': 'string',
                'Total Avg Rating': 'float16',
                'Number of Pages': 'int16',
                'Edition': 'category',
                'First Published date': 'datetime64[ns]',
                'Kindle Price': 'float16'}
df = df.astype(convert_dict)


# In[10]:


#Separate the currency from the text and put it in the new column
df['Kindle Version'] = df['Kindle Version and Price'].str.extract('([a-zA-Z ]+)', expand=False).str.strip()

#Change the column into correct data type
df['Kindle Version'] = df['Kindle Version'].astype('category')

#Remove the previous column
df = df.drop('Kindle Version and Price', axis=1)


# In[11]:


df.info()


# In[12]:


df.describe()


# In[13]:


##analyzing 
cat_counts = df['Readers Choice Category'].value_counts()
print(cat_counts)

plt.figure(figsize=(12, 6))
sns.barplot(x=cat_counts.index, y=cat_counts.values, palette='Blues_d')
plt.title('Distribution of Books Across Categories')
plt.xlabel('Category')
plt.ylabel('Number of Books')
plt.xticks(rotation=30, ha='right')
plt.show()


# In[15]:


fig, axes = plt.subplots(3, 2, figsize=(16, 18), sharey=False, sharex=True)

# First plot Distributions of Readers Choice Votes
sns.boxplot(data=df, x='Readers Choice Category', y='Readers Choice Votes', palette='Set3', ax=axes[0, 0])
axes[0, 0].set_title('Distribution of Readers Choice Votes for Each Category')
axes[0, 0].set_ylabel('Votes')

# Second plot Distribution of Average Ratings
sns.boxplot(data=df, x='Readers Choice Category', y='Total Avg Rating', palette='Set3', ax=axes[0, 1])
axes[0, 1].set_title('Distribution of Average Ratings for Each Category')
axes[0, 1].set_ylabel('Avg Ratings')

# Third plot Distribution of Number of Ratings
sns.boxplot(data=df, x='Readers Choice Category', y='Number of Ratings', palette='Set3', ax=axes[1, 0])
axes[1, 0].set_title('Distribution of Number of Ratings for Each Category')
axes[1, 0].set_ylabel('Ratings')

# Fourth plot Distribution of Number of Reviews
sns.boxplot(data=df, x='Readers Choice Category', y='Number of Reviews', palette='Set3', ax=axes[1, 1])
axes[1, 1].set_title('Distribution of Number of Reviews for Each Category')
axes[1, 1].set_ylabel('Reviews')

# Fifth plot Distribution of Number of Pages
sns.boxplot(data=df, x='Readers Choice Category', y='Number of Pages', palette='Set3', ax=axes[2, 0])
axes[2, 0].set_title('Distribution of Number of Pages for Each Category')
axes[2, 0].set_ylabel('Pages')

# Sixth plot Distribution of Kindle Price
sns.boxplot(data=df, x='Readers Choice Category', y='Kindle Price', palette='Set3', ax=axes[2, 1])
axes[2, 1].set_title('Distribution of Kindle Price ($) for Each Category')
axes[2, 1].set_ylabel('Kindle Price ($)')

for ax in axes[2, :]:
   ax.set_xticklabels(ax.get_xticklabels(), rotation=30, ha='right')
   
fig.tight_layout()
plt.show()


# In[16]:


#Determine which column we want to aggregate
aggregations = {'Readers Choice Votes': 'sum', 
                'Total Avg Rating': 'mean',
               'Number of Ratings': 'sum',
               'Number of Reviews': 'sum',
                'Number of Pages': 'median',
                'Kindle Price': 'median',
               }

#Group by book category
category_vote = df.groupby('Readers Choice Category').agg(aggregations).sort_values('Readers Choice Votes', ascending=False)

# Calculate the percentage of total votes, total ratings, and total reviews for each category
total_votes = category_vote['Readers Choice Votes'].sum()
total_ratings = category_vote['Number of Ratings'].sum()
total_reviews = category_vote['Number of Reviews'].sum()
percent_of_total_votes = (category_vote['Readers Choice Votes'] / total_votes) * 100
percent_of_total_ratings = (category_vote['Number of Ratings'] / total_ratings) * 100
percent_of_total_reviews = (category_vote['Number of Reviews'] / total_reviews) * 100

# Create new DataFrame of Votes, Ratings, and Reviews
result_df = pd.DataFrame({
    'Votes (sum)': category_vote['Readers Choice Votes'], 
    '% Votes': percent_of_total_votes, 
    'Avg Ratings': category_vote['Total Avg Rating'].round(2),
    'Number of Ratings': category_vote['Number of Ratings'],
    '% of Total Ratings': percent_of_total_ratings.round(2),
    'Number of Reviews': category_vote['Number of Reviews'],
    '% of Total Reviews': percent_of_total_reviews.round(2),
    'Median Pages': category_vote['Number of Pages'],
    'Median Kindle Price': category_vote['Kindle Price'].round(2)
    })

#Find the most voted category
max_voted_cat = result_df['Votes (sum)'].idxmax()
max_votes = result_df['Votes (sum)'].max()
avg_rat = result_df.loc[max_voted_cat, 'Avg Ratings']

#Find the most rated category
max_rated_cat = result_df['Number of Ratings'].idxmax()
max_rates = result_df['Number of Ratings'].max()
pct_max_rates = result_df['% of Total Ratings'].max()

#Find the most reviewed category
max_reviewed_cat = result_df['Number of Reviews'].idxmax()
max_reviews = result_df['Number of Reviews'].max()
pct_max_reviews = result_df['% of Total Reviews'].max()

#Print the result 
print(f"The category '{max_voted_cat}' is The Most Voted Category of 2023, with {max_votes:,} votes")
print(f"The category '{max_rated_cat}' is The Most Rated Category of 2023, having an average rating of {format(avg_rat, '.2f')}, and number of ratings: {max_rates:,}, or {format(pct_max_rates, '.2f')}% of total ratings")
print(f"The category '{max_reviewed_cat}' is The Most Reviewed Category of 2023, with {max_reviews:,} number of reviews, or {format(pct_max_reviews, '.2f')}% of total reviews")

result_df


# In[17]:


fig, axes = plt.subplots(3, 2, figsize=(16, 18), sharey=False)

# First plot
sns.barplot(x=result_df.index, y=result_df['Votes (sum)'], palette='Blues_d', order=result_df.index, ax=axes[0, 0])
axes[0, 0].set_title('Readers Choice Votes for Each Category')
axes[0, 0].set_ylabel('Votes')
axes[0, 0].set_xticklabels(labels=result_df.index, rotation=30, ha='right')

# Second plot
result_df_sorted = result_df.sort_values(by='Avg Ratings', ascending=False)
sns.barplot(x=result_df_sorted.index, y=result_df_sorted['Avg Ratings'], palette='Blues_d', order=result_df_sorted.index, ax=axes[0, 1])
axes[0, 1].set_title('Average Ratings for Each Category')
axes[0, 1].set_ylabel('Avg Ratings')
axes[0, 1].set_xticklabels(labels=result_df_sorted.index, rotation=30, ha='right')

# Third plot
result_df_sorted = result_df.sort_values(by='Number of Ratings', ascending=False)
sns.barplot(x=result_df_sorted.index, y=result_df_sorted['Number of Ratings'], palette='Blues_d', order=result_df_sorted.index, ax=axes[1, 0])
axes[1, 0].set_title('Number of Ratings for Each Category')
axes[1, 0].set_ylabel('Ratings')
axes[1, 0].set_xticklabels(labels=result_df_sorted.index, rotation=30, ha='right')

# Fourth plot
result_df_sorted = result_df.sort_values(by='Number of Reviews', ascending=False)
sns.barplot(x=result_df_sorted.index, y=result_df_sorted['Number of Reviews'], palette='Blues_d', order=result_df_sorted.index, ax=axes[1, 1])
axes[1, 1].set_title('Number of Reviews for Each Category')
axes[1, 1].set_ylabel('Reviews')
axes[1, 1].set_xticklabels(labels=result_df_sorted.index, rotation=30, ha='right')

# Fifth plot
result_df_sorted = result_df.sort_values(by='Median Pages', ascending=False)
sns.barplot(x=result_df_sorted.index, y=result_df_sorted['Median Pages'], palette='Blues_d', order=result_df_sorted.index, ax=axes[2, 0])
axes[2, 0].set_title('Average Pages for Each Category')
axes[2, 0].set_ylabel('Pages')
axes[2, 0].set_xticklabels(labels=result_df_sorted.index, rotation=30, ha='right')

# Sixth plot
result_df_sorted = result_df.sort_values(by='Median Kindle Price', ascending=False)
sns.barplot(x=result_df_sorted.index, y=result_df_sorted['Median Kindle Price'], palette='Blues_d', order=result_df_sorted.index, ax=axes[2, 1])
axes[2, 1].set_title('Average Kindle Price for Each Category')
axes[2, 1].set_ylabel('Kindle Price ($)')
axes[2, 1].set_xticklabels(labels=result_df_sorted.index, rotation=30, ha='right')

plt.tight_layout()
plt.show()


# In[18]:


# Assign the columns
columns_of_interest = ['Number of Reviews', 'Number of Ratings', 'Number of Pages', 'Total Avg Rating', 'Readers Choice Votes', 'Kindle Price']

# Calculate the correlation matrix
correlation_matrix = df[columns_of_interest].corr()

# Display the correlation matrix
plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f", linewidths=.5)
plt.title('Correlation Matrix')
plt.xticks(rotation=30, ha='right')
plt.show()


# In[19]:


most_voted_books = df[['Title', 'Readers Choice Category', 'Readers Choice Votes', 'Total Avg Rating', 'Number of Ratings', 'Number of Reviews', 'Number of Pages']].sort_values(by=['Readers Choice Votes', 'Number of Ratings', 'Number of Reviews'], ascending=False).head(20)

plt.figure(figsize=(14, 6))
sns.barplot(x=most_voted_books['Title'], y=most_voted_books['Readers Choice Votes'], data=most_voted_books, palette='Blues_d')
plt.title('Most Voted Books in 2023')
plt.xlabel('Book Title')
plt.ylabel('Votes')
plt.xticks(rotation=30, ha='right')
plt.show()

most_voted_books


# In[20]:


max_votes_index = df.groupby('Readers Choice Category')['Readers Choice Votes'].idxmax()
titles_with_max_votes = df.loc[max_votes_index, ['Readers Choice Category', 'Title', 'Readers Choice Votes', 'Total Avg Rating', 'Number of Ratings', 'Number of Reviews', 'Number of Pages']].sort_values('Readers Choice Votes', ascending=False)
titles_with_max_votes


# In[ ]:




