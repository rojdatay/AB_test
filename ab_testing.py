##############################################################
# AB Testing: Comparison of Facebook Bidding Methods
# in terms of the Number of Products Sold after Clicks
##############################################################

# Facebook bidding allows advertisers to set the amount they are willing to pay for their ads to reach their
# target audience through an auction-based system.

##############################################################
## 1. Business Problem
##############################################################

# Facebook introduced a new bidding type called "average bidding" as an alternative to the existing "maximum bidding"
# type. In this study, the statistical significance of any differences in the number of product purchases made by
# customers after clicking on ads will be examined, based on the utilization of these bidding methods.

# Variables:
# Impression: Number of ad impressions
# Click: Number of clicks on the ads
# Purchase: Number of product purchases after the clicks
# Earning: Revenue generated from the purchases

###############################################################
# 2. Data Preparation
###############################################################

## Importing libraries
##############################################

import pandas as pd
import statsmodels.stats.api as sms
from scipy.stats import ttest_1samp, shapiro, levene, ttest_ind, mannwhitneyu, \
    pearsonr, spearmanr, kendalltau, f_oneway, kruskal

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 10)
pd.set_option('display.float_format', lambda x: '%.5f' % x)
pd.set_option('display.expand_frame_repr', False)

df_cont= pd.read_excel("Dataset/Measurement_problems/ab_testing.xlsx",
                       sheet_name="Control Group")
df_test= pd.read_excel("Dataset/Measurement_problems/ab_testing.xlsx",
                       sheet_name="Test Group")

##############################################
# Data understanding
##############################################
def data_analysis(df):
    print("###################### First 5 Lines ###################")
    print(df.head())
    print("###################### Last 5 Lines ###################")
    print(df.tail())
    print("###################### Types ###################")
    print(df.dtypes)
    print("######################## Shape #########################")
    print(df.shape)
    print("######################### Info #########################")
    print(df.info())
    print("######################### N/A ##########################")
    print(df.isnull().sum())
    print("######################### Quantiles  ######################")
    print(df.describe().T)


data_analysis(df_test)
data_analysis(df_cont)


#####################################################
# AB Testing for 'Purchase' Variable
#####################################################

cont_purchase = df_cont['Purchase']
cont_purchase.mean()  # 550.8940587702316

test_purchase = df_test['Purchase']
test_purchase.mean() # 582.1060966484677

#####################################################
# Hypothesize
#####################################################

# H0: M1  = M2
# AverageBinding has no effect on purchase relative to MaximumBidding
# H0: M1 != M2
# AverageBinding has effect on purchase relative to MaximumBidding

# Assumption of normality
##############################################

def shapiro_test(a,b):
    test_stat, pvalue = shapiro(a)
    if pvalue < 0.05:
        print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue),
              "HO is rejected, the assumption of normal distribution is not satisfied")
    else:
        print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue),
              "HO is not rejected, the assumption of normal distribution is satisfied")
    test_stat, pvalue = shapiro(b)
    if pvalue < 0.05:
        print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue),
              "HO is rejected, the assumption of normal distribution is not satisfied")
    else:
        print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue),
              "HO is not rejected, the assumption of normal distribution is satisfied")


shapiro_test(test_purchase, cont_purchase)

#Test Stat = 0.9589, p-value = 0.1541 HO is not rejected, the assumption of normal distribution is satisfied
#Test Stat = 0.9773, p-value = 0.5891 HO is not rejected, the assumption of normal distribution is satisfied


# Assumption of homogeneity of variance
##############################################

def levene_test(a,b):
    test_stat, pvalue = levene(a,b)
    if pvalue < 0.05:
        print("Test Stat = %.4f, p-value = %.4f" % (test_stat, pvalue),
              "HO is rejected, the homogeneity of variance is not satisfied")
    else:
        print("Test Stat = %.4f, p-value = %.4f" % (test_stat, pvalue),
              "HO is not rejected, the homogeneity of variance is satisfied")

levene_test(test_purchase, cont_purchase)
# test Stat = 2.6393, p-value = 0.1083 HO is not rejected, the homogeneity of variance is satisfied

### When both assumptions are met, an 'Two-Sample Independent t-Test' is conducted.


# Two-Sample Independent t-Test
##############################################

def ttest_ind_test(a,b):
    test_stat, pvalue = ttest_ind(a, b)
    if pvalue < 0.05:
        print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue),
              "HO is rejected, there is a statistically significant difference between the groups")
    else:
        print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue),
              "HO is not rejected, there is not a statistically significant difference between the groups")


ttest_ind_test(test_purchase,cont_purchase)
#Test Stat = 0.9416, p-value = 0.3493 HO is not rejected,
# #there is not a statistically significant difference between the groups


#####################################################
# Defining of the Whole Process
#####################################################

# Defining mannwhitneyu Test
##############################################
def mannwhitneyu_test(a,b):
    test_stat, pvalue = mannwhitneyu(a, b)
    if pvalue < 0.05:
        print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue),
              "HO is rejected, there is a statistically significant difference between the groups")
    else:
        print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue),
              "HO is not rejected, there is not a statistically significant difference between the groups")


# Defining AB Test
##############################################

def ab_test(a,b):
    print("Shapiro Test Stat")
    shapiro_test(a,b)
    if pvalue < 0.05:
        print("Levene Test Stat")
        levene_test(a,b)
        print("When just one assumptions are not met, use the non parametric test mannwhitneyu")
        return mannwhitneyu_test(a,b)
    else:
        print("Levene Test Stat")
        levene_test(a, b)
            if pvalue < 0.05:
                print("When both assumptions are not met, use the non parametric test mannwhitneyu")
                return mannwhitneyu_test(a, b)
            else:
                print("When just one assumptions are not met, an 'Two-Sample Independent t-Test' is conducted")
                return ttest_ind_test(a, b)


ab_test(cont_purchase, test_purchase)

#Shapiro Test Stat
#Test Stat = 0.9773, p-value = 0.5891 HO is not rejected, the assumption of normal distribution is satisfied
#Test Stat = 0.9589, p-value = 0.1541 HO is not rejected, the assumption of normal distribution is satisfied
#Levene Test Stat
#Test Stat = 2.6393, p-value = 0.1083 HO is not rejected, the homogeneity of variance is satisfied
#When just one assumptions are not met, an 'Two-Sample Independent t-Test' is conducted
#Test Stat = -0.9416, p-value = 0.3493 HO is not rejected, there is not a statistically significant difference between the groups

