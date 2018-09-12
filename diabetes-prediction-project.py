# Emily M. Hoang
# spring quarter 2016

# pre: needs training file open for reading
# post: returns list of diabetic data averages, list of
# nondiabetic data averages, number of diabetic patients,
# and number of nondiabetic patients.
def add_data(t_file):
    ill_people = 0 #count ill people
    healthy_people = 0 #count healthy people
    update_list1 = [0]*6 
    update_list2 = [0]*6
        
    for l in t_file: #parse lines
        t_list = l.split(",") 
        diagnosis = float(t_list[len(t_list)-1]) #diagnosis is 7th element

        clean_list = replace_question(t_list) #replace question marks w/ zero

        if diagnosis >= 0.5: #if ill patient
            ill_people += 1
            summed_ill = summed_data(clean_list, update_list1) #add data to all other ill patients' data
        else: #if patient is healthy
            healthy_people += 1
            summed_healthy = summed_data(clean_list, update_list2) #add data to all other healthy patients' data

    return summed_ill, summed_healthy, ill_people, healthy_people


## pre: needs list of one patient's data
## post: returns list where question marks are replaced by zeros
def replace_question(list1):
    idx = -1
    for el in list1: #if there's a question mark, replace with 0
        idx += 1 
        if el == "?": 
            list1[idx] = 0 

    return list1


## pre: needs list of one patient's data
## post: returns list with summed data
def summed_data(data_list, alist):
    idx = -1  
    for el in data_list:
        idx += 1 
        el = float(el)
        if idx < len(data_list)-1: #if element is NOT diagnosis (last element)
            alist[idx] += el #add element into new list at that index
            
    return alist


# pre: needs list of summed data and number of patients
# post: returns averaged data
def average_data(summed_list, patients):
    idx = -1
    avg_data = [] #list for averaged data

    for el in summed_list:
        idx += 1
        avg = float(format(summed_list[idx]/patients, ".2f")) #divide ea. summed
                                    #element by number of patients (to obtain average)
        avg_data.append(avg)
        
    return avg_data


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

    setFile.seek(0) #reset file reading marker
    
    outfile = input("Enter the name of the output file: ") 
    csv = open(outfile, "w") 

    predictSetFile(setFile,csv,averages) 

    setFile.close() 
    csv.close()
    
    
def main():
    infile = input("Enter the name of the training set file: ")
    training_file = open(infile, "r")

    add_ill, add_healthy, diabetic, nondiabetic = add_data(training_file)
    
    avg_ill = average_data(add_ill, diabetic) #average ill data
    avg_healthy = average_data(add_healthy, nondiabetic) #average healthy data

    training_file.seek(0) #reset file reading marker
    
    averages = means(avg_ill, avg_healthy) 
    PEOPLE, ACC = predictTrainingFile(training_file, averages)
    accuracy1 = accuracy(PEOPLE, ACC)

    printStats(avg_healthy, avg_ill, averages, accuracy1) 
    writeStats(averages) 

    training_file.close() 
    
main()
