import numpy as np
import os
import os.path
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib
from matplotlib.axes._axes import _log as matplotlib_axes_logger
matplotlib_axes_logger.setLevel('ERROR')

from aiphad import  make_color_list
from mpl_toolkits.mplot3d import Axes3D

def print_for_json(pdc):
    """
    print attributes with json format
    """
    
    if (pdc._page_type == "ternary_section"):
        print('{')
        for i in range(pdc.prob_num): # for i in range(num_multi):
            rank = i + 1
            print(
                  '"Next_Point_{}":'.format(rank),
                  pdc.composition_data_list[pdc.multi_uncertainty_index[i]],
                  ',',
                  '"Row_Number_{}":'.format(rank),
                  pdc.multi_uncertainty_index[i],
                  ','
                 )

        print('"Uncertainty_score_points":[')
        for i in range(len(pdc.u_score_list)):
            if i == len(pdc.u_score_list) - 1:
                print(
                      '[',
                          pdc.data_list[pdc.unlabeled_index_list][i][0], ',',
                          pdc.data_list[pdc.unlabeled_index_list][i][1],
                      ']'
                     )
            else:
                print(
                      '[',
                          pdc.data_list[pdc.unlabeled_index_list][i][0], ',',
                          pdc.data_list[pdc.unlabeled_index_list][i][1],
                      '],'
                     )
        print('],')

        print('"Uncertainty_score":[')
        for i in range(len(pdc.u_score_list)):
            if i == len(pdc.u_score_list) - 1:
                print(pdc.u_score_list[i], '],')
            else:
                print(pdc.u_score_list[i], ',')

        hex_color_list = make_color_list(pdc.u_score_list)
        print('"Uncertainty_score_color":[')
        for i in range(len(pdc.u_score_list)):
            if i == len(pdc.u_score_list) - 1:
                print('"{}"'.format(hex_color_list[i]), '],')
            else:
                print('"{}"'.format(hex_color_list[i]), ',')

        print('"Phase_diagram_estimation_points":[')
        for i in range(len(pdc.composition_data_list)):
            if i == len(pdc.composition_data_list) - 1:
                print(pdc.composition_data_list[i], '],')
            else:
                print(pdc.composition_data_list[i], ',')

        print('"Phase_diagram_estimation":[')
        for i in range(len(pdc.composition_data_list)):
            if i == len(pdc.composition_data_list) - 1:
                print(pdc.predicted_all_labels[i], '],')
            else:
                print(pdc.predicted_all_labels[i], ',')

        propose_num = pdc.prob_num
        print('"phase_type_num":' + str(pdc.phase_type_num) + ",")

        for i in range(pdc.phase_type_num):
            pdc.ranking = np.array(pdc.label_distributions[:,i]).argsort()[::-1]
            pdc.data_ranking = [pdc.composition_data_list[pdc.unlabeled_index_list[pdc.ranking[j]]] for j in range(propose_num)]
            data_dist = [pdc.label_distributions[:,i][pdc.ranking[j]] for j in range(propose_num)]

            print('"belong_proba_{}":['.format(i))
            for j in range(propose_num):
                if j == propose_num - 1:
                    print(list(pdc.data_ranking[j]))
                else:
                    print(list(pdc.data_ranking[j]), ",")
            print('],')
            

            print('"proba_value_{}":['.format(i))
            for j in range(propose_num):
                if j == propose_num - 1:
                    print(data_dist[j])
                else:
                    print(data_dist[j], ",")
            if i == pdc.phase_type_num-1:
                print("]")
            else:
                print("],")
        print('}')

    if (pdc._page_type == "two_variables"):
        print("{")
        for i in range(pdc.prob_num):
            rank = i + 1
            print(
                  '"Next_Point_{}":['.format(rank),
                  np.array(pdc.data_list[pdc.multi_uncertainty_index[i]])[0], ',',
                  np.array(pdc.data_list[pdc.multi_uncertainty_index[i]])[1], '],'
                 )
            print(
                  '"Row_Number_{}":'.format(rank),
                str(pdc.multi_uncertainty_index[i]), ","
                )

        print('"Uncertainty_score_points":[')
        for i in range(len(pdc.u_score_list)):
            if i == len(pdc.u_score_list) - 1:
                print('[', pdc.data_list[pdc.unlabeled_index_list][i][0], ',', pdc.data_list[pdc.unlabeled_index_list][i][1],"]")
            else:
                print('[', pdc.data_list[pdc.unlabeled_index_list][i][0], ',', pdc.data_list[pdc.unlabeled_index_list][i][1] ,'],')
        print('],')

        hex_color_list = make_color_list(pdc.u_score_list)
        print('"Uncertainty_score_color":[')
        for i in range(len(pdc.u_score_list)):
            if i == len(pdc.u_score_list) - 1:
                print('"{}"'.format(hex_color_list[i]), '],')
            else:
                print('"{}"'.format(hex_color_list[i]), ',')

        print('"Uncertainty_score":[')
        for i in range(len(pdc.u_score_list)):
            if i == len(pdc.u_score_list) - 1:
                print(pdc.u_score_list[i])
            else:
                print(pdc.u_score_list[i],',')
        print('],')

        print('"Phase_diagram_estimation_points":[')
        for i in range(len(pdc.predicted_all_labels)):
            if i == len(pdc.predicted_all_labels) - 1:
                print('[', pdc.data_list[i][0], ',', pdc.data_list[i][1],"]")
            else:
                print('[', pdc.data_list[i][0], ',', pdc.data_list[i][1] ,'],')
        print('],')

        print('"Phase_diagram_estimation":[')
        for i in range(len(pdc.predicted_all_labels)):
            if i == len(pdc.predicted_all_labels) - 1:
                print(pdc.predicted_all_labels[i])
            else:
                print(pdc.predicted_all_labels[i],',')
        print('],')

        propose_num = pdc.prob_num
        print('"phase_type_num":' + str(pdc.phase_type_num) + ",")

        for i in range(pdc.phase_type_num):
            pdc.ranking = np.array(pdc.label_distributions[:,i]).argsort()[::-1]
            pdc.data_ranking = [pdc.data_list[pdc.unlabeled_index_list[pdc.ranking[j]]] for j in range(propose_num)]
            data_dist = [pdc.label_distributions[:,i][pdc.ranking[j]] for j in range(propose_num)]

            print('"belong_proba_{}":['.format(i))
            for j in range(propose_num):
                if j == propose_num - 1:
                    print("[", pdc.data_ranking[j][0], ",", pdc.data_ranking[j][1], "]")
                else:
                    print("[", pdc.data_ranking[j][0], ",", pdc.data_ranking[j][1], "],")

            print('],')
            
            print('"proba_value_{}":['.format(i))
            for j in range(propose_num):
                if j == propose_num - 1:
                    print(data_dist[j])
                else:
                    print(data_dist[j], ",")
            if i == pdc.phase_type_num-1:
                print("]")
            else:
                print("],")
        print("}")
    
    elif pdc._page_type == "three_variables":

        print("{")
        for i in range(pdc.prob_num):
            rank = i + 1

            print(
                  '"Next_Point_{}":['.format(rank),
                  np.array(pdc.data_list[pdc.multi_uncertainty_index[i]])[0], ',',
                  np.array(pdc.data_list[pdc.multi_uncertainty_index[i]])[1], ',',
                  np.array(pdc.data_list[pdc.multi_uncertainty_index[i]])[2], '],'
                 )
            print(
                  '"Row_Number_{}":'.format(rank),
                  str(pdc.multi_uncertainty_index[i]), ","
                 )

        print('"Uncertainty_score_points":[')
        for i in range(len(pdc.u_score_list)):
            if i == len(pdc.u_score_list) - 1:
                print(list(pdc.data_list[pdc.unlabeled_index_list][i]))
            else:
                print(list(pdc.data_list[pdc.unlabeled_index_list][i]), ',')
        print('],')

        hex_color_list = make_color_list(pdc.u_score_list)
        print('"Uncertainty_score_color":[')
        for i in range(len(pdc.u_score_list)):
            if i == len(pdc.u_score_list) - 1:
                print('"{}"'.format(hex_color_list[i]), '],')
            else:
                print('"{}"'.format(hex_color_list[i]), ',')

        print('"Uncertainty_score":[')
        for i in range(len(pdc.u_score_list)):
            if i == len(pdc.u_score_list) - 1:
                print(pdc.u_score_list[i])
            else:
                print(pdc.u_score_list[i], ',')
        print('],')

        print('"Phase_diagram_estimation_points":[')
        for i in range(len(pdc.predicted_all_labels)):
            if i == len(pdc.predicted_all_labels) - 1:
                print(list(pdc.data_list[i]))
            else:
                print(list(pdc.data_list[i]), ',')
        print('],')

        print('"Phase_diagram_estimation":[')
        for i in range(len(pdc.predicted_all_labels)):
            if i == len(pdc.predicted_all_labels) - 1:
                print(pdc.predicted_all_labels[i])
            else:
                print(pdc.predicted_all_labels[i], ',')
        print('],')

        propose_num = pdc.prob_num
        print('"phase_type_num":' + str(pdc.phase_type_num) + ",")

        for i in range(pdc.phase_type_num):
            pdc.ranking = np.array(pdc.label_distributions[:,i]).argsort()[::-1]
            pdc.data_ranking = [pdc.data_list[pdc.unlabeled_index_list[pdc.ranking[j]]] for j in range(propose_num)]
            data_dist = [pdc.label_distributions[:,i][pdc.ranking[j]] for j in range(propose_num)]

            print('"belong_proba_{}":['.format(i))
            for j in range(propose_num):
                if j == propose_num - 1:
                    print(list(pdc.data_ranking[j]))
                else:
                    print(list(pdc.data_ranking[j]), ",")
            print('],')

            print('"proba_value_{}":['.format(i))
            for j in range(propose_num):
                if j == propose_num - 1:
                    print(data_dist[j])
                else:
                    print(data_dist[j], ",")
            if i == pdc.phase_type_num-1:
                print("]")
            else:
                print("],")
        print("}")

    elif pdc._page_type == "quaternary_section":
        print('{')
        for i in range(pdc.prob_num): # for i in range(num_multi):
            rank = i + 1
            print(
                  '"Next_Point_{}":'.format(rank),
                  pdc.composition_data_list[pdc.multi_uncertainty_index[i]],
                  ',',
                  '"Row_Number_{}":'.format(rank),
                  pdc.multi_uncertainty_index[i],
                  ','
                 )

        print('"Uncertainty_score_points":[')
        for i in range(len(pdc.u_score_list)):
            if i == len(pdc.u_score_list) - 1:
                print(
                      '[',
                          pdc.data_list[pdc.unlabeled_index_list][i][0], ',',
                          pdc.data_list[pdc.unlabeled_index_list][i][1], ',',
                          pdc.data_list[pdc.unlabeled_index_list][i][2],
                      ']'
                     )
            else:
                print(
                      '[',
                          pdc.data_list[pdc.unlabeled_index_list][i][0], ',',
                          pdc.data_list[pdc.unlabeled_index_list][i][1], ',',
                          pdc.data_list[pdc.unlabeled_index_list][i][2],
                      '],'
                     )
        print('],')

        print('"Uncertainty_score":[')
        for i in range(len(pdc.u_score_list)):
            if i == len(pdc.u_score_list) - 1:
                print(pdc.u_score_list[i], '],')
            else:
                print(pdc.u_score_list[i], ',')

        hex_color_list = make_color_list(pdc.u_score_list)
        print('"Uncertainty_score_color":[')
        for i in range(len(pdc.u_score_list)):
            if i == len(pdc.u_score_list) - 1:
                print('"{}"'.format(hex_color_list[i]), '],')
            else:
                print('"{}"'.format(hex_color_list[i]), ',')

        print('"Phase_diagram_estimation_points":[')
        for i in range(len(pdc.composition_data_list)):
            if i == len(pdc.composition_data_list) - 1:
                print(pdc.composition_data_list[i], '],')
            else:
                print(pdc.composition_data_list[i], ',')

        print('"Phase_diagram_estimation":[')
        for i in range(len(pdc.composition_data_list)):
            if i == len(pdc.composition_data_list) - 1:
                print(pdc.predicted_all_labels[i], '],')
            else:
                print(pdc.predicted_all_labels[i], ',')

        propose_num = pdc.prob_num
        print('"phase_type_num":' + str(pdc.phase_type_num) + ",")

        for i in range(pdc.phase_type_num):
            pdc.ranking = np.array(pdc.label_distributions[:,i]).argsort()[::-1]
            pdc.data_ranking = [pdc.composition_data_list[pdc.unlabeled_index_list[pdc.ranking[j]]] for j in range(propose_num)]
            data_dist = [pdc.label_distributions[:,i][pdc.ranking[j]] for j in range(propose_num)]

            print('"belong_proba_{}":['.format(i))
            for j in range(propose_num):
                if j == propose_num - 1:
                    print(list(pdc.data_ranking[j]))
                else:
                    print(list(pdc.data_ranking[j]), ",")
            print('],')
            

            print('"proba_value_{}":['.format(i))
            for j in range(propose_num):
                if j == propose_num - 1:
                    print(data_dist[j])
                else:
                    print(data_dist[j], ",")
            if i == pdc.phase_type_num-1:
                print("]")
            else:
                print("],")
        print('}')

    elif pdc._page_type == "ternary":
        print('{')
        for i in range(pdc.prob_num):
            rank = i + 1
            print(
                  '"Next_Point_{}":'.format(rank),
                  pdc.composition_data_list[pdc.multi_uncertainty_index[i]],
                  ',',
                  '"Row_Number_{}":'.format(rank),
                  pdc.multi_uncertainty_index[i],
                  ','
                 )

        print('"Uncertainty_score_points":[')
        for i in range(len(pdc.u_score_list)):
            if i == len(pdc.u_score_list) - 1:
                print(
                      '[',
                          pdc.data_list[pdc.unlabeled_index_list][i][0], ',',
                          pdc.data_list[pdc.unlabeled_index_list][i][1], ',',
                          pdc.data_list[pdc.unlabeled_index_list][i][2],
                      ']'
                     )
            else:
                print(
                      '[',
                          pdc.data_list[pdc.unlabeled_index_list][i][0], ',',
                          pdc.data_list[pdc.unlabeled_index_list][i][1], ',',
                          pdc.data_list[pdc.unlabeled_index_list][i][2],
                      '],'
                     )
        print('],')

        print('"Uncertainty_score":[')
        for i in range(len(pdc.u_score_list)):
            if i == len(pdc.u_score_list) - 1:
                print(pdc.u_score_list[i], '],')
            else:
                print(pdc.u_score_list[i], ',')

        hex_color_list = make_color_list(pdc.u_score_list)

        print('"Uncertainty_score_color":[')
        for i in range(len(pdc.u_score_list)):
            if i == len(pdc.u_score_list) - 1:
                print('"{}"'.format(hex_color_list[i]), '],')
            else:
                print('"{}"'.format(hex_color_list[i]), ',')

        print('"Phase_diagram_estimation_points":[')
        for i in range(len(pdc.composition_data_list)):
            if i == len(pdc.composition_data_list) - 1:
                print(pdc.composition_data_list[i], '],')
            else:
                print(pdc.composition_data_list[i], ',')

        print('"Phase_diagram_estimation":[')
        for i in range(len(pdc.composition_data_list)):
            if i == len(pdc.composition_data_list) - 1:
                print(pdc.predicted_all_labels[i], '],')
            else:
                print(pdc.predicted_all_labels[i], ',')

        phase_type_num = len(pdc.phase_id_dict)
        print('"phase_type_num":' + str(phase_type_num) + ",")

        propose_num = pdc.prob_num 
        for i in range(phase_type_num):
            pdc.ranking = np.array(pdc.label_distributions[:,i]).argsort()[::-1]
            pdc.data_ranking = [pdc.composition_data_list[pdc.unlabeled_index_list[pdc.ranking[j]]] for j in range(propose_num)]
            data_dist = [pdc.label_distributions[:,i][pdc.ranking[j]] for j in range(propose_num)]

            print('"belong_proba_{}":['.format(i))
            for j in range(propose_num):
                if j == propose_num - 1:
                    print(
                          "[",
                              pdc.data_ranking[j][0], ",",
                              pdc.data_ranking[j][1], ",",
                              pdc.data_ranking[j][2], ",",
                              pdc.data_ranking[j][3],
                           "]")
                else:
                    print(
                          "[",
                              pdc.data_ranking[j][0], ",",
                              pdc.data_ranking[j][1], ",",
                              pdc.data_ranking[j][2], ",",
                              pdc.data_ranking[j][3],
                          "],")
            print('],')

            print('"proba_value_{}":['.format(i))
            for j in range(propose_num):
                if j == propose_num - 1:
                    print(data_dist[j])
                else:
                    print(data_dist[j], ",")
            if i == phase_type_num-1:
                print("]")
            else:
                print("],")
        print('}')

def plot_out(pdc, elev_num = 30, azim_num = 45, save_fig = False, extension = "png", directory_name = "./out1"):
    """
    draw figures of results

    specify whether the image is saved as an image or outputted directly

    Parameters
    ----------
    elev_num:int
        elevation angle from z axis viewpoint
    azim_num:int
        azimuth from x, y axis direction
    save_fig:bool
        option for saving figure
    extension:str
        extension for the saving file
    directory_name:str
        directiory for the saving file
    """
    window_width = 10
    color_array = default_color() 
    dirname =  directory_name + "/" + pdc._page_type; 
    os.makedirs(dirname, exist_ok=True)
    array_t = []
    diff_number = 0

    for i in pdc.phase_id_dict:
        array_t.append(pdc.phase_id_dict[i])
    
    diff_number = min(array_t)
   
    if pdc._page_type == "ternary_section":

        # Cheked points
        fig = plt.figure(figsize=(10,10))
        for i in pdc.labeled_index_list:
            plt.scatter([pdc.data_list[i][0]], [pdc.data_list[i][1]], c=color_array[pdc.label_list[i]-diff_number], marker="o", s=4*window_width, label=pdc.existed_phase[pdc.label_list[i]-diff_number], alpha = 0.7)
        for i in pdc.unlabeled_index_list:
            plt.scatter([pdc.data_list[i][0]], [pdc.data_list[i][1]], c='gray',label = 'unknown', marker = 'o', s=4*window_width, alpha = 0.7)
        plt.title("Checked Points")
        plt.ylim(-0.1,1.0)
        plt.gca().spines['bottom'].set_position('zero')
        plt.gca().spines['left'].set_position('zero')
        plt.gca().spines['right'].set_visible(False)
        plt.gca().spines['top'].set_visible(False)
        handles, labels = plt.gca().get_legend_handles_labels()
        unique = [(h, l) for i, (h, l) in enumerate(zip(handles, labels)) if l not in labels[:i]]
        plt.legend(*zip(*unique))
        if save_fig == True:
            #matplotlib.use('Agg')
            all_directory = dirname +"/Checked_points." + extension
            plt.savefig(all_directory, dpi=150)
        else:
            plt.show()

        #Uncertainty Score
        fig = plt.figure(figsize=(10,10))
        u_score_colors = cm.Greens(pdc.u_score_list)
        for i in pdc.labeled_index_list:
            plt.scatter([pdc.data_list[i][0]], [pdc.data_list[i][1]], c='white', marker="o", s=4*window_width,  alpha = 0.7)
        for i in range(len(pdc.data_list[pdc.unlabeled_index_list])):
            plt.scatter([pdc.data_list[pdc.unlabeled_index_list][i][0]], [pdc.data_list[pdc.unlabeled_index_list][i][1]],   c= u_score_colors[i], marker = 'o', s=4*window_width, alpha = 0.7)
        plt.title("Uncertainty Score")
        plt.ylim(-0.1,1.0)
        plt.gca().spines['bottom'].set_position('zero')
        plt.gca().spines['left'].set_position('zero')
        plt.gca().spines['right'].set_visible(False)
        plt.gca().spines['top'].set_visible(False)
        if save_fig == True:
            #matplotlib.use('Agg')
            all_directory = dirname +"/Uncertainty_score." + extension
            plt.savefig(all_directory, dpi=150)
        else:
            plt.show()

        # Estimated
        fig = plt.figure(figsize=(10,10))
        for i in pdc.unlabeled_index_list:
            plt.scatter([pdc.data_list[i][0]], [pdc.data_list[i][1]],  c=color_array[pdc.predicted_all_labels[i]-diff_number], marker = 'o', s= 4*window_width, alpha = 0.7)
        pointed_label_list = []
        for i in pdc.labeled_index_list:
            if pdc.label_list[i] not in pointed_label_list:
                plt.scatter([pdc.data_list[i][0]], [pdc.data_list[i][1]],  c=color_array[pdc.label_list[i]-diff_number], marker="o", s=4*window_width, label = pdc.existed_phase[pdc.label_list[i]-diff_number], alpha = 0.7)
                pointed_label_list.append(pdc.label_list[i])
            else:
                plt.scatter([pdc.data_list[i][0]], [pdc.data_list[i][1]],  c=color_array[pdc.label_list[i]-diff_number], marker="o", s=4*window_width, alpha = 0.7)
        plt.title("Estimated")
        plt.ylim(-0.1,1.0)
        plt.gca().spines['bottom'].set_position('zero')
        plt.gca().spines['left'].set_position('zero')
        plt.gca().spines['right'].set_visible(False)
        plt.gca().spines['top'].set_visible(False)
        plt.legend()
        if save_fig == True:
            #matplotlib.use('Agg')
            all_directory = dirname +"/Estimated." + extension
            plt.savefig(all_directory, dpi=150)
        else:
            plt.show()

    elif pdc._page_type == "two_variables":

        # Cheked points
        window_width = 30
        color_array = default_color() 
        fig = plt.figure(figsize=(10,10))
        for i in pdc.labeled_index_list:
            plt.scatter([pdc.data_list[i][0]], [pdc.data_list[i][1]], c=color_array[pdc.label_list[i]-diff_number], marker="o", s=4*window_width, label=pdc.existed_phase[pdc.label_list[i]-diff_number], alpha = 0.7)
        for i in pdc.unlabeled_index_list:
            plt.scatter([pdc.data_list[i][0]], [pdc.data_list[i][1]], c='gray',label = 'unknown', marker = 'o', s=4*window_width, alpha = 0.7)
        plt.title("Checked Points")
        plt.gca().spines['top'].set_visible(False)
        plt.gca().spines['right'].set_visible(False)
        plt.gca().spines['left'].set_visible(False)
        plt.gca().spines['bottom'].set_visible(False)
        handles, labels = plt.gca().get_legend_handles_labels()
        unique = [(h, l) for i, (h, l) in enumerate(zip(handles, labels)) if l not in labels[:i]]
        plt.legend(loc='upper left', bbox_to_anchor=(1, 1),*zip(*unique))
        if save_fig == True:
            #matplotlib.use('Agg')
            all_directory = dirname +"/Checked_points." + extension
            plt.savefig(all_directory, dpi=150)
        else:
            plt.show()

        #Uncertainty Score
        fig = plt.figure(figsize=(10,10))
        u_score_colors = cm.Greens(pdc.u_score_list)
        for i in range(len(pdc.data_list[pdc.unlabeled_index_list])):
            plt.scatter([pdc.data_list[pdc.unlabeled_index_list][i][0]], [pdc.data_list[pdc.unlabeled_index_list][i][1]],  c= u_score_colors[i], marker = 'o', s=4*window_width, alpha = 0.7)
        plt.title("Uncertainty Score")
        plt.gca().spines['top'].set_visible(False)
        plt.gca().spines['right'].set_visible(False)
        plt.gca().spines['left'].set_visible(False)
        plt.gca().spines['bottom'].set_visible(False)
        plt.legend()
        if save_fig == True:
            #matplotlib.use('Agg')
            all_directory = dirname +"/Uncertainty_score." + extension
            plt.savefig(all_directory, dpi=150)
        else:
            plt.show()

        # Estimated
        fig = plt.figure(figsize=(10,10))
        for i in pdc.unlabeled_index_list:
            plt.scatter([pdc.data_list[i][0]], [pdc.data_list[i][1]],  c=color_array[pdc.predicted_all_labels[i]-diff_number], marker = 'o', s= 4*window_width, alpha = 0.7)
        pointed_label_list = []
        for i in pdc.labeled_index_list:
            if pdc.label_list[i] not in pointed_label_list:
                plt.scatter([pdc.data_list[i][0]], [pdc.data_list[i][1]],  c=color_array[pdc.label_list[i]-diff_number], marker="o", s=4*window_width, label = pdc.existed_phase[pdc.label_list[i]-diff_number], alpha = 0.7)
                pointed_label_list.append(pdc.label_list[i])
            else:
                plt.scatter([pdc.data_list[i][0]], [pdc.data_list[i][1]],  c=color_array[pdc.label_list[i]-diff_number], marker="o", s=4*window_width, alpha = 0.7)
        plt.title("Estimated")
        plt.gca().spines['top'].set_visible(False)
        plt.gca().spines['right'].set_visible(False)
        plt.gca().spines['left'].set_visible(False)
        plt.gca().spines['bottom'].set_visible(False)
        plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
        if save_fig == True:
            #matplotlib.use('Agg')
            all_directory = dirname +"/Estimated." + extension
            plt.savefig(all_directory, dpi=150)
        else:
            plt.show()

    elif pdc._page_type == "three_variables":
        window_width = 10
        color_array = default_color() 

        # Cheked points
        fig = plt.figure(figsize=(10,10))
        ax = Axes3D(fig)
        for i in pdc.labeled_index_list:
            ax.scatter([pdc.data_list[i][0]], [pdc.data_list[i][1]], [pdc.data_list[i][2]], c = color_array[pdc.label_list[i]-diff_number], marker="o", s=4*window_width, label=pdc.existed_phase[pdc.label_list[i]-diff_number], alpha = 0.7)
        for i in pdc.unlabeled_index_list:
            ax.scatter([pdc.data_list[i][0]], [pdc.data_list[i][1]], [pdc.data_list[i][2]], c='gray',label = 'unknown', marker = 'o', s=4*window_width, alpha = 0.7)
        plt.title("Checked Points")
        ax.set_xlim(pdc.data_list[0][0],pdc.data_list[len(pdc.data_list)-1][0])
        ax.set_ylim(pdc.data_list[0][1],pdc.data_list[len(pdc.data_list)-1][1])
        ax.set_zlim(pdc.data_list[0][2],pdc.data_list[len(pdc.data_list)-1][2])
        ax.view_init(elev=elev_num, azim=azim_num)
        handles, labels = plt.gca().get_legend_handles_labels()
        unique = [(h, l) for i, (h, l) in enumerate(zip(handles, labels)) if l not in labels[:i]]
        plt.legend(*zip(*unique))
        if save_fig == True:
            #matplotlib.use('Agg')
            all_directory = dirname +"/Checked_points_%s_%s." + extension
            plt.savefig(all_directory % (('%03d' % int(elev_num)),('%03d' % int(azim_num))), dpi=150)
        else:
            plt.show()

        #Uncertainty Score
        fig = plt.figure(figsize=(10,10))
        ax = Axes3D(fig)
        u_score_colors = cm.Greens(pdc.u_score_list)
        for i in range(len(pdc.data_list[pdc.unlabeled_index_list])):
            ax.scatter([pdc.data_list[pdc.unlabeled_index_list][i][0]], [pdc.data_list[pdc.unlabeled_index_list][i][1]], [pdc.data_list[pdc.unlabeled_index_list][i][2]],  c= u_score_colors[i], marker = 'o', s=4*window_width, alpha = 0.7)
        plt.title("Uncertainty Score")
        ax.set_xlim(pdc.data_list[0][0],pdc.data_list[len(pdc.data_list)-1][0])
        ax.set_ylim(pdc.data_list[0][1],pdc.data_list[len(pdc.data_list)-1][1])
        ax.set_zlim(pdc.data_list[0][2],pdc.data_list[len(pdc.data_list)-1][2])
        ax.view_init(elev=elev_num, azim=azim_num)
        if save_fig == True:
            #matplotlib.use('Agg')
            all_directory = dirname +"/Uncertainty_score_%s_%s." + extension
            plt.savefig(all_directory % (('%03d' % int(elev_num)),('%03d' % int(azim_num))), dpi=150)
        else:
            plt.show()

        # Estimated
        fig = plt.figure(figsize=(10,10))
        ax = Axes3D(fig)
        for i in pdc.unlabeled_index_list:
            ax.scatter([pdc.data_list[i][0]], [pdc.data_list[i][1]], [pdc.data_list[i][2]],  c=color_array[pdc.predicted_all_labels[i]-diff_number], marker = 'o', s= 4*window_width, alpha = 0.7)
        pointed_label_list = []
        for i in pdc.labeled_index_list:
            if pdc.label_list[i] not in pointed_label_list:
                ax.scatter([pdc.data_list[i][0]], [pdc.data_list[i][1]], [pdc.data_list[i][2]],  c=color_array[pdc.label_list[i]-diff_number], marker="o", s=4*window_width, label = pdc.existed_phase[pdc.label_list[i]-diff_number], alpha = 0.7)
                pointed_label_list.append(pdc.label_list[i])
            else:
                ax.scatter([pdc.data_list[i][0]], [pdc.data_list[i][1]], [pdc.data_list[i][2]],  c=color_array[pdc.label_list[i]-diff_number], marker="o", s=4*window_width, alpha = 0.7)
        plt.title("Estimated")
        ax.set_xlim(pdc.data_list[0][0],pdc.data_list[len(pdc.data_list)-1][0])
        ax.set_ylim(pdc.data_list[0][1],pdc.data_list[len(pdc.data_list)-1][1])
        ax.set_zlim(pdc.data_list[0][2],pdc.data_list[len(pdc.data_list)-1][2])
        ax.view_init(elev=elev_num, azim=azim_num)
        plt.legend()
        if save_fig == True:
            #matplotlib.use('Agg')
            all_directory = dirname +"/Estimated_%s_%s." + extension
            plt.savefig(all_directory % (('%03d' % int(elev_num)),('%03d' % int(azim_num))), dpi=150)
        else:
            plt.show()

    elif pdc._page_type == "quaternary_section":
        window_width = 10
        color_array = default_color() 
        # Cheked points
        fig = plt.figure(figsize=(10,10))
        ax = Axes3D(fig)
        for i in pdc.labeled_index_list:
            ax.scatter([pdc.data_list[i][0]], [pdc.data_list[i][1]], [pdc.data_list[i][2]], c=color_array[pdc.label_list[i]-diff_number], marker="o", s=4*window_width, label=pdc.existed_phase[pdc.label_list[i]-diff_number], alpha = 0.7)
        for i in pdc.unlabeled_index_list:
            ax.scatter([pdc.data_list[i][0]], [pdc.data_list[i][1]], [pdc.data_list[i][2]], c='gray',label = 'unknown', marker = 'o', s=4*window_width, alpha = 0.7)
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.set_zlim(0, 1)
        plt.title("Checked Points")
        handles, labels = plt.gca().get_legend_handles_labels()
        unique = [(h, l) for i, (h, l) in enumerate(zip(handles, labels)) if l not in labels[:i]]
        plt.legend(*zip(*unique))
        ax.view_init(elev=elev_num, azim=azim_num)
        if save_fig == True:
            #matplotlib.use('Agg')
            all_directory = dirname +"/Checked_points_%s_%s." + extension
            plt.savefig(all_directory % (('%03d' % int(elev_num)),('%03d' % int(azim_num))), dpi=150)
        else:
            plt.show()

        #Uncertainty Score
        fig = plt.figure(figsize=(10,10))
        ax = Axes3D(fig)
        u_score_colors = cm.Greens(pdc.u_score_list)
        for i in range(len(pdc.data_list[pdc.unlabeled_index_list])):
            ax.scatter([pdc.data_list[pdc.unlabeled_index_list][i][0]], [pdc.data_list[pdc.unlabeled_index_list][i][1]], [pdc.data_list[pdc.unlabeled_index_list][i][2]],  c= u_score_colors[i], marker = 'o', s=4*window_width, alpha = 0.7)
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.set_zlim(0, 1)
        ax.view_init(elev=elev_num, azim=azim_num)
        plt.title("Uncertainty Score")
        if save_fig == True:
            #matplotlib.use('Agg')
            all_directory = dirname +"/Uncertainty_score_%s_%s." + extension
            plt.savefig(all_directory % (('%03d' % int(elev_num)),('%03d' % int(azim_num))), dpi=150)
        else:
            plt.show()

        # Estimated
        fig = plt.figure(figsize=(10,10))
        ax = Axes3D(fig)
        for i in pdc.unlabeled_index_list:
            ax.scatter([pdc.data_list[i][0]], [pdc.data_list[i][1]], [pdc.data_list[i][2]],  c=color_array[pdc.predicted_all_labels[i]-diff_number], marker = 'o', s= 4*window_width, alpha = 0.7)
        pointed_label_list = []
        for i in pdc.labeled_index_list:
            if pdc.label_list[i] not in pointed_label_list:
                ax.scatter([pdc.data_list[i][0]], [pdc.data_list[i][1]], [pdc.data_list[i][2]],  c=color_array[pdc.label_list[i]-diff_number], marker="o", s=4*window_width, label = pdc.existed_phase[pdc.label_list[i]-diff_number], alpha = 0.7)
                pointed_label_list.append(pdc.label_list[i])
            else:
                ax.scatter([pdc.data_list[i][0]], [pdc.data_list[i][1]], [pdc.data_list[i][2]],  c=color_array[pdc.label_list[i]-diff_number], marker="o", s=4*window_width, alpha = 0.7)
        plt.title("Estimated")
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.set_zlim(0, 1)
        ax.view_init(elev=elev_num, azim=azim_num)
        plt.legend()
        if save_fig == True:
            #matplotlib.use('Agg')
            all_directory = dirname +"/Estimated_%s_%s." + extension
            plt.savefig(all_directory % (('%03d' % int(elev_num)),('%03d' % int(azim_num))), dpi=150)
        else:
            plt.show()

    elif pdc._page_type == "ternary":

        # Cheked points
        window_width = 10
        color_array = default_color() 
        fig = plt.figure(figsize=(10,10))
        ax = Axes3D(fig)
        x_label = []
        y_label = []
        z_label = []
        for i in pdc.data_list:
            x_label.append(float(i[0]))
            y_label.append(float(i[1]))
            z_label.append(float(i[2]))
        for i in pdc.labeled_index_list:
            ax.scatter([pdc.data_list[i][0]], [pdc.data_list[i][1]], [pdc.data_list[i][2]], c=color_array[pdc.label_list[i]-diff_number], marker="o", s=4*window_width, label=pdc.existed_phase[pdc.label_list[i]-diff_number], alpha = 0.7)
        for i in pdc.unlabeled_index_list:
            ax.scatter([pdc.data_list[i][0]], [pdc.data_list[i][1]], [pdc.data_list[i][2]], c='gray',label = 'unknown', marker = 'o', s=4*window_width, alpha = 0.7)
        plt.title("Checked Points")
        ax.set_xlim(min(x_label),max(x_label))
        ax.set_ylim(min(y_label),max(y_label))
        ax.set_zlim(min(z_label),max(z_label))
        handles, labels = plt.gca().get_legend_handles_labels()
        unique = [(h, l) for i, (h, l) in enumerate(zip(handles, labels)) if l not in labels[:i]]
        plt.legend(*zip(*unique))
        ax.view_init(elev=elev_num, azim=azim_num)
        if save_fig == True:
            #matplotlib.use('Agg')
            all_directory = dirname +"/Checked_points_%s_%s." + extension
            plt.savefig(all_directory % (('%03d' % int(elev_num)),('%03d' % int(azim_num))), dpi=150)
        else:
            plt.show()

        #Uncertainty Score
        fig = plt.figure(figsize=(10,10))
        ax = Axes3D(fig)
        u_score_colors = cm.Greens(pdc.u_score_list)
        plt.title("Uncertainty Score")
        for i in range(len(pdc.data_list[pdc.unlabeled_index_list])):
            ax.scatter([pdc.data_list[pdc.unlabeled_index_list][i][0]], [pdc.data_list[pdc.unlabeled_index_list][i][1]], [pdc.data_list[pdc.unlabeled_index_list][i][2]],  c= u_score_colors[i], marker = 'o', s=4*window_width, alpha = 0.7)
        ax.set_xlim(min(x_label),max(x_label))
        ax.set_ylim(min(y_label),max(y_label))
        ax.set_zlim(min(z_label),max(z_label))
        ax.view_init(elev=elev_num, azim=azim_num)

        if save_fig == True:
            #matplotlib.use('Agg')
            all_directory = dirname +"/Uncertainty_score_%s_%s." + extension
            plt.savefig(all_directory % (('%03d' % int(elev_num)),('%03d' % int(azim_num))), dpi=150)
        else:
            plt.show()

        # Estimated
        fig = plt.figure(figsize=(10,10))
        ax = Axes3D(fig)
        for i in pdc.unlabeled_index_list:
            ax.scatter([pdc.data_list[i][0]], [pdc.data_list[i][1]], [pdc.data_list[i][2]],  c=color_array[pdc.predicted_all_labels[i]-diff_number], marker = 'o', s= 4*window_width, alpha = 0.7)
        pointed_label_list = []
        for i in pdc.labeled_index_list:
            if pdc.label_list[i] not in pointed_label_list:
                ax.scatter([pdc.data_list[i][0]], [pdc.data_list[i][1]], [pdc.data_list[i][2]],  c=color_array[pdc.label_list[i]-diff_number], marker="o", s=4*window_width, label = pdc.existed_phase[pdc.label_list[i]-diff_number], alpha = 0.7)
                pointed_label_list.append(pdc.label_list[i])
            else:
                ax.scatter([pdc.data_list[i][0]], [pdc.data_list[i][1]], [pdc.data_list[i][2]],  c=color_array[pdc.label_list[i]-diff_number], marker="o", s=4*window_width, alpha = 0.7)
        plt.title("Estimated")
        ax.set_xlim(min(x_label),max(x_label))
        ax.set_ylim(min(y_label),max(y_label))
        ax.set_zlim(min(z_label),max(z_label))
        plt.legend()
        ax.view_init(elev=elev_num, azim=azim_num)
        if save_fig == True:
            #matplotlib.use('Agg')
            all_directory = dirname +"/Estimated_%s_%s." + extension
            plt.savefig(all_directory % (('%03d' % int(elev_num)),('%03d' % int(azim_num))), dpi=150)
        else:
            plt.show()

def default_color():
    """
    colors for legend in output figure
    """
    color_array=[
        "#E60012", "#F39800", "#009944", "#0068B7", "#1D2088", "#920783",
        "#DE6641", "#E8AC51", "#F2E55C", "#39A869", "#4784BF", "#5D5099",
        "#A55B9A", "#F5B090", "#FCD7A1", "#FFF9B1", "#A5D4AD", "#A3BCE2",
        "#A59ACA", "#CFA7CD", "#C7000B", "#D28300", "#DFD000", "#00873C",
        "#005AA0", "#181878", "#800073", "#ff7f7f", "#ff7fbf", "#ff7fff",
        "#bf7fff", "#7f7fff", "#7fbfff", "#7fffff", "#7fffbf", "#7fff7f",
        "#bfff7f", "#ffff7f", "#ffbf7f", "#ff8e8e", "#ff8ec6", "#ff8eff",
        "#c68eff", "#8e8eff", "#8ec6ff", "#8effff", "#8effc6", "#8eff8e",
        "#c6ff8e", "#ffff8e", "#ffc68e", "#ff9e9e", "#ff9ece", "#ff9eff",
        "#ce9eff", "#9e9eff", "#9eceff", "#9effff", "#9effce", "#9eff9e",
        "#ceff9e", "#ffff9e", "#ffce9e", "#ffadad", "#ffadd6", "#ffadff",
        "#d6adff", "#adadff", "#add6ff", "#adffff", "#adffd6", "#adffad",
        "#d6ffad", "#ffffad", "#ffd6ad", "#ffbcbc", "#ffbcdd", "#ffbcff",
        "#ddbcff", "#bcbcff", "#bcddff", "#bcffff", "#bcffdd", "#bcffbc",
        "#ddffbc", "#ffffbc", "#ffddbc"]
    return color_array
