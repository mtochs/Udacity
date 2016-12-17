# -*- coding: utf-8 -*-
"""
Created on Wed Dec 09 16:46:42 2015

@author: mykel

survival        Survival
                (0 = No; 1 = Yes)
pclass          Passenger Class
                (1 = 1st; 2 = 2nd; 3 = 3rd)
name            Name
sex             Sex
age             Age
sibsp           Number of Siblings/Spouses Aboard
parch           Number of Parents/Children Aboard
ticket          Ticket Number
fare            Passenger Fare
cabin           Cabin
embarked        Port of Embarkation
                (C = Cherbourg; Q = Queenstown; S = Southampton)
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

pd.set_option('expand_frame_repr', False)

def print_all(x):
    pd.set_option('display.max_rows', len(x))
    print(x)
    pd.reset_option('display.max_rows')


filename = 'titanic_data.csv'
titanic_df = pd.read_csv(filename)

all_males_df = titanic_df.drop(titanic_df[titanic_df.Sex == "female"].index)
all_females_df = titanic_df.drop(titanic_df[titanic_df.Sex == "male"].index)

all_males_with_age_df = all_males_df[np.isfinite(all_males_df['Age'])]
all_females_with_age_df = all_females_df[np.isfinite(all_females_df['Age'])]

all_passengers_without_siblings = titanic_df.drop(titanic_df[titanic_df.SibSp > 0].index)
all_passengers_with_siblings = titanic_df.drop(titanic_df[titanic_df.SibSp == 0].index)

all_children = titanic_df.drop(titanic_df[titanic_df.Age > 18].index)
all_children_with_parents = all_children.drop(all_children[all_children.Parch == 0].index)
all_children_without_parents = all_children.drop(all_children[all_children.Parch > 0].index)

print_all(all_children_without_parents)
#print all_passengers_without_siblings.values

#sns.barplot(all_children["survival"], all_children["sex"])


survival_by_class = sns.factorplot(x="Pclass", y="Survived", hue="Sex", data=titanic_df, size=6, order=np.arange(1,4), kind="bar", palette="muted")
survival_by_class.despine(left=True)
survival_by_class.set_ylabels("Survival Probability")
survival_by_class.set_xlabels("Passenger Class")

all_children_with_parents_survival_by_class = sns.factorplot(x="Pclass", y="Survived", hue="Sex", data=all_children_with_parents, size=6, order=np.arange(1,4), kind="bar", palette="muted")
all_children_with_parents_survival_by_class.despine(left=True)
all_children_with_parents_survival_by_class.set_ylabels("Survival Probability")
all_children_with_parents_survival_by_class.set_xlabels("Passenger Class (Children with 1 or 2 Parents)")

sibling_bool = titanic_df
sibling_bool["SibSp"] = titanic_df["SibSp"].astype('bool')
survival_by_sibling = sns.factorplot(x="SibSp", y="Survived", hue="Sex", data=sibling_bool, size=6, kind="bar", palette="muted")
survival_by_sibling.despine(left=True)
survival_by_sibling.set_ylabels("Survival Probability")
survival_by_sibling.set_xlabels("Passenger With or Without Siblings")

survival_by_age = sns.violinplot(x="Survived", y="Age", hue="Sex", data=titanic_df, split=True, inner="quart")


#print all_females_with_age_df.sort(columns="Age", ascending=True)

#print titanic_df.describe()
#print titanic_df.sort(columns="SibSp", ascending=True)


#print titanic_df.groupby("Sex").sum()
#print all_males_with_age_df.mean()
'''
- more than twice the number of females survived
- overall average age was 29.7
--- average age of females was 27.9
--- average age of males was 30.7

'''
