'''
Data Mining Assignment 4, Cluster Validation
2016253072
명수환(Myeong Suhwan)
'''
from datetime import datetime


def getDataFromFile(filename):
    input_file = open(filename, 'r')
    gene_id = dict()
    
    line_num = 0
    for line in input_file:
        time_point_data = line.split()
        gene_id[line_num] = time_point_data[2:]
        
        line_num += 1
        
        
    return gene_id



def output_to_file(filename,String):
    file = open(filename, 'a')
    file.write(String)
    file.write("\n")
        
    file.close()
    print("Finished to print to output file : ", filename)

def MakeIncidentMatrix(file, total_size):
    input_file = open(file, 'r')
    
    Incident_Matrix = [[0 for col in range(total_size)] for row in range(total_size)] # * 0 is init value that means two data isn't in same cluster.
    cluster_from1 = [0 for col in range(k)]
    
    
    index = 0
    for line1 in input_file:
        cluster_from1[index] = line1.split()
        cluster_from1[index] = cluster_from1[index][1:]
        index += 1
    
    for cluster_num in range(k):
        if cluster_from1[cluster_num] == 0:
            continue
        for i in cluster_from1[cluster_num]:
            
            for j in cluster_from1[cluster_num]:
                index_i = int(i)
                index_j = int(j)
                
                Incident_Matrix[index_i-1][index_j-1] = cluster_num+1
    
    #print(Incident_Matrix)
    return Incident_Matrix
    

def GetGroundTruth(input_file,total_size):
    file = open(input_file, 'r')
    ground_truth_list = list()
    P_Matrix = [[0 for col in range(total_size)] for row in range(total_size)]
    for line in file:
        data = line.split()
        ground_truth = int(data[1])
        ground_truth_list.append(ground_truth)
    
    for i in range(total_size):
        for j in range(total_size):
            if ground_truth_list[i] == ground_truth_list[j] and ground_truth_list[i] != -1:
                P_Matrix[i][j] = ground_truth_list[i]
            elif ground_truth_list[i] == -1:
                P_Matrix[i][j] = -1
    
    #print(P_Matrix)
    return P_Matrix

def EvaluationJaccard(Matrix_C,Matrix_P,total_size):
    SS = 0
    SD = 0
    DS = 0
    
    for i in range(total_size):
        for j in range(i,total_size):
            if Matrix_C[i][j] == Matrix_P[i][j] and Matrix_P[i][j] > 0: # * p is not outlier.
                #print("SS => i:",i,"j:",j,"Matrix_C[]:",Matrix_C[i][j])
                SS += 1
            elif Matrix_C[i][j] != Matrix_P[i][j] and Matrix_C[i][j] != 0:
                #print("SD => i:",i,"j:",j,"Matrix_C[]:",Matrix_C[i][j])
                SD += 1
            elif Matrix_C[i][j] == 0 and Matrix_P[i][j] > 0:
                #print("DS => i:",i,"j:",j,"Matrix_C[]:",Matrix_C[i][j])
                DS += 1
            

    # print("SS : ",SS)
    # print("SD : ",SD)
    # print("DS : ",DS)
    
    #print("[+]Calculating the accuracy using Jaccard Index . . .")
    accuracy = (SS / (SS+SD+DS)) * 100
    
    return accuracy

def main():
    global DIMENSION,k
    DIMENSION = 12
    k = 10
    input_filename1 = 'assignment4_input.txt' #517
    input_filename2 = 'assignment2_output.txt' #K-Means
    input_filename3 = 'assignment3_output.txt' #Improved K-Medoids
    
    output_filename = 'assignment4_output.txt'

    gene_id = getDataFromFile(input_filename1)
    total_size = len(gene_id)

    start_time = datetime.now()

    incident_Matrix_C = MakeIncidentMatrix(input_filename2, total_size)
    incident_Matrix_P = GetGroundTruth(input_filename1,total_size)
    accuracy = EvaluationJaccard(incident_Matrix_C,incident_Matrix_P,total_size)
    
    k_means_output = ("K-Means Accuracy : {0}%".format(accuracy))
    print(k_means_output)
    output_to_file(output_filename,k_means_output)


    incident_Matrix_C = MakeIncidentMatrix(input_filename3, total_size)
    incident_Matrix_P = GetGroundTruth(input_filename1,total_size)
    accuracy = EvaluationJaccard(incident_Matrix_C,incident_Matrix_P,total_size)
    
    k_medoids_output = ("Imrpoved K-medoids Accuracy : {0}%".format(accuracy))
    print(k_medoids_output)
    output_to_file(output_filename,k_medoids_output)
    
    



    end_time = datetime.now()
    
    print("Time Elapsed : ", end_time - start_time,"microseconds")



if __name__ == '__main__':
    main()