# -*- coding: utf-8 -*-
"""
Created on Fri Aug 21 16:18:21 2020

@author: 54074
"""

import re
import random
import matplotlib.pyplot as plt
from math import sin, asin, cos, radians, fabs, sqrt 

# =============================================================================
#                           Import data 
# =============================================================================
def OpenData(path):
    #打开该路径下的数据样本
    data = open(path,'r')
    data_original = data.readlines()
    return data_original

def CleanData(data_original):
    data_sorted = []
    data_cleaned = []
    temp_poi_data = []
    #提取数据中的数据
    temp = re.findall(r'\d[\.\d]*',data_original[0])#正则表达式提取整数或小数
    hotel_number = int(temp[1])+2
    temp = re.findall(r'\d[\.\d]*',data_original[1])#正则表达式提取整数或小数
    start_time = int(temp[0])
    trip_length = re.findall(r'\d[\.\d]*',data_original[2])#正则表达式提取整数或小数
    trip_length = [float(i) for i in trip_length]
    trip_number = len(trip_length)
    #
    for i in range(4,len(data_original)):
        if i > 3 + hotel_number:
            temp1=[]
            temp1 = re.findall(r'\d[\.\d]*',data_original[i])#正则表达式提取整数或小数
            temp1 = [float(i) for i in temp1]
            temp_poi_data.append(temp1)
            temp1[0] = i-4
            data_cleaned.append(temp1)
        else:
            temp2=[]
            temp2 = re.findall(r'\d[\.\d]*',data_original[i])#正则表达式提取整数或小数
            temp2 = [float(i) for i in temp2]
            temp2[0] = i-4
            data_cleaned.append(temp2)
    #根据score的值对poi数据进行排序
    temp_poi_data = sorted(temp_poi_data,key = lambda x:x[3],reverse = True)
    poi_number = len(temp_poi_data)
    data_sorted = data_cleaned[0:hotel_number] + temp_poi_data
    return poi_number,hotel_number,trip_number,trip_length,data_sorted,\
           data_cleaned,start_time

    
# =============================================================================
#===========================   Models of MM algorithm   =======================
# =============================================================================
#************ 1. Preprocessing
# =============================================================================
def Preprocessing(trip_length,hotel_number):
    #生成所有trip中hotel可能的组合
    combination_trip_hotel = []
    for i in range(len(trip_length)):
        if i ==0:
            for j in range(hotel_number):
                combination_trip_hotel.append([i+1,(0,j)])
        else:
            if i+1 == len(trip_length):
                for j in range(hotel_number):
                    combination_trip_hotel.append([i+1,(j,1)])
            else:
                for j in range(hotel_number):
                    for k in range(hotel_number):
                        combination_trip_hotel.append([i+1,(j,k)])
    return combination_trip_hotel        

# =============================================================================
#************ 2. Generate initial population 
# =============================================================================         
def initialTour(day,hotel_number,population_size):
    initial_population_tour = []
    population_num = 0
    while population_num <population_size:
        population_num +=1
        temp_tour = []
        while len(temp_tour)<day+1:
            rand_value = random.randint(0,hotel_number-1)
            if rand_value in temp_tour:
                continue
            else:
                temp_tour.append(rand_value)
        initial_population_tour.append(temp_tour)
    return initial_population_tour


def InsertTour(tour,original_score,trip_length,hotel_number,data_cleaned,start_time):
    #对tour中的每一个trip进行插入操作
    trips = tourTotrips(tour,hotel_number) 
    for i in range(len(trips)):
        for j in range(hotel_number,len(data_cleaned)):
            #判断是否满足约束条件POI只访问一次
            if j in tour:
                continue 
            else:
                #插入规则一：直接插入尾部
                # trip.insert(-1,j)
                #插入规则二：最小增加值插入法
                improve_trip = minAddValue(trips[i],j,data_cleaned)
                #判断该trip是否满足约束条件
                day = i+1
                Judge_1,Judge_2 = tripFeasible(day,improve_trip,trip_length,data_cleaned,start_time)
                if Judge_1 == True and Judge_2 == True:
                    #如果满足约束条件就接受该插入的trip
                    trips[i] = improve_trip
            new_tour = tripsTotour(trips)
    #判断是否有递归的必要
    improve_score = tourScore(new_tour,data_cleaned)
    if original_score <improve_score:
        original_score = improve_score
        return InsertTour(new_tour,original_score,trip_length,hotel_number,data_cleaned,start_time)
    return new_tour

def minAddValue(trip,point,data_cleaned):#最小增加值插入法则
    temp_trip = trip.copy()
    #所有可行的插入点
    insert_position_set = [i for i in range(1,len(trip))]
    #计算每一个插入点的增加值
    add_values = []
    for i in insert_position_set:
        A = temp_trip[i-1]
        B = temp_trip[i]
        add_value = distance(data_cleaned[A][1],data_cleaned[A][2],data_cleaned[point][1],data_cleaned[point][2])\
                    + distance(data_cleaned[point][1],data_cleaned[point][2],data_cleaned[B][1],data_cleaned[B][2])
        original_value = distance(data_cleaned[A][1],data_cleaned[A][2],data_cleaned[B][1],data_cleaned[B][2])
        temp_save = add_value - original_value
        add_values.append(temp_save)
    #寻找最小增加值的插入位置
    temp_point = add_values.index(min(add_values))
    min_add_value_insert_position = insert_position_set[temp_point]
    #插入该点到trip中
    temp_trip.insert(min_add_value_insert_position,point)
    return temp_trip


def InsertOPT(day,trip,trip_length,hotel_number,data_cleaned,start_time):
    for i in range(hotel_number,len(data_cleaned)):
        #判断是否满足约束条件POI只访问一次
        if i in trip:
            continue 
        else:
            original_score = tripsScore(trip,data_cleaned)
            #插入规则：直接插入尾部
            trip.insert(-1,i)
            #判断该trip是否满足约束条件
            Judge_1,Judge_2 = tripFeasible(day,trip,trip_length,data_cleaned,start_time)
            if Judge_1 == True and Judge_2 == True:
                improve_score = tripsScore(trip,data_cleaned)
                if original_score <= improve_score:
                    return InsertOPT(day,trip,trip_length,hotel_number,data_cleaned,start_time)
            else:
                trip.remove(i)
    return trip


def hav(theta):    
    s = sin(theta / 2)    
    return s * s 

def distance( lng0,lat0, lng1, lat1 ):    
    "用haversine公式计算球面两点间的距离。"  
    EARTH_RADIUS=6371           # 地球平均半径，6371km 
    # 经纬度转换成弧度    
    lat0 = radians(lat0)    
    lat1 = radians(lat1)    
    lng0 = radians(lng0)    
    lng1 = radians(lng1)     
    dlng = fabs(lng0 - lng1)    
    dlat = fabs(lat0 - lat1)    
    h = hav(dlat) + cos(lat0) * cos(lat1) * hav(dlng)    
    distance = 2 * EARTH_RADIUS * asin(sqrt(h))     
    return distance 


def tripsScore(trip,data_cleaned):
    trip_score = 0
    for i in trip:
        trip_score += data_cleaned[i][3]
    return int(trip_score)
    
def tripLength(trip,data_cleaned):
    length = []
    temp_length = 0
    sighting_time = 0
    #计算trip的长度    
    for i in range(len(trip)-1):
        temp = distance(data_cleaned[trip[i]][1],data_cleaned[trip[i]][2],\
                        data_cleaned[trip[i+1]][1],data_cleaned[trip[i+1]][2])
        temp_length += temp*1000
        sighting_time += data_cleaned[trip[i]][4]
        length.append(temp_length)
    return length,sighting_time
        
def tripFeasible(day,temp_trip,trip_length,data_cleaned,start_time):
    speed = 7    
    leave_time = start_time        
    Judge_1,Judge_2 = False,False
    #约束条件一：不超过每天的trip长度
    length,sighting_time = tripLength(temp_trip,data_cleaned) 
    if length[-1]/speed/60+sighting_time < trip_length[0]:
        Judge_1 = True
        #约束条件二：POIs的时间窗约束
        poi_trip = temp_trip.copy()
        poi_trip.pop()
        poi_trip.pop(0)
        for k in range(len(length)-1):
            travel_time = length[k]/speed/60
            arrive_time = leave_time+travel_time
            if arrive_time>data_cleaned[poi_trip[k]][5] and arrive_time<data_cleaned[poi_trip[k]][6]:
                leave_time = arrive_time + data_cleaned[poi_trip[k]][4]#观光时间
                Judge_2 = True
            else:
                if arrive_time<data_cleaned[poi_trip[k]][5]:
                    leave_time = data_cleaned[poi_trip[k]][5] + data_cleaned[poi_trip[k]][4]
                    Judge_2 = True
                else:
                    Judge_2 = False
                    break
    return Judge_1,Judge_2

def tourRepeat(tour):
    poi = []
    for i in tour:
        poi = poi + i[2][1:-1]   
    if len(poi)==len(set(poi)):
        feasible = True        
    else:
        feasible = False
    return feasible


def populationScore(initial_population_tour,data_cleaned):
    initial_population_score = []
    for tour in initial_population_tour:
        tour_score = tourScore(tour,data_cleaned)
        initial_population_score.append(tour_score)
    return initial_population_score

def populationLength(initial_population_tour,data_cleaned):
    initial_population_length = []
    for tour in initial_population_tour:
        tour_length = tourLength(tour,data_cleaned)
        initial_population_length.append(tour_length)
    return initial_population_length
        

def tourLength(standard_tour,data_cleaned):
    tour_length = 0
    sighting_time = 0
    for i in range(len(standard_tour)-1):
        i_longitude = data_cleaned[standard_tour[i]][1]
        i_latitude = data_cleaned[standard_tour[i]][2]
        j_longitude = data_cleaned[standard_tour[i+1]][1]
        j_latitude = data_cleaned[standard_tour[i+1]][2]
        temp_distance = distance(i_longitude,i_latitude,j_longitude,j_latitude)
        tour_length += temp_distance*1000
        sighting_time +=data_cleaned[standard_tour[i]][4]
    tour_length = tour_length/7/60 + sighting_time
    return tour_length

                
def tourScore(standard_tour,data_cleaned):
    score = 0
    for j in standard_tour:
        score += data_cleaned[j][3]
    return int(score)

def tourFeasible(hotel_number,tour,trip_length,data_cleaned,start_time):
    #将tour分割成trip
    temp_trip_sets = tourTotrips(tour,hotel_number)    
    #判断每一个trip是否可行
    for i in range(len(temp_trip_sets)):
        Judge_1,Judge_2 = tripFeasible(i+1,temp_trip_sets[i],trip_length,data_cleaned,start_time)
        if Judge_1 == True and Judge_2 == True:
            tour_feasible = True
        else:
            tour_feasible = False
            break
    return tour_feasible
        
def tourTotrips(tour,hotel_number):
    temp_trip_sets = []
    start = 0
    #将tour分割成trip
    for i in range(1,len(tour)):
        if tour[i] < hotel_number:
            temp_trip_sets.append(tour[start:i+1])
            start = i 
    return temp_trip_sets

def tripsTotour(trip_list):
    tour = [trip_list[0][0]]
    for i in trip_list:
        tour = tour + i[1:]
    return tour

# =============================================================================
#************ 4. crossover
# ============================================================================= 
def crossoverOperator(parent_1,parent_2,trip_length,hotel_number,data_cleaned,start_time):
    #确定交叉点
    temp_1 = []
    temp_2 = []
    for i in range(len(parent_1)):
        if parent_1[i] <hotel_number:
            temp_1.append(i)
    for i in range(len(parent_2)):
        if parent_2[i] <hotel_number:
            temp_2.append(i)        
    crossover_point = random.randint(1,len(temp_1)-2)  
    #交叉操作
    offspring_1 = parent_1[0:temp_1[crossover_point]+1] + parent_2[temp_2[crossover_point+1]:] 
    offspring_2 = parent_2[0:temp_2[crossover_point]+1] + parent_1[temp_1[crossover_point+1]:]
    score_1 = tourScore(offspring_1,data_cleaned)
    score_2 = tourScore(offspring_2,data_cleaned)
    offspring_1 = InsertTour(offspring_1,score_1,trip_length,hotel_number,data_cleaned,start_time)
    offspring_2 = InsertTour(offspring_2,score_2,trip_length,hotel_number,data_cleaned,start_time)
    return offspring_1,offspring_2

# =============================================================================
#************ 5. mutation 
# ============================================================================= 
def mutationOperator(parent,trip_length,hotel_number,data_cleaned,start_time):
    #确定变异点
    temp = []
    for i in range(len(parent)):
        if parent[i] <hotel_number:
            temp.append(i)               
    mutation_point = random.randint(1,len(temp)-2)
    #变异操作
    mutation_hotel = random.randint(0,hotel_number-1)
    offspring = parent[0:temp[mutation_point-1]+1] + [mutation_hotel] + parent[temp[mutation_point+1]:]
    score = tourScore(offspring,data_cleaned)
    offspring = InsertTour(offspring,score,trip_length,hotel_number,data_cleaned,start_time)
    return offspring



# =============================================================================
#************ 6. Evalution process 
# ============================================================================= 
def evalutionProcess(crossover_proportion,mutation_proportion,population_size,improve_population_tour,\
                       trip_length,hotel_number,data_cleaned,trip_number,start_time):
    crossover_operator_num = int(crossover_proportion * population_size)
    mutation_operator_num = int(mutation_proportion * population_size)
    remain_num = population_size-crossover_operator_num-mutation_operator_num
    
    next_population = []
    #构造新的种群
    for i in range(remain_num):
        next_population.append(improve_population_tour[i][0])
    #交叉获取新个体   
    for i in range(crossover_operator_num):
        random_1 = random.randint(0,population_size-1)
        random_2 = random.randint(0,population_size-1)
        while random_1 == random_2:
            random_2 = random.randint(0,population_size-1)
        temp_tour_1,temp_tour_2 = crossoverOperator(improve_population_tour[random_1][0],improve_population_tour[random_2][0],trip_length,hotel_number,data_cleaned,start_time)      
        next_population.append(temp_tour_1)
        next_population.append(temp_tour_2)
    #变异获取新个体   
    for i in range(mutation_operator_num):
        random_3 = random.randint(0,population_size-1)
        temp_tour_3 = mutationOperator(improve_population_tour[random_3][0],trip_length,hotel_number,data_cleaned,start_time)
        next_population.append(temp_tour_3)
    #修改population的格式
    new_population = []
    for i in range(population_size):
        score = tourScore(next_population[i],data_cleaned)
        length = tourLength(next_population[i],data_cleaned)    
        new_population.append([next_population[i],(score,length)])
    #根据tour的score排序  
    new_population = sorted(new_population,key = lambda x:x[1][0],reverse = True)
    return new_population


def repeatCheck(tour,hotel_number):
    temp_tour = tour.copy()
    for i in temp_tour:
        if i >= hotel_number:
            for j in temp_tour:
                if i ==j:
                    tour.remove(i)
    return tour
            
# =============================================================================
#                           Plot parts 
# ============================================================================= 

def plotScatter(hotel_number,data_cleaned):
    plt.figure()
    plt.rcParams['font.sans-serif'] = ['SimHei'] #解决中文显示
    plt.rcParams['axes.unicode_minus'] = False #解决符号无法显示
    x_1 = [data_cleaned[i][1] for i in range(hotel_number)]
    y_1 = [data_cleaned[i][2] for i in range(hotel_number)]
    x_2 = [data_cleaned[i][1] for i in range(hotel_number,len(data_cleaned))]
    y_2 = [data_cleaned[i][2] for i in range(hotel_number,len(data_cleaned))]
    plt.scatter(x_1,y_1,color="red")
    plt.scatter(x_2,y_2,color="blue")
    txt_hotels = ['H' + str(i) for i in range(hotel_number)] #生成可行解中访问城市的坐标数据及标签数据
    txt_attractions = [i for i in range(hotel_number,len(data_cleaned))] #生成可行解中访问城市的坐标数据及标签数据
    for i in range(len(txt_hotels)):    #在图中增加标签数据
        plt.annotate( txt_hotels[i],(x_1[i],y_1[i]))
    for i in range(len(txt_attractions)):    #在图中增加标签数据
        plt.annotate( txt_attractions[i],(x_2[i],y_2[i]))
    
def plotLink(best_tour,data_cleaned):       
    x_1 = [data_cleaned[i][1] for i in best_tour]
    y_1 = [data_cleaned[i][2] for i in best_tour]
    plt.plot(x_1,y_1,color='green')














           