import streamlit as st
import pandas as pd
import seaborn as sn
import matplotlib.pyplot as plt

df = pd.read_csv("airlines_flights_data.csv")

plt.style.use("dark_background")
sn.set_theme(style="darkgrid", palette="pastel")

def plot_chart(plot_func, **kwargs):
    fig, ax = plt.subplots()
    fig.patch.set_facecolor("black")
    ax.set_facecolor("black")
    plot_func(ax=ax, **kwargs)
    ax.tick_params(colors='white')
    ax.set_xlabel(ax.get_xlabel(), color='white')
    ax.set_ylabel(ax.get_ylabel(), color='white')
    plt.xticks(rotation=45, color='white')
    return fig

st.sidebar.header("Route Selector")
routes = df.groupby(["source_city", "destination_city"]).size().reset_index(name='count')
routes["route_name"] = routes["source_city"] + " → " + routes["destination_city"]

selected_route = st.sidebar.selectbox(
    "Choose Source → Destination",
    options=routes["route_name"].unique()
)


src, dest = selected_route.split(" → ")
df_filtered = df[(df["source_city"] == src) & (df["destination_city"] == dest)]

st.markdown(f"""
<center><h1 style='color:white;'>Airlines Flights Insights: {selected_route}</h1></center>
""", unsafe_allow_html=True)


col1, col2 = st.columns(2)

with col1:
        st.subheader("distribution of airlines")
        st.pyplot(plot_chart(sn.histplot, data=df_filtered, x='airline', discrete=True))
        

with col2:
        st.subheader("departure vs arrival with stops")
    
        st.pyplot(plot_chart(sn.violinplot, data=df_filtered, x='departure_time',y='arrival_time',hue='stops'))
        
  
col3, col4 = st.columns(2)
with col3:
        st.subheader("airline vs prices")
    
        st.pyplot(plot_chart(sn.lineplot, data=df_filtered, x='airline',y='price'))
       

with col4:
    st.subheader("No.of flights")
    top_10 = df_filtered['flight'].value_counts().head(10)
    st.pyplot(plot_chart(sn.barplot, x=top_10.index, y=top_10.values))

col5, col6 = st.columns(2)
with col5:
    st.subheader("count of departure_time")
    st.pyplot(plot_chart(sn.histplot, data=df_filtered, x='departure_time'))
with col6:
    st.subheader("count of arrival_time")
    st.pyplot(plot_chart(sn.histplot, data=df_filtered, x='arrival_time'))
col7,col8=st.columns(2)
with col7:
     st.subheader("count of stops")
     st.pyplot(plot_chart(sn.histplot,data=df_filtered,x='stops'))   
with col8:

    st.subheader("stops vs duration")
    st.pyplot(plot_chart(sn.lineplot,data=df_filtered,x='stops',y='duration'))    
col9,col10=st.columns(2)
with col9:
     st.subheader("Types of class") 
     st.pyplot(plot_chart(sn.histplot,data=df_filtered,x='class'))



with st.expander("Count of Airlines"):
    st.write(df_filtered['airline'].value_counts())

with st.expander("Count of Flights"):
    st.write(df_filtered['flight'].value_counts())

with st.expander("Full Route Data"):
    st.write(df_filtered)
with st.expander("count of departure_time"):
     st.write(df_filtered['departure_time'].value_counts()) 
with st.expander("count of arrival_time"):
     st.write(df_filtered['arrival_time'].value_counts()) 
with st.expander("count of stops"):
     st.write(df_filtered['stops'].value_counts())   
with st.expander("count of class"):
     st.write(df_filtered['class'].value_counts())  
                       
