from plotly import graph_objects as go
import pandas as pd

# Get one year of gapminder data
url = 'https://raw.githubusercontent.com/plotly/datasets/master/gapminderDataFiveYear.csv'
df = pd.read_csv(url)
df = df[df['year']==2007]
df["gdp"]=df["pop"]*df['gdpPercap']


# Build the summary of interest
df_summarized = df.groupby("continent", observed=True).agg("sum").reset_index()

df_summarized["percent of world population"]=100*df_summarized["pop"]/df_summarized["pop"].sum()
df_summarized["percent of world GDP"]=100*df_summarized["gdp"]/df_summarized["gdp"].sum()


df = df_summarized[["continent",
"percent of world population",
"percent of world GDP",
]]

# We now have a wide data frame, but it's in the opposite orientation from the one that px is designed to deal with.
# Transposing it and rebuilding the indexes is an option, but iterating through the DF using graph objects is more succinct.
print(df.continent)

fig=go.Figure()
for category in df_summarized["continent"].values:
    print(category)
    fig.add_trace(go.Bar(
            x=df.columns[1:],
            # We need to get a pandas series that contains just the values to graph;
            # We do so by selecting the right row, selecting the right columns
            # and then transposing and using iloc to convert to a series
            # Here, we assume that the bar element category variable is in column 0
            y=list(df.loc[df["continent"]==category][list(df.columns[1:])].transpose().iloc[:,0]),
            name=str(category)


        )
)
fig.update_layout(barmode="stack")

#fig.show()