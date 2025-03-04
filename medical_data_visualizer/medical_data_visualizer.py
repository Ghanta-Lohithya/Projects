import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# 1
df = pd.read_csv("medical_examination.csv")


# 2
df["BMI"] = df["weight"] / (df["height"] / 100) ** 2  # BMI = weight(kg) / height(m)^2
df["overweight"] = (df["BMI"] > 25).astype(int)  # Overweight (1) if BMI > 25, else 0
df.drop(columns=["BMI"], inplace=True)  # Remove BMI column after classification

# 3
df["cholesterol"] = (df["cholesterol"] > 1).astype(int)
df["gluc"] = (df["gluc"] > 1).astype(int)


# 4
def draw_cat_plot():
    # 5
    df_cat = pd.melt(df, id_vars=["cardio"], value_vars=["cholesterol", "gluc", "smoke", "alco", "active", "overweight"])


    # 6
    df_cat = df_cat.groupby(["cardio", "variable", "value"]).size().reset_index(name="total")
    

    # 7



    # 8
    fig =sns.catplot(
        x="variable", 
        y="total", 
        hue="value", 
        col="cardio", 
        data=df_cat, 
        kind="bar"
    ).fig


    # 9
    fig.savefig('catplot.png')
    return fig


# 10
def draw_heat_map():
    # 11
    df_heat = df[
        (df["ap_lo"] <= df["ap_hi"]) &  # Keep rows where diastolic ≤ systolic
        (df["height"] >= df["height"].quantile(0.025)) &  # Height ≥ 2.5th percentile
        (df["height"] <= df["height"].quantile(0.975)) &  # Height ≤ 97.5th percentile
        (df["weight"] >= df["weight"].quantile(0.025)) &  # Weight ≥ 2.5th percentile
        (df["weight"] <= df["weight"].quantile(0.975))    # Weight ≤ 97.5th percentile
    ]


    # 12
    corr = df_heat.corr()

    # 13
    mask = np.triu(np.ones_like(corr, dtype=bool))




    # 14
    fig, ax = plt.subplots(figsize=(10, 8))

    # 15
    sns.heatmap(
        corr, 
        mask=mask, 
        annot=True, 
        fmt=".1f", 
        linewidths=0.5, 
        cmap="coolwarm", 
        center=0, 
        square=True
    )


    # 16
    fig.savefig('heatmap.png')
    return fig
