#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import seaborn as sb
import numpy as np
import matplotlib.pyplot as plt


# In[2]:


df = pd.read_excel("C:/Users/Ck/Desktop/Study/2024 Jan Sesmester/Data Mining/Assignment 1 Individual/JapanMenuItems.xlsx")
df


# # Data Exploration 

# In[3]:


X = df.values
n_samples, n_features = X.shape
print("This dataset has {0} samples and {1} features".format(n_samples, n_features))


# In[4]:


X


# ### Checking the dataset is there are any null 

# In[5]:


print(df.isnull().sum())


# ### Checking the datatypes of the values

# In[6]:


print(df.dtypes)


# In[35]:


import seaborn as sns

# Compute the correlation matrix
correlation_matrix = np.corrcoef(X, rowvar=False)

# Create the heatmap
plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', xticklabels=features, yticklabels=features)

# Labeling
plt.title('Correlation Heatmap of Features')
plt.xticks(rotation=45)
plt.yticks(rotation=0)

# Show plot
plt.show()


# ### Adding name into features columns

# In[8]:


features = ["California Roll", "Salmon Nigiri", "Tonkotsu Ramen", "Chicken Teriyaki Bento", "Edamame", "Gyoza (Dumplings)", "Tempura (Shrimp)", 
            "Green Tea Ice Cream", "Mochi Ice Cream", "Matcha Latte"]


# ### bar chart 

# In[34]:


import matplotlib.pyplot as plt

# Count the number of purchases for each item
purchase_counts = [sum(1 for sample in X if sample[i] == 1) for i in range(len(features))]

# Create the bar plot
plt.figure(figsize=(10, 6))  # Adjust the figure size as needed
plt.bar(features, purchase_counts)

# Labeling
plt.xlabel('Items')
plt.ylabel('Number of Purchases')
plt.title('Number of Purchases for Each Item')
plt.xticks(rotation=45)  # Rotate x-axis labels for better readability

# Show the plot
plt.tight_layout()  # Adjust layout to prevent overlap of labels
plt.show()


# In[10]:


# First, how many rows contain our premise: that a person is buying california roll
num_californiaRoll_purchases = 0
for sample in X:
    if sample[0] == 1:  # This person bought california roll
        num_californiaRoll_purchases += 1
print("{0} people bought California Roll".format(num_californiaRoll_purchases))


# In[31]:


# First, how many rows contain our premise: that a person is buying california roll
num_californiaRoll_purchases = 0
for sample in X:
    if sample[0] == 0:  # This person bought california roll
        num_californiaRoll_purchases += 1
print("{0} people bought California Roll".format(num_californiaRoll_purchases))


# In[11]:


rule_valid = 0
rule_invalid = 0
for sample in X:
    if sample[0] == 1:  # This person bought california roll
        if sample[9] == 1:
            # This person bought both california roll and matcha latte
            rule_valid += 1
        else:
            # This person bought california roll, but not matchal atte
            rule_invalid += 1
print("{0} cases of the rule being valid were discovered".format(rule_valid))
print("{0} cases of the rule being invalid were discovered".format(rule_invalid))


# In[12]:


# Now we have all the information needed to compute Support and Confidence
support = rule_valid  # The Support is the number of times the rule is discovered.
confidence = rule_valid / num_californiaRoll_purchases
print("The support is {0} and the confidence is {1:.3f}.".format(support, confidence))
# Confidence can be thought of as a percentage using the following:
print("As a percentage, that is {0:.1f}%.".format(100 * confidence))


# In[13]:


from collections import defaultdict

# Now compute for all possible rules
valid_rules = defaultdict(int)
invalid_rules = defaultdict(int)
num_occurences = defaultdict(int)

for sample in X:
    for premise in range(n_features):
        if sample[premise] == 0: continue
        # Record that the premise was bought in another transaction
        num_occurences[premise] += 1
        for conclusion in range(n_features):
            if premise == conclusion:  # It makes little sense to measure if X -> X.
                continue
            if sample[conclusion] == 1:
                # This person also bought the conclusion item
                valid_rules[(premise, conclusion)] += 1
            else:
                # This person bought the premise, but not the conclusion
                invalid_rules[(premise, conclusion)] += 1
support = valid_rules
confidence = defaultdict(float)
for premise, conclusion in valid_rules.keys():
    confidence[(premise, conclusion)] = valid_rules[(premise, conclusion)] / num_occurences[premise]


# In[14]:


for premise, conclusion in confidence:
    premise_name = features[premise]
    conclusion_name = features[conclusion]
    print("Rule: If a person buys {0} they will also buy {1}".format(premise_name, conclusion_name))
    print(" - Confidence: {0:.3f}".format(confidence[(premise, conclusion)]))
    print(" - Support: {0}".format(support[(premise, conclusion)]))
    print("")


# In[15]:


def print_rule(premise, conclusion, support, confidence, features):
    premise_name = features[premise]
    conclusion_name = features[conclusion]
    print("Rule: If a person buys {0} they will also buy {1}".format(premise_name, conclusion_name))
    print(" - Confidence: {0:.3f}".format(confidence[(premise, conclusion)]))
    print(" - Support: {0}".format(support[(premise, conclusion)]))
    print("")


# In[16]:


premise = 1
conclusion = 3
print_rule(premise, conclusion, support, confidence, features)


# In[17]:


# Sort by support
from pprint import pprint
pprint(list(support.items()))


# In[18]:


from operator import itemgetter
sorted_support = sorted(support.items(), key=itemgetter(1), reverse=True)


# In[19]:


for index in range(10):
    print("Rule #{0}".format(index + 1))
    (premise, conclusion) = sorted_support[index][0]
    print_rule(0, conclusion, support, confidence, features)


# In[20]:


sorted_confidence = sorted(confidence.items(), key=itemgetter(1), reverse=True)


# In[28]:


for index in range(10):
    print("Rule #{0}".format(index + 1))
    (premise, conclusion) = sorted_confidence[index][0]
    print_rule(9, conclusion, support, confidence, features)


# ### Adding all function into one

# In[38]:


def recommendFood (user_input):
    def printRule(premise, conclusion, support, confidence, features):
        premise_name = features[premise]
        conclusion_name = features[conclusion]
        print("Rule: If a person buys {0} they will also buy {1}".format(premise_name, conclusion_name))
        print(" - Confidence: {0:.3f}".format(confidence[(premise, conclusion)]))
        print(" - Support: {0}".format(support[(premise, conclusion)]))
        print("")

    # Prompt the user to input a premise
    user_input = input("Enter a Food Name: ")

    # Find the index of the user-input premise in the features list
    premise_index = features.index(user_input)

    # Create a list to store the rules
    rules = []

    # Iterate over the sorted confidence list
    for index in range(len(sorted_confidence)):
        if len(rules) >= 3:
            break

        (premise, conclusion) = sorted_confidence[index][0]
        premise_name = features[premise]
        conclusion_name = features[conclusion]

        # Check if the premise and conclusion names are different and if the premise matches user input
        if premise_name != conclusion_name and premise == premise_index:
            rules.append((premise, conclusion))

    # Sort the rules based on confidence score
    sorted_rules = sorted(rules, key=lambda x: confidence[x], reverse=True)

    # Print the top three rules
    for i, rule in enumerate(sorted_rules[:3]):
        print("Rule #{0}".format(i + 1))
        printRule(rule[0], rule[1], support, confidence, features)


# In[41]:


recommendFood(x)


# In[ ]:




