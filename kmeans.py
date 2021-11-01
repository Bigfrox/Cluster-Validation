'''
Data Mining Assignment 2, K-Means
2016253072
명수환(Myeong Suhwan)
'''
from datetime import date, datetime
import math



def getDataFromFile(filename):
    input_file = open(filename, 'r')
    gene_id = dict()
    
    line_num = 0
    for line in input_file:
        time_point_data = line.split()
        
        gene_id[line_num] = time_point_data[2:]
        
        line_num += 1
        
        
    return gene_id

def randClustering(gene_id):
    cluster = list() # k개의 cluster 생성, k : 10
    # * init_mem_num_in_cluster = int(len(gene_id) / k)
    # * length = len(gene_id)
    init_mem_num_in_cluster = 50
    last_partition = 50+17
    length = 517 - last_partition
    line_num = 0

    for i in range(0,length-1,init_mem_num_in_cluster):
        same_cluster = list()
        for i in range(init_mem_num_in_cluster):
            same_cluster.append(line_num)
            line_num += 1    
        cluster.append(same_cluster)

    #* ################################
    if last_partition:
        same_cluster = list()
        for i in range(last_partition):
            same_cluster.append(line_num)
            line_num += 1
        cluster.append(same_cluster)
    #* ################################

    return cluster

def getKMeans(cluster,cluster_num,gene_id):
    kmeans = [0,0,0,0,0,0,
                0,0,0,0,0,0,] #* 12-dimension
    object_num = len(cluster[cluster_num])

    for i in range(DIMENSION):
        
        tmp = 0
        for num in range(object_num):
            
            tmp += (float(gene_id[cluster[cluster_num][num]][i]))
            
        tmp /= float(object_num)
        
        kmeans[i] = float("{:.3f}".format(tmp))
        
    #*print("k-means : ", kmeans)
    return kmeans

def getDistance(kmeans, object):
    dist = 0
    
    for dimension in range(DIMENSION):
        dist_dimesion = float(kmeans[dimension]) - float(object[dimension])
        tmp = math.pow(dist_dimesion,2)
        dist += tmp
    dist = math.sqrt(dist)
    dist = "{:.3f}".format(dist)
    
    return float(dist)

def Reassign(obj_num, to,from_cluster_num,cluster):
    # * add to new cluster
    cluster[to].append(obj_num) # * number of object

    
    # * remove from old cluster
    cluster[from_cluster_num].remove(obj_num)
    #print(obj_num,"이", "cluster",to,"에 추가되었습니다.")

def output_to_file(filename,cluster):
    file = open(filename, 'w')
    
    for i in range(k):
        file.write('{0}: '.format(len(cluster[i])))
        for v in cluster[i]:
            file.write(str(v)+" ")
        file.write("\n")
        

    file.close()
    print("Finished to print to output file : ", filename)

def main():
    start_time = datetime.now()
    global DIMENSION,k
    DIMENSION = 12
    k = 10
    input_filename = 'assignment4_input.txt' #517
    
    #input_filename = 'test1.txt'

    output_filename = 'k-means_output.txt'

    gene_id = getDataFromFile(input_filename)
    
    print(gene_id)

    ##*print(len(gene_id))
    cluster = randClustering(gene_id)
    print("Start . . . ")
    print(cluster)

    for num in range(k):
        print("cluster",num,cluster[num])
        for i in range(len(cluster[num])):
            print(gene_id[cluster[num][i]])
        print("\n")
    ##*print(cluster)

    # * get K-means value at all clusters
    
    isChanged = True # * default value is True
    count_for_debug = 0
    while isChanged:  
        
        count_for_debug += 1
        print("[*]",count_for_debug,"번 반복하였습니다.")
        isChanged = False
        for cluster_num in range(k): # * A cluster 
                
            if not cluster[cluster_num]:
                ##*print("Cluster",cluster_num,"is empty cluster.")
                continue
            #*#*print("Cluster", cluster_num)
            #*#*print("The number of objects in Cluster : ",len(cluster[cluster_num]))
            kmeans1 = getKMeans(cluster,cluster_num,gene_id) # [0,1]
            #print(cluster[cluster_num])
            iter_index = 0
            while iter_index < len(cluster[cluster_num]): # * iter_index is index of an element of a cluster
                
                distance = getDistance(kmeans1,gene_id[cluster[cluster_num][iter_index]])
                #print("클러스터 ",cluster_num,"의 오브젝트 : ", cluster[cluster_num][iter_index])
                #print("거리: ",distance)
                for i in range(k): # * other cluster to compare
                    # * Find the shorter distance with other K-Means of other clusters with loop
                    if cluster_num == i: # * Don't need to compare with myself 
                        continue
                    if not cluster[i]: # * pass the empty cluster
                        #*print("Cluster",i,"is empty cluster.")
                        continue
                    
                    if cluster[cluster_num] and cluster[i]:
                        
                        kmeans2 = getKMeans(cluster,i,gene_id)#* K-Means of i-cluster
                        dist = getDistance(kmeans2,gene_id[cluster[cluster_num][iter_index]]) # * Distance to K-Means of i-cluster
                        
                        
                        if dist < distance: # * after finding, Re-assign objects to clusters based on the distance that I've found.
                            #print(cluster[cluster_num][iter_index],"오브젝트에 대하여 ", end=" ")
                            #print("cluster",cluster_num,"의 K-Means와","cluster",i,"의 K-Means중 가까운 것을 찾는 중입니다.")
                            #print("거리가 더 가까운 K-Means를 찾았습니다.")
                            # print("\n오브젝트 ",cluster[cluster_num][iter_index],"에 대하여 ")
                            # print("원래 Cluster",cluster_num,"에서 K-Means까지의","Distance : ", distance)
                            # print("비교할 Cluster",i,"에서 K-Means까지의","Distance : ", dist)
                            # print(dist," < ", distance,"이므로 이동합니다.")
                            
                            obj_num = cluster[cluster_num][iter_index]
                            to = i
                            Reassign(obj_num,to,cluster_num,cluster)                            
                            isChanged = True

                            iter_index -= 1
                            if iter_index < 0:
                                iter_index = 0
                            
                    
                    
                    else:
                        continue

                iter_index += 1

    print("\n\n")
    size_ = 0
    for i in range(k):
        cluster[i].sort()
        print(i,"번 클러스터 :","SIZE: ",len(cluster[i]), cluster[i])
        size_ += len(cluster[i])
        print("\n")
    print("Total size : ", size_)
    output_to_file(output_filename,cluster)
    
    print("Time Elapsed : ", datetime.now() - start_time)

if __name__ == '__main__':
    main()