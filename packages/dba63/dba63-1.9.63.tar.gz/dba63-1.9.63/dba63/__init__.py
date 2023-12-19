class L1:
    """Introduction to Data Analytics"""
    def __init__(self):
        self.content = [func for func in dir(L1) if callable(getattr(L1, func))]
        self.content = [func for func in self.content if not func.startswith("__")]

    def machine_learning(self):
        ml = {
            "- Supervised:": "\n    - Goal: predict a single 'target' or 'outcome' variable"
                             "\n    - Training data, where target value is known"
                             "\n    - Score to data where value is not known"
                             "\n    - Methods: classifiation and prediction",
            "- Unsupervised:": "\n    - Goal: Segment data into meaningful segments; detect patterns"
                               "\n    - There is no target (outcome) variable to predict or classify"
                               "\n    - Methods: Association rules, collaborative filter, data reduction & exploration, visualization\n"
        }

        print("Types of Machine learning")
        for x,y in ml.items():
            print(x,y)

        methods = {
            "\n- Supervised: Classification": "\n -> Goal: Predict categorical target (outcome) variable"
                                            "\n -> Examples: Purchase/no purchase, fraud/no fraud, creditworthy/not creditworthy"
                                            "\n    - each row is a case (customer, tax return, applicant)"
                                            "\n    - each column is a variable"
                                            "\n    - target variable is often binary (yes/no)",
            "\n- Supervised: Prediction": "\n -> Goal: Predict numerical target (outcome) variable"
                                        "\n -> Examples: sales, revenue, performance"
                                        "\n    - As in classification, each row = case, each column = variable"
                                        "\n    - Taken together, classification + prediction constitute \"predictive analytics\"",
            "\n- Unsupervised: Association Rule": "\n -> Goal: Produce rules that define \"what goes with what\" in transactions"
                                                "\n -> Example: \"If X was purchased, Y was also purchased\""
                                                "\n    - Rows are transactions"
                                                "\n    - Used in recommender systems"
                                                "\n    - Also called \"affinity analysis\"",
            "\n- Unsupervised: Collaborative Filtering": "\n -> Goal: Recommend products to purchase"
                                                       "\n    - Based on products that customer rates, selects, views or purchases"
                                                       "\n    - Recommend products that \"customers like you\" purchase (user-based)"
                                                       "\n    - Or, recommend products that share a \"product purchaser profile\" with your purchase (item-based)",
            "\n- Unsupervised: Data reduction": "\n    - Distillation of complex/large data into simpler/smaller data"
                                              "\n    - Reducing the number variables/columns (e.g, principal components)"
                                              "\n    - Reducing the number of records/rows (e.g, clustering)",
            "\n- Unsupervised: Data Visualization": "\n    - Graphs and plots of data"
                                                  "\n    - Histograms, boxplots, bar charts, scatterplots"
                                                  "\n    - Especially useful to examine relationships between pairs of variables\n"
            }

        print("\nMachine Learning Methods:")
        for x,y in methods.items():
            print(x, y)

    def data_analytics_steps(self):
        steps = {
            "1.": "Define/Understand Purpose",
            "2.": "Obtain data (may involve random sampling)",
            "3.": "Explore, clean. pre-process data",
            "4.": "Reduce the data; if supervised, partition it",
            "5.": "Specify task (classification, clustering, etc.)",
            "6.": "Choose the techniques (regression, CART, neural networks, etc.)",
            "7.": "Iterative implementation and tuning",
            "8.": "Assess results - compare models",
            "9.": "Deploy best model\n"
        }
        print("Steps in Data Analytics")
        for x,y in steps.items():
            print(x, y)

    def obtaining_data(self):
        sampling = {
            "Obtaining Data: Sampling": "\n    - Data analytics typically deals with huge databases "
                                          "\n    - For piloting/prototyping, algorithms and models are typically applied to a sample from a database, to produce statistically valid results"
                                          "\n    - Once you develop and select a final model, you use it to \"score\" (predict values or classes for) the observation in the larger database"
                                          "\n    - python: df.sample(n, weights)",
            "\nRare Event: Oversampling": "\n    - Often the event of interest is rare"
                                          "\n -> Examples: response to mailing, fraud in taxes, etc."
                                          "\n    - Sampling may yield too few \"interesting\" cases to effectively train a model"
                                          "\n -> A popular solution: Oversample the rare cases to obtain a more balanced training set"
                                          "\n    - Later, need to adjust for the oversampling"
                                          "\n    - python: weights = [0.9 if rooms > 10 else 0.1 for rooms in df.ROOMS]\n"
        }
        for x,y in sampling.items():
            print(x, y)

    def types_of_variables(self):
        vars = {
            "Info": "\n    - Determine the types of pre-processing needed, and algorithms used"
                    "\n  ->  Main distinction: Categorical vs Numeric",
            "\nNumeric": "\n    - Continous (age, weight, height)"
                       "\n    - Discrete (number of cards, number of patients)"
                       "\n    - Most algortihms can handle numeric data"
                       "\n    - May occasionally need to \"bin\" into categories",
            "\nCategorical": "\n    - Ordered (low, medium, high)"
                           "\n    - Nominal (male, female)"
                           "\n    - Naive Bayes can use as if"
                           "\n    - In most other algorithms, must create binary dummies "
                           "(number of dummies = number of categorical - 1)\n"
        }
        for k,v in vars.items():
            print(k, v)

    def cleaning_data(self):
        cleaning = {
            "Missing data": "\n    - If few records, might be omitted"
                            "\n    - Imputation methods (mean, median, distribution)",
            "\nOutliers": "\n    - No fixed definition"
                        "\n    - Measurement or data entry error"
                        "\n    - Sometimes everythingg larger than 3 std from mean"
                        "\n    - Domain knowledge can help",
            "\nDetecting Outliers": "\n    - Outlier = \"extreme\" observation, being distant from rest of data"
                                  "\n    - Outlier can have disproportionate influence on model"
                                  "\n    - important step in data pre=processing is detecting outliers"
                                  "\n    - once detected, domain knowledge is required to determine if error, or truly extreme"
                                  "\n    - in some contexts, finding outliers is the purpose of the data analytics exercise"
                                  "(airport security screening). This is called \"anomaly detection\"",
            "\nPre-process data": "\n    - Combining different datasets"
                                  "\n    - Creating new variables from existing ones"
                                  "\n    - Normalizing/rescaling"
                                  "\n    - Numerically coding categorical ordinal variables"
                                  "\n    - Creating dummy variables from categorical nominal variables\n"
        }

        for k,v in cleaning.items():
            print(k, v)

    def handling_missing_data(self):
        d = {
            "Handling Missing Data": "\n    - Most algorithms will not process records with missing values. "
                                     "Default is to drop those records",
            "\nSolution 1": "\n    - If a small number of records have missing values, can omit them"
                            "\n    - If many records are missing values on a small set of variables, can drop those varibles (or use prozies)"
                            "\n    - If many records have missing values, omittion is not practical",
            "\nSolution 2: Imputation": "\n    - Replace missing varaibles with reasonable substitutes"
                                        "\n    - Lets you keep the record and use the rest of it's (non-missing) information\n"
        }

        for k,v in d.items():
            print(k, v)

    def normalising_data(self):
        n = {
            "Normalizing Data": "\n    - Used in some techniques when variables with the largest scale would dominate and skew results"
                                "\n    - Puts all variables on same scale"
                                "\n    - Useful for when the data contain dummies and numerix"
                                "\n  ->  Normalizing Function:    Subtract mean and divide by standard deviation"
                                "\n  ->  Alternative function:    Scale to 0-1 by subtracting minimum and dividing by range\n"
        }

        for k,v in n.items():
            print(k, v)

    def reducing_dimensions(self):
        r = {
            "Reducing Data Dimensions": "\n    - Eliminating unneeded variables"
                                        "\n    - Combining and/pr transforming variables"
                                        "\n  ->  Rule of thumb:    Min 10 records per predictor variable\n"
        }
        for k,v in r.items():
            print(k, v)

    def overfitting(self):

        of = {
            "Overfitting": "\n    - Treating noise as if it was signal, modelling all variations"
                           "\n  ->  High variance:    model changes significantly based on training data",
            "\nUnderfitting": "\n    - A failure to learn the relationships in the training data"
                            "\n  ->  High bias:    assumptions about model lead to ignoring training data",
            "\nThe problem of overfitting": "\n    - Statistical models can produce highly complex explanations of relationships between variables"
                                            "\n    - The \"fit\" may be excellent"
                                            "\n    - When used with new data, models of great complexity do not do so wel"
                                            "\n  ->  Causes:    Too many predictors, too many parameters, trying many different models"
                                            "\n  ->  Consequece:    Deployed model will not work as well as expected with complete data"
        }
        for k, v in of.items():
            print(k, v)


    def data_partition(self):
        dp = {
            "Data Partition": "\n    - Relevant for supervised learning"
                              "\n    - Divide data into train, validation, and test sets    (why? unbiased estimation of performance)"
                              "\n    - K-fold cross-validation for small dataset (splitting k times with different training set each time)"
                              "\n  ->  Problem:    How well will our model perform with new data?"
                              "\n  ->  Solution:    Separate data into two parts   (Training partition: develop model,    Validation partition: implement model and evaluate on \"new\" data)",
            "\nTest Partition": "\n    - When model developed on training data, it can overfti (hence need to assess on validation)"
                              "\n    - Assessing multiple models over same validation data can overfit validation data"
                              "\n  ->  Solution:    final selected model is applied to a test partition to give unbiased estimate of its performance on new data\n"
        }
        for k, v in dp.items():
            print(k, v)

    def python_code(self):
        p = {
            "Normalising Data": "\n    - norm_df_by_mean = (df - df.mean()) / df.std()"
                                "\n    - norm_df_by_range = (df - df.min()) / (df.max() - df.min())",
            "\nPartition Data": "\n  # importing packages"
                        "\n    - from sklearn.model_selection import train_test_split\n"
                        "\n  # training (60%) and validation (40%)"
                        "\n    - trainData, validData = train_test_split(df, test_size = 0.40, random_state = 1)\n"
                        "\n  # training (50%), validation (30%) and testing (20%)"
                        "\n    - trainData, temp = train_test_split(df, test_size = 0.5, random_state = 1)"
                        "\n    - validData, testData = train_test_split(temp, test_sizs = 0.4, random_state = 1)",
            "\nFit Model and make predictions": "\n  # importing packages"
                        "\n    - from sklearn.linear_model import LinearRegression\n"
                        "\n  # fit model"
                        "\n    - model = LinearRegression()"
                        "\n    - model.fit(train_X, train_y)\n"
                        "\n  # make predictions"
                        "\n    - train_pred = model.predict(train_X)\n"
        }
        for k, v in p.items():
            print(k, v)

# -------------------------------------------------------------------------------------------------------------------- #

class L2:
    "Data exploration, dimension reduction, performance evaluation"
    def __init__(self):
        self.content = [func for func in dir(L2) if callable(getattr(L2, func))]
        self.content = [func for func in self.content if not func.startswith("__")]

    def data_visualization(self):
        dv = {
            "Defintion": "\n    - The graphic represententation of data",
            "\nWhy is it useful?": "\n    - Exploration:    nothing is known"
                                   "\n    - Analysis:    testing hypothesis"
                                   "\n    - Presentation:    communication of results",
            "\nBox plots": "\n    - Numerical variables per category"
                         "\n    - Comparing sub-groups"
                         "\n    - Identifying outliers"
                         "\n    - Quartiles and median"
                         "\n    - Min:    Q1 - 1.5(Q3 - Q1)"
                         "\n    - Max:    Q3 + 1.5(Q3 - q1)",
            "\nHeat maps": "\n    - helps decide to drop values"
                         "\n    - helps decide to uce mutation methods",
            "\nDisplay extra information by:": "\n    - N:    Color, intensity, size"
                                             "\n    - C:    Symbols color, multipanels"
                                             "\n    - T:    multipanels, animation",
            "\nScatter Plot Matrix": "\n    - Unsupervised:    cluster identification or finding associations"
                                     "\n    - Supervised:    Finding relationships, -> var transformation, -> var selection"
                                     "\n    - Outliers identification",
            "\nHuman perception": "\n    - Color:    is your friend if you use it with care"
                                  "\n    - Lines:    should connect related things"
                                  "\n    - Proximity:    things that are closer are easier to compare",
            "\nBest practices": "\n    - One message = one visualisation"
                                "\n    - Reduce clutter"
                                "\n    - Highlight what's important"
                                "\n    - Use proper scale"
                                "\n    - Proper x and y labels"
                                "\n    - Use legends\nx",
        }
        for k, v in dv.items():
            print(k, v)

    def dimension_reduction(self):
        dr = {
            "Why is it better?": "\n    - Too many vars lead to overfitting & models that are difficult to interpret",
            "\nReducing categories": "\n    - A single categorical variable with m categories is typically transformedinto m or m-1 dummy variables"
                                   "\n    - Each dummy variable takes the values 0 or 1"
                                   "\n    - Problem:    Can end up with too many variables"
                                   "\n    - Solution:    Reduce by combining categories that are close to each other",
            "\nPrincipal Component Analysis": "\n  ->  Goal:    Reduce a set of numerical variables"
                                            "\n  ->  The Idea:    Remove the overlap of information between these variables (“Information” is measured by the sum of the variances of the variables)"
                                            "\n  ->  Final product:    A smaller number of numerical variables that contain most of the information"
                                            "\n    - Create new variables that are linear combinations of the original variables (i.e. they are weighted averages of the original variables)"
                                            "\n    - These linear combinations are uncorrelated, and only a few of them contain most of the original information"
                                            "\n    - The new variables are called \"Principal components\""
                                            "\n    - Re-projection of points to new system"
                                            "\n    - Weighted linear combination of original vars"
                                            "\n    - Removes co-variation"
                                            "\n    - Total variability = sum of variances"
                                            "\n    - All information is kept in the sense of variability",
            "\nPCA: Important Notes": "\n    - Assumptions:    Higher variance = higher information content"
                                    "\n    - Normalization:    Data in different units"
                                    "\n    - PCA in classification / prediction:"
                                    "\n        - Apply PCA to training data"
                                    "\n        - Decide how many PC's to use"
                                    "\n        - Use variable weights in those PC's with validation/new data"
                                    "\n        - This creates a new reduced set of predictors in validation/new data"
        }
        for k, v in dr.items():
            print(k, v)

    def performance_measures(self):
        pm = {
            "Predictive performance": "\n    - Predictive accuracy != goodness-of-fit"
                                      "\n    - Statistical metrics → measures how well the model fits the data"
                                      "\n    - Data analytical metrics → measures how well the model performs on new data"
                                      "\n    - Key component of most measures is difference between actual y and predicted y (error)"
                                      "\n    - Naive benchmark:    prediction is the average across all observed outcomes"
                                      "\n    - Good prediction model outperforms Naive benchmark",
            "\nPerformance Assesment": "\n    - Histograms & box plots are very useful to assess performance"
                                     "\n    - Training errors usually smaller than validation error"
                                     "\n    - Overfitting indication:    training and validation errors are very different",
            "\nClassifier Performance": "\n  ->  Naive rule:"
                                      "\n    - Assign all records to majority class, often used as benchmark, we hope to do better than that"
                                      "\n    - Exception:    when goal is to identify high-value but rare outcomes, we may do well by doing worse than the naïve rule"
                                      "\n  ->  Seperation of records:"
                                      "\n    - \"High seperation of records\" means that using predictor variables attain low errors - Small dataset is enough "
                                      "\n    - \"Low seperation of records\" means that using predictor variables does not improve much on naïve rule - Large dataset does not help improve",
            "\nConfusion matrix & derived metrics": "\n    - Overall error = (false positive + false negative) / n"
                                                  "\n    - Overall accuracy = (true positive + true negative) / n"
                                                  "\n    - Sensitivity = true positive / (true positive + true negative)"
                                                  "\n    - Specificity = true negative / (false positive + true negative)"
                                                  "\n    - False discovery rate = false positive / (true positive + false positive)"
                                                  "\n    - False omission rate = false negative / (false negative + true negative)",
            "\nPropensities & Cutoffs": "\n  ->  For each record:"
                                      "\n    - Compute probability of belonging to class \"1\""
                                      "\n    - Compare to cutoff value, and classify accordingly"
                                      "\n    - If >= 0.50, classify as “1”"
                                      "\n    - If < 0.50, classify as “0”",
            "\nWhen one class is more important": "\n    - In many cases it is more important to identify members of one class"
                                                "\n    - In such cases, we are willing to tolerate greater overall error, in return for better identifying the important class for further attention"
                                                "\n    - If “C1” is the important class:"
                                                "\n        - Sensitivity (also called “recall) = % of “C1” class correctly classified"
                                                "\n        - Specificity = % of “C0” class correctly classified"
                                                "\n        - Precision = % of predicted “C1’s” that are actually “C1’s”",
            "\nLift Curves and Decile Charts": "\n    - Evaluates how well a model identifies the most important class"
                                             "\n    - Helps evaluate, e.g. how many tax records to examine, how many loans to grant, how many customers to mail offer to"
                                             "\n    - Compare performance of model to “no model, pick randomly”"
                                             "\n    - Measures ability of model to identify the important class, relative to the average prevalence of the class"
                                             "\n    - Charts give explicit assessment of results over a large number of cutoffs"
                                             "\n    - In lift curve:    compare step function to straight line"
                                             "\n    - In decile chart:    compare to ratio of 1"
                                             "\n  ->  Compute lift: Accumulate the correctly classified “important class” records (Y axis) and compare to number of total records (X axis)",
            "\nLift (gains) )curve vs decile charts": "\n    - Both embody concept of “moving down” through the records, starting with the most probable 1’s" \
                                                    "\n    - Decile chart does this in decile chunks of data  (Y axis shows ratio of decile mean to overall mean)"
                                                    "\n    - Lift curve shows continuous cumulative results  (Y axis shows number of important class records identified",
            "\nCumulative gain & Lift charts": "\n    - Compare predictive performance to baseline with no predictors"
                                             "\n    - Helps finding subset of records with highest cumulative performance",
            "\nOversampling & Undersamplingc": "\n    - Asymmetric costs/benefits typically go hand in hand with presence of rare but important class"
                                             "\n    - Often we oversample rare cases to give model more information to work with  (typically use 50% “1” and 50% “0” for training)"
                                             "\n    - Following graphs show optimal classification under threescenarios:"
                                             "\n        - Assuming equal costs of misclassification"
                                             "\n        - Assuming that misclassifying “o” is five times the cost of misclassifying “x”"
                                             "\n        - Oversampling scheme allowing methods to incorporateasymmetric costs"
                                             "\n  -> Relevant when dealing with rare classes"
                                             "\n  -> Possible solution:    Sample equal number of observations per class"
                                             "\n  -> Model evaluation options:    1. Score model on validation set randomly selected,    2. Score model on over/under-sampled validation & re-weight results!\n"
        }
        for k,v in pm.items():
            print(k, v)

    def python(self):
        p = {
            "Scatter plot": "\n    - df.plot.scatter(x = colA, y = colB)",
            "\nBox plot": "\n    - df.boxplot(column = colY, by = colX, grid = False)",
            "\nHistogram": "\n    - df.colname.hist(grid = False)",
            "\nHeat maps": "\n    - import seaborn as sns"
                         "\n    - sns.heatmap(df.corr(), annot = True, fmt = \".if\" , cmap = \"RdBu\")",
            "\nScatter plot matrix": "\n    - from pandas.plotting import scatter_matrix"
                                   "\n    - axes = scatter_matrix(df, figsize = (8, 8))"
        }
        for k, v in p.items():
            print(k, v)

    def tutorial(self):

        t = {
            "Packages":
                """
            import numpy as np
            import pandas as pd
            import matplotlib.pylab as plt
            import plotly.express as px
            import seaborn as sns

            from sklearn.decomposition import PCA
            from sklearn import preprocessing
            """,
            "\n\nBoxplot":
                """
            fig = px.box(df, x="CAT_MEDV", y="CRIM", log_y=True)
            fig.show()
            """,
            "\n\nHeatmap":
                """
            dataplot = sns.heatmap(df.corr(), cmap="RdBu", annot=True)
            sns.set(rc={"figure.figsize":(15, 10)})
            plt.show()
            """,
            "\n\nBinning RM variable":
                """
            df['RM_bin'] = pd.cut(df.RM, range(0, 10), labels=False)
            
            
            # TODO: bin the AGE variable with a bin size of 10
            # then create a pivot table of AGE_bin vs CHAS that displays the median of MEDV
            # and do show the labels this time
            
            df['AGE_bin'] = pd.cut(df.AGE, range(1, 110, 10), labels = ['0> Age <=10','10> Age <=20','20> Age <=30'
                                            ,'30> Age <=40','40> Age <=50','50> Age <=60','60> Age <=70','70> Age <=80','80> Age <=90','90> Age <=100'])
            pd.pivot_table(df, values='MEDV', index=['AGE_bin'], columns=['CHAS'],
                            aggfunc= np.median, margins=True)
            """,
            "\n\nFitting PCA":
                """
                pcs = PCA(n_components=2)
                pcs.fit(df_cereals[['calories', 'rating']])
                
                pcsComponents = pd.DataFrame(pcs.components_.transpose(),
                                            columns=['PC1', 'PC2'],
                                            index=['calories', 'rating'])
                                            
                # Use the `transform` method to get the scores, i.e. projected variables:
                scores = pd.DataFrame(pcs.transform(df_cereals[['calories', 'rating']]),
                                     columns=['PC1', 'PC2'])
                                     
                #TODO Now let's perform a principal component analysis of the whole table ignoring the first three non-numerical columns.
                
                pcs = PCA()

                pcs.fit(df_cereals.iloc[:, 3:].dropna(axis=0))
                pcsSummary = pd.DataFrame({'Standard deviation': np.sqrt(pcs.explained_variance_),
                                        'Proportion of variance': pcs.explained_variance_ratio_,
                                        'Cumulative proportion': np.cumsum(pcs.explained_variance_ratio_)})
                pcsSummary = pcsSummary.transpose()
                pcsSummary.columns = ['PC{}'.format(i) for i in range(1, len(pcsSummary.columns) + 1)]
                pcsSummary.round(4)
                
                pcsComponents = pd.DataFrame(pcs.components_.transpose(),
                                            columns=pcsSummary.columns,
                                            index=df_cereals.iloc[:, 3:].columns)
                                            
                # Dropping records with NaN values
                df_cereals_red = df_cereals.dropna(axis=0)
                df_cereals_red = df_cereals_red.reset_index(drop=True)

                # Re-projecting data to new system
                scores = pd.DataFrame(pcs.fit_transform(preprocessing.scale(df_cereals_red.iloc[:, 3:])),
                                    columns=['PC{}'.format(i) for i in range(1, len(pcsSummary.columns) + 1)])

                # Adding column with cereal names
                df_pca = pd.concat([df_cereals_red['Cereal name'], scores[['PC1', 'PC2']]], axis=1)

                df_pca.head()
            """
        }
        for k,v in t.items():
            print(k, v)
# -------------------------------------------------------------------------------------------------------------------- #

class L3:

    def __init__(self):
        self.content = [func for func in dir(L3) if callable(getattr(L3, func))]
        self.content = [func for func in self.content if not func.startswith("__")]

    def decision_trees(self):

        dt = {
            "Trees and Rules": "\n  ->  Goal:    Classify or predict an outcome based on a set of predictors"
                               "\n    - The output is a set of rules"
                               "\n  ->  Example:"
                               "\n      - Goal:    lassify a record as “will accept credit card offer” or “will not accept”"
                               "\n      - Rule might be “IF (Income >= 106) AND (Education < 1.5) AND (Family <= 2.5) THEN Class = 0 (nonacceptor)"
                               "\n      - Also called CART, Decision Trees, or just Trees"
                               "\n      - Rules are represented by tree diagrams"
                               "\n  ->  Key Ideas:"
                               "\n      - Recursive partitioning / split on predictors: for constructing"
                               "\n      - Pruning: limiting size",
            "\nDecision Rule": "\n    - Easily understandable rules, if tree is not too big"
                             "\n    - Each leaf node is equivalent to a classification rule",
            "\nPredicting new record": "\n    - Drop record down the tree until it reaches a leaf node"
                                     "\n    - Assign class taking a vote / prediction taking average\n"
        }

        for k, v in dt.items():
            print(k, v)
    def classification_trees(self):

        ct = {
            "How is the tree produced?": "\n    - Recursive partitioning:    Repeatedly split the records into two parts so as to achieve maximum homogeneity of outcome within each new part"
                                         "\n    - Stopping Tree Growth:    A fully grown tree is too complex and will overfit",
            "\nBuilding a classification tree": "\n    - Algorithm checks all possible splits and chooses the best one"
                                              "\n      - Numerical splits =    mid-points between pairs of consecutive values, e.g. income (38.1, ..., 109.5)"
                                              "\n      - Categorical splits =    all possible combinations for two groups, e.g. categories {a, b, c} divided into three"
                                              "\n        [{a}, {b, c}]; [{b}, {a, c}]; [{c}, {a, b}]"
                                              "\n    - Splits ranked by how much impurity is reduced on rectangle"
                                              "\n      - Impurity reduction =    Impurity before split - Sum of impurities after split"
                                              "\n    - Normalization is not needed",
            "\nRecursive partitioning steps": "\n    - Pick one of the predictor variables, xi"
                                            "\n    - Pick a value of xi, say si, that divides the training data into two (not necessarily equal) portions"
                                            "\n    - Measure how “pure” or homogeneous each of the resulting portions is “Pure” = containing records of mostly one class (or, for prediction, records with similar outcome values)"
                                            "\n    - Algorithm tries different values of xi, and si to maximize purity in initial split"
                                            "\n    - After you get a “maximum purity” split, repeat the process for a second split (on any variable), and so on",
            "\nMeasuring impurity": "\n    - Gini impurity index"
                                    "\n      - Gini(A) = 1 − ∑mk=1 (pk)^2"
                                    "\n      - pk = proportion of records in rectangle A that belongs to k"
                                    "\n      - Gini ranges from {0, (m − 1)/m}"
                                    "\n    - Entropy measure"
                                    "\n      - Entropy(A) = − ∑mk=1 pklog2 (pk)"
                                    "\n      - Entropy ranges from {0, log2(m)}",
            "\nImpurity and Recursive Partitioning": "\n    - Obtain overall impurity measure (weighted avg. of individual rectangles)"
                                                     "\n    - At each successive stage, compare this measure across all possible splits in all variables"
                                                     "\n    - Choose the split that reduces impurity the most"
                                                     "\n    - Chosen split points become nodes on the tree",
            "\nOverfitting": "\n    - Deep trees are likely to produce overfitting"
                             "\n    - A) Tree properly modelling relationships"
                             "\n    - B) Overfitting → high discrepancy between train and validation errors"
                             "\n    - Overfitting & instability produce poor predictive performance – past a certain point in tree complexity, the error rate on new data starts to increase",
            "\nCross valdation": "\n    - With cross validation (CV), test multiple trees"
                               "\n    - Partition data into sets (folds) for model-fitting, and data for evaluating"
                               "\n    - Fit model with training fold, and evaluate with holdout fold"
                               "\n    - Repeat, typically with evaluation folds that are non-overlapping and smaller than training folds"
                               "\n    - e.g. 5-fold CV fits 5 models, each evaluated on 20% of the data that is held out, with each set of evaluation data non-overlapping with the others",
            "\nBuilding Regression Trees": "\n    - Differences from classification trees:"
                                           "\n      - Prediction:    Computed as the average of numerical target variable in the rectangle (in CT it is majority vote)"
                                           "\n      - Impurity:    measured by sum of squared deviations from leaf node"
                                           "\n      - Performance:    measured by RMSE (root mean squared error), same as for any prediction models"
        }
        for k,v in ct.items():
            print(k, v)

    def improving_predictions(self):
        ip = {
            "Random Forests": "\n    - Basic idea:    Taking an average of multiple estimates (models) is more reliable than just using a single estimate"
                              "\n    1. Draw multiple random samples from data (”bootstrap resampling”)"
                              "\n    2. Fit tree to each resample using a random set of predictors"
                              "\n    3. Combine the classifications/predictions from all the resampled trees (the “forest”) to obtain improved predictions",
            "\nVariable importance": "\n    - Each variable is used by some trees and not others"
                                   "\n    - We can, therefore, measure each variable’s contribution to reducing impurity (reduction in Gini Index)"
                                   "\n    - This is the variable importance score"
                                   "\n  ->  Can be used for variable selection",
            "\nBoosted Trees": "\n    - Fits a succession of single trees"
                               "\n    - Each successive fit up-weights the misclassified records from prior stage"
                               "\n    - You now have a set of classifications or predictions, one from each tree"
                               "\n    - Use weighted voting for classification, weighted average for prediction, higher weights to later trees"
                               "\n    - Especially useful for the “rare case” scenario (suppose 1’s are the rare class)"
                               "\n    - With simple classifiers, it can be hard for a “1” to “break out” from the dominant classification, & many get misclassified"
                               "\n    - Up-weighting them focuses the tree fitting on the 1’s, and reduces the dominating effect of the 0’s"
                               "\n\n    1. Fit single tree"
                               "\n    2. Draw sample that gives highest selection probability to misclassified records"
                               "\n    3. Fit tree to new sample"
                               "\n    4. Repeat steps 2 & 3 multiple times"
                               "\n    5. Use weighted voting to classify records giving more weight to later trees",
            "\nPro's of decision trees": "\n    - Easy to use, understand"
                                         "\n    - Single trees produce rules that are easy to interpret & implement"
                                         "\n    - Variable selection & reduction is automatic"
                                         "\n    - Robust to outliers"
                                         "\n    - Non-linear & non-parametric"
                                         "\n    - Good for high degree of separation"
                                         "\n    - Handles missing data"
                                         "\n    - Do not require the assumptions of statistical models",
            "\nCons of decision trees": "\n    - Sensitive to changes in data"
                                        "\n    - Misses relationships between vars"
                                        "\n    - Bad for diagonal splits"
                                        "\n    - Requires large datasets"
                                        "\n    - Can be computationally expensive"
                                        "\n    - Favors vars with many splits"
                                        "\n    - Ensembles lose interpretability"
        }
        for k, v in ip.items():
            print(k, v)

    def tutorial(self):

        t = {
            "Data Partition":
                """
                # Splitting data into train/validation sets
                X_train, X_valid, y_train, y_valid = train_test_split(X, y, test_size=0.4, random_state=1)
                
                classTree = DecisionTreeClassifier()
                
                # TODO: what do we need to give as input for fit?
                classTree.fit(X_train, y_train)
                
                def tree_visualization(decisionTree, feature_names=None, class_names=None):
    
                    plt.figure(figsize=(60, 30))
                     tree.plot_tree(decisionTree, filled=True, rounded=True, impurity=False,
                                    feature_names=feature_names, class_names=class_names, label='root')

                    return plt.show()
                    
                    tree_visualization(classTree, feature_names=X_train.columns)
                    
                    # Performance with training data
                    y_pred = classTree.predict(X_train)
                    cm = confusion_matrix(y_train, y_pred)
                    accuracy = accuracy_score(y_train, y_pred)
                    settype = 'Train'
                    
                    sns.heatmap(cm, annot=True, fmt="d", cbar=False)
                    plt.title('%s accuracy = %f' % (settype, accuracy))
                    plt.xlabel('Prediction')
                    plt.ylabel('Actual')
                    plt.show()
            """
        }
        for k,v in t.items():
            print(k, v)
# -------------------------------------------------------------------------------------------------------------------- #

class L4:
    """Unsupervised models: Clustering"""
    def __init__(self):
        self.content = [func for func in dir(L4) if callable(getattr(L4, func))]
        self.content = [func for func in self.content if not func.startswith("__")]

    def cluster_analysos(self):
        d = {
            "Main Idea": "\n    - Goal: Form groups (clusters) of similar records"
                         "\n    - Used for segmenting markets into groups of similar customers",
            "\nPrediction": "\n    - Clustering is used in many areas from astronomy to sociology"
                          "\n    - lustering → segments the data"
                          "\n    - Useful to improve performance of supervised methods"
                          "\n      - Model clusters separately instead of heterogeneous dataset",
            "\nMore than 2 dimensions": "\n    - Multiple dimensions require formal algorithm with (1) a distance measure and (2) a way to use the distance measure in forming clusters"
                                      "\n    - hierarchical vs non-hierarchical algorithms\n"
        }
        for k,v in d.items():
            print(k, v)

    def measuring_distance(self):
        d = {
            "Distance between records": "\n    - Record i: (xi1, xi2, ..., xip)"
                                        "\n    - Record j: (xj1, xj2, ..., xjp)"
                                        "\n    - d_ij: distance metric dissimilarity measure"
                                        "\n    - Properties for distances"
                                        "\n    - Non-negative: d_ij ≥ 0"
                                        "\n    - Self-proximity: d_ii = 0"
                                        "\n    - Symmetry: d_ij = d_ji"
                                        "\n    - riangle inequality: d_ij ≤ d_ik + d_kj",
            "\nEuclidean distance": "\n    - dij = √(xi1 − xj1)2 + (xi2 − xj2)2 + ... + (xip − xjp)2"
                                  "\n    - Normalization before computing distances, z-score"
                                  "\n    - Unequal weights possible"
                                  "\n    - Feautures of this measure: highly scale dependent, ignores vars relationships, sensitive to outliers",
            "\nNormalizing": "\n    - Problem:    Raw distance measures are highly influenced by scale of measurement"
                           "\n    - Solution:    Normalize (standardize) the data first",
            "\nChoosing distance measures": "\n    - Euclidean → dissimilarity"
                                          "\n    - Square of Pearson → correlation-based similarity"
                                          "\n    - Mahalanobis → accounts for correlation between vars"
                                          "\n    - Manhattan → absolute distance"
                                          "\n    - Maximum → vars with highest deviation",
            "\nDistance for categorical variables": "\n    - Example: binary variables"
                                                  "\n    - Matching coeﬀicient: (a+d)/p"
                                                  "\n    - Jaquard’s coeﬀicient: d/(b+c+d)"
                                                  "\n    - Gower’s similarity: mixed data",
            "\nDistance between clusters": "\n    - Minimum distance: min{d(Ai, Bj)}"
                                         "\n    - Maximum distance: max{d(Ai, Bj)}"
                                         "\n    - Average distance: mean{d(Ai, Bj)}"
                                         "\n    - Centroid distance: d(xA, xB)"
                                         "\n    - entroid: xA =[( 1/m∑mi=1 xi1, ..., 1/m∑mi=1 xip)]",
            "\nHierarchical Methods": "\n  ->  Agglomerative Methods:"
                                    "\n      - Begin with n-clusters (each record its own cluster)"
                                    "\n      - Keep joining records into clusters until one cluster is left (the entire data set)"
                                    "\n      - Most popular"
                                    "\n  ->  Divisive Methods:"
                                    "\n      - Start with one all-inclusive cluster"
                                    "\n      - Repeatedly divide into smaller clusters"
        }
        for k, v in d.items():
            print(k, v)

    def clustering_techniques(self):

        d = {
            "Linkage type": "\n    - Single-link"
                            "\n    - Complete-link"
                            "\n    - Average-link"
                            "\n    - Centroid distance",
            "\nWards Method": "\n    - Measures information loss from grouping records"
                            "\n    - Information loss = error sum of squares = ∑mi=1(xi − ˆx)2",
            "\nDendrograms": "\n    - Summarizes process of clustering"
                             "\n    - x-axis: records"
                             "\n    - y-axis: distance"
                             "\n    - Cutoff distance: horizontal line"
                             "\n  ->  See process of clustering: Lines connected lower down aremerged earlier",
            "K-means": "\n    - Pre-specified number of clusters"
                       "\n    - Minimize measure of dispersion within clusters  --> (1) Sum of distances of records to centroid (2) Sum of squared Euclidean distances of records to centroid"
                       "\n   1. Start with k initial clusters"
                       "\n   2. At every step, each record is reassigned to cluster with closest centroid"
                       "\n   3. Recompute centroid of clusters that lost/gained records and repeat 2"
                       "\n   4. Stop when moving records increases cluster dispersion",
            "Validating Clusters": "\n  ->  Goal: obtain meaningful and useful clusters"
                                   "\n  -> Caveats:    (1) (1) Random chance can often produce apparent clusters  (2)  Different cluster methods produce different results"
                                   "\n  -> Solutions: "
                                   "\n    - Obtain summary statistics"
                                   "\n    - Also review clusters in terms of variables not used in clustering"
                                   "\n    - Label the cluster (e.g. clustering of financial firms in 2008 might yield label like “midsize, sub-prime loser”)"
                                   "\n  ->  Separation:    Check ratio of between-cluster variation to within-cluster variation (higher is better)"
        }
        for k,v in d.items():
            print(k, v)

    def time_series(self):
        d = {
            "Applications": "\n    - Governments → tax receipts and spending"
                            "\n    - World Bank and IMF → inflation, economic activity"
                            "\n    - Energy companies → reserves, production, demand, prices"
                            "\n    - Transport → number of passengers"
                            "\n    - Retail stores → sales",
            "\nDescriptive vs Predictive": "\n  ->  Descriptive:    Trends, Seasonal patterns, Seasonal patterns"
                                         "\n  ->  Predictive:    Single TS Forecasting, Multivariate TS forecasting",
            "\nComponents of TS": "\n    - Level:    average value of the series"
                                "\n    - Trend:    change in TS from one period to next"
                                "\n    - Seasonality:    Short-term cyclical behaviour"
                                "\n    - Noise:     random variation from measurement error or other non accounted for causes",
            "\nTime-series forecasting": "\n  ->  Model-driven:"
                                       "\n    - Regression-based forecasting"
                                       "\n    - Analyst needs to specify model"
                                       "\n    - Assumptions about data structure"
                                       "\n    - Good for global patterns"
                                       "\n  ->  Data-driven:"
                                       "\n    - Smoothing-based methods"
                                       "\n    - Method learns patterns from data"
                                       "\n    - Good for local patterns",
            "\nForecasting new values": "\n    - Before forecasting recombine train and validation TS’s and re-run model"
                                        "\n  ->  Why?"
                                        "\n    - Validation is most recent and has valuable information"
                                        "\n    - More data improves accuracy"
                                        "\n    - Otherwise needs to forecast even further into future",
            "\nAutocorrelation": "\n    - Stickiness: positive lag-1 autocorrelation"
                               "\n    - Swings: negative lag-1 autocorrelation, high values followed by low values",
            "\nSecond-level forecasting model": "\n    - Generate Ft+k (k-step ahead) forecast using forecast model"
                                              "\n    - Generate Et+k forecast of residuals using AR model"
                                              "\n    - Improved forecast: F∗t+k = Ft+k + Et+k"
                                              "\n  ->  AutoRegressive Integrated Moving Average (ARIMA) models = Very flexible forecasting method",
            "\nMoving Average": "\n    - Average values across a window of consecutive periods"
                              "\n  ->  Centered moving average:"
                              "\n      - MAt = 1/w (Yt−(w−1)/2 + ... + Yt−1 + Yt + Yt+1 + ... + Yt+(w−1)/2)"
                              "\n      - Good for visualizing trends"
                              "\n      - Can remove seasonality and noise"
                              "\n  ->  Trailing moving average"
                              "\n      - Ft+k = 1/w (Yt + Yt−1 + ... + Yt−w+1)"
                              "\n      - Useful for forecasting"
                              "\n      - Not good for TS with trend and/or seasonality",
            "\nChoosing window": "\n    - Balance between over/under-smoothing"
                               "\n  ->  Centered:"
                               "\n      - Wider exposes global trends"
                               "\n      - Wider exposes global trends"
                               "\n  ->  Trailing:"
                               "\n      - Relevance of past values"
                               "\n      - How fast does TS change?"
                               "\n      - Empirical search, but be carefull with overfitting",
            "\nSimple exponential smoothing": "\n    - Weighted average of all past values"
                                              "\n      - Weights decrease exponentially into past"
                                              "\n      - Recent information has higher influence"
                                              "\n      - But past information is not ignored"
                                              "\n  ->  Exponential smoothing forecaster:"
                                              "\n      - Ft+1 = αYt + α(1 − α)Yt−1 + α(1 − α)2Yt−2 + ..."
                                              "\n      - Ft+1 = Ft + αEt"
                                              "\n      - Method is active learner"
                                              "\n      - Not fit for TS with trend and/or seasonality"
                                              "\n      - Can be applied to TS of residuals",
            "\nChoosing α": "\n    - Determines rate of learning"
                          "\n      - Close to 1: fast learning (recent values have more influence)"
                          "\n      - Close to 0: slow learning (past has more influence)"
                          "\n    - α = 0.1 − 0.2 leads to good results in general"
                          "\n    - Empirical search can be done, but attention to overfitting",
            "\nAdvanced Exponential Smoothing": "\n    - Can capture trend and seasonality"
                                              "\n    - Trend shape is not assumed to be global and can change over time"
                                              "\n    - Future forecasts are no longer identical"
                                              "\n    - Lt: weighted average of actual period and level in previous adjusted by trend"
                                              "\n    - Tt: weighted average of trend in previous period and recent change of level"
        }
        for k,v in d.items():
            print(k, v)

    def tutorial(self):

        t = """"
        pip install dmba
        
        import dmba

        import pandas as pd
        import matplotlib.pylab as plt
        import seaborn as sns
        
        from sklearn import preprocessing
        from sklearn.metrics import pairwise
        from sklearn.cluster import KMeans
        from scipy.cluster.hierarchy import dendrogram, linkage, fcluster
        from pandas.plotting import parallel_coordinates
        
        %matplotlib inline
        
        
        df = dmba.load_data('Utilities.csv')
        df.set_index('Company', inplace=True)
        
        
        # Notice the similarity between the following two lines of codes
        
        (1) df['Cost'] = df['Cost'].astype('float64') <= Changing one column at a time
        (2) df = df.apply(lambda x: x.astype('float64')) # <= Change all columns at once
        
        !!! Distance between points !!!!
        
        d = pairwise.pairwise_distances(df, metric='euclidean')
        pd.DataFrame(d, columns=df.index, index=df.index).head()
        
        # Compute the Manhattan distance between the points
        d = pairwise.pairwise_distances(df, metric='manhattan')
        df_d = pd.DataFrame(d, columns=df.index, index=df.index)
        df_d.head()
        
        # Approach 1: (Using scikitlearn) Population standard deviation
        df_norm = df.apply(preprocessing.scale, axis=0)
        
        # Approach 2: (Using Pandas) Sample standard deviation
        df_norm = (df - df.mean())/df.std()
        
        d_norm = pairwise.pairwise_distances(df_norm, metric='euclidean')
        pd.DataFrame(d_norm, columns=df.index, index=df.index).head()
        
        # How to use "linkage" funciton: https://docs.scipy.org/doc/scipy/reference/generated/scipy.cluster.hierarchy.linkage.html
        Z = linkage(df_norm, method='single', metric='euclidean')
        
        fig = plt.figure(figsize=(10, 6))
        fig.subplots_adjust(bottom=0.23)
        plt.title('Hierarchical Clustering Dendrogram (Single linkage)')
        plt.xlabel('Company')
        dendrogram(Z, labels=list(df_norm.index), color_threshold=2.75)
        plt.axhline(y=2.75, color='black', linewidth=0.5, linestyle='dashed')
        plt.show()
        
        
        # Run hierarchical clustering using average linkage and Euclidean distance
        # Plot the result of the algorithm as a dendrogram and use a cutoff of 3.6
        Z = linkage(df_norm, method='average', metric='euclidean')
        
        fig = plt.figure(figsize=(10, 6))
        fig.subplots_adjust(bottom=0.23)
        plt.title('Hierarchical Clustering Dendrogram (Average linkage)')
        plt.xlabel('Company')
        dendrogram(Z, labels=list(df_norm.index), color_threshold=3.6)
        plt.axhline(y=3.6, color='black', linewidth=0.5, linestyle='dashed')
        plt.show()
        
        
        # TODO: run k-Means for k=3 and check the cluster membership
        kmeans = KMeans(n_clusters=3, random_state=0).fit(df_norm)
        kmeans3 = pd.Series(kmeans.labels_, index=df_norm.index)
        for key, item in kmeans3.groupby(kmeans3):
            print(key, ': ', ', '.join(item.index))
        """

    def tut_5(self):
        txt = """
        df_ridership['Date'] = pd.to_datetime(df_ridership.Month, format='%d/%m/%Y')
        
        # plot ts line plot
        ax = df_ts.plot(figsize=(10,5))
        ax.set_xlabel('Time')
        ax.set_ylabel('Ridership (in 000s)')
        ax.set_ylim(1300, 2300)
        plt.show()
        
        # add trend
        df = tsatools.add_trend(df_ts, trend='ct')

        # partition data
        m_test = 36
        m_train = len(df) - m_test
        
        df_train = df[:m_train]
        df_train.tail()
        
        # fit trend
        ridership_trend = sm.ols(formula='Ridership ~ trend + np.square(trend)', data=df_train).fit()
        
        fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(9, 7.5))

        ridership_trend.predict(df_train).plot(ax=axes[0], color='C1')
        ridership_trend.predict(df_test).plot(ax=axes[0], color='C1', linestyle='dashed')
            
        residual = df_train.Ridership - ridership_trend.predict(df_train)
        residual.plot(ax=axes[1], color='C1')
        residual = df_test.Ridership - ridership_trend.predict(df_test)
        residual.plot(ax=axes[1], color='C1', linestyle='dashed')
        graph_layout(axes, df_train, df_test)
        plt.show()
        
        # modelling seasonality
        ax = df_ts['1997':'1999'].plot(figsize=(10,5))
        ax.set_xlabel('Time')
        ax.set_ylabel('Ridership (in 000s)')
        ax.set_ylim(1300, 2310)
        plt.show()
        
        # re-partition + fit seasonality
        df_train = df[:m_train]
        df_test = df[m_train:]
        ridership_season = sm.ols(formula='Ridership ~ C(Month)', data=df_train).fit()
        
        
        
        fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(9, 7.5))

        ridership_season.predict(df_train).plot(ax=axes[0], color='C1')
        ridership_season.predict(df_test).plot(ax=axes[0], color='C1', linestyle='dashed')
        
        residual = df_train.Ridership - ridership_season.predict(df_train)
        residual.plot(ax=axes[1], color='C1')
        residual = df_test.Ridership - ridership_season.predict(df_test)
        residual.plot(ax=axes[1], color='C1', linestyle='dashed')
        
        graph_layout(axes, df_train, df_test)
        
        plt.show()
        """
        print(t)

#--------------------------------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------------------------------------------#

