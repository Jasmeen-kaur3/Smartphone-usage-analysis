import streamlit as st
import pandas as pd
import plotly_express as px
from streamlit_option_menu import option_menu
import sqlite3

import streamlit as st

def local_css():
    st.markdown("""
    <style>

    /* Full App Background */
    .stApp {
        background: linear-gradient(to right, #141e30, #243b55);
        color: white;
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background: linear-gradient(to bottom, #000000, #434343);
        color: white;
    }

    /* Headings */
    h1, h2, h3 {
        color: #00FFD1;
        font-family: Arial;
    }

    /* Text */
    p {
        color: #F5F5F5;
        font-size: 18px;
    }

    /* Buttons */
    .stButton>button {
        background-color: #00FFD1;
        color: black;
        border-radius: 10px;
        height: 45px;
        width: 200px;
        font-size: 18px;
        border: none;
    }

    .stButton>button:hover {
        background-color: #00bfa6;
        color: white;
    }

    </style>
    """, unsafe_allow_html=True)
local_css()    

st.set_page_config(layout="wide",page_title="My project",page_icon="📞")
st.title("Smartphone Usage Analysis")
st.sidebar.title("OPTIONS.")
section = st.sidebar.selectbox("Go to", ["Introduction","FORM","DATASET","2D Graphs Visualization","3D Graph Representation","System","Conclusion"])


# with st.sidebar:
#    option=option_menu("Menu",["INTRO","FORM","DATASET","VISUALIZATION","CONCLUSION"],icons=["house","form","table","graph-up","info-circle"])

def get_connection():
       return sqlite3.connect("project.db")
    
conn = get_connection()
cursor = conn.cursor()
cursor.execute("drop table if exists userdata")
# Table create
cursor.execute("""
    CREATE TABLE IF NOT EXISTS userdata(
    USER_ID INTEGER  PRIMARY KEY  AUTOINCREMENT,               
    Age INTEGER,
    Gender TEXT,
    Occupation TEXT,
    Device_Type TEXT,
    Daily_Phone_Hours REAL,
    Social_Media_Hours REAL,
    Work_Productivity_Score REAL,
    Sleep_Hours REAL,
    Stress_level REAL,
    App_Usage_Count INTEGER,
    Caffeine_Intake_Cups INTEGER,
    Weekend_Screen_Time_Hours REAL
   )
   """)
conn.commit()

if section=="Introduction":
    st.header("INTRODUCTION ABOUT PROJECT📞")
    st.write("This project is about analyzing the impact of smartphone usage on productivity and well-being. The dataset contains information about users' smartphone habits, including daily phone hours, social media usage, work productivity scores, sleep hours, stress levels, app usage count, caffeine intake, and weekend screen time hours. By analyzing this data, we aim to understand how smartphone usage affects various aspects of users' lives and identify potential correlations between these factors.")


elif section=="FORM":
    st.header("LOGIN..")
    user=st.text_input("Username:")
    email=st.text_input("Email:")
    security=st.text_input("Password:",type="password")
    st.button("Done")
    if st.button=="Done":
     st.header("REGISTRATION FORM")
     conn=sqlite3.connect("project.db")
     cursor=conn.cursor()
#st.title("Add New Data")
    
     age = st.number_input("Age", min_value=0)
     gen = st.selectbox("Gender", ["Male","Female","Other"])
     occupation = st.text_input("occupation")
     dev = st.selectbox("Device_Type", ["Android","iOS"])
     daily = st.number_input("Daily Phone Hours")
     soc = st.number_input("Social Media Hours")
     work = st.number_input("Work Productivity Score")
     sleep = st.number_input("Sleep Hours")
     stress = st.number_input("Stress Level")
     ap = st.number_input("App Usage Count")
     ca = st.number_input("Caffeine Intake Cups")
     we = st.number_input("Weekend Screen Time Hours")
   
    if st.button("Add Data"):
        if occupation:
            cursor.execute("""
       INSERT INTO userdata (Age, Gender, Occupation, Device_Type, Daily_Phone_Hours, Social_Media_Hours, Work_Productivity_Score, Sleep_Hours, Stress_level, App_Usage_Count, Caffeine_Intake_Cups, Weekend_Screen_Time_Hours) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)
       """,(age,gen,occupation,dev,daily,soc,work,sleep,stress,ap,ca,we))
    conn.commit()
    st.success("Data added successfully!")
    #sirf latest data show karna hai
    st.subheader("your recent submission:")
    query="SELECT * FROM userdata ORDER BY rowid DESC LIMIT 1"
    new_data=pd.read_sql_query(query,conn)
    st.dataframe(new_data,use_container_width=True)
    #    latest_data=pd.read_sql_query("SELECT * FROM userdata ORDER BY USER_ID DESC LIMIT 1 ",conn)
    #    st.dataframe(latest_data,use_container_width=True)

    
    
conn.close()     
# data = pd.read_sql_query("SELECT * FROM userdata ORDER BY USER_ID DESC LIMIT 1 ",conn)
# st.dataframe(data,use_container_width=True)

#ml use here
elif section=="DATASET":
    # st.subheader("About Dataset")
    try:
        df=pd.read_csv("Smartphone_Usage_Productivity_Dataset_50000.csv") 
        col1,col2=st.columns([2,1])   

        with col1:
            st.dataframe(df)
            st.write(f"TOTAL ROWS:{df.shape[0]} | Columns: {df.shape[1]}")
        with col2: 
            st.markdown("DATASET DESCRIPTION")
            st.subheader("COLUMNS:")        
            st.write(df.columns.tolist())
            column=st.selectbox("Select a column to filter", df.columns)
            value=st.selectbox("Select a value to filter", df[column].unique())
            filtered_data=df[df[column]==value]
            st.dataframe(filtered_data)
    except FileNotFoundError:
        st.error("CSV FILE NHI MILI.PLEASE CHECK THE FILE PATH AND NAME.")  
        conn.close()           

elif section=="2D Graphs Visualization":
      st.set_page_config(layout="wide",page_title="Multiple Graphs")
      st.header("Here we are representing some 2 dimentional graphs based on our dataset .")
      df=pd.read_csv('Smartphone_Usage_Productivity_Dataset_50000.csv')
        
      st.subheader("1. Phone Usage by Device Type")
      st.write("This bar chart represents the average daily phone usage based on device type. "
            "It helps in analyzing whether Android or iOS users spend more time on their phones.")

      fig3 = px.bar(df, x="Device_Type", y="Daily_Phone_Hours", color="Device_Type")
      st.plotly_chart(fig3, use_container_width=True)

      st.subheader("2. Phone Usage Distribution by Gender")
      st.write("This box plot shows the distribution of daily phone usage for each gender. "
            "It helps in understanding the spread, median, and presence of outliers "
            "in smartphone usage between males and females.")

      fig6 = px.box(df, x="Gender", y="Daily_Phone_Hours", color="Gender")
      st.plotly_chart(fig6, use_container_width=True)

      st.subheader("3. Average Productivity vs Phone Usage")
      st.write("This line chart shows the trend of average productivity with respect to daily phone usage. "
            "It helps in understanding how productivity changes as phone usage increases.")

      avg_data = df.groupby("Daily_Phone_Hours", as_index=False)["Work_Productivity_Score"].mean()

      fig9 = px.line(avg_data, x="Daily_Phone_Hours", y="Work_Productivity_Score", markers=True)
      st.plotly_chart(fig9, use_container_width=True)

      st.subheader("4. Phone Usage vs Productivity")
      st.write("This scatter plot shows the relationship between daily phone usage and productivity. "
            "It helps in identifying whether increased phone usage leads to lower productivity, "
            "highlighting a possible negative correlation between the two variables.")

      fig1 = px.scatter(df, x="Daily_Phone_Hours", y="Work_Productivity_Score", color="Occupation")
      st.plotly_chart(fig1, use_container_width=True)

      st.subheader("Stress Level Distribution")

    # Group stress levels
      df["Stress_Category"] = df["Stress_Level"].apply(
        lambda x: "Low" if x <= 3 else ("Medium" if x <= 6 else "High")
     )

    # Pie chart
      fig = px.pie(df, names="Stress_Category", title="Stress Level Distribution")

      st.plotly_chart(fig, use_container_width=True)

elif section=="3D Graph Representation":
    st.set_page_config(layout="wide",page_title="3D Graphs")
    data=pd.read_csv("Smartphone_Usage_Productivity_Dataset_50000.csv")
    st.dataframe(data)
    st.header("Here we are representing some 3 dimensional graphs based on our dataset .")
    st.header("1) 3D scatter plot")
    fig=px.scatter_3d(data.head(50),
               x='Age',y='Daily_Phone_Hours',
               z='Work_Productivity_Score',
               color='Occupation')
    st.plotly_chart(fig)
    st.markdown("x-axis:AGE,y-axis:DAILY PHONE HOURS,z-axis:WORK PRODUCTIVITY SCORE")
    st.write("This graph suggests that excessive phone usage may be associated with lower productivity,especially among younger users and certain occupations, but the effect is nit exactly the same for everyone.")
    st.header("-------------------------------------------------------------")
#2ND GRAPH
    st.header("2) Line graph")

    fig1=px.line_3d(data.head(50),x='Work_Productivity_Score',y='Sleep_Hours',z='Stress_Level',color='Occupation')
    st.plotly_chart(fig1)
    st.markdown("x-axis:WORK PRODUCTIVITY SCORE,y-axis:SLEEP HOURS,z-axis:STRESS LEVEL")
    st.write("This graph indicates that higher productivity scores are often associated with more sleep hours and lower stress levels, particularly for certain occupations, suggesting that good sleep and low stress may contribute to better productivity.")
    st.header("-------------------------------------------------------------")
#3rd graph
# st.write("bar graph")
# fig2=px.surface(data.head(50),x='Daily_Phone_Hours',y='Social_Media_Hours',z='Work_Productivity_Score',color='Occupation')
# st.plotly_chart(fig2)
    # st.header("3) Mesh plot")
    # fig3=go.Figure(data=[go.Mesh3d(x=data['Daily_Phone_Hours'],y=data['Social_Media_Hours'],z=data['Work_Productivity_Score'])])
    # st.plotly_chart(fig3)
    # st.markdown("x-axis:DAILY PHONE HOURS,y-axis:SOCIAL MEDIA HOURS,z-axis:WORK PRODUCTIVITY SCORE")
    # st.write("This graph suggests that higher phone and social media usage may be associated with lower productivity scores, indicating a potential negative impact of excessive screen time on work performance.")
    # st.header("-------------------------------------------------------------")
#4th graph
    st.header("3) Piechart")
    fig4=px.pie(data.head(50),values='Daily_Phone_Hours',names='Weekend_Screen_Time_Hours')
    st.plotly_chart(fig4)
    st.write("This pie chart illustrates the distribution of daily phone hours based on weekend screen time hours, showing how different levels of weekend screen time contribute to overall phone usage.")
    st.header("-------------------------------------------------------------")
#5th graph
    st.header("4) Bar chart")
    fig5=px.bar(data.head(50),x='Occupation',y='Age',color='Device_Type')
    st.plotly_chart(fig5)
    st.markdown("x-axis:OCCUPATION,y-axis:AGE,color:DEVICE TYPE")
    st.write("This graph indicates that certain occupations may have a higher average age of users, and that device type usage may vary across different occupations, suggesting potential demographic trends in smartphone usage.")
    st.header("-------------------------------------------------------------")
#6th graph
    st.header("5) Bubble chart")
    fig6=px.scatter(data.tail(50),x='Sleep_Hours',y='Stress_Level',size='Work_Productivity_Score',hover_name='Caffeine_Intake_Cups')
    st.plotly_chart(fig6)
    st.markdown("x-axis:SLEEP HOURS,y-axis:STRESS LEVEL,size:WORK PRODUCTIVITY SCORE,hover:Caffeine Intake Cups")
    st.write("This graph suggests that individuals with more sleep hours tend to have lower stress levels,  and that higher productivity scores are often associated with lower stress, while caffeine intake may also play a role in this relationship.")
    st.header("-------------------------------------------------------------")
#7th graph
    st.header("6) Heatmap")
    import plotly.graph_objects as go

    fig7 = go.Figure(data=go.Heatmap(
    z=data.values,  # 2D array of values
    x=data.columns,  # X-axis labels
    y=data.index,    # Y-axis labels
    autocolorscale=True
    ))
    st.plotly_chart(fig7)
    st.write("This heatmap provides a visual representation of the dataset, allowing for the identification of patterns and correlations between different variables based on color intensity.")
    st.write("This graph helps in identifying patterns and correlations between different variables in the dataset, with color intensity indicating the strength of relationships, making it easier to spot trends and outliers.")  

elif section=="System":
    st.header("SMARTPHONE USAGE RECOMMENDATION SYSTEM")
    screen_time=st.text_input("Enter your screening hours...")
    screen_time=float(screen_time)
    social_media=st.text_input("Enter your social media hours...")
    social_media=float(social_media)                   
    sleep_hours=st.text_input("Enter your sleep hours...")
    sleep_hours=float(sleep_hours)
    stress_level=st.text_input("Enter your stress level...")
    stress_level=float(stress_level)
    
    def get_recommend(screen_time,social_media,sleep_hours,stress_level):
        if screen_time>5 and social_media>3 and sleep_hours<6 and stress_level>7:
            st.write("Your smartphone usage is excessive. Consider reducing screen time, especially on social media, and prioritize getting more sleep to improve your well-being.")
        elif screen_time>3 and social_media>2 and sleep_hours<7 and stress_level>5:
            st.write("Your smartphone usage is moderate. Try to limit screen time, especially on social media, and ensure you get enough sleep to maintain a healthy balance.")
        else:
            st.write("Your smartphone usage is within a reasonable range. Keep up the good habits of managing screen time, limiting social media use, and prioritizing sleep for overall well-being.")
    get_recommend(screen_time,social_media,sleep_hours,stress_level)
elif section=="Conclusion":
  st.write("The above data analysis brings out the substantial influence of smartphone use on productivity and general way of life. " 
    "From the results, we see that too much use of a cell phone in one day correlates with decreased productivity levels, high levels of stress, and poor quality of sleep. " 
    "People who use their smartphones for long periods of time and even more when it comes to social media have high-stress levels and low productivity."
    "Nonetheless, it seems like reasonable smartphone use can promote good balance enabling users to stay productive while being active at the same time. " 
    "This data analysis confirms that certain things like occupation can significantly affect the effects of smartphone use on people."
    "In conclusion, we should remember about the crucial significance of careful smartphone use.")
    st.markdown("""
    <div style=""text-align:center;font-size:14 px; color:gray;">
            Developed on the purpose to limit the usage of smartphone <br>
            powered by Streamlit<br>
            For feedback or more information contact: <a href='mailto:example@email.com'>jasmeenghuman189@gmail.com</a>
            </div>""",unsafe_allow_html=True)
else: 
 st.Warning("Sorry, this section is under construction. Please check back later.")




