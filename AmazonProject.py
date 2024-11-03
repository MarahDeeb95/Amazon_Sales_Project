# Import Libraries
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import numpy as np
import streamlit as st

# Load the dataset
df = pd.read_csv("FinalAmazonSales.csv")
# Drop the first column
df = df.iloc[:, 1:]

# Add logo Amazon in the top left of the application
logourl = 'https://upload.wikimedia.org/wikipedia/commons/a/a9/Amazon_logo.svg'
st.image(logourl, caption='Amazon Sales Project', width=200)

# Set up the Streamlit app layout
c1, c2 = st.columns(2)
# Define button click actions
if c1.button('Home', use_container_width=True):
    st.session_state.active_page = "Home"
if c2.button('Data Visualization', use_container_width=True):
    st.session_state.active_page = "Data Visualization"

if st.session_state.active_page == 'Home':
    # Add a colored title using Markdown with a hexadecimal color code
    st.markdown("<h1 style='color: #00000;'>Amazon Sales Analysis</h1>", unsafe_allow_html=True)
    pdf_url = 'https://drive.google.com/file/d/1Vfx4Ke5IR6Try7CVFr59L-CT3EJymDLC/view?usp=sharing'
    all_materials = 'https://drive.google.com/drive/folders/1B8QT1xSP0mFDE7-ZP7JYTv_hYKdwLYGs?usp=sharing'
    st.markdown("<h3 style='color: #FF9910;'>From the below buttons you can get the project presentation PDF and Materials.</p>", unsafe_allow_html=True)
    st.markdown(f"""
        <a href="{pdf_url}" target="_blank" style="
            display: inline-block;
            padding: 10px 20px;
            font-size: 16px;
            color: white;
            background-color: #232F3E;
            text-decoration: none;
            border-radius: 5px;
            margin: 5px 0;">
            Project Presentation PDF
        </a>
        """, unsafe_allow_html=True)
    # st.markdown(f"<p style='color: #232F3E;'><a href='{pdf_url}' target='_blank'>Project Overview</a></p>", unsafe_allow_html=True)
    # st.markdown("<h3 style='color: #FF9910;'>From the below URL you can get the project materials.</p>", unsafe_allow_html=True)
    st.markdown(f"""
        <a href="{all_materials}" target="_blank" style="
            display: inline-block;
            padding: 10px 20px;
            font-size: 16px;
            color: white;
            background-color: #232F3E;
            text-decoration: none;
            border-radius: 5px;
            margin: 5px 0;">
            Project Materials
        </a>
        """, unsafe_allow_html=True)
elif st.session_state.active_page == 'Data Visualization':
    st.sidebar.markdown("<h1 style='color: #00000;'>Choose your filters:</h1>", unsafe_allow_html=True)
    
    # Sidebar - Selection
    sidebar_option = st.sidebar.radio("On what you want to check?", ["Data Overview", "EDA", "Visualizations"])

    # Display if selected Data Overview
    if sidebar_option == "Data Overview":
        st.markdown("<h1 style='color: #00000;'>Amazon Sales Analysis</h1>", unsafe_allow_html=True)
        st.header("Data Overview")
        st.markdown("<p style='color: #FF9910;'>This dataset provides information about Products Sales, Discount, and Ratings across different Categories and Subcategories.</p>", unsafe_allow_html=True)
        st.write(df.iloc[:, [17,16,1,3, 4, 5, 6, 7]])
        st.markdown("### Dataset Summary")
        st.write(df.describe())
        
    # Exploratory Data Analysis (EDA)
    elif sidebar_option == "EDA":
        # Display the EDA title
        st.markdown("<h1 style='color: #000000;'>Exploratory Data Analysis</h1>", unsafe_allow_html=True)
        st.markdown("<p style='color: #000000;'>Here we will represent some diagrams to help us understand our dataset structure and correlations</br> We will represent Uni-Variate or Bi-Variate Analysis.</p>", unsafe_allow_html=True)
    ##Uni-Variate Analysis#
        with st.expander("Uni-Variate Analysis"):
        ##Distribution Figures#
            st.markdown("<h2 style='color: #FF9900;'>Uni-Variate Analysis</h2>", unsafe_allow_html=True)       
            #st.markdown("<h3 style='color: #232F3E;'>Quick Insights of Our Data Distribution:</h3>", unsafe_allow_html=True)
            data_columns = ['actual_price','discounted_price','rating']
            for x in data_columns:
                fig,ax =plt.subplots(figsize=(5,4))
                sns.histplot(df[x],ax=ax,bins=30)
                ax.set_title(f"Distribution of {x}")
                ax.tick_params(axis='x', rotation=45) #This to avoid text overlapping
                st.pyplot(fig)


        ##Sales Distribution before & after discount#
            st.markdown("<h3 style='color: #232F3E;'>Sales Distribution Before & After Discount:</h3>", unsafe_allow_html=True)
            #Add discount variables if > 0 or =0
            disc_rate = df[df['discount_percentage'] > 0]
            no_disc = df[df['discount_percentage'] == 0]
            #Add grouping by item in both cases
            disc_grp = disc_rate.groupby('user_id').size()
            ndisc_grp  = no_disc.groupby('user_id').size()
            #create the figure with subplots
            fig2,(ax1,ax2) = plt.subplots(2,figsize = (6,7))
            sns.histplot(ndisc_grp,color='#FF9900',label='Without Discount',ax=ax1)
            ax1.set_title("Sales Distribution without Discount = 0")
            ax1.set_xlabel("Number of Purchases per Item")
            ax1.set_ylabel("Frequency")

            sns.histplot(disc_grp,color='Blue',label='With Discount',ax=ax2)
            ax2.set_title("Sales Distribution with Discount > 0")
            ax2.set_xlabel("Number of Purchases per Item")
            ax2.set_ylabel("Frequency")
            plt.tight_layout() #to prevent layout overlap
            st.pyplot(fig2)
            
    ##BI-Variate Analysis#   
        with st.expander("Bi-Variate Analysis"):
            st.markdown("<h2 style='color: #FF9900;'>Bi-Variate Analysis</h2>", unsafe_allow_html=True)       
        #Correlation Between Data
            st.markdown("<h3 style='color: #232F3E;'>Correlation Analysis</h3>", unsafe_allow_html=True)
            fig3,ax = plt.subplots(figsize=(6,4))
            sns.heatmap(df.corr(numeric_only=True),vmin=-1,vmax=1,cmap='Oranges',annot=True,linecolor="white",linewidths=0.2)
            st.pyplot(fig3)
        #Categorical Rating
            st.markdown("<h3 style='color: #232F3E;'>Categorical Rating Analysis</h3>", unsafe_allow_html=True)
            avg_rating = df.groupby('main_category')['rating'].mean().reset_index()
            fig4 = px.scatter(avg_rating,x='main_category',y='rating', title="Average Rating per Category")
            st.plotly_chart(fig4)

        #Top 10 Subcats Rating
            st.markdown("<h3 style='color: #232F3E;'>Top 10 Rated Products</h3>", unsafe_allow_html=True)
            top_rated = df[['sub_category','product_name','rating_count','rating']].sort_values(by='rating_count',ascending=False).head(10)
            st.write(top_rated)
            ##Chart bgrb feha sub_category rate
            # fig5,ax = plt.subplots(figsize=(6,4))
            # sns.barplot(data=top_rated, x='sub_category', y='rating', ax=ax)
            # ax.tick_params(axis='x', rotation=45)
            # # plt.xticks(rotation=45, ha='right')
            # st.pyplot(fig5)

    # Data Visualizations
    elif sidebar_option == "Visualizations":
        main_category_options = ['Select All'] + list(df['main_category'].unique())
        selected_maincat = st.sidebar.selectbox("Select Category", main_category_options)

        # Handle selection logic for main category
        if selected_maincat == 'Select All':
            categorical_data = df  # Show all data if "Select All" is chosen
        else:
            # Proceed with filtering
            sub_category_options = ['Select All'] + list(df[df['main_category'] == selected_maincat]['sub_category'].unique())
            selected_subcat = st.sidebar.selectbox("Select Sub-Category", sub_category_options)
            
            # Handle selection logic for sub-category
            if selected_subcat == 'Select All':
                categorical_data = df[df['main_category'] == selected_maincat]  # Show all subcategories for selected main category
            else:
                categorical_data = df[(df['main_category'] == selected_maincat) & (df['sub_category'] == selected_subcat)]

     
        # Display the Visualizations title
        st.markdown("<h1 style='color: #000000;'>Data Visualizaztions</h1>", unsafe_allow_html=True)
        st.markdown("<p style='color: #000000;'>Here we will represent some inteactive charts to visualize data.</p>", unsafe_allow_html=True)
        
        #Rating charts
        st.markdown("<h3 style='color: #232F3E;'>Rating Distribution Analytics</h3>", unsafe_allow_html=True)
        fig5 =px.histogram(categorical_data,x='rating',histnorm='percent')
        st.plotly_chart(fig5)

        #Top 5 Selling items
        st.markdown("<h3 style='color: #232F3E;'>Best Seller Products</h3>", unsafe_allow_html=True)
        #Calculate items sales & top 5
        categorical_data['total_sales'] = categorical_data['discounted_price'] * categorical_data['rating_count'] #this assuming rating count is the number of sellings of an item
        best_seller = categorical_data.groupby('product_name')['total_sales'].sum().reset_index()
        best_seller=best_seller.sort_values(by='total_sales', ascending=False).head(5)
        fig6 = px.pie(best_seller,values='total_sales',names='product_name')
        fig6.update_layout(
            showlegend=False
        )
        st.plotly_chart(fig6)

        # Scatter Plot for Sales vs subcategory
        st.markdown("<h3 style='color: #232F3E;'>Sub Categories Sales</h3>", unsafe_allow_html=True)
        fig7 = px.scatter(categorical_data, x='discounted_price', y='sub_category', color='main_category', size='discounted_price')
        st.plotly_chart(fig7)


#         fig = px.pie(top_selling_items, values='total_sales', names='product_name', title="Top 10 Selling Items", 
#              color_discrete_sequence=px.colors.qualitative.Set3)

# # Show the pie chart in Streamlit
# st.plotly_chart(fig)

         



# st.markdown("Created by [Marah Deeb](https://www.linkedin.com/in/marah-deeb/)")
st.markdown(
    """
    <div style="position: fixed; bottom: 0; right: 0; text-align: right; width: 100%; padding: 10px;">
        Created by <a href="https://www.linkedin.com/in/marah-deeb/" target="_blank" style="text-decoration: none; color: #1E90FF;">Marah Deeb</a>
    </div>
    """,
    unsafe_allow_html=True
)