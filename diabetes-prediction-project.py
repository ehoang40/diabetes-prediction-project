# Emily M. Hoang
# spring quarter 2016

# pre: needs training file open for reading
# post: returns number of people diagnosed with diabetes, list of
# averages for sick people, and list of the averages for healthy people
def training_file_list(trainingFile):
    ill = [0]*6 #emtpy list for ill averages
    healthy = [0]*6 #empty list for healthy averages

    illPeople = 0 #count number of ill people
    healthyPeople = 0 #count number of healthy people

    for l in trainingFile:
        IDX = -1 #set index for finding question marks
        trainingList = l.split(",") 
        diagnosis = float(trainingList[len(trainingList)-1]) #7th element is diagnosis

        for element in trainingList: #if there's a question mark, replace with 0
            IDX += 1 
            if element == "?": 
                trainingList[IDX] = 0 
            
        if diagnosis >= 0.5: #if patient is ill
            illPeople += 1 
            idxIll = -1 #set index for elements of an ill person

            for element in trainingList: 
                element = float(element) 
                idxIll += 1 
                if idxIll < len(trainingList)-1: #for any index that's LESS than the
                                                 #index of last element (don't want diagnosis)
                    ill[idxIll] = (ill[idxIll] + element) #add element into ill list AT THAT
                                                          #INDEX
        else: #if patient is not ill
            healthyPeople += 1 
            idxHealthy = -1 #set index for elements of a healthy person

            for element in trainingList:
                idxHealthy += 1 
                if idxHealthy < len(trainingList)-1: #for any index that's LESS than the
                                                     #index of last element
                    healthy[idxHealthy] = (healthy[idxHealthy] + float(element)) #add element
                                                     #(as a float) into healthy list AT THAT
                                                     #INDEX

    index1 = -1 
    for element in ill:
        index1 += 1
        ill[index1] = float(format(ill[index1]/illPeople, ".2f")) #divide every element in ill
                                    #by number of ill people (to get the averages)

    index1 = -1 
    for element in healthy:
        index1 += 1
        healthy[index1] = float(format(healthy[index1]/healthyPeople, ".2f")) #divide every
                                    #element in healthy by number of healthy people
    return illPeople, ill, healthy 



# pre: needs list of averages for sick people and list of averages for healthy people
# post: returns list of the mean values calculated between ill and healthy
def means(ill, healthy):
    idx = -1
    averages = [0]*6 #empty list for averages calculated between ill and healthy

    for element in ill:
        idx += 1 
        averages[idx] = float(format((ill[idx] + healthy[idx])/2, ".2f")) #for every element in
                     #ill, add element to healthy at that index.  Divide by 2 to get average
    return averages



# pre: needs training file open for reading and list of averages (calculated
# between ill and healthy)
# post: returns total number of people in training file, and number of
# people for whom predictions are CORRECT.
def predictTrainingFile(trainingFile, averages):
    PEOPLE = 0 #count total number of people
    ACC = 0 #count number of people for whom the predictions are CORRECT.  This is
            #the ACCURACY COUNTER
    
    for l in trainingFile:
        PEOPLE += 1
        IDX = -1 #set index for finding question marks
        trainingList = l.split(",") 
        idx = -1 #set index for elements 
        greater_than_average = 0 #count number of "at risk" elements (elements that are
                                 #greater than corresponding value in averages list) 

        for element in trainingList:#if there's a question mark, replace with 0
            IDX += 1
            if element == "?": 
                trainingList[IDX] = 0

        for element in trainingList: 
            element = float(element) 
            idx += 1
            if idx < len(trainingList)-1:#for any index that's LESS than the index of
                                         #last element
                if element > averages[idx]: #if element is greater than the value in averages
                                            #list, at that index 
                    greater_than_average += 1
                    
        if greater_than_average > 3 and float(trainingList[len(trainingList)-1])>0.5:
             ACC += 1 #if more than 3 "at risk" attributes and person is ill, increment
                      #accuracy counter
        if greater_than_average <= 3 and float(trainingList[len(trainingList)-1])<=0.5:
             ACC += 1 #if 3 or fewer "at risk" attributes and person is healthy, increment
                      #accuracy counter 

    return PEOPLE, ACC



# pre: needs total number of people in training file, and number of people for whom
# predictions are correct
# post: returns accuracy of program's predictions
def accuracy(PEOPLE, ACC): 
    accuracy = float(format(ACC/PEOPLE, ".2f"))
    
    return accuracy



# pre: needs test file open for reading, file open for writing, and
# list of averages (calculated between ill and healthy)
# post: writes each patient's ID number to file, and their predicted diagnosis
def predictSetFile(setFile, csv,averages):
    csv.write("id" +"," + "disease?\n") #write first line
    for l in setFile:
        newList = l.split(",") 
        idx = -1 
        atRisk = 0 #count number of "at risk" attributes

        for element in newList:
            idx += 1
            if idx == 0: #first element of list (patient id)
                csv.write(element + ",")   
            else:
                element = float(element) 
                if element > averages[idx-1]: #if element is greater than value in averages
                                              #at that index MINUS 1 ("index minus 1" because
                                              #averages has only six elements, but newList has
                                              #seven.  We don't want the first element from
                                              #newList, so we have to account for that.)
                    atRisk += 1

        if atRisk > 3: #if more than 3 "at risk" attributes
            csv.write("Yes\n") 
        else: 
            csv.write("No\n") 



# pre: needs list of averages for sick people, list of averages for healthy people,
# list of averages calculated between ill and healthy, and accuracy
# post: prints stats for training file 
def printStats(healthy,ill,averages,accuracy): 
    print("Healthy patients' averages:\n", healthy)
    print("Ill patients' averages:\n", ill)
    print("Separator values:\n", averages)
    print("Accuracy:\n", accuracy)
    print()



# pre: needs list of averages (calculated between ill and healthy)
# post: executes predictSetFile function (which writes to another file)
def writeStats(averages):
    while True: 
        infile = input("Enter the name of the test set file: ") 
        if infile == "": #if user doesn't enter any file name
            print("You must enter a file name.")
        else:
            setFile = open(infile, "r")
            file = setFile.read()
            if file == "":
                print("This file is empty.")
            else:
                break
            
    setFile = open(infile, "r") #note-to-self: needed to open/read file AGAIN
                                #outside of while loop. 
    outfile = input("Enter the name of the output file: ") 
    csv = open(outfile, "w") 

    predictSetFile(setFile,csv,averages) 

    setFile.close() 
    csv.close()
    
    
def main():
    infile = input("Enter the name of the training set file: ")
    trainingFile = open(infile, "r") 

    illPeople, ill, healthy = training_file_list(trainingFile) 

    trainingFile.seek(0) #reset file reading marker
    
    averages = means(ill, healthy) 
    PEOPLE, ACC = predictTrainingFile(trainingFile, averages)
    accuracy1 = accuracy(PEOPLE, ACC)

    printStats(healthy, ill, averages, accuracy1) 
    writeStats(averages) 

    trainingFile.close() 
    
main()
