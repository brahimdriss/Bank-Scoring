class Prepro:
    """
    
    Data cleaning and preprocessing class .
    
    Parameters
    
    data : pandas Dataframe object
        The main data frame to clean and preprocess .
        (Target column must no be included)
    
    target : pandas Series or DataFrame column
        The target column of classification .

    ----------
    Attributes

    data        :  the data argument
    target      :  the target argument
    quali       :  Dataframe containing the quali variables created after data_split (Default = None)
    numdisc     :  Dataframe containing the numerical discrete variables created after data_split (Default = None)
    num         :  Dataframe containing the numerical continuous created after data_split (Default = None)

    
    ----------
    Methods 
    
    data_split : Splitting data into categorical and numerical seperate dataframes
    data_join  : Joins 2 dataframes into one .
    scaler     : Applies Sklearn MinMax or Standard scaler to the selected data
    onehot     : Applies One Hot Encoder to the selected data
    ACP        : Projects data into lower dimensional space using Sklearn PCA
    
    (Not Working)
    # Kmeans     : Kmeans clustering
        
    """

    def __init__(self, data, target):
        self.data = data
        self.target = target
        self.quali = None
        self.numdisc = None
        self.num = None
        self.kmlab = None

    def data_split(self, num, numdisc):
        """
        
        Splitting data into categorical and numerical seperate dataframes 

        The new dataframes are stored as attributes for the Prepro instance .
        
         ----------
        Parameters
        
        num     : array of indexes of numerical Continuous variables
        
        numdisc : array of indexes of numerical discrete variables
        
        quali   : array of indexs of categorical variables
        
        """
        import pandas as pd
        import numpy as np

        if len(num) > 0:
            num = np.array(num)
            data_num = self.data.iloc[:, num[0]]
            num = np.delete(num, 0)
            for i in num:
                data_nums = self.data.iloc[:, i]
                data_num = pd.concat([data_num, data_nums], axis=1)
            self.num = pd.DataFrame(data_num)

        if len(numdisc) > 0:
            numdisc = np.array(numdisc)
            data_catn = self.data.iloc[:, numdisc[0]]
            numdisc = np.delete(numdisc, 0)
            for i in numdisc:
                data_catns = self.data.iloc[:, i]
                data_catn = pd.concat([data_catn, data_catns], axis=1)
            self.numdisc = pd.DataFrame(data_catn)

        # if len(quali) > 0:
        #     quali = np.array(quali)
        #     data_cat = data.iloc[:, quali[0]]
        #     quali = np.delete(quali, 0)
        #     for i in quali:
        #         data_cats = data.iloc[:, i]
        #         data_cat = pd.concat([data_cat, data_cats], axis=1)
        #     self.quali = pd.DataFrame(data_cat)

        data_cat = self.data.select_dtypes(include=['object'])
        if data_cat.shape[1]>0:
            self.quali = pd.DataFrame(data_cat)

    def ACP(self, data, n_comp):
        """
        Returns the reduced data after applying sklearn PCA  

        args : 

        data : pandas data frame
        n_comp : number of acp components 
                
        """
        from sklearn.decomposition import PCA
        import pandas as pd
        acp = PCA(n_components=n_comp).fit(data)
        print("La variance expliquée pour", n_comp,
              "composantes est : ", sum(acp.explained_variance_ratio_))
        return pd.DataFrame(acp.transform(data))

    def data_join(self, data1, data2):
        import pandas as pd
        """
        returns join of data1 and data2
        
        data1 , data2 : pandas DataFrames to be joined together
        """
        return pd.DataFrame(pd.concat([data1, data2], axis=1))

    # def Kmenas(self, data, n_cl):
    #     """
    #     data , n_cl: number of clusters
        
    #     Applies Sklearn kmeans to data and returns pandas crosstab with the target from the main DS2PIPE
        
    #     """

    #     from sklearn.cluster import KMeans
    #     kmeans = KMeans(n_clusters=n_cl)
    #     kmeans.fit(data)
    #     self.kmlab = kmeans.labels_
    #     return pd.crosstab(self.target, self.kmlab)

    def onehot(self,data_cat):
        """
        Returns the categorical data passed as parameter after Onehot encoding the columns
         
        """
        import pandas as pd

        for col in data_cat:
            onehot = pd.get_dummies(data_cat[col])
            data_cat = data_cat.drop(col, axis=1)
            data_cat = data_cat.join(onehot)
        
        return data_cat

    def scaler(self,data_num,opt = 1):
        """
        Returns a scaled dataframe from numerical Dataframe given as parameter

        opt :

        0 = MinMaxScaler
        1 = StandardScaler
        """
        from sklearn.preprocessing import MinMaxScaler
        from sklearn.preprocessing import StandardScaler
        import pandas as pd

        if opt==0:
            scaler = MinMaxScaler()
        else:
            scaler = StandardScaler()
        
        data_num_sc = pd.DataFrame(scaler.fit_transform(data_num), columns=data_num.columns)
        
        return data_num_sc
