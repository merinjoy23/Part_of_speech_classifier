
# coding: utf-8

# In[1]:


'''
Introduction :


Authors : Merin Joy and Sai Nikitha
Date : 17th October 2018
This program takes as input as tagger output and the gold standard file and generates the accuracy and confusion matrix.


Instructions to run :


1) Run the tagger program in the command prompt as follows:
$ python tagger.py pos-train.txt pos-test.txt > pos-test-with-tags.txt
2) The txt document with tags on test data will be obtained in pos-test-with-tags.txt. Also, any output file name can be specified since STDOUT function is used.
3) Run the scorer program in the command prompt as follows:
$ python scorer.py pos-test-with-tags.txt pos-test-key.txt > pos-taggingreport.txt
4) The txt document with accuracy and confusion matrix will be generated in pos-taggingreport.txt. Also, any output file name can be specified since STDOUT function is used.


Sample Output:


Accuracy is: 
0.8927018988789751
Confusion Matrix: 
col_0    #    $   ''   (   )     ,     .    :    CC    CD ...    VBD  VBG  \
row_0                                                     ...               
#        5    0    0   0   0     0     0    0     0     0 ...      0    0   
$        0  371    0   0   0     4     0    0     0     0 ...      0    0   
''       0    0  527   0   0     0     0    0     0     0 ...      0    0   
(        0    0    0  76   0     0     0    0     0     0 ...      0    0   
)        0    0    0   0  76     0     0    0     0     0 ...      0    0   
,        0    0    0   0   0  3070     0    0     0     0 ...      0    0   
.        0    0    0   0   0     0  2363    0     0     0 ...      0    0   
:        0    0    0   0   0     0     0  336     0     0 ...      0    0   
CC       0    0    0   0   0     0     0    0  1364     0 ...      0    0   
CD       3  188    0   1   1     7     8   16    13  1508 ...      6    1   



Algorithm :


Step 1: Start
Step 2: Cleaning the tagger ouput and gold standard text files.
Step 3: Creating tokens from the tagger output and gold standard file.
Step 4: If the tokens in the same postion for both the files match
    Step 4.1: then, increment the counter
Step 5: Calculate the accuracy.
Step 6: Generate the confusion matrix using the pandas library package. 
Step 7: End
'''


import sys, nltk, scipy
import pandas as pd
from sklearn.metrics import confusion_matrix


def main():
    
    output = sys.argv[1] #get the tagger output
    test_key = sys.argv[2] #get the gold standard dataset.
    
    with open(output) as f: #cleaning the tagger output
        read_output = f.read().replace('\n', '')
        tokens_output = [nltk.tag.str2tuple(x) for x in read_output.split()] #generating tokens from thr tagger output
    
    with open(test_key) as f: #cleanig the gold standard dataset.
        read_key1 = f.read().replace('\n', '')
    
        read_key2 = read_key1.replace("[","")
        read_key3=read_key2.replace("]","")
        tokens_key = [nltk.tag.str2tuple(x) for x in read_key3.split()] #generating tokes from the gold standard
    
    list_key = [x[1] for x in tokens_key] #create a list of tokens from gold standard key.
    list_output = [x[1] for x in tokens_output] #create a list of tokens for tagger output.
    
    i=0 #initializing i
   
    for word in list_key:
        index = list_key.index(word)
        if ( word== list_output[index]): #find the occurence of gold standard token with tagger ouput tokens.
            i += 1 #increment the counter.
    
    accuracy = i/ len(tokens_key) #generate the accuracy
    
    index_key = set(list_key)
    list(index_key) #generate the gold standard key list.
    index_output = set(list_output)
    list(index_output) #generate the tagger output list.
    
    
    df1 = pd.Series( (v for v in list_key) ) #create dataframe for gold standard list.
    df2 = pd.Series( (v for v in list_output) ) #create dataframe for tagger output list.
    df_confusionmatrix = pd.crosstab(df1, df2)  #generates the confusion matrix.
    
    sys.stdout.write("Accuracy is: \n" +str(accuracy)+"\nConfusion Matrix: \n"+str(df_confusionmatrix)) #prints the accuracy and confusion matrix in the desired file.

if __name__ == "__main__": #Main function
    main()
    
    
    
