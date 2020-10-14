 # -*- coding: utf-8 -*-
"""
Created on Fri Aug 21 16:20:21 2020

@author: JianZhong

                standard genetic algorithm to solve the MDTTDP

"""
import sGA_model as model
import time

'''                         1.sorted the attraction                         '''
# =============================================================================
#                           Setting Parameters 
# =============================================================================
start = time.process_time()
iteration = 5  #迭代次数
population_size = 30  #种群数量
crossover_proportion = 0.3  #交叉概率
mutation_proportion =0.7  #变异概率
path = r'2days.txt'

count = 0
score_list = []
while count<10:
    count +=1
    # =============================================================================
    #               *************  Input data  ****************
    # =============================================================================
    data_original = model.OpenData(path)#Input data
    poi_number,hotel_number,trip_number,trip_length,data_sorted,data_cleaned,start_time = model.CleanData(data_original)
    # =============================================================================
    #          *************  Generate Initial population  **************** 
    initial_population_tour = model.initialTour(trip_number,hotel_number,population_size)
    initial_population_score = model.populationScore(initial_population_tour,data_cleaned)
    initial_population_length = model.populationLength(initial_population_tour,data_cleaned)
    
    # =============================================================================
    #          *************  Evalution process  **************** 
    # =============================================================================
    Best_tour_pool = []
    improve_population_tour = [[initial_population_tour[i],(initial_population_score[i],initial_population_length[i])] for i in range(len(initial_population_tour))]
    #根据tour的score排序  
    improve_population_tour = sorted(improve_population_tour,key = lambda x:x[1][0],reverse = True)
    #存储最佳的tour
    Best_tour_pool.append(improve_population_tour[0])
    
    i = 0
    while i <iteration: 
        new_population = model.evalutionProcess(crossover_proportion,mutation_proportion,\
                                                population_size,improve_population_tour,\
                                                trip_length,hotel_number,data_cleaned,trip_number,start_time)
        improve_population_tour = new_population
        Best_tour_pool.append(improve_population_tour[0])
        i += 1
    
    # =============================================================================
    #                           Plot parts 
    # ============================================================================= 
    #model.plotScatter(hotel_number,data_cleaned)
    Best_tour_sorted = sorted(Best_tour_pool,key = lambda x:x[1][0],reverse = True)
    best_tour = Best_tour_sorted[0][0]
    #model.plotLink(best_tour,data_cleaned)
    # =============================================================================
    #                           record score 
    # =============================================================================
    score_list.append(Best_tour_sorted[0][1][0])
end = time.process_time()
print("平均计算时间:",(end-start)/10)
print("线路的平均分" ,sum(score_list)/10)
print("线路的最高分" ,max(score_list))

'''                    2.recommand  the travel mode                         '''
# =============================================================================
#                           Setting Parameters 
# =============================================================================








    
    
    