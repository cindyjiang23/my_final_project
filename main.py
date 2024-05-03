import streamlit as st
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
import matplotlib.pyplot as plt
import numpy as np
import pydeck as pdk

st.sidebar.write("*Please choose filters to start :)*")

def perform_regression(aggregated_data, column):
    if aggregated_data.empty:
        st.write("No data available for regression.")
        return None, None, None, None

    X = aggregated_data[[column]].values.reshape(-1, 1)
    y = aggregated_data['Restaurant_Count'].values
    countries = aggregated_data['Country'].values

    model = LinearRegression()
    model.fit(X, y)
    y_pred = model.predict(X)
    r_squared = model.score(X, y)
    correlation_coefficient = np.corrcoef(X.ravel(), y)[0, 1]

    return model, X, y, countries, r_squared, correlation_coefficient

def plot_regression(X, y, countries, model, xlabel, ylabel):
    plt.figure(figsize=(10, 6))
    plt.scatter(X, y, color='blue', label='Data Points')
    plt.plot(X, model.predict(X), color='red', label='Regression Line')
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(f'Relationship between {xlabel} and {ylabel}')

    for i, txt in enumerate(countries):
        plt.annotate(txt, (X[i], y[i]), textcoords="offset points", xytext=(0,10), ha='center')

    plt.legend()
    plt.grid(True)
    plt.show()
    st.pyplot(plt)

file_path = 'my_final_project/final_merged_data.csv'
data = pd.read_csv(file_path)
data = data.dropna(subset=['GDP per Capita (USD)', 'Household Spending (Million US$)'])
data['Award'] = data['Award'].str.lower().str.strip()
data['Price_Numeric'] = data['Price'].apply(lambda x: len(x) if pd.notna(x) else None)
data['Star_Numeric'] = data['Award'].apply(lambda x: {'1 star': 1, '2 stars': 2, '3 stars': 3}.get(x, None))

st.title('Michelin Restaurant Analysis')
st.caption("Navigate to different sections using the sidebar.")
st.markdown('''
        1. **My name**<br>
            Cindy Jiang

            
        2. **An explanation of how to use the webapp**<br>
            The purpose of this webapp is to analyze various factors affecting Michelin-rated restaurants across different countries. Those factors include price and awards. The webapp focuses on the relationship between the two economic factors, GDP per capita and household spending, and the number of Michelin-starred or Michelin-guided restaurants.<br>

            On the top left hand side, user can navigate to different sections using the sidebar. "main" displays the main project page and "about" shows answers to questions 4 to 8. After selecting different filter options, user can click on the "Analyze" button and the webapp will start generating the analysis report on the right hand side.<br>

            The interactivity of the webapp primarily takes place in the "Filter Options." By choosing price, award type, or number of stars, user can see different charts and plots displayed on the right hand side to visually explore how these factors can affect the relationship between number of Michelin restaurants in each country and the two economic factors. User can also scroll down to see a more holistic analysis on the two linear regression models, r-sqared values, correlation coefficients, and a dynamic world map showing the locations for each restaurant based upon user selection. The map was created by using the latitude and longitude columns in the dataset. Moreover, tab options are also available for user to see more information regarding this webapp.<br>

            The first table lists information about the number of restaurants that fulfill user's selection for each country. By using country as the common factor, the columns GDP per Capita and Household Spending for countries listed are also displayed. The analysis report is divided into two parts, specifically GDP per Capita and Household Spending. The linear regression models showcase the relationship between each of the two economic factors and number of restaurants according to user selection.<br>

            Based on my Michelin restaurant analysis, my conclusions were that<br>
            a) Compared to GDP per Capita, Household Spending shows a more positive, though not robust, correlation with the number of Michelin restaurants.<br>
            b) The correlation coefficient for GDP per Capita analysis is almost always negative or near 0 no matter what the price is and what Michelin award type is.<br>
            c) The higher the price, the stronger the correlation between Household Spending and number of restaurants.<br>
            d) When the award type is limited to "Bib Gourmand," Household Spending has a strong positive correlation with number of restaurants.<br>
            e) <u>The key factor lies in whether or not the country is developed or developing. GDP per Capita, in comparison to Household Spending, is directly related to this factor.</u> For example, China has a high number of Michelin restaurants, but because the country's GDP per Capita is quite low, the linear regression model generally shows a slight negative correlation. <u>On the other hand, Household Spending means the amount of final consumption expenditure made by resident households to meet their everyday needs, which is more associated with the number of restaurants.</u><br>
        
        3. **Any major “gotchas” (i.e. things that don’t work, go slowly, could be improved, etc.)**<br>
            I think the first major "gotcha" is that the map is not very interactive. When user zooms out, the locations for each restaurant become unclear and invisible. I think this is because I used pydeck instead of streamlit_folium. I was trying to install streamlit_folium in a new virtual environment but I failed. If I were to have more time, I would definitely work on that more and generate a clearer map no matter what zoom level is. Another major "gotcha" is that by turning price and number of stars into numeric values, I could've also investigated how average star by country correlates to GDP per Capita and Household Spending.<br>
            
    ''', unsafe_allow_html=True
    )


st.write("*Click 'Analyze' and scroll down to see Data & Visualizations analysis*")

main_tab, description = st.tabs(['Data & Visualizations', 'Description of Datasets'])

# Sidebar for filtering
st.sidebar.header('Filter Options')
price_range = st.sidebar.slider("Price ('1' means '$', '4' means '$$$$')", 1, 4, (1, 4))
award_selection = st.sidebar.radio('Select Award Type:', ['Stars', 'Bib Gourmand'])
star_selections = st.sidebar.multiselect('Select Number of Stars:', options=[1, 2, 3], default=[1, 2, 3]) if award_selection == 'Stars' else []

with main_tab:
    if st.sidebar.button('Analyze', key='analyze'):
        filtered_data = data[data['Price_Numeric'].between(*price_range)]
        if award_selection == 'Stars':
            filtered_data = filtered_data[filtered_data['Star_Numeric'].isin(star_selections)]
        elif award_selection == 'Bib Gourmand':
            filtered_data = filtered_data[filtered_data['Award'] == 'bib gourmand']

        if filtered_data.empty:
            st.write("No data found with the selected filters.")
        else:
            restaurant_counts = filtered_data.groupby('Country').agg(
                Restaurant_Count=pd.NamedAgg(column='Name', aggfunc='size'),
                GDP_Per_Capita=pd.NamedAgg(column='GDP per Capita (USD)', aggfunc='mean'),
                Household_Spending=pd.NamedAgg(column='Household Spending (Million US$)', aggfunc='mean')
            ).reset_index()
            st.session_state['aggregated_data'] = restaurant_counts
            st.write("Number of Restaurants, GDP per Capita, and Household Spending by Country", restaurant_counts)

            col1, col2 = st.columns(2)
            with col1:
                st.header("GDP per Capita Analysis")
                if 'aggregated_data' in st.session_state:
                    model_gdp, X_gdp, y_gdp, countries, r_squared_gdp, corr_coef_gdp = perform_regression(st.session_state['aggregated_data'], 'GDP_Per_Capita')
                    if model_gdp is not None:
                        plot_regression(X_gdp, y_gdp, countries, model_gdp, 'GDP per Capita (USD)', 'Number of Restaurants')
                        st.write(f"GDP Model R-squared: {r_squared_gdp:.3f}")
                        st.write(f"GDP Model Correlation Coefficient: {corr_coef_gdp:.3f}")

            with col2:
                st.header("Household Spending Analysis")
                if 'aggregated_data' in st.session_state:
                    model_spending, X_spending, y_spending, countries, r_squared_spending, corr_coef_gdp = perform_regression(st.session_state['aggregated_data'], 'Household_Spending')
                    if model_spending is not None:
                        plot_regression(X_spending, y_spending, countries, model_spending, 'Household Spending (Million US$)', 'Number of Restaurants')
                        st.write(f"Household Spending Model R-squared: {r_squared_spending:.3f}")
                        st.write(f"Household Spending Model Correlation Coefficient: {corr_coef_gdp:.3f}")

        if not filtered_data.empty:
        # Define the layer to display
            layer = pdk.Layer(
                'ScatterplotLayer',
                data=filtered_data,
                get_position='[Longitude, Latitude]',
                get_color='[200, 30, 0, 160]',
                get_radius=150,
                pickable=True,
                auto_highlight=True
            )

            # Set the initial view state for the deck
            view_state = pdk.ViewState(
                longitude=filtered_data['Longitude'].iloc[0],  # Use the longitude of the first entry as the initial view center
                latitude=filtered_data['Latitude'].iloc[0],   # Use the latitude of the first entry as the initial view center
                zoom=11,
                pitch=0
            )

            deck = pdk.Deck(
                layers=[layer],
                initial_view_state=view_state,
                map_provider="carto",  # Use CARTO as the base map provider which does not require an API key
                tooltip={"text": "{Name}"}  # Display restaurant names as tooltips
            )

            # Show the map
            st.pydeck_chart(deck)
        else:
            st.write("No data available for the selected filters.")

with description:
     st.markdown('''
        **DATA SOURCE 1**: https://data.oecd.org/hha/household-spending.htm#indicator-chart<br>
        *Brief description*: The dataset from OECD provides information on household spending across various countries. The dataset is valuable for understanding consumption patterns, economic trneds, and standards of living across different regions and countries.<br>
                 
        **DATA SOURCE 2**: http://api.worldbank.org/v2/country<br>
        *Brief description*: The dataset from The World Bank API offers information about countries around the world, including country names, income levels, populations, and GDP per Capita which is the specific data column I need to scrape.<br>
    
        **DATA SOURCE 3**: https://www.kaggle.com/datasets/ngshiheng/michelin-guide-restaurants-2021<br>
        *Brief description*: The dataset from Kaggle contains information about Michelin Guide-rated restaurants. It includes data on restaurant names, locations, price, awards, cuisine types, longitude and latitude, and restaurant descriptions.<br>
    
        From data source 1, I'd like to get information about Household Spending by country. From data source 2, I'd like to use the dataset to find GDP per Capita by country. Finally, for data source 3, I want to retrieve data related to the Michelin restaurants and their specific countries. I'll need data such as longtitude and latitude to create a map for visualizations, price and awards. These 3 datasets are associated with each other based on the common factor Country. I'd like to connect them through Country and explore the relationship between the two economic factors and number of Michelin restaurants based on price, award type, and number of stars selected.<br>
        
        In the project, I intend to determine how the relationships between GDP per Capita and Household Spending with the number of Michelin restaurants. I'd like to see how the variations in price, "Michelin-guide" or "Michelin-starred," and the number of stars may affect the linear regression between number of Michelin restaurants for each country and their related economnic factors. I hope the final submission will create an interactive platform where users will be able to choose and filter options on the sidebar and see a holistic analysis on Michelin restaurants on the main project page. Users may play around options including price, award type, and number of stars to see the changes in the two linear regression models as well as their associated r-squared values, correlation coefficient, and a dynamic world map.<br>
    ''', unsafe_allow_html=True
    )
