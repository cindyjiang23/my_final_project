import streamlit as st
def app():
    st.title('Research Questions')
    st.markdown('''
        4. **What did you set out to study?  (i.e. what was the point of your project?  This should be close to your Milestone 1 assignment, but if you switched gears or changed things, note it here.)**<br>
            Initially I intended to investigate if regions with Michelin-starred restaurants tend to have higher wine prices then those without. I also wanted to determine whether wine prices can be an indicator of a region's culinary prestige. However, I switched gears for my final project because there's neither API nor public data source for wine prices. I then finalized to set out to study how the two economic factors, namely GDP per Capita and Household Spending, may have different relationships with number of Michelin restaurants for each country based upon price and award selections.<br>
                
        5. **What did you Discover/what were your conclusions (i.e. what were your findings?  Were your original assumptions confirmed, etc.?)**<br>
            I discovered that in stark contrast to GDP per Capita, Household Spending generally shows a more positive, though not robust, correlation with the number of Michelin restaurants. Next, the correlation coefficient for GDP per Capita analysis is almost always negative or near 0 no matter what the price is and what Michelin award type is. Furthermore, the number of stars doesn't reflect much variations in the relationships but when the award type is limited to "Bib Gourmand," Household Spending has a strong positive correlation with number of restaurants. These conclusions were compelling to me because originally I simply assumed that the higher the price as well as number of stars, the two economic factors will both show a positive correlation with number of restaurants. I assumed that richer countries will have more Michelin restaurants.<br>
                
        6. **What difficulties did you have in completing the project?**<br>
            One of the key difficulties was thinking about the filter options. I was struggling how to design the webapp so that it has a logic flow leading to the analysis results. The major difficulty was designing the layout of my webapp and creating subdirectories to create a seperate page for the research questions. Furthermore, it was also quite tricky generating the interactive map and I spent a lot of time working on fixing streamlit_folium but still failed at the end.<br>

        7. **What skills did you wish you had while you were doing the project?**<br>
            I really wished to have a better analysis skill while working on the project. I was struggling to figure out what factors and what relationships I should investigate for the linear regression models. I hoped that I could have the ability to finesse each part logically and quickly.<br>
                
        8. **What would you do “next” to expand or augment the project?**<br>
            I would like to make the map more interactive. Moreover, I'd like to also investigate the relationship between number of Michelin restaurants with other non-economic factors such as weather and language use.<br>
                
    ''', unsafe_allow_html=True
    )

    
app()