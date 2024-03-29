# coding: utf-8

# In[1]:

'''
Introduction :


Authors : Merin Joy and Sai Nikitha
Date : 17th October 2018
This program takes as input a training file containing part of speech tagged text and a file containing text to be part of speech tagged. It implements the "most likely tag" baseline. 
Baseline accuracy is 0.8803
Accuracy after applying rules is 0.8927
Rules added are:
1. For cardinal numbers assign CD tag
2. For words ending with 'ing' assign VBG tag
3. For words ending with 'ed' assign VBN tag
4. For words ending with ful, ous, ble, ic, ive, est, able, al assign JJ tag
5. For words ending with ly assign RB tag


Instructions to run :


1) Run the tagger program in the command prompt as follows:
$ python tagger.py pos-train.txt pos-test.txt > pos-test-with-tags.txt
2) The txt document with tags on test data will be obtained in pos-test-with-tags.txt. Also, any output file name can be specified since STDOUT function is used.
3) Run the scorer program in the command prompt as follows:
$ python scorer.py pos-test-with-tags.txt pos-test-key.txt > pos-taggingreport.txt
4) The txt document with accuracy and confusion matrix will be generated in pos-taggingreport.txt. Also, any output file name can be specified since STDOUT function is used.


Possible Tags:


1. CC Coordinating conjunction 
2. CD Cardinal number 
3. DT Determiner 
4. EX Existential there 
5. FW Foreign word 
6. IN Preposition or subordinating conjunction 
7. JJ Adjective 
8. JJR Adjective, comparative 
9. JJS Adjective, superlative 
10. LS List item marker 
11. MD Modal 
12. NN Noun, singular or mass 
13. NNS Noun, plural 
14. NNP Proper noun, singular 
15. NNPS Proper noun, plural 
16. PDT Predeterminer 
17. POS Possessive ending 
18. PRP Personal pronoun 
19. PRP$ Possessive pronoun 
20. RB Adverb 
21. RBR Adverb, comparative 
22. RBS Adverb, superlative 
23. RP Particle 
24. SYM Symbol 
25. TO to 
26. UH Interjection 
27. VB Verb, base form 
28. VBD Verb, past tense 
29. VBG Verb, gerund or present participle 
30. VBN Verb, past participle 
31. VBP Verb, non-3rd person singular present 
32. VBZ Verb, 3rd person singular present 
33. WDT Wh-determiner 
34. WP Wh-pronoun 
35. WP$ Possessive wh-pronoun 
36. WRB Wh-adverb 


Sample Output:


No/DT ,/,  it/PRP  was/VBD n't/RB Black/NNP Monday/NNP ./. But/CC while/IN  the/DT New/NNP York/NNP Stock/NNP Exchange/NNP did/VBD n't/RB  fall/NN apart/NN  Friday/NNP as/IN  the/DT Dow/NNP Jones/NNP Industrial/JJ Average/NNP plunged/VBN  190.58/NN points/NNS --/: most/JJS of/IN  it/PRP in/IN  the/DT final/JJ hour/NN --/:  it/PRP barely/NN managed/VBN to/TO stay/VB  this/DT side/NN of/IN  chaos/NN ./.  Some/DT ``/``  circuit/NN breakers/NNS ''/'' installed/VBN after/IN  the/DT October/NNP 1987/CD crash/NN failed/VBN  their/PRP$ first/JJ test/JJ ,/,  traders/NNS say/VBP ,/, unable/JJ to/TO cool/JJ  the/DT selling/VBG panic/JJ in/IN  both/DT  stocks/NNS and/CC  futures/NNS ./.  The/DT 49/CD stock/NN specialist/NN firms/NNS on/IN  the/DT Big/NNP Board/NNP floor/NN --/:  the/DT buyers/NNS and/CC  sellers/NN of/IN  last/JJ resort/NN  who/WP were/VBD criticized/VBN after/IN  the/DT 1987/CD crash/NN --/: once/RB again/RB could/MD 

Algorithm :


Step 1: Start
Step 2: Cleaning the traning and testing datasets.
Step 3: Creating tokens from the training datasets along with there tags and finding the conditional frequency distribution.
Step 4: Creating tokens for test dataset and finding the most likely tag for the appropriate test data token.
Step 5: Using the rules to determine the tags and giving "NN" as default.
Step 6: Replacing the test data with the final tags.
Step 7: Write the test data with tags into an output file.
Step 8: End
'''

import nltk, sys, re, string

def main():
    
    training_data = sys.argv[1] #get the training dataset with tags.
    testing_data = sys.argv[2] #get the testing dataset without tags.     
    
    with open(training_data) as f: #cleaning the training dataset.
        raw_train = f.read().replace('\n', '')
    raw_train2 = raw_train.replace("[","")
    raw_train3=raw_train2.replace("]","")
    
    with open(testing_data) as f: # cleaning the testing dataset.
        raw_test = f.read().replace('\n', '')    
    raw_test2 = raw_test.replace("[","")
    raw_test3 = raw_test2.replace("]","") 
    
    if raw_train3:
        tag_tokens_train = [nltk.tag.str2tuple(x) for x in raw_train3.split()] #generating tokens for train data.
        tokens_train = nltk.ConditionalFreqDist(tag_tokens_train) #determing the conditional frequency distribution for tokens.
      
    if raw_test3 and tokens_train:
        raw_test3 = " "+raw_test3+" "   #adding white spaces to generalize replace function.
        tokens_test = [i for i in raw_test3.split()] #generating tokens for test data.
        for token_test in tokens_test:
            result_match = 'NN' #assign NN for default match
            
            #Baseline Accuracy gives 0.8803
            match = tokens_train[token_test].most_common() #generating the most likely tag.
            if match:                                      
                if (re.search (r'^-?[0-9]+(.[0-9]+)?$', token_test) != None):
                    result_match = "CD"
                elif (re.search(r'.*ing$', token_test) != None):
                    result_match = "VBG"
                elif (re.search(r'.*ed$', token_test) != None):
                    result_match = "VBN"
                elif (re.search(r'(.*ful$)|(.*ous$)|(.*ble$)|(.*ic$)|(.*ive$)|(.*est$)|(.*able$)|(.*al$)', token_test) != None):
                    result_match = "JJ"
                elif(re.search(r'.*ly$', token_test) != None):
                    result_match = "RB"
                else:
                    result_match = match[0][0]
             #Accuracy after adding rules gives 0.8927
            
                tag_tokens_test = token_test+"/"+result_match #adding result tags for the output text.
            raw_test3 = raw_test3.replace(" "+token_test+" "," "+tag_tokens_test+" ") #replace test tokens with tokens and tags.
            raw_test3 = raw_test3.replace("\n"+token_test+" ","\n"+tag_tokens_test+" ")
            raw_test3 = raw_test3.replace(""+token_test+"\n",""+tag_tokens_test+"\n")
            
    raw_test3 = raw_test3[1:-1] #Removing the white spaces added before.
    
    sys.stdout.write(raw_test3) #Writing the output into the output file mentioned in the command line.

if __name__ == "__main__": #Main function
    main()