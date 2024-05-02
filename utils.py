import pandas as pd
import os as os
from decimal import Decimal


def readWeights():
    print('Read weight file')
    Weights = pd.read_csv('Config/Pesos.csv', delimiter=';')
    print(Weights)
    return Weights

def readDataset():
    print('Read dataset file')
    Dataset = pd.read_csv('Config/Dataset.csv', delimiter=';')
    return Dataset

def getMaxAndMin(Dataset):
    MaxValuePerColumn = {}
    MinValuePerColumn = {}
    print('Get max and min values for each column and save on the dictionaries')
    for columnName in Dataset:
        MaxValuePerColumn[columnName] = Dataset[columnName].max()
        MinValuePerColumn[columnName] = Dataset[columnName].min()
    return (MaxValuePerColumn, MinValuePerColumn)

def sumWeights(Weights):
    print('Sum Weights')
    WeightsSum = Weights.iloc[0].sum(axis=0)
    return WeightsSum

def readInput():
    print('Read all inputs from the code')
    Inputs = {}

    for file in os.listdir('Input'):
        tempDF = pd.read_csv('Input/'+file, delimiter=';')
        #Add case to list of cases
        Inputs[
            #Get name of file
            file[
               0:file.find('.')
            ]
        ] = tempDF
    return Inputs

def calcSimilarity(Inputs, Dataset, Weights, WeightsSum, MaxValuePerColumn, MinValuePerColumn, nameInput):
    print('Calculate similarities of all cases into a dataframe')
    Outputs = {}
    for name, case in Inputs.items():
        if nameInput != '' and name != nameInput:
            continue
        #Create a dataset for this output
        tempDF = Dataset.copy()

        #init sum of similarities
        SumOfColumnSimilarity = 0

        #Find the row of the input based on country and week
        rowsOfCase = tempDF.loc[(tempDF['Entity'] == case['Entity'].iloc[0]) & (tempDF['Week'] == case['Week'].iloc[0])]

        #check if row is found based on country name
        if len(rowsOfCase) == 0:
            print('O caso ' + name + ' possui um país não identificado')
            exit(400)

        #Get first row of the search dataframe
        rowOfCase = rowsOfCase.copy().iloc[0]

        #Assign the value of the area burnt of the searched row to the case row
        rowOfCase['area burnt by wildfires in 2024'] = case['area burnt by wildfires in 2024'][0]


        #For each column in dataset
        #for _, row in tempDF.iterrows():
        for columnName in tempDF:
            #Check if column is numerical
            try:
                float(tempDF.iloc[0][columnName])
            except:
                continue
            if columnName == 'Week':
                continue
            # Sum the similarities of all columns based on the numeric similarity formula
            print(columnName)
            tempDF[columnName] = tempDF[columnName].apply(lambda row: Decimal(str(row)))
            decimalValueOfRowFound = Decimal(str(rowOfCase[columnName]))

            SumOfColumnSimilarity += (
                (1 -(
                        abs((tempDF[columnName] - decimalValueOfRowFound))
                        /
                        (MaxValuePerColumn[columnName] - MinValuePerColumn[columnName])
                        )
                 )
                        * Decimal(str(Weights[columnName][0]))
            )
            #print(float(rowOfCase[columnName]))
            print(SumOfColumnSimilarity)
        SumOfColumnSimilarity /= Decimal(str(WeightsSum))
        print('Similarity of the output '+ name)
        print(SumOfColumnSimilarity)
        tempDF['Similarity'] = SumOfColumnSimilarity
        Outputs[name] = tempDF

        #tempDF['Similarity'] = SumOfColumnSimilarity
    return Outputs

def writeOutput(Outputs):
    print('Writing outputs')
    for name, similarity in Outputs.items():
        print(f'Writing {name}')
        similarity.to_csv('Output/'+name+'.csv')

def writeWeights(Weights):
    print('Writing Weights')
    Weights.to_csv('Config/Pesos.csv', sep=';',index=False)

def writeInput(Input, name):
    print('Writing Input')
    Input.to_csv(f'Input/{name}.csv', sep=';',index=False)

