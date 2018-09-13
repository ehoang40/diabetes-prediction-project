# Emily M. Hoang
# Spring quarter 2016 project
# Edited Sept. 2018

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
# post: returns total number of people in training file, and number of correct
# diagnoses predictions.
def predict_training_file(file1, means):
    people = 0 #count patients
    correct_predictions = 0 #count number of correct diagnoses predictions
    
    for l in file1:
        people += 1
        t_list = l.split(",") 
        idx = -1 #set index for elements 
        greater_than_mean = 0 #count number of the patient's "at risk" elements 
                                 #(elements that are greater than corresponding
                                 #value in means/averages list) 

        clean_list = replace_question(t_list) #replace question marks w/ zero

        for el in t_list: 
            el = float(el) 
            idx += 1
            if idx < len(t_list)-1:#if element is not diagnoses
                if el > means[idx]: #if element is "at risk"
                    greater_than_mean += 1
                    
        if greater_than_mean > 3 and float(t_list[len(t_list)-1]) >= 0.5:
             correct_predictions += 1 #if over 3 data elements are "at risk" and
                                      #person is diabetic, increment correct_predictions counter
        if greater_than_mean <= 3 and float(t_list[len(t_list)-1]) < 0.5:
             correct_predictions += 1 #if 3 or fewer elements are "at risk" and person is nondiabetic,
                                      #increment correct_predictions counter 

    return people, correct_predictions



# pre: needs total number of people in training file, and number of people for whom
# predictions are correct
# post: returns accuracy of program's predictions
def model_accuracy(people, accuracy1): 
    ACC = float(format(accuracy1/people, ".2f"))
    
    return ACC


# pre: needs test file open for reading, file open for writing, and
# list of averages (calculated between ill and healthy)
# post: writes each patient's ID number to file, and their predicted diagnosis
def predict_set_file(f1, f2,averages):
    f2.write("id" +"," + "disease?\n") #write first line
    for l in f1:
        f1_list = l.split(",") 
        idx = -1 
        at_risk = 0 #count number of "at risk" attributes

        for el in f1_list:
            idx += 1
            if idx == 0: #first element of list (patient id)
                f2.write(el + ",")   
            else:
                el = float(el) 
                if el > averages[idx-1]: #if element is greater than value in averages
                                         #at that index MINUS 1 (because averages has
                                         #only six elements, but f1_list has seven.  We
                                         #don't want the first element from f1_list, so
                                         #we have to account for that.)
                    at_risk += 1

        if at_risk > 3: #if more than 3 attributes are "at risk"
            f2.write("Yes\n") 
        else: 
            f2.write("No\n") 



# pre: needs list of averages for nondiabetic patients, list of averages for diabetic patients,
# list of averages calculated between ill and healthy, and model's accuracy
# post: prints stats for training file 
def print_stats(healthy,ill,avg,acc): 
    print("Healthy patients' averages:\n", healthy)
    print("Ill patients' averages:\n", ill)
    print("Separator values:\n", avg)
    print("Accuracy:\n", acc)
    print()



# pre: needs list of averages (calculated between ill and healthy)
# post: executes predictSetFile function (which writes to another file)
def write_stats(avg):
    while True: 
        infile = input("Enter the name of the test set file: ") 
        if infile == "": #if user doesn't enter any file name
            print("You must enter a file name.")
        else:
            set_file = open(infile, "r")
            file1 = set_file.read()
            if file1 == "":
                print("This file is empty.")
            else:
                break

    set_file.seek(0) #reset file reading marker
    
    outfile = input("Enter the name of the output file: ") 
    results_file = open(outfile, "w") 

    predict_set_file(set_file,results_file,avg) 

    set_file.close() 
    results_file.close()
    
    
def main():
    infile = input("Enter the name of the training set file: ")
    training_file = open(infile, "r")

    add_ill, add_healthy, diabetic, nondiabetic = add_data(training_file)
    
    avg_ill = average_data(add_ill, diabetic) #average ill data
    avg_healthy = average_data(add_healthy, nondiabetic) #average healthy data    
    averages = means(avg_ill, avg_healthy)

    training_file.seek(0) #reset file reading marker
    patients, accurate_predictions = predict_training_file(training_file, averages)
    accuracy = model_accuracy(patients, accurate_predictions)

    print_stats(avg_healthy, avg_ill, averages, accuracy) 
    write_stats(averages) 

    training_file.close() 
    
main()

