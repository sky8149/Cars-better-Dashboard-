import altair as alt
import streamlit as st
from vega_datasets import data
import seaborn as sns
import matplotlib.pyplot as plt

# Loading the cars dataset
df = data.cars()

# List of quantitative data items
item_list = [
    col for col in df.columns if df[col].dtype in ['float64', 'int64']]

# List of Origins
origin_list = list(df['Origin'].unique())

# Create the column of YYYY 
df['YYYY'] = df['Year'].apply(lambda x: x.year)
min_year = df['YYYY'].min().item()
max_year = df['YYYY'].max().item()

st.set_page_config(layout="wide")

# Sidebar
st.sidebar.title("Dashboard of Cars Dataset")
st.sidebar.markdown('###')
st.sidebar.markdown("### *Settings*")
start_year, end_year = st.sidebar.slider(
    "Period",
    min_value=min_year, max_value=max_year,
    value=(min_year, max_year))

st.sidebar.markdown('###')
origins = st.sidebar.multiselect('Origins', origin_list,
                                 default=origin_list)
st.sidebar.markdown('###')
item1 = st.sidebar.selectbox('Item 1', item_list, index=0)
item2 = st.sidebar.selectbox('Item 2', item_list, index=3)

df_rng = df[(df['YYYY'] >= start_year) & (df['YYYY'] <= end_year)]
source = df_rng[df_rng['Origin'].isin(origins)]

# Content
base = alt.Chart(source).properties(height=300)

bar = base.mark_bar().encode(
    x=alt.X('count(Origin):Q', title='Number of Records'),
    y=alt.Y('Origin:N', title='Origin'),
    color=alt.Color('Origin:N', legend=None)
)

point = base.mark_circle(size=50).encode(
    x=alt.X(item1 + ':Q', title=item1),
    y=alt.Y(item2 + ':Q', title=item2),
    color=alt.Color('Origin:N', title='',
                    legend=alt.Legend(orient='bottom-left'))
)

line1 = base.mark_line(size=5).encode(
    x=alt.X('yearmonth(Year):T', title='Date'),
    y=alt.Y('mean(' + item1 + '):Q', title=item1),
    color=alt.Color('Origin:N', title='',
                    legend=alt.Legend(orient='bottom-left'))
)

line2 = base.mark_line(size=5).encode(
    x=alt.X('yearmonth(Year):T', title='Date'),
    y=alt.Y('mean(' + item2 + '):Q', title=item2),
    color=alt.Color('Origin:N', title='',
                    legend=alt.Legend(orient='bottom-left'))
)

# Layout (Content)
left_column, right_column = st.columns(2)

left_column.markdown(
    '**Number of Records (' + str(start_year) + '-' + str(end_year) + ')**')
left_column.altair_chart(bar, use_container_width=True)

right_column.markdown(
    '**Scatter Plot of _' + item1 + '_ and _' + item2 + '_**')
right_column.altair_chart(point, use_container_width=True)

left_column.markdown('**_' + item1 + '_ (Monthly Average)**')
left_column.altair_chart(line1, use_container_width=True)

right_column.markdown('**_' + item2 + '_ (Monthly Average)**')
right_column.altair_chart(line2, use_container_width=True)

#
interval = alt.selection_interval()

B = alt.Chart(df).mark_point().encode(
    x='Displacement',
    y='Horsepower',
    color=alt.condition(interval, 'Origin', alt.value('lightgray'))
).add_selection(
    interval
)

B

lines_origin = alt.Chart(df, title='Miles_per_Gallon vs. Year').mark_line(color='red').encode(
    x='Year',
    y=alt.Y('mean(Miles_per_Gallon)', title='MPG',
            scale=alt.Scale(zero=False)),
    color='Origin'
)

lines_origin



x = alt.Chart(source).mark_arc().encode(
    theta=alt.Theta(field="Origin", type="quantitative"),
    color=alt.Color(field="category", type="nominal"),
)
print(x)


u= sns.heatmap(df.corr(method='spearman'), annot = True, vmin = -1, vmax = 1, center = 0, cmap = 'coolwarm')
plt.show()
st.write(u)
fig,ax =plt.subplots()
sns.heatmap(df.corr(), ax=ax)
st.write(fig)

















