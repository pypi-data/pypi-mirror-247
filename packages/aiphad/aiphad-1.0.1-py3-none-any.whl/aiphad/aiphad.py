import numpy as np
import os
import os.path
import sys
import matplotlib.cm as cm
import csv

from scipy import stats
import sklearn.semi_supervised
from sklearn.preprocessing import StandardScaler

class pdc_sampler:
    """
    pdc_sampler instance

    Parameters
    ----------
    page_type: string
        specify page type from "two_variables", "three_variables", "ternary_section", "ternary", and "quaternary_section"
    input_data:　numpy.ndarray
        label for the phase ("-1" is used at the point with no label)
    estimation: string
        specify estimation method from 'LP' ,'LS'
    sampling : string 
        specify sampling method from 'LC', 'MS', 'EA', and 'RS'
    phase_id_option: dict
        label name. e.g. {"Fe": 0, "Cr": 1, "Ni": 2}
    proposal: integer
        number of proposals
    parameter_constraint: bool
        whether parameter constraint is used / not used
    prev_point: list
        previous experimental point
    multi_method : string
        specify multi uncertainty score option from 'OU' or 'NE'
    NE_k: integer
        exclusion of NE_k nearest neighbors from proposals
    """

    def __init__(self, page_type=None, input_data=None, estimation=None, gamma=None, alpha=None,\
                 sampling=None, phase_id_option=None, proposal = None,\
                 parameter_constraint = None, prev_point = None, \
                 multi_method = None, NE_k = None):

        self._input = input_data
        self._page_type = page_type
        self._LP_algorithm = estimation
        self.gamma = gamma
        self.alpha = alpha
        self._US_strategy = sampling
        self.phase_id_dict = 0

        if phase_id_option != None:
            self.phase_id_dict = phase_id_option
        else:
            self.phase_id_dict = None

        self.prob_num = int(proposal)

        self._parameter_constraint = parameter_constraint
        self.prev_point = prev_point
        
        self._multi_method = multi_method
        self.num_multi = int(proposal)
        if NE_k:
            self.NE_k = int(NE_k)
        else:
            self.NE_k = None
       

        self.data_list = []        
        self.u_score_list = 0
        self.unlabeled_index_list = 0
        self.predicted_all_labels = 0
        self.phase_type_num = 0
        self.label_distributions = 0
        self.data_list_std = 0
        self.label_train = 0
        self.label_list = []
        self.label_list_text = []
        self.composition_data_list = []
        self.labeled_index_list = []
        self.labeled_array_list = []
        self.existed_phase = []
        self.data_ranking = []
        self.ranking = []

    def fit(self,X = [],y = []):
        """
        perform phase diagram estimation using the label propagation method for inputted X and y

        Parameters
        ----------
        X:  numpy.ndarray
            data points in phase diagram
        y:　numpy.ndarray
            label for the phase ("-1" is used at the point with no label)
        """
        self.preprocessing(X,y)
        lp_model = self.calculate()
        self.postprocessing(lp_model) 

    def us(self):
        """
        calculate uncertainty score by EA, LC, MS, and RS method which is specified by user
        """

        if self._US_strategy == 'EA':
            self.us_EA()
        elif self._US_strategy == 'LC':
            self.us_LC()
        elif self._US_strategy == 'MS':
            self.us_MS()
        elif self._US_strategy == 'RS':
            self.us_RS()
        
        self.output_res()
    
    def cross_selection(self, prev_data, unlabeled_index_list, data_list):
        """
        use option to fix one variable for proposals

        Parameters
        ----------
        prev_data:numpy.ndarray
            previous experimental point
        
        unlabeled_index_list:list
            indexces of uncertain points
        
        data_list:numpy.ndarray
            all data points

        Returns
        ----------
        candidate_index_list:list
            Candicate indexes will be return if there are candidate points such that one variable is not changed.

        unlabeled_index_list:list
            Unlabeled indexes will be return if there are no candidate points such that one variable is not changed.
        
        """
        candidate_index_list = []
        for ui in unlabeled_index_list:
            if (prev_data == data_list[ui]).any():
                candidate_index_list.append(ui)

        if len(candidate_index_list) > 0:
            return candidate_index_list
        else:
            return unlabeled_index_list 

    ###########################################################
    ###ラベル名が最初にきているときの場合
    def make_data_labelbefore(self,reader):
        """
        create label and numeric data from input file or array

        transform from compositions to Cartesian coordinates

        Parameters
        ----------
        reader:_csv.reader
            all inputs (input from csv file or array)
        
        """
        if(type(self._input) == str):
            number = 0
        else: 
            number = -1
        
        for row in reader:
            if(type(self._input) == str):
                self.label_list_text.append(row[0])
            
            if (self._page_type == "ternary_section"):
                self.composition_data_list.append([float(p) for p in row[(1+number):]])
                self.data_list.append([(float(row[1+number])/2+float(row[3+number])),np.sqrt(3)*float(row[1+number])/2]) # xy list
            elif((self._page_type == "two_variables")or(self._page_type == "three_variables")):
                self.data_list.append([float(p) for p in row[(1+number):]]) # abc... list
            elif(self._page_type == "quaternary_section"):
                self.composition_data_list.append([float(p) for p in row[(1+number):]])
                x = float(row[1+number])/2+float(row[2+number])/2+float(row[4+number])
                y = np.sqrt(3)*float(row[1+number])/6+np.sqrt(3)*float(row[2+number])/2
                z = np.sqrt(6)*float(row[1+number])/3

                self.data_list.append([x, y, z])

            elif(self._page_type == "ternary"):
                
                self.composition_data_list.append([float(row[1+number]),float(row[2+number]),float(row[3+number]),float(row[4+number])])
                self.data_list.append([(float(row[1+number])/2+float(row[3+number])),np.sqrt(3)*float(row[1+number])/2,float(row[4+number])])

            elif(self._page_type == None):

                length_row = len(row)
                array_row = []
                for i in range(1+number,length_row):
                    array_row.append(float(row[i]))
                    #array_row.append(float(row[i+number]))
                self.data_list.append(array_row) # abc... list
                self.composition_data_list.append(array_row)

             

    ##########################################################
    ##ラベル名が最後にきている場合

    def make_data(self,reader):
    
        """
        create label and numeric data from input file or array then
        convert data list (e.g. a, b, c points to x, y points)

        Parameters
        ----------
        reader:_csv.reader
           all inputs. (input from csv file or array)
        
        """

        for row in reader:
                                           
            if (self._page_type == "ternary_section"):
                self.composition_data_list.append([float(row[0]),float(row[1]),float(row[2])])
                self.data_list.append([(float(row[0])/2+float(row[2])),np.sqrt(3)*float(row[0])/2]) # xy list
                if(type(self._input) == str):
                    self.label_list_text.append(row[3])
            elif(self._page_type == "two_variables"):
                self.data_list.append([float(row[0]),float(row[1])]) # abc... list
                if(type(self._input) == str):
                    self.label_list_text.append(row[2])
            
            elif(self._page_type == "three_variables"):
                self.data_list.append([float(row[0]),float(row[1]),float(row[2])]) # abc... list
                if(type(self._input) == str):
                    self.label_list_text.append(row[3])
            
            elif(self._page_type == "quaternary_section"):
                self.composition_data_list.append([float(row[0]),float(row[1]),float(row[2]),float(row[3])])
                x = float(row[0])/2+float(row[1])/2+float(row[3])
                y = np.sqrt(3)*float(row[0])/6+np.sqrt(3)*float(row[1])/2
                z = np.sqrt(6)*float(row[0])/3

                self.data_list.append([x, y, z]) # data_list.append([x/100,y/100,z/100])
                if(type(self._input) == str):
                    self.label_list_text.append(row[4])

            elif(self._page_type == "ternary"):
                
                self.composition_data_list.append([float(row[0]),float(row[1]),float(row[2]),float(row[3])])
                self.data_list.append([(float(row[0])/2+float(row[2])),np.sqrt(3)*float(row[0])/2,float(row[3])])
                if(type(self._input) == str):
                    self.label_list_text.append(row[4])

            elif(self._page_type == None):
                length_row = len(row)
                array_row = []
                for i in range(length_row - 1):
                    array_row.append(float(row[i])) 
                self.data_list.append(array_row) # abc... list
                self.composition_data_list.append(array_row)
                if(type(self._input) == str):
                    self.label_list_text.append(row[length_row-1])


    def make_label(self):
        """
        create label automatically depending on input file or value, specifined label or not

        """

        if type(self._input) == str:
            
            if type(self.phase_id_dict) != dict:
                count_id = 0
                self.phase_id_dict = {}
                label_name = []
                for i in self.label_list_text:
                    if i != "":
                        label_name.append(i)

                label_name = sorted(set(label_name), key=label_name.index)

                for j in label_name:
                    self.phase_id_dict[j] = count_id
                    count_id += 1

            #sort label((ex)c:2,b:1,a:0→a:0,b:1,c:2)
            self.phase_id_dict = dict(sorted(self.phase_id_dict.items(), key=lambda x:x[1]))
            self.label_list, self.labeled_index_list = self.make_label_list(self.phase_id_dict, self.label_list_text)

            color_count_id = 0
            color_label_name = []
            
            for i in self.label_list:
                if i == -1:
                    color_label_name.append(-1)
                else:
                    for j in self.phase_id_dict:
                        if i == self.phase_id_dict[j]:
                            color_label_name.append(color_count_id)
                            color_count_id += 1


        elif type(self._input) != str:
            
            if type(self.phase_id_dict) == dict:
                self.phase_id_dict = dict(sorted(self.phase_id_dict.items(), key=lambda x:x[1]))
                for i in self.label_list:
                    if i == -1:
                        self.label_list_text.append("")
                    else:
                        for j in self.phase_id_dict:
                            if i == self.phase_id_dict[j]:
                                self.label_list_text.append(j)
        
            elif type(self.phase_id_dict) != dict:
                self.phase_id_dict = {}
                label_name = []
                for i in self.label_list:
                    if i != -1:
                        label_name.append(i)
                label_name = list(set(label_name))
        
                for j in label_name:
                    self.phase_id_dict[j] = j

    def preprocessing(self,X,y):
        """
        make learning data and standardized data
        """
        if(type(self._input) == str):
            current_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
            f = open(os.path.join(current_dir, self._input), 'r')
            reader = csv.reader(f)
            header = next(reader)
            
            if(header != []):
                if((header[0] == "phase")or(header[0] == "objective")):
                    self.make_data_labelbefore(reader)        
                #else:
                #    self.make_label()
                else:
                    self.make_data(reader)        
            else:
                self.make_data(reader)


        else:
            reader = X
            header = []
            self.label_list = y

            self.make_data_labelbefore(reader)

        self.make_label() 

        for i in self.phase_id_dict:
            self.existed_phase.append(i)

        if self.num_multi == None:
            self.num_multi = 2
        if self.NE_k == None:
            self.NE_k = 1

        self.labeled_index_list = [index for index in range(len(self.data_list)) if self.label_list[index] != -1]
        for i in self.labeled_index_list:
             self.labeled_array_list.append(self.data_list[i])

        self.unlabeled_index_list = [index for index in range(len(self.data_list)) if self.label_list[index] == -1]
        if self.prob_num > len(self.unlabeled_index_list):
            self.prob_num = len(self.unlabeled_index_list)
        if self._parameter_constraint:
            self.prev_parameter = np.array(self.prev_point)
        #parameter_constraintを使うときは, １つ前のパラメータを入れる
        #python PDC_sampler.py data.csv --parameter_constraint True --prev_parameter [10, 20]

        self.data_list = np.array(self.data_list)
        phase_list = list(set(self.label_list))
        phase_list.remove(-1)
        self.phase_type_num = len(phase_list)
      
        ss = StandardScaler()
        ss.fit(self.data_list)
        self.data_list_std = ss.transform(self.data_list)
        self.label_train= np.copy(self.label_list)

    def calculate(self):
        """
        calculate with machine learning method (label spreading or label propagation) which is specified by user
        
        Returns
        ----------
        lp_model:sklearn.semi_supervised._label_spreading.LabelSpreading
        or
        sklearn.semi_supervised._label_propagation.LabelPropagation
        """

        if self._LP_algorithm == 'LS':
            
            if self.gamma == None and self.alpha == None:
                lp_model = sklearn.semi_supervised.LabelSpreading()
            elif self.gamma == None:
                lp_model = sklearn.semi_supervised.LabelSpreading(alpha = self.alpha)
            elif self.alpha == None:
                lp_model = sklearn.semi_supervised.LabelSpreading(gamma = self.gamma)
            else:
                lp_model = sklearn.semi_supervised.LabelSpreading(gamma = self.gamma, alpha = self.alpha)

        elif self._LP_algorithm == 'LP':

            if self.gamma == None:
                lp_model = sklearn.semi_supervised.LabelPropagation()
            else:
                lp_model = sklearn.semi_supervised.LabelPropagation(gamma = self.gamma)
        
        lp_model.fit(self.data_list_std, self.label_train)

        return lp_model


    def postprocessing(self,lp_model):
        """
        perform output processing for specified model attributes
        """
        self.predicted_all_labels = lp_model.transduction_
        self.label_distributions = lp_model.label_distributions_[self.unlabeled_index_list]
        self.label_distributions_all = lp_model.label_distributions_

    def us_EA(self):
        """
        calculate uncertainty score by EA
        """
        pred_entropies = stats.distributions.entropy(self.label_distributions.T)
        self.u_score_list = pred_entropies/np.max(pred_entropies)
        if self._parameter_constraint:
            cand_index_list = self.cross_selection(self.prev_parameter, self.unlabeled_index_list, self.data_list)
            pred_entropies_all = stats.distributions.entropy(self.label_distributions_all.T)
            cand_E_list = []
            for i in cand_index_list:
                cand_E_list.append(pred_entropies_all[i])
            self.uncertainty_index = [cand_index_list[np.argmax(cand_E_list)]]
        else:
            self.uncertainty_index = [self.unlabeled_index_list[np.argmax(self.u_score_list)]]
        
        # all ranking of uncertain point
        ranking = np.array(self.u_score_list).argsort()[::-1]
        self.multi_uncertainty_index = [self.unlabeled_index_list[ranking[i]] for i in range(len(self.unlabeled_index_list))]
    
        
    def us_LC(self):
        """
        calculate uncertainty score by LC
        """
        self.u_score_list = 1- np.max(self.label_distributions, axis = 1)
        if self._parameter_constraint:
            cand_index_list = self.cross_selection(self.prev_parameter, self.unlabeled_index_list, self.data_list)
            cand_LC_list = []
            for i in cand_index_list:
                cand_LC_list.append(self.label_distributions_all[i])
        
            self.uncertainty_index = [cand_index_list[np.argmax(1- np.max(np.array(cand_LC_list), axis = 1))]]
        else:
            self.uncertainty_index = [self.unlabeled_index_list[np.argmax(self.u_score_list)]] 
        # all ranking of uncertain point
        ranking = np.array(self.u_score_list).argsort()[::-1]
        self.multi_uncertainty_index = [self.unlabeled_index_list[ranking[i]] for i in range(len(self.unlabeled_index_list))]
        

    def us_MS(self):
        """
        calculate uncertainty score by MS
        """
        self.u_score_list = []
        for pro_dist in self.label_distributions:
            pro_ordered = np.sort(pro_dist)[::-1]
            margin = pro_ordered[0] - pro_ordered[1]
            self.u_score_list.append(margin)
        
        if self._parameter_constraint:
            cand_index_list = self.cross_selection(self.prev_parameter, self.unlabeled_index_list, self.data_list)
            cand_margin_list = []
            for i in cand_index_list:
                pro_ordered = np.sort(self.label_distributions_all[i])[::-1]
                margin = pro_ordered[0] - pro_ordered[1]
                cand_margin_list.append(margin)
            self.uncertainty_index = [cand_index_list[np.argmin(cand_margin_list)]]
        else:
            self.uncertainty_index = [self.unlabeled_index_list[np.argmin(self.u_score_list)]]
        self.u_score_list = 1 - np.array(self.u_score_list)
            
        # all ranking of uncertain point
        ranking = np.array(self.u_score_list).argsort()[::-1]
        self.multi_uncertainty_index = [self.unlabeled_index_list[ranking[i]] for i in range(len(self.unlabeled_index_list))]
    
    def us_RS(self):
        """
        calculate uncertainty score by RS
        """
        if self._parameter_constraint:
            cand_index_list = self.cross_selection(self.prev_parameter, self.unlabeled_index_list, self.data_list)
            self.uncertainty_index = [np.random.permutation(cand_index_list)[0]]
        else:
            self.uncertainty_index = [np.random.permutation(self.unlabeled_index_list)[0]]
        # all ranking of uncertain point
            ranking = np.random.permutation(self.unlabeled_index_list)
            self.multi_uncertainty_index = list(ranking)
        #########################
        self.u_score_list = [0.5 for i in range(len(self.label_distributions))]
            
        # all ranking of uncertain point
        self.multi_uncertainty_index = np.random.permutation(self.unlabeled_index_list)
        
    def make_label_list(self, phase_id_dict, label_list_text):
        """
        make label data before learning
    
        Parameters
        ----------
        phase_id_dict:dict
            list of label
        label_list_text:dist
            data of label ("" is used for no label, "")
        """
        label_list = []
        labeled_index_list = []
        for i in range(len(label_list_text)):
            sim_flag = 0
            atom_name = label_list_text[i]
            for j in phase_id_dict:
                if (atom_name == j):
                    sim_flag = 1
                    break
                elif(atom_name == j):
                    sim_flag = 0
            if (atom_name != "")&(sim_flag == 0):
                print("label_Error")
                return
            if atom_name == "":
                atom_to_label = -1
            else:
                atom_to_label = phase_id_dict[atom_name]
                labeled_index_list.append(i)
            label_list.append(atom_to_label)
        return label_list, labeled_index_list
    
    #########################
    # Added by Ryo

    def output_res(self):
    
        """
             make variables for outputs
        """


        if self.prob_num == 1:
            US_point = self.uncertainty_index

        if self.prob_num != 1:

            if self._multi_method == 'OU' or self._multi_method == None:
                US_point = self.multi_uncertainty_index[0:self.prob_num]

            if self._multi_method == 'NE':
                from scipy.spatial import distance
                neighbor_dist = []
                for i in range(len(self.data_list)):
                    dist_value = round(distance.euclidean(self.data_list[0],self.data_list[i]),5)
                    if dist_value not in neighbor_dist:
                        neighbor_dist.append(dist_value)
                delta = neighbor_dist[self.NE_k]
                US_point = []
                for i in range(len(self.multi_uncertainty_index)):
                    if i == 0: 
                        US_point.append(self.multi_uncertainty_index[i])
                    true_num = 0
                    for j in range(len(US_point)):
                        two_dist = distance.euclidean(self.data_list[US_point[j]], self.data_list[self.multi_uncertainty_index[i]])
                        if round(two_dist, 5) > delta:
                            true_num += 1
                    if true_num == len(US_point) and len(US_point) < self.prob_num: US_point.append(self.multi_uncertainty_index[i])
       
        self.proposals = []
        self.proposals_X = []
        self.proposals_us = []

        for i in range(len(US_point)):
            self.proposals.append(US_point[i])
            if self._page_type == "ternary_section" or self._page_type == "quaternary_section" or self._page_type == "ternary":
                self.proposals_X.append(list(self.composition_data_list[US_point[i]]))
            else:
                self.proposals_X.append(list(self.data_list[US_point[i]]))
            self.proposals_us.append(self.u_score_list[self.unlabeled_index_list.index(US_point[i])])

        self.belonging_index = []
        self.belonging_X = []
        self.belonging_probability = []

        for i in range(self.phase_type_num):
            ranking_p = np.array(self.label_distributions[:,i]).argsort()[::-1]
            if self._page_type == "ternary_section" or self._page_type == "quaternary_section" or self._page_type == "ternary":
                data_ranking_p = [list(self.composition_data_list[self.unlabeled_index_list[ranking_p[j]]]) for j in range(self.prob_num)]
            else:
                data_ranking_p = [list(self.data_list[self.unlabeled_index_list[ranking_p[j]]]) for j in range(self.prob_num)]
            prob_ranking_p = [self.label_distributions[ranking_p[j],i] for j in range(self.prob_num)]


            self.belonging_index.append([self.unlabeled_index_list[ranking_p[k]] for k in range(self.prob_num)])

            self.belonging_X.append(list(data_ranking_p))
            self.belonging_probability.append(list(prob_ranking_p))

def make_color_list(u_score_list):
    """
    create color list for figure

    Parameters
    ----------
    u_score_list:numpy.ndarray
        uncertainty score

    Returns
    ----------
    hex_color_list:list
        list of hex color
        
    """
    hex_color_list = []
    u_score_colors = cm.Greens(u_score_list)
    u_score_colors = 255 * u_score_colors
    for color_index in range(len(u_score_colors)):
        red = int(u_score_colors[color_index][0])
        green = int(u_score_colors[color_index][1])
        blue = int(u_score_colors[color_index][2])

        color_code = '#{}{}{}'.format(hex(red)[2:].zfill(2), hex(green)[2:].zfill(2), hex(blue)[2:].zfill(2))

        color_code = color_code.replace('0x', '')
        hex_color_list.append(color_code)
    return hex_color_list

