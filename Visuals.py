# This creates the page for users to input data.
# The collected data should be appended to the 'data.csv' file.

import streamlit as st
import json
import matplotlib.pyplot as plt
import pandas as pd
import altair as alt

# PAGE CONFIGURATION
st.set_page_config(
    page_title="Visuals",
    page_icon="📈",
)


st.title("Data Visualizations 📈")

with open("data.json", "r") as infile:
    CleanupData = json.load(infile)


labels = []
values = []

for item in CleanupData["data_points"]:
    labels.append(item["label"])
    values.append(item["value"])

fig, ax = plt.subplots()

ax.bar(labels, values)

ax.set_title(CleanupData["chart_title"])
ax.set_xlabel("Type of Waste")
ax.set_ylabel("Number of Items")

plt.xticks(rotation=30, ha="right")
plt.tight_layout()

st.pyplot(fig)


##INTERACTION

st.subheader("Explore Waste Categories")

##minimum number of items
min_items = st.slider(
    "Show categories with at least this many items:",
    min_value=0,
    max_value=max(values),
    value=min(10, max(values)),
    key="min_items"
)

#filter based on slider
filtered_labels = []
filtered_values = []

for i in range(len(values)):
    if values[i] >= st.session_state.min_items:
        filtered_labels.append(labels[i])
        filtered_values.append(values[i])

#show pie chart
if filtered_values and sum(filtered_values) > 0:
    fig2, ax2 = plt.subplots()

    ax2.pie(
        filtered_values,
        labels=filtered_labels,
        autopct="%1.1f%%",
        startangle=90
        )

    ax2.set_title("Waste Categories")
    st.pyplot(fig2)

else:
    st.info("No categories meet this threshold. Try lowering the slider.")

# PART 2: GRAPHS FROM data.csv
# --- YOUR CODE GOES HERE ---
csv_data = pd.read_csv("data.csv")

st.subheader("Beach Cleanup Survey Results")

st.dataframe(csv_data)

grouped_data = csv_data.groupby("Category", as_index=False)["Value"].sum()

#STATIC VISUALIZATION

st.divider()
st.subheader("Most Common Beach Cleanup Items 🌊")

if not grouped_data.empty:
    static_data = grouped_data.sort_values(
        "Value",
        ascending=False
    )

    if len(static_data) > 5:
        top_categories = static_data.head(5).copy()

        #Combine remaining categories into "Other"
        other_value = static_data.iloc[5:]["Value"].sum()

        other_row = pd.DataFrame({
            "Category": ["Other"],
            "Value": [other_value]
        })

        static_data = pd.concat(
            [top_categories, other_row],
            ignore_index=True
        )

    #Sort for the horizontal graph
    static_data = static_data.sort_values(
        "Value",
        ascending=True
    )

    #Create horizontal dot plot
    fig_static, ax_static = plt.subplots(
        figsize=(9, 4)
    )

    ax_static.scatter(
        static_data["Value"],
        static_data["Category"],
        s=100
    )

    #Add value labels
    for i in range(len(static_data)):

        ax_static.annotate(
            f'{static_data["Value"].iloc[i]:,.0f}',
            (
                static_data["Value"].iloc[i],
                static_data["Category"].iloc[i]
            ),
            xytext=(8, 0),
            textcoords="offset points",
            va="center"
        )

    ax_static.set_title(
        "Total Items Collected by Category"
    )

    ax_static.set_xlabel("Number of Items Collected")
    ax_static.set_ylabel("Trash Category")

    ax_static.grid(
        axis="x",
        linestyle="--",
        alpha=0.4
    )

    ax_static.set_xlim(
        0,
        max(1, static_data["Value"].max()) * 1.2
    )

    plt.tight_layout()
    st.pyplot(fig_static)

else:
    st.info("There is not enough data to create the static visualization yet.")


##DYNAMIC VISUALIZATION: Beach Cleanup Survey

st.divider()
st.subheader("Explore Our LOCAL Beach Cleanup Data 🌊")

if not grouped_data.empty:

    #Set the slider range
    max_value = max(1, int(grouped_data["Value"].max()))

    #let users filter categories
    min_value = st.slider(
        "Show categories with at least this many items:",
        min_value=0,
        max_value=max_value,
        value=0,
        key="csv_min_value"
    )

    #ise Session State to get the slider selection
    selected_minimum = st.session_state.csv_min_value

    #filter the data based on the slider
    filtered_data = grouped_data[
        grouped_data["Value"] >= selected_minimum
    ]

    #display the dynamic chart and extra credit metrics
    if not filtered_data.empty:

        #extra credittt - Calculate mean and median
        mean_value = filtered_data["Value"].mean()
        median_value = filtered_data["Value"].median()

        col1, col2 = st.columns(2)

        col1.metric("Mean", f"{mean_value:.2f}")
        col2.metric("Median", f"{median_value:.2f}")

        #the Altair bar chart
        chart = alt.Chart(filtered_data).mark_bar().encode(
            x=alt.X("Category:N", title="Trash Category", sort="-y"),
            y=alt.Y("Value:Q", title="Total Number of Items"),
            color=alt.Color("Category:N", legend=None),
            tooltip=["Category", "Value"]
        ).properties(
            title="Total Trash Collected by Category"
        )

        #display the chart
        st.altair_chart(chart, use_container_width=True)

    else:
        st.info("No categories meet this threshold. Try lowering the slider.")

else:
    st.info("Submit some survey responses to create the dynamic visualization.")