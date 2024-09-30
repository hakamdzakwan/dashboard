import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from datetime import datetime

# Membaca data
day_df = pd.read_csv('dashboard/main_data.csv')

# Mengubah kolom 'dteday' menjadi tipe datetime
day_df['dteday'] = pd.to_datetime(day_df['dteday'])

# Judul Dashboard
st.title('Dashboard Bike Sharing')

# Menggunakan Tabs untuk Berbagai Visualisasi dan Filter
tab1, tab2, tab3, tab4, tab5 = st.tabs(['How does the season affect the patern of bicycle rentals?',
                                        'Does the weather affect the patern of bicycle rentals?',
                                        'What is the trend in the number of bicycle rentals between 2011 and 2012?',
                                        'How does temperature affect the number of bicycle rentals?',
                                        'What is the trend of bicycle usage on weekdays compared to weekends or holidays?'])

with tab1:
    # Question 1
    st.header('How does the season affect the pattern of bicycle rentals?')
    season_pattern = day_df.groupby('season')[['registered', 'casual']].sum().reset_index()

    plt.figure(figsize=(10, 6))
    plt.bar(season_pattern['season'], season_pattern['registered'], label='Registered', alpha=0.6)
    plt.bar(season_pattern['season'], season_pattern['casual'], label='Casual', alpha=0.6)
    plt.title('Number of Bicycle Rentals by Season')
    plt.legend()
    st.pyplot(plt)
    
    with st.expander("See explanation"):
        st.write(
            """The data shows that bike rental patterns are strongly
            influenced by the season, with the fall being the most
            preferred time for cycling. This could be due to more
            favourable weather conditions.
            """
        )

with tab2:
    # Question 2
    st.header('Does the weather affect the pattern of bicycle rentals?')
    weather_pattern = day_df.groupby('weathersit')[['registered', 'casual']].sum().reset_index()
    
    plt.figure(figsize=(10, 6))
    plt.bar(weather_pattern['weathersit'], weather_pattern['registered'], label='Registered', alpha=0.6)
    plt.bar(weather_pattern['weathersit'], weather_pattern['casual'], label='Casual', alpha=0.6)
    plt.title('Number of Bicycle Rentals by Weather')
    plt.legend()
    st.pyplot(plt)
    
    with st.expander("See explanation"):
            st.write(
                """The pattern of bicycle rentals based on weather shows
                that the most bicycle users occur during clear weather.
                This means that the highest number of bicycle rentals
                occur during clear weather. In contrast, bicycle rentals
                slightly decrease during misty weather. In addition, the
                least number of bicycle rentals occurs during rainy weather.  
                """
            )

with tab3:
    # Question 3
    st.header('What is the trend in the number of bicycle rentals between 2011 and 2012?')
    day_df['mnth'] = pd.Categorical(day_df['mnth'], categories=[
        'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
    ], ordered=True)
    
    monthly_counts = day_df.groupby(by=["mnth", "yr"]).agg({"cnt": "sum"}).reset_index()
    
    plt.figure(figsize=(10, 6))
    sns.lineplot(data=monthly_counts, x="mnth", y="cnt", hue="yr", marker="o")
    plt.title("Bicycle Rental Trend")
    plt.legend(title="Year", loc="upper right")
    plt.tight_layout()
    st.pyplot(plt)
    
    with st.expander("See explanation"):
                st.write(
                    """There is a difference in bicycle rental demand in 2011 and 2012,
                    where in 2012 there were more demanders than 2011. In addition, the
                    data shows that from the beginning of the year, demand always increases
                    until the middle of the year, then decreases until the end of the year.
                    """
                )

with tab4:
    # Question 4
    st.header('How does temperature affect the number of bicycle rentals?')        
    plt.figure(figsize=(10, 6))
    plt.scatter(day_df['temp'], day_df['cnt'], alpha=0.5, label='Data Points')

    # Menghitung regresi linear
    z = np.polyfit(day_df['temp'], day_df['cnt'], 1)  # Koefisien linear
    p = np.poly1d(z)  # Membuat polinomial dari koefisien

    # Menambahkan garis regresi ke plot
    plt.plot(day_df['temp'], p(day_df['temp']), color='red', label='Regression Line')
    
    plt.title('Effect of Temperature on Bike Rentals')
    plt.xlabel('Temperature (Normalized)')
    plt.ylabel('Number of Bike Rentals')
    plt.grid(True)
    plt.legend()
    st.pyplot(plt)
    
    with st.expander("See explanation"):
        st.write(
            """Temperature has an effect on the number of bicycle rental demand,
            where the number of bicycle demand, increases along with the increase
            in temperature, but will slightly decrease when the temperature position is too high. 
            """
        )

with tab5:
    # Question 5
    st.header('What is the trend of bicycle usage on weekdays compared to weekends or holidays?')
    
    plt.figure(figsize=(10, 6))
    sns.barplot(x='workingday', y='cnt', data=day_df, estimator='mean')
    plt.title('Average Bike Rentals: Working Day vs Weekend/Holiday')
    plt.ylabel('Average Number of Bike Rentals')
    st.pyplot(plt)
    
    with st.expander("See explanation"):
            st.write(
            """The number of bicycle rentals is higher on workingday.
            This shows that people use bicycles more for daily activities.
            """
        )
