# Code adapted from https://panel.holoviz.org/tutorials/basic/build_dashboard.html
import hvplot.pandas
import pandas as pd
import panel as pn
from analyze import join_zillow_to_svi, MONTHS_COLUMNS
from scipy.stats import linregress
import holoviews as hv
import os
import numpy as np

pn.extension("tabulator")

ACCENT = "teal"

styles = {
    "box-shadow": "rgba(50, 50, 93, 0.25) 0px 6px 12px -2px, rgba(0, 0, 0, 0.3) 0px 3px 7px -3px",
    "border-radius": "4px",
    "padding": "10px",
}

# Extract Data


# @pn.cache()  # only download data once
# def get_data():
#     return pd.read_csv("https://assets.holoviz.org/panel/tutorials/turbines.csv.gz")


def make_file_path(filename):
    return os.path.join(os.path.dirname(__file__), f"../data/{filename}")


def get_data():
    joined_data = join_zillow_to_svi(
        zillow_path=make_file_path("zillow_new_home.csv"),
        svi_path=make_file_path("SVI_2022_US_county.csv"),
        zip_to_county_path=make_file_path("CountyCrossWalk_Zillow.csv"),
    )

    # Add up all the months columns into a sum
    joined_data[MONTHS_COLUMNS[0]] = joined_data[MONTHS_COLUMNS[1:]].sum(axis=1)
    return joined_data


source_data = get_data()


def custom_mean(x):
    return np.mean(x)


def custom_aggregation(group, date_window):
    return np.sum(group[date_window] / group["E_HU"])


DERIVED_FIELD = "Housing_Starts_Per_Existing_Units"


def filter_data(date_window):
    group_by_column = "RegionName"

    data = (
        source_data.loc[
            :, [group_by_column, "RPL_THEMES", "E_HU", date_window]
        ]  # E_HU is estimated housing units, M_HU is Margin of Error
        .groupby(group_by_column)
        .apply(
            lambda group: pd.Series(
                {
                    "SVI_INDEX": custom_mean(group["RPL_THEMES"]),
                    DERIVED_FIELD: custom_aggregation(group, date_window),
                }
            )
        )
    )
    # Ensure GroupColumn is set as the index
    # data.index.name = group_by_column
    return data


# Filters

date_window = pn.widgets.Select(
    name="Month",
    value=MONTHS_COLUMNS[0],  # Default All
    options=MONTHS_COLUMNS,
    description="Which month",
)

# Reactive data filter
df = pn.rx(filter_data)(date_window=date_window)
count = df.rx.len()
total_starts = df[DERIVED_FIELD].sum()
avg_starts = df[DERIVED_FIELD].mean()

# Plot Data
fig = df.hvplot.scatter(
    x="SVI_INDEX",
    y=DERIVED_FIELD,
    title="Housing Starts Per Existing Housing Units vs SVI",
    # rot=90,
    ylabel="Housing Starts",
    xlabel="SVI ranking",
    # xlim=(min_year, max_year),
    hover_cols=["SVI_INDEX", DERIVED_FIELD, "RegionName"],
    logy=True,
    color=ACCENT,
)

# x = df.loc[:, ["SVI_INDEX"]].values
# y = df.loc[:, [DERIVED_FIELD]].values

# # Calculating linear regression
# slope, intercept, r_value, p_value, std_err = linregress(x, y)
# regression_line = slope * x + intercept

# # Creating a linear regression line plot
# line_plot = hv.Curve((x, regression_line), "SVI_INDEX", DERIVED_FIELD).opts(color="red")

# # Combine the scatter plot and the regression line plot
# combined_plot = fig * line_plot

# # Adding R² value to the plot
# r_squared_text = hv.Text(
#     x.max(),
#     y.max(),
#     f"R² = {r_value**2:.2f}",
#     halign="right",
# )

# # Combine the plot and the text
# final_plot = combined_plot * r_squared_text

final_plot = fig

# final_plot = fig * hv.Slope.from_scatter(fig)

# final_plot.opts(
#     title="Scatter Plot with Linear Regression and R²",
#     xlabel="PercentileColumn1",
#     ylabel="PercentileColumn2",
#     height=400,
#     width=600,
# )

# Display Data

image = pn.pane.JPG("https://apps.hud.gov/images/fheo200.tif")

indicators = pn.FlexBox(
    pn.indicators.Number(
        value=count,
        name="Number of Geographic Regions",
        format="{value:,.0f}",
        styles=styles,
    ),
    pn.indicators.Number(
        value=total_starts,
        name="Total Housing Starts / hu",
        format="{value:,.1f}",
        styles=styles,
    ),
    pn.indicators.Number(
        value=avg_starts,
        name="Avg. House Starts / hu",
        format="{value:,.1f}",
        styles=styles,
    ),
)

plot = pn.pane.HoloViews(final_plot, sizing_mode="stretch_both", name="Plot")
table = pn.widgets.Tabulator(df, sizing_mode="stretch_both", name="Table")

# Layout Data

tabs = pn.Tabs(
    plot, table, styles=styles, sizing_mode="stretch_width", height=500, margin=10
)

pn.template.FastListTemplate(
    title="Zillow SVI Dashboard",
    sidebar=[image, date_window],
    main=[pn.Column(indicators, tabs, sizing_mode="stretch_both")],
    main_layout=None,
    accent=ACCENT,
).servable()
