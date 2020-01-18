class Prepro:
    """
    
    Data cleaning and preprocessing class .
    
    
    ----------
    Parameters
    
    data : pandas Dataframe object
        The main data frame to clean and preprocess .
        (Target column must no be included)
    
    target : pandas Series or DataFrame column
        The target column of classification .
        
    
    ----------
    Methods 
    
    data_split : Splitting data into categorical and numerical seperate dataframes
    
    data_join  : Joins 2 dataframes into one .
    
    scaler     : Applies Sklearn MinMax or Standard scaler to the selected data
    
    onehot     : Applies One Hot Encoder to the selected data
    
    ACP        : Projects data into lower dimensional space using Sklearn PCA
    
    Kmeans     : Kmeans clustering
    
    
    """

    def __init__(self, data, target):
        import pandas as pd
        import numpy as np
        self.data = data
        self.target = target
        self.quali = None
        self.numdisc = None
        self.num = None
        self.kmlab = None

    def data_split(self, num, numdisc, quali):
        """
        
        Splitting data into categorical and numerical seperate dataframes
        
         ----------
        Parameters
        
        num     : array of indexes of numerical Continuous variables
        
        numdisc : array of indexes of numerical discrete variables
        
        quali   : array of indexs of categorical variables
        
        """

        if len(num) > 0:
            num = np.array(num)
            data_num = data.iloc[:, num[0]]
            num = np.delete(num, 0)
            for i in num:
                data_nums = data.iloc[:, i]
                data_num = pd.concat([data_num, data_nums], axis=1)
            self.num = pd.DataFrame(data_num)

        if len(numdisc) > 0:
            numdisc = np.array(numdisc)
            data_catn = data.iloc[:, numdisc[0]]
            numdisc = np.delete(numdisc, 0)
            for i in numdisc:
                data_catns = data.iloc[:, i]
                data_catn = pd.concat([data_catn, data_catns], axis=1)
            self.numdisc = pd.DataFrame(data_catn)

        if len(quali) > 0:
            quali = np.array(quali)
            data_cat = data.iloc[:, quali[0]]
            quali = np.delete(quali, 0)
            for i in quali:
                data_cats = data.iloc[:, i]
                data_cat = pd.concat([data_cat, data_cats], axis=1)
            self.quali = pd.DataFrame(data_cat)

    def ACP(self, data, n_comp):
        """
        args : 
        data : pandas data frame
        n_comp : number of acp components 
        
        Applies sklearn PCA
        
        """
        from sklearn.decomposition import PCA
        acp = PCA(n_components=n_comp).fit(data)
        print("La variance expliquée pour", n_comp,
              "composantes est : ", sum(acp.explained_variance_ratio_))
        return pd.DataFrame(acp.transform(data))

    def data_join(self, data1, data2):
        """
        returns join of data1 and data2
        
        data1 , data2 : pandas DataFrames to be joined together
        """
        return pd.DataFrame(pd.concat([data1, data2], axis=1))

    def Kmenas(self, data, n_cl):
        """
        data , n_cl: number of clusters
        
        Applies Sklearn kmeans to data and returns pandas crosstab with the target from the main DS2PIPE
        
        """

        from sklearn.cluster import KMeans
        kmeans = KMeans(n_clusters=n_cl)
        kmeans.fit(data)
        self.kmlab = kmeans.labels_
        return pd.crosstab(self.target, self.kmlab)
