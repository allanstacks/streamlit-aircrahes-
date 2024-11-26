import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt 
import seaborn as sns
import streamlit as st

# import dataset
def load_data():
    file = "aircrahesFullDataUpdated_2024 (1).csv"
    df = pd.read_csv(file)
    # merging the date and creating a new column
    df.loc[:,"Date"] = df['Year'].astype(str) + '-' + df['Month'].astype(str) + '-' + df['Day'].astype(str)
    # dropping the columns
    df.drop(columns=['Year','Month','Day'],axis=1, inplace=True)
    # changing tr date format
    df["Date"] = pd.to_datetime(df["Date"])
    # filling nan values on the country/region
    df["Country/Region"] = df['Country/Region'].fillna('unknown')

    # conutry/Region
    df['Country/Region'] = df['Country/Region'].str.strip().str.title()
    # Aircraft Manufacturer
    df['Aircraft Manufacturer'] = df['Aircraft Manufacturer'].str.strip().str.title()
    # Aircraft
    df['Aircraft'] = df['Aircraft'].str.strip()
    # location
    df['Location'] = df['Location'].str.strip()
    # Operator
    df['Operator'] = df['Operator'].str.strip()     
    # check for duplicate
    duplicate_count = df.duplicated().sum()
    print(duplicate_count)
    
    
    return df

# load the dataset 
df = load_data()

# app title
st.title("AIRCRASHES ANALYSIS")

# Calculate the total number of accidents
total_accidents = len(df)

# Calculate the total number of fatalities
total_fatalities = df['Fatalities (air)'].sum()

# Calculate the total number of survivors
total_survivors = df['Aboard'].sum() - total_fatalities

# Calculate the survival rate
survival_rate = (total_survivors / total_accidents) * 100
print(f'Survival rate: {survival_rate:.1f}%')


Q1_fatalities = df['Fatalities (air)'].quantile(0.25)
Q3_fatalities = df['Fatalities (air)'].quantile(0.75)
IQR_fatalities = Q3_fatalities - Q1_fatalities


st.subheader("Calculations")
col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("Total number of accidents",total_accidents)
col2.metric("Total number of fatalities", total_fatalities)
col3.metric("Total number of survivors", total_survivors)
col4.metric("Survival rate", survival_rate)
col5.metric("IQR Fatalities", IQR_fatalities)

st.write(df)

# Charts and graphs
# Year fatality
try:
    st.write("## Crashes by Year ")
    Year_fatality = df.groupby('Date')['Fatalities (air)'].sum().reset_index()
    # plot
    st.subheader("Crashes by Year")
    fig, ax = plt.subplots()
    Year_fatality.plot(kind='line', ax=ax)
    ax.set_title('Number of Crashes by Year')
    ax.set_xlabel('Year')
    ax.set_ylabel('Number of Crashes')
    st.pyplot(fig)
except ValueError as e:
    st.error(
       """ Error: """ % e.reason
    )

# Fatalities by Country/Region - Line plot
try:
    country_fatality = df.groupby('Country/Region')['Fatalities (air)'].sum().reset_index()
    top_countries = country_fatality.head(20)
    print(top_countries)
    st.subheader("Country/Region Fatality")
    fig, ax = plt.subplots()
    top_countries.plot(kind='line', ax=ax, color='red')
    ax.set_title('Fatalities by Country/Region')
    ax.set_xlabel('Year')
    ax.set_ylabel('Number of Fatalities')
    st.pyplot(fig)
except ValueError as e:
    st.error(
       """ Error: """ % e.reason
    )

## location fatality - Bar plot
try:
    location_fatality = df.groupby('Location')['Fatalities (air)'].sum().reset_index()
    top_location = location_fatality.head(20)
    print(top_location)
    st.subheader("location fatality")
    fig, ax = plt.subplots()
    top_location.plot(kind='bar', ax=ax)
    ax.set_title('Location Fatalities (Top 20)')
    ax.set_xlabel('Manufacturer')
    ax.set_ylabel('Number of Fatalities')
    st.pyplot(fig)
except ValueError as e:
    st.error(
       """ Error: """ % e.reason
    )

# aircraft fatality
aircraft_fatality = df.groupby('Aircraft')['Fatalities (air)'].sum().reset_index()
top_aircraft = aircraft_fatality.head(20)
print(top_aircraft)
st.subheader("Crashes by Aircraft")
fig, ax = plt.subplots()
top_aircraft.plot(kind='bar', ax=ax, color='green')
ax.set_title('Crashes by Country/Region (Top 10)')
ax.set_xlabel('Country/Region')
ax.set_ylabel('Number of Crashes')
st.pyplot(fig)

# bar plot of Aboard vs Fatalities
data = { 'Category': ['Aboard', 'Fatalities'], 
        'Count': [df['Aboard'].sum(), df['Fatalities (air)'].sum()] }
df_bar = pd.DataFrame(data)
 # Bar plot
fig, ax = plt.subplots()
sns.barplot(x='Category', y='Count', data=df_bar, ax=ax)
ax.set_title('Total Number of People Aboard vs. Total Number of Fatalities')
ax.set_xlabel('Category')
ax.set_ylabel('Count')
st.pyplot(fig)


# Assuming df is your DataFrame 
# # Group by Aircraft Manufacturer 
accidents_by_manufacturer = df.groupby('Aircraft Manufacturer').size() 
fatalities_by_manufacturer = df.groupby('Aircraft Manufacturer')['Fatalities (air)'].sum()
#  # Combine accidents and fatalities data into one DataFrame for correlation analysis 
manufacturer_analysis = pd.DataFrame({ 'Accidents': accidents_by_manufacturer, 
                                      'Fatalities': fatalities_by_manufacturer }).fillna(0) # Handle missing data by filling NaN with 0 
# # Display the top manufacturers with the highest accidents and fatalities
top_manufacturer = manufacturer_analysis.sort_values(by='Accidents', ascending=False).head(10) 
# # Calculate the correlation between the number of accidents and fatalities
correlation = manufacturer_analysis['Accidents'].corr(manufacturer_analysis['Fatalities'])
print(f"Correlation between number of accidents and fatalities: {correlation}") 
# # Plot the bar chart 
fig, ax = plt.subplots(figsize=(12, 8))
top_manufacturer.plot(kind='bar', ax=ax, color=['red', 'black'])
ax.set_title('Crashes by Aircraft Manufacturer (Top 10)', fontsize=16)
ax.set_xlabel('Manufacturer', fontsize=14)
ax.set_ylabel('Count', fontsize=14) 
ax.grid(True, linestyle='--', alpha=0.6) 
plt.xticks(rotation=45)
plt.tight_layout() 
st.pyplot(fig)

# heatmap showing the correlation between the number of accidents and fatalities by aircraft manufacturer.


# Assuming df is your DataFrame # Group by Aircraft Manufacturer
accidents_by_manufacturer = df.groupby('Aircraft Manufacturer').size() 
fatalities_by_manufacturer = df.groupby('Aircraft Manufacturer')['Fatalities (air)'].sum()
# Combine accidents and fatalities data into one DataFrame for correlation analysis
manufacturer_analysis = pd.DataFrame({ 'Accidents': accidents_by_manufacturer, 
                                      'Fatalities': fatalities_by_manufacturer }).fillna(0) # Handle missing data by filling NaN with 0
# Calculate the correlation matrix 
correlation_matrix = manufacturer_analysis.corr() 
# Plot the heatmap
fig, ax = plt.subplots(figsize=(8, 6)) 
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', ax=ax)
ax.set_title('Correlation Matrix of Accidents and Fatalities', fontsize=16)
plt.tight_layout() 
st.pyplot(fig)