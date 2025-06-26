import dash
from dash import html, dcc, callback, Input, Output
import pandas as pd
import plotly.express as px
from components.navbar import get_navbar

# Register page
dash.register_page(__name__, path="/customer", name="Customer Info")

# Load and preprocess data
df = pd.read_csv("dataset/Bank_Churn.csv")
df.rename(columns={"Exited": "Churn"}, inplace=True)
df["Stayed"] = 1 - df["Churn"]

# Age Grouping
bins = [0, 25, 35, 45, 55, 65, 100]
labels = ["<25", "25-35", "35-45", "45-55", "55-65", "65+"]
df["AgeGroup"] = pd.cut(df["Age"], bins=bins, labels=labels)

# Salary Category
def salary_category(salary):
    if salary < 50000:
        return "<50K"
    elif salary < 100000:
        return "50K-100K"
    elif salary < 150000:
        return "100K-150K"
    else:
        return "150K+"
    
df["SalaryCategory"] = df["EstimatedSalary"].apply(salary_category)

# Tenure Category
def tenure_category(tenure):
    if tenure < 3:
        return "0-2"
    elif tenure < 6:
        return "3-5"
    elif tenure < 9:
        return "6-8"
    else:
        return "9+"
df["TenureCategory"] = df["Tenure"].apply(tenure_category)

layout = html.Div([
    get_navbar(),
    html.Div(className="container-fluid", children=[
        html.H2("Customer Information", className="text-center my-4", style={"color": "#023047"}),

        # KPI Cards
        html.Div(id="kpi-cards", className="row text-center my-4", children=[
            html.Div(className="col-md-3 mb-3", children=[
                html.Div(className="card bg-light shadow", children=[
                    html.Div(className="card-body", children=[
                        html.H5("Total Customers", className="card-title", style={"color": "#023047"}),
                        html.P(f"{len(df):,}", className="card-text display-6", style={"color": "#023047"}),
                        html.P(
                            f"Active: {round((df['IsActiveMember'].sum() / len(df)) * 100, 2)}% | "
                            f"Inactive: {round(((len(df) - df['IsActiveMember'].sum()) / len(df)) * 100, 2)}%",
                            className="small",
                            style={"color": "#023047", "font-weight": "bold"}
                        )
                    ])
                ])
            ]),
            html.Div(className="col-md-3 mb-3", children=[
                html.Div(className="card bg-light shadow", children=[
                    html.Div(className="card-body", children=[
                        html.H5("Total Churn", className="card-title", style={"color": "#023047"}),
                        html.P(f"{df['Churn'].sum():,}", className="card-text display-6", style={"color": "#023047"}),
                        html.P(
                            f"Churn: {round((df['Churn'].mean()) * 100, 2)}% | "
                            f"Stayed: {round((df['Stayed'].mean()) * 100, 2)}%",
                            className="small",
                            style={"color": "#023047", "font-weight": "bold"}
                        )
                    ])
                ])
            ]),
            html.Div(className="col-md-3 mb-3", children=[
                html.Div(className="card bg-light shadow", children=[
                    html.Div(className="card-body", children=[
                        html.H5("Avg Salary", className="card-title", style={"color": "#023047"}),
                        html.P(f"€{df['EstimatedSalary'].mean():,.2f}", className="card-text display-6", style={"color": "#023047"}),
                        html.P(
                            f"Churn: {round((df[df['Churn'] == 1]['EstimatedSalary'].sum() / df['EstimatedSalary'].sum()) * 100, 2)}% | "
                            f"Stayed: {round((df[df['Churn'] == 0]['EstimatedSalary'].sum() / df['EstimatedSalary'].sum()) * 100, 2)}%",
                            className="small",
                            style={"color": "#023047", "font-weight": "bold"}
                        )
                    ])
                ])
            ]),
            html.Div(className="col-md-3 mb-3", children=[
                html.Div(className="card bg-light shadow", children=[
                    html.Div(className="card-body", children=[
                        html.H5("Avg Tenure", className="card-title", style={"color": "#023047"}),
                        html.P(f"{df['Tenure'].mean():.2f} yrs", className="card-text display-6", style={"color": "#023047"}),
                        html.P(
                            f"Active: {df[df['IsActiveMember'] == 1]['Tenure'].mean():.2f} yrs | "
                            f"Inactive: {df[df['IsActiveMember'] == 0]['Tenure'].mean():.2f} yrs",
                            className="small",
                            style={"color": "#023047", "font-weight": "bold"}
                        )
                    ])
                ])
            ])
        ]),

        html.Div(className="row mb-4 justify-content-center", children=[
            html.Div(className="col-md-2", children=[
                dcc.Dropdown(
                    id="geo-filter",
                    options=[{"label": g, "value": g} for g in df["Geography"].unique()],
                    placeholder="Select Geography"
                )
            ]),
            html.Div(className="col-md-2", children=[
                dcc.Dropdown(
                    id="gender-filter",
                    options=[{"label": g, "value": g} for g in df["Gender"].unique()],
                    placeholder="Select Gender"
                )
            ]),
            html.Div(className="col-md-2", children=[
                dcc.Dropdown(
                    id="tenure-filter",
                    options=[{"label": t, "value": t} for t in df["TenureCategory"].unique()],
                    placeholder="Select Tenure"
                )
            ]),
            html.Div(className="col-md-2", children=[
                dcc.Dropdown(
                    id="salary-filter",
                    options=[{"label": s, "value": s} for s in df["SalaryCategory"].unique()],
                    placeholder="Select Salary"
                )
            ]),
            html.Div(className="col-md-2", children=[
                html.Button("Reset Filters", id="reset-btn", className="btn w-100", style={"background-color": "#023047", "color": "#ffffff"})
            ])
        ]),

        html.Div(className="row", children=[
            html.Div(className="col-md-6 mb-4", children=[
                html.Div(className="p-2 border rounded shadow-sm bg-white", children=[
                    dcc.Graph(id="chart-salary-tenure")
                ])
            ]),
            html.Div(className="col-md-6 mb-4", children=[
                html.Div(className="p-2 border rounded shadow-sm bg-white", children=[
                    dcc.Graph(id="chart-top5-credit")
                ])
            ]),
        ]),
        html.Div(className="row", children=[
            html.Div(className="col-md-6 mb-4", children=[
                html.Div(className="p-2 border rounded shadow-sm bg-white", children=[
                    dcc.Graph(id="chart-age-group")
                ])
            ]),
            html.Div(className="col-md-6 mb-4", children=[
                html.Div(className="p-2 border rounded shadow-sm bg-white", children=[
                    dcc.Graph(id="chart-gender")
                ])
            ]),
        ]),
        html.Div(className="row", children=[
            html.Div(className="col-md-6 mb-4", children=[
                html.Div(className="p-2 border rounded shadow-sm bg-white", children=[
                    dcc.Graph(id="chart-location")
                ])
            ]),
            html.Div(className="col-md-6 mb-4", children=[
                html.Div(className="p-2 border rounded shadow-sm bg-white", children=[
                    dcc.Graph(id="chart-products-age")
                ])
            ]),
        ]),
        html.Div(className="row", children=[
            html.Div(className="col-md-6 mb-4", children=[
                html.Div(className="p-2 border rounded shadow-sm bg-white", children=[
                    dcc.Graph(id="chart-products-gender")
                ])
            ]),
            html.Div(className="col-md-6 mb-4", children=[
                html.Div(className="p-2 border rounded shadow-sm bg-white", children=[
                    dcc.Graph(id="chart-products-location")
                ])
            ]),
        ]),
    ])
])

@callback(
    Output("chart-salary-tenure", "figure"),
    Output("chart-top5-credit", "figure"),
    Output("chart-age-group", "figure"),
    Output("chart-gender", "figure"),
    Output("chart-location", "figure"),
    Output("chart-products-age", "figure"),
    Output("chart-products-gender", "figure"),
    Output("chart-products-location", "figure"),
    Input("geo-filter", "value"),
    Input("gender-filter", "value"),
    Input("tenure-filter", "value"),
    Input("salary-filter", "value")
)
def update_all_charts(geo, gender, tenure, salary):
    dff = df.copy()
    if geo: dff = dff[dff["Geography"] == geo]
    if gender: dff = dff[dff["Gender"] == gender]
    if tenure: dff = dff[dff["TenureCategory"] == tenure]
    if salary: dff = dff[dff["SalaryCategory"] == salary]

    fig1 = px.histogram(dff, x="Tenure", y="EstimatedSalary", color="Churn",
                        barmode="stack", title="Customer by Salary and Tenure", color_discrete_sequence=["#023047", "#219EBC"])
    fig1.update_layout(
        title={'x': 0.5},
        legend=dict(
            orientation="h",
            yanchor="top",
            y=1.1,
            xanchor="center",
            x=0.5
        ),
        plot_bgcolor="white",
        paper_bgcolor="white",
        xaxis=dict(
            showgrid=False,
            zeroline=False,
            showline=True,
            linecolor='#023047'
        ),
        yaxis=dict(
            showgrid=False,
            zeroline=False,
            showline=True,
            linecolor='#023047'
        ),
    )

    top5 = dff.groupby("CreditScore", observed=False)[["Churn", "Stayed"]].sum().sort_values("Churn", ascending=False).head(5).reset_index()

    fig2 = px.bar(top5, x="CreditScore", y=["Stayed", "Churn"], barmode="stack", title="Top 5 Credit Scores", color_discrete_sequence=["#023047", "#219EBC"])
    fig2.update_layout(
        title={'x': 0.5},
        legend=dict(
            orientation="h",
            yanchor="top",
            y=1.1,
            xanchor="center",
            x=0.5
        ),
        plot_bgcolor="white",
        paper_bgcolor="white",
        xaxis=dict(
            showgrid=False,
            zeroline=False,
            showline=True,
            linecolor='#023047'
        ),
        yaxis=dict(
            showgrid=False,
            zeroline=False,
            showline=True,
            linecolor='#023047'
        ),
    )

    age_df = dff.groupby("AgeGroup", observed=False)[["Churn", "Stayed"]].sum()
    age_df["Total"] = age_df.sum(axis=1)

    fig3 = px.bar(age_df.reset_index(), x="AgeGroup", y=["Stayed", "Churn"], barmode="stack", title="Churn by Age Group", color_discrete_sequence=["#023047", "#219EBC", "#FB8500", "#FFB703"])
    fig3.update_layout(
        title={'x': 0.5},
        legend=dict(
            orientation="h",
            yanchor="top",
            y=1.1,
            xanchor="center",
            x=0.5
        ),
        plot_bgcolor="white",
        paper_bgcolor="white",
        xaxis=dict(
            showgrid=False,
            zeroline=False,
            showline=True,
            linecolor='#023047'
        ),
        yaxis=dict(
            showgrid=False,
            zeroline=False,
            showline=True,
            linecolor='#023047'
        ),
    )

    gender_df = dff.groupby("Gender", observed=False)[["Churn", "Stayed"]].sum()
    gender_df["Total"] = gender_df.sum(axis=1)

    fig4 = px.bar(gender_df.reset_index(), x="Gender", y=["Stayed", "Churn"], barmode="stack", title="Churn by Gender", color_discrete_sequence=["#023047", "#219EBC", "#FB8500", "#FFB703"])
    fig4.update_layout(
        title={'x': 0.5},
        legend=dict(
            orientation="h",
            yanchor="top",
            y=1.1,
            xanchor="center",
            x=0.5
        ),
        plot_bgcolor="white",
        paper_bgcolor="white",
        xaxis=dict(
            showgrid=False,
            zeroline=False,
            showline=True,
            linecolor='#023047'
        ),
        yaxis=dict(
            showgrid=False,
            zeroline=False,
            showline=True,
            linecolor='#023047'
        ),
    )

    geo_df = dff.groupby("Geography", observed=False)[["Churn", "Stayed"]].sum()
    geo_df["Total"] = geo_df.sum(axis=1)

    fig5 = px.bar(geo_df.reset_index(), x="Geography", y=["Stayed", "Churn"], barmode="stack", title="Churn by Location", color_discrete_sequence=["#023047", "#219EBC", "#FB8500", "#FFB703"])
    fig5.update_layout(
        title={'x': 0.5},
        legend=dict(
            orientation="h",
            yanchor="top",
            y=1.1,
            xanchor="center",
            x=0.5
        ),
        plot_bgcolor="white",
        paper_bgcolor="white",
        xaxis=dict(
            showgrid=False,
            zeroline=False,
            showline=True,
            linecolor='#023047'
        ),
        yaxis=dict(
            showgrid=False,
            zeroline=False,
            showline=True,
            linecolor='#023047'
        ),
    )

    prod_age = dff.groupby("AgeGroup", observed=False)["NumOfProducts"].value_counts().unstack().fillna(0)

    fig6 = px.line(
    prod_age,
    markers=True,
    title="Products by Age Group",
    color_discrete_sequence=["#023047", "#219EBC", "#FB8500", "#FFB703"]
    )
    fig6.update_layout(
        title={'x': 0.5},
        legend=dict(orientation="h", y=1.15, x=0.5, xanchor="center"),
        plot_bgcolor="white",
        paper_bgcolor="white",
        xaxis=dict(
            showgrid=False,
            zeroline=False,
            showline=True,
            linecolor='#023047'
        ),
        yaxis=dict(
            showgrid=False,
            zeroline=False,
            showline=True,
            linecolor='#023047'
        ),
    )

    prod_gender = dff.groupby("Gender", observed=False)["NumOfProducts"].value_counts().unstack().fillna(0)

    fig7 = px.line(
    prod_gender,
    markers=True,
    title="Products by Gender",
    color_discrete_sequence=["#023047", "#219EBC", "#FB8500", "#FFB703"]
    )
    fig7.update_layout(title={'x': 0.5}, legend=dict(orientation="h", y=1.15, x=0.5, xanchor="center"),
        plot_bgcolor="white",
        paper_bgcolor="white",
        xaxis=dict(
            showgrid=False,
            zeroline=False,
            showline=True,
            linecolor='#023047'
        ),
        yaxis=dict(
            showgrid=False,
            zeroline=False,
            showline=True,
            linecolor='#023047'
        ),
    )

    prod_geo = dff.groupby("Geography", observed=False)["NumOfProducts"].value_counts().unstack().fillna(0)

    fig8 = px.bar(prod_geo, barmode="stack", title="Products by Location", color_discrete_sequence=["#240046", "#5A189A", "#9D4EDD", "#E0AAFF"])
    fig8 = px.line(
    prod_geo,
    markers=True,
    title="Products by Location",
    color_discrete_sequence=["#023047", "#219EBC", "#FB8500", "#FFB703"]
    )
    fig8.update_layout(title={'x': 0.5}, legend=dict(orientation="h", y=1.15, x=0.5, xanchor="center"),
        plot_bgcolor="white",
        paper_bgcolor="white",
        xaxis=dict(
            showgrid=False,
            zeroline=False,
            showline=True,
            linecolor='#023047'
        ),
        yaxis=dict(
            showgrid=False,
            zeroline=False,
            showline=True,
            linecolor='#023047'
        ),                  
    )

    return fig1, fig2, fig3, fig4, fig5, fig6, fig7, fig8

@callback(
    Output("kpi-cards", "children"),
    Input("geo-filter", "value"),
    Input("gender-filter", "value"),
    Input("tenure-filter", "value"),
    Input("salary-filter", "value")
)
def update_kpis(geo, gender, tenure, salary):
    dff = df.copy()
    if geo: dff = dff[dff["Geography"] == geo]
    if gender: dff = dff[dff["Gender"] == gender]
    if tenure: dff = dff[dff["TenureCategory"] == tenure]
    if salary: dff = dff[dff["SalaryCategory"] == salary]

    total = len(dff)
    churn = dff["Churn"].sum()
    stayed = dff["Stayed"].sum()
    active = dff["IsActiveMember"].sum()
    inactive = total - active

    return html.Div(className="row text-center my-4", children=[
        html.Div(className="col-md-3 mb-3", children=[
            html.Div(className="card bg-light shadow", children=[
                html.Div(className="card-body", children=[
                    html.H5("Total Customers", className="card-title", style={"color": "#023047"}),
                    html.P(f"{total:,}", className="card-text display-6", style={"color": "#023047"}),
                    html.P(
                        f"Active: {round((active / total) * 100, 2)}% | Inactive: {round((inactive / total) * 100, 2)}%",
                        className="small",
                        style={"color": "#023047", "font-weight": "bold"}
                    )
                ])
            ])
        ]),
        html.Div(className="col-md-3 mb-3", children=[
            html.Div(className="card bg-light shadow", children=[
                html.Div(className="card-body", children=[
                    html.H5("Total Churn", className="card-title", style={"color": "#023047"}),
                    html.P(f"{churn:,}", className="card-text display-6", style={"color": "#023047"}),
                    html.P(
                        f"Churn: {round((churn / total) * 100, 2)}% | Stayed: {round((stayed / total) * 100, 2)}%",
                        className="small",
                        style={"color": "#023047", "font-weight": "bold"}
                    )
                ])
            ])
        ]),
        html.Div(className="col-md-3 mb-3", children=[
            html.Div(className="card bg-light shadow", children=[
                html.Div(className="card-body", children=[
                    html.H5("Avg Salary", className="card-title", style={"color": "#023047"}),
                    html.P(f"€{dff['EstimatedSalary'].mean():,.2f}", className="card-text display-6", style={"color": "#023047"}),
                    html.P(
                        f"Churn: {round((dff[dff['Churn'] == 1]['EstimatedSalary'].sum() / dff['EstimatedSalary'].sum()) * 100, 2)}% | "
                        f"Stayed: {round((dff[dff['Churn'] == 0]['EstimatedSalary'].sum() / dff['EstimatedSalary'].sum()) * 100, 2)}%",
                        className="small",
                        style={"color": "#023047", "font-weight": "bold"}
                    )
                ])
            ])
        ]),
        html.Div(className="col-md-3 mb-3", children=[
            html.Div(className="card bg-light shadow", children=[
                html.Div(className="card-body", children=[
                    html.H5("Avg Tenure", className="card-title", style={"color": "#023047"}),
                    html.P(f"{dff['Tenure'].mean():.2f} yrs", className="card-text display-6", style={"color": "#023047"}),
                    html.P(
                        f"Active: {dff[dff['IsActiveMember'] == 1]['Tenure'].mean():.2f} yrs | "
                        f"Inactive: {dff[dff['IsActiveMember'] == 0]['Tenure'].mean():.2f} yrs",
                        className="small",
                        style={"color": "#023047", "font-weight": "bold"}
                    )
                ])
            ])
        ])
    ])

@callback(
    Output("geo-filter", "value"),
    Output("gender-filter", "value"),
    Output("tenure-filter", "value"),
    Output("salary-filter", "value"),
    Input("reset-btn", "n_clicks"),
    prevent_initial_call=True
)
def reset_filters(n_clicks):
    # When button is clicked, reset all dropdowns to None
    return None, None, None, None
