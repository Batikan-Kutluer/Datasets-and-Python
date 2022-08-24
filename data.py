import pandas as pd
import matplotlib.pyplot as plt
import seaborn

seaborn.set()

# Load Happiness Dataset
_happiness = pd.DataFrame(
    pd.read_csv("world-happiness-report-2021.csv")[["Country name", "Ladder score", "Logged GDP per capita"]])

# Load Non-Religious Dataset
non_religious = pd.DataFrame(
    pd.read_csv("GPI and religion.csv")[["country", "percentage_non_religious"]])

# Load Religion Dataset
religion = pd.DataFrame(pd.read_csv("World Religion Dataset.csv"))

# Load World Population Estimated
population = pd.DataFrame(pd.read_csv(
    "World Population Estimated 2022.csv"))

# --------------------------------
# ------- Processing Data --------
# --------------------------------

# Getting sum of all religions
religion = religion[["country", "chistians", "muslims", "hindus",
                    "buddhists", "folkReligions", "jews", "other"]]
religion["total"] = religion.iloc[:, 1:-1].sum(axis=1)

# Renaming column names for migrating datasets
population = population.rename(
    columns={"name": "country", "value": "population"})
happiness = _happiness.rename(columns={
                              "Country name": "country", "Ladder score": "happiness", "Logged GDP per capita": "GDP"})

# Filtering selected columns and merge them with world religion dataset
population = population[["country", "population"]]
population = population.merge(
    religion[["country", "total"]], on="country")

# "," causes Int - String converting problem
population["population"] = population["population"].str.replace(
    ",", "").astype("int")

# Filtering false data as much as we can
population["religious_percent"] = population["total"] / \
    population["population"]*100
population = population[population["religious_percent"] <= 100]

# Merge Data
happiness = happiness.merge(non_religious, how="inner", on="country")
happiness = happiness.merge(population, how="inner", on="country")

# Serving chart & correlation using seaborn
seaborn.regplot(
    x=happiness["percentage_non_religious"], y=happiness["happiness"])

# Printing Final dataset to see the all data
print(happiness)

# Show chart
plt.show()
