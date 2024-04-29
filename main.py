import pandas as pd
import os as os
from decimal import Decimal

print('Read input files')
Weights = pd.read_csv('Config/Pesos.csv', delimiter=';')
Dataset = pd.read_csv('Config/Dataset.csv', delimiter=';')

print('Initialize memory position for minimum and maximun values for similarity calculation')
MaxValuePerColumn = {}
MinValuePerColumn = {}

print('Get max and min values for each column and save on the dictionaries')
for columnName in Dataset:
    MaxValuePerColumn[columnName] = Dataset[columnName].max()
    MinValuePerColumn[columnName] = Dataset[columnName].min()

print('Sum Weights')
WeightsSum = Weights.iloc[0].sum(axis=0)

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

print('Calculate similarities of all cases into a dataframe')
Outputs = {}
for name, case in Inputs.items():

    #Create a dataset for this output
    tempDF = Dataset

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
    print('Similarity of the output')
    print(SumOfColumnSimilarity)
    tempDF['Similarity'] = SumOfColumnSimilarity
    Outputs[name] = tempDF
    #tempDF['Similarity'] = SumOfColumnSimilarity

for name, similarity in Outputs.items():
    similarity.to_csv('Output/'+name+'.csv')

