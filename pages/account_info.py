import dash
from dash import html, dcc, Input, Output, callback
import pandas as pd
import plotly.express as px
from components.navbar import get_navbar

dash.register_page(__name__, path="/account", name="Account Info")

# Load data
df = pd.read_csv("dataset/Bank_Churn.csv")
df.rename(columns={"Exited": "Churn"}, inplace=True)
df["Stayed"] = 1 - df["Churn"]

# Preprocessing
bins = [0, 50000, 100000, 150000, 200000]
labels = ["<50K", "50K-100K", "100K-150K", "150K+"]
df["SalaryCategory"] = pd.cut(df["EstimatedSalary"], bins=bins, labels=labels, include_lowest=True)

def tenure_category(t):
    if t < 3: return "0-2"
    elif t < 6: return "3-5"
    elif t < 9: return "6-8"
    else: return "9+"
df["TenureCategory"] = df["Tenure"].apply(tenure_category)

# Balance Category
balance_bins = [0, 50000, 100000, 150000, 200000]
balance_labels = ["<50K", "50K-100K", "100K-150K", "150K+"]
df["BalanceCategory"] = pd.cut(df["Balance"], bins=balance_bins, labels=balance_labels, include_lowest=True)

layout = html.Div([
    get_navbar(),
    html.Div(className="container-fluid", children=[

        html.H2("Account Information", className="text-center my-4", style={"color": "#023047"}),

        # KPI Cards
        html.Div(id="account-kpis", className="row text-center my-4"),

        # Filters
        html.Div(className="row mb-4 justify-content-center", children=[
            html.Div(className="col-md-2", children=[
                dcc.Dropdown(id="geo-filter-acct", options=[{"label": g, "value": g} for g in df["Geography"].unique()], placeholder="Select Geography")
            ]),
            html.Div(className="col-md-2", children=[
                dcc.Dropdown(id="gender-filter-acct", options=[{"label": g, "value": g} for g in df["Gender"].unique()], placeholder="Select Gender")
            ]),
            html.Div(className="col-md-2", children=[
                dcc.Dropdown(id="tenure-filter-acct", options=[{"label": t, "value": t} for t in df["TenureCategory"].unique()], placeholder="Select Tenure")
            ]),
            html.Div(className="col-md-2", children=[
                dcc.Dropdown(id="salary-filter-acct", options=[{"label": s, "value": s} for s in df["SalaryCategory"].unique()], placeholder="Select Salary")
            ]),
            html.Div(className="col-md-2", children=[
                html.Button("Reset Filters", id="reset-btn-acct", className="btn w-100", style={"background-color": "#023047", "color": "#fff"})
            ])
        ]),

        # Charts
        html.Div(className="row", children=[
            html.Div(className="col-md-6 mb-4", children=[
                html.Div(className="p-2 border rounded shadow-sm bg-white", children=[
                    dcc.Graph(id="chart-tenure-balance")
                ])
            ]),
            html.Div(className="col-md-6 mb-4", children=[
                html.Div(className="p-2 border rounded shadow-sm bg-white", children=[
                    dcc.Graph(id="chart-balance-category")
                ])
            ]),
        ]),
        html.Div(className="row", children=[
            html.Div(className="col-md-6 mb-4", children=[
                html.Div(className="p-2 border rounded shadow-sm bg-white", children=[
                    dcc.Graph(id="chart-cc-churn")
                ])
            ]),
            html.Div(className="col-md-6 mb-4", children=[
                html.Div(className="p-2 border rounded shadow-sm bg-white", children=[
                    dcc.Graph(id="chart-product-churn")
                ])
            ]),
        ]),
        html.Div(className="row", children=[
            html.Div(className="col-md-6 mb-4", children=[
                html.Div(className="p-2 border rounded shadow-sm bg-white", children=[
                    dcc.Graph(id="chart-salary-cc")
                ])
            ]),
        ])
    ])
])

@callback(
    Output("account-kpis", "children"),
    Input("geo-filter-acct", "value"),
    Input("gender-filter-acct", "value"),
    Input("tenure-filter-acct", "value"),
    Input("salary-filter-acct", "value")
)
def update_kpis(g, gender, tenure, salary):
    dff = df.copy()
    if g: dff = dff[dff["Geography"] == g]
    if gender: dff = dff[dff["Gender"] == gender]
    if tenure: dff = dff[dff["TenureCategory"] == tenure]
    if salary: dff = dff[dff["SalaryCategory"] == salary]

    return html.Div(className="row text-center my-4", children=[
        html.Div(className="col-md-3 mb-3", children=[
            html.Div(className="card bg-light shadow", children=[
                html.Div(className="card-body", children=[
                    html.H5("Active Members", className="card-title", style={"color": "#023047"}),
                    html.P(f"{dff['IsActiveMember'].sum()}", className="card-text display-6", style={"color": "#023047"}),
                    html.P(
                        f"Inactive: {(~dff['IsActiveMember'].astype(bool)).sum()}",
                        className="small",
                        style={"color": "#023047", "font-weight": "bold"}
                    )
                ])
            ])
        ]),
        html.Div(className="col-md-3 mb-3", children=[
            html.Div(className="card bg-light shadow", children=[
                html.Div(className="card-body", children=[
                    html.H5("Credit Card Holders", className="card-title", style={"color": "#023047"}),
                    html.P(f"{dff['HasCrCard'].sum()}", className="card-text display-6", style={"color": "#023047"}),
                    html.P(
                        f"No: {(~dff['HasCrCard'].astype(bool)).sum()}",
                        className="small",
                        style={"color": "#023047", "font-weight": "bold"}
                    )
                ])
            ])
        ]),

        html.Div(className="col-md-3 mb-3", children=[
            html.Div(className="card bg-light shadow", children=[
                html.Div(className="card-body", children=[
                    html.H5("Avg. No. of Product Usage", className="card-title", style={"color": "#023047"}),
                    html.P(f"{dff['NumOfProducts'].mean():.2f}", className="card-text display-6", style={"color": "#023047"}),
                    html.P(
                        f"Most: {dff['NumOfProducts'].mode()[0]}",
                        className="small",
                        style={"color": "#023047", "font-weight": "bold"}
                    )
                ])
            ])
        ]),

        html.Div(className="col-md-3 mb-3", children=[
            html.Div(className="card bg-light shadow", children=[
                html.Div(className="card-body", children=[
                    html.H5("Avg. Balance per Customer", className="card-title", style={"color": "#023047"}),
                    html.P(f"€{dff['Balance'].mean():,.2f}", className="card-text display-6", style={"color": "#023047"}),
                    html.P(
                        f"High: €{dff['Balance'].max():,.2f}",
                        className="small",
                        style={"color": "#023047", "font-weight": "bold"}
                    )
                ])
            ])
        ])
    ])

@callback(
    Output("chart-tenure-balance", "figure"),
    Output("chart-balance-category", "figure"),
    Output("chart-cc-churn", "figure"),
    Output("chart-product-churn", "figure"),
    Output("chart-salary-cc", "figure"),
    Input("geo-filter-acct", "value"),
    Input("gender-filter-acct", "value"),
    Input("tenure-filter-acct", "value"),
    Input("salary-filter-acct", "value")
)
def update_charts(g, gender, tenure, salary):
    dff = df.copy()
    if g: dff = dff[dff["Geography"] == g]
    if gender: dff = dff[dff["Gender"] == gender]
    if tenure: dff = dff[dff["TenureCategory"] == tenure]
    if salary: dff = dff[dff["SalaryCategory"] == salary]

    # Chart 1: Churn Rate by Tenure & Balance Category
    temp1 = dff.groupby(["TenureCategory", "BalanceCategory"], observed=False)["Churn"].mean().reset_index()
    fig1 = px.bar(temp1, x="TenureCategory", y="Churn", color="BalanceCategory", barmode="stack", title="Churn Rate by Tenure & Balance", color_discrete_sequence=["#023047", "#219EBC", "#FB8500", "#FFB703"])
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

    # Chart 2: Balance Category Breakdown
    temp2 = dff.groupby("BalanceCategory", observed=False).agg({
        "Churn": "sum",
        "Stayed": "sum",
        "IsActiveMember": lambda x: (x == 1).sum(),
    }).reset_index()
    temp2["Inactive"] = dff.groupby("BalanceCategory", observed=False)["IsActiveMember"].apply(lambda x: (x == 0).sum()).values
    fig2 = px.bar(temp2, x="BalanceCategory", y=["Stayed", "Churn", "IsActiveMember", "Inactive"],
                  barmode="stack", title="Balance Category Breakdown", color_discrete_sequence=["#023047", "#219EBC", "#FB8500", "#FFB703"])
    fig2.update_layout(
        legend_title_text="MemberCategory",
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

    # Chart 3: Credit Card vs Churn
    temp3 = dff.groupby("HasCrCard", observed=False)[["Churn", "Stayed"]].sum().reset_index()
    fig3 = px.bar(temp3, x="HasCrCard", y=["Stayed", "Churn"], barmode="stack", title="Credit Card vs Churn", color_discrete_sequence=["#023047", "#219EBC"])
    fig3.update_layout(
        legend_title_text="CustomerType",
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

    # Chart 4: Product Count vs Churn Rate
    temp4 = dff.groupby("NumOfProducts", observed=False)["Churn"].mean().reset_index()
    fig4 = px.bar(temp4, x="NumOfProducts", y="Churn", title="Churn Rate by Product Count", color_discrete_sequence=["#219EBC"])
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

    # Chart 5: Salary by Credit Card
    dff["HasCreditCard"] = dff["HasCrCard"].map({1: "Yes", 0: "No"})
    fig5 = px.histogram(
        dff,
        x="SalaryCategory",
        color="HasCreditCard",
        barmode="group",
        title="Salary vs Credit Card Ownership",
        color_discrete_sequence=["#023047", "#219EBC"],
    )
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

    for fig in [fig1, fig2, fig3, fig4, fig5]:
        fig.update_layout(title={'x': 0.5}, plot_bgcolor="white", paper_bgcolor="white")

    return fig1, fig2, fig3, fig4, fig5

@callback(
    Output("geo-filter-acct", "value"),
    Output("gender-filter-acct", "value"),
    Output("tenure-filter-acct", "value"),
    Output("salary-filter-acct", "value"),
    Input("reset-btn-acct", "n_clicks"),
    prevent_initial_call=True
)
def reset_filters(n):
    return None, None, None, None
