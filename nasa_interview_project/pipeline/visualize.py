# Code adapted from https://panel.holoviz.org/tutorials/basic/build_dashboard.html
import hvplot.pandas
import pandas as pd
import panel as pn
from analyze import join_zillow_to_svi
import os
import numpy as np

pn.extension("tabulator")

ACCENT = "teal"

styles = {
    "box-shadow": "rgba(50, 50, 93, 0.25) 0px 6px 12px -2px, rgba(0, 0, 0, 0.3) 0px 3px 7px -3px",
    "border-radius": "4px",
    "padding": "10px",
}
MONTHS_COLUMNS = [
    "All_Months_Sum",  # This is a new column
    "2018-01-31",
    "2018-02-28",
    "2018-03-31",
    "2018-04-30",
    "2018-05-31",
    "2018-06-30",
    "2018-07-31",
    "2018-08-31",
    "2018-09-30",
    "2018-10-31",
    "2018-11-30",
    "2018-12-31",
    "2019-01-31",
    "2019-02-28",
    "2019-03-31",
    "2019-04-30",
    "2019-05-31",
    "2019-06-30",
    "2019-07-31",
    "2019-08-31",
    "2019-09-30",
    "2019-10-31",
    "2019-11-30",
    "2019-12-31",
    "2020-01-31",
    "2020-02-29",
    "2020-03-31",
    "2020-04-30",
    "2020-05-31",
    "2020-06-30",
    "2020-07-31",
    "2020-08-31",
    "2020-09-30",
    "2020-10-31",
    "2020-11-30",
    "2020-12-31",
    "2021-01-31",
    "2021-02-28",
    "2021-03-31",
    "2021-04-30",
    "2021-05-31",
    "2021-06-30",
    "2021-07-31",
    "2021-08-31",
    "2021-09-30",
    "2021-10-31",
    "2021-11-30",
    "2021-12-31",
    "2022-01-31",
    "2022-02-28",
    "2022-03-31",
    "2022-04-30",
    "2022-05-31",
    "2022-06-30",
    "2022-07-31",
    "2022-08-31",
    "2022-09-30",
    "2022-10-31",
    "2022-11-30",
    "2022-12-31",
    "2023-01-31",
    "2023-02-28",
    "2023-03-31",
    "2023-04-30",
    "2023-05-31",
    "2023-06-30",
    "2023-07-31",
    "2023-08-31",
    "2023-09-30",
    "2023-10-31",
    "2023-11-30",
    "2023-12-31",
    "2024-01-31",
    "2024-02-29",
    "2024-03-31",
    "2024-04-30",
]

# Extract Data


# @pn.cache()  # only download data once
# def get_data():
#     return pd.read_csv("https://assets.holoviz.org/panel/tutorials/turbines.csv.gz")


def make_file_path(filename):
    return os.path.join(os.path.dirname(__file__), f"../data/{filename}")


def get_data():
    return join_zillow_to_svi(
        zillow_path=make_file_path("zillow_new_home.csv"),
        svi_path=make_file_path("SVI_2022_US_county.csv"),
        zip_to_county_path=make_file_path("CountyCrossWalk_Zillow.csv"),
    )


source_data = get_data()

# Transform Data

# min_year = int(source_data["p_year"].min())
# max_year = int(source_data["p_year"].max())
# top_manufacturers = (
#     source_data.groupby("t_manu").p_cap.sum().sort_values().iloc[-10:].index.to_list()
# )


def custom_median(x):
    return np.median(x)


def custom_aggregation(group, t_month):
    return np.sum(group[t_month] / group["E_HU"])


DERIVED_FIELD = "Housing_Starts_Per_Existing_Units"


def filter_data(t_month):
    group_by_column = "RegionName"
    source_data[MONTHS_COLUMNS[0]] = source_data[MONTHS_COLUMNS[1:]].sum(axis=1)
    data = (
        source_data.loc[
            :, [group_by_column, "RPL_THEMES", "E_HU", t_month]
        ]  # E_HU is estimated housing units, M_HU is Margin of Error
        .groupby(group_by_column)
        .apply(
            lambda group: pd.Series(
                {
                    "RPL_THEMES": custom_median(group["RPL_THEMES"]),
                    DERIVED_FIELD: custom_aggregation(group, t_month),
                }
            )
        )
    )
    # Ensure GroupColumn is set as the index
    data.index.name = group_by_column
    # data = (
    #     source_data.loc[:, ["RegionName", t_month, "RPL_THEMES"]]
    #     .groupby("RegionName")
    #     .median()
    # )
    return data


# Filters

t_month = pn.widgets.Select(
    name="Month",
    value=MONTHS_COLUMNS[0],
    options=MONTHS_COLUMNS,
    description="The name of the manufacturer",
)
# p_year = pn.widgets.IntSlider(name="Year", value=max_year, start=min_year, end=max_year)

# Transform Data 2

df = pn.rx(filter_data)(t_month=t_month)
count = df.rx.len()
total_capacity = df[DERIVED_FIELD].sum()
avg_capacity = df[DERIVED_FIELD].mean()
avg_rotor_diameter = df[DERIVED_FIELD].mean()

# Plot Data

fig = df.hvplot.scatter(
    x="RPL_THEMES",
    y=DERIVED_FIELD,
    title="Housing Starts",
    rot=90,
    ylabel="Housing Starts",
    xlabel="SVI ranking",
    # xlim=(min_year, max_year),
    logy=True,
    color=ACCENT,
)

# fig * hv.Slope.from_scatter(normal)
# fig = df.hvplot.hist(
#     DERIVED_FIELD,
#     xlabel="Aggregate median SVI ranking",
#     logy=False,
#     # bins=1000,
#     # ylim=(0, 50),
# )

# Display Data

image = pn.pane.JPG(
    "https://assets.holoviz.org/panel/tutorials/wind_turbines_sunset.png"
)

indicators = pn.FlexBox(
    pn.indicators.Number(
        value=count, name="Count", format="{value:,.0f}", styles=styles
    ),
    pn.indicators.Number(
        value=total_capacity / 1e6,
        name="Total Capacity (TW)",
        format="{value:,.1f}",
        styles=styles,
    ),
    pn.indicators.Number(
        value=avg_capacity / 1e3,
        name="Avg. Capacity (MW)",
        format="{value:,.1f}",
        styles=styles,
    ),
    pn.indicators.Number(
        value=avg_rotor_diameter,
        name="Avg. Rotor Diameter (m)",
        format="{value:,.1f}",
        styles=styles,
    ),
)

plot = pn.pane.HoloViews(fig, sizing_mode="stretch_both", name="Plot")
table = pn.widgets.Tabulator(df, sizing_mode="stretch_both", name="Table")

# Layout Data

tabs = pn.Tabs(
    plot, table, styles=styles, sizing_mode="stretch_width", height=500, margin=10
)

pn.template.FastListTemplate(
    title="Zillow SVI Dashboard",
    sidebar=[image, t_month],  # , p_year],
    main=[pn.Column(indicators, tabs, sizing_mode="stretch_both")],
    main_layout=None,
    accent=ACCENT,
).servable()
