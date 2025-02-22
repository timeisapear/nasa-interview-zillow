# Code adapted from https://panel.holoviz.org/tutorials/basic/build_dashboard.html, permitted under LICENSE:
# https://github.com/holoviz/holoviz/blob/main/LICENSE.txt
import hvplot.pandas
import pandas as pd
import panel as pn
from analyze import join_zillow_to_svi, MONTHS_COLUMNS
from scipy.stats import linregress
import holoviews as hv
import numpy as np
from pipeline.helpers import make_file_path, MONTHS_COLUMNS, HSTARTS_COL_NAME
from pipeline.analyze import filter_data_on_dashboard

pn.extension("tabulator")

ACCENT = "teal"

styles = {
    "box-shadow": "rgba(50, 50, 93, 0.25) 0px 6px 12px -2px, rgba(0, 0, 0, 0.3) 0px 3px 7px -3px",
    "border-radius": "4px",
    "padding": "10px",
}


# Extract Data
def get_data():
    joined_data = pd.read_csv(make_file_path("joined_zillow_svi.csv"))
    return joined_data


source_data = get_data()

# Filters

date_window = pn.widgets.Select(
    name="Month",
    value=MONTHS_COLUMNS[0],  # Default All
    options=MONTHS_COLUMNS,
    description="Which month",
)

# Reactive data filter
df = pn.rx(filter_data_on_dashboard)(date_window=date_window, source_data=source_data)
count = df.rx.len()
total_starts = df[HSTARTS_COL_NAME].sum()
avg_starts = df[HSTARTS_COL_NAME].mean()

# Plot Data
fig = df.hvplot.scatter(
    x="SVI_INDEX",
    y=HSTARTS_COL_NAME,
    title="New Construction Sold Per Existing Housing Units vs SVI",
    ylabel="New Construction Sold",
    xlabel="SVI ranking",
    ylim=(0, None),
    hover_cols=["SVI_INDEX", HSTARTS_COL_NAME, "RegionName"],
    logy=True,
    color=ACCENT,
)

final_plot = fig

# Display Data
image = pn.pane.JPG("https://apps.hud.gov/images/fheo200.tif")

indicators = pn.FlexBox(
    pn.indicators.Number(
        value=count,
        name="Geographic Regions",
        format="{value:,.0f}",
        styles=styles,
    ),
    pn.indicators.Number(
        value=total_starts,
        name="Sum House Starts / hu",
        format="{value:,.1f}",
        styles=styles,
    ),
    pn.indicators.Number(
        value=avg_starts,
        name="Avg. House Starts / hu",
        format="{value:,.5f}",
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
