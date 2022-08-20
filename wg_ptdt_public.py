import pandas as pd
import numpy as np
from scipy import stats
import glob

def ptdt(structure_path, score_path):   
    structure_file = pd.read_csv(structure_path, sep = " ")
    score_file = pd.read_csv(score_path, sep = ",")
    score_file.columns = ['id', 'score']
    
    score_dictionary = score_file.set_index('id')['score'].to_dict()
    structure_file_prs = structure_file.replace(score_dictionary)

    structure_file_prs_1 = structure_file_prs[pd.to_numeric(structure_file_prs.iloc[:,1], errors='coerce').notnull()]
    structure_file_prs_2 = structure_file_prs_1[pd.to_numeric(structure_file_prs_1.iloc[:,2], errors='coerce').notnull()]
    structure_file_prs_3 = structure_file_prs_2[pd.to_numeric(structure_file_prs_2.iloc[:,3], errors='coerce').notnull()]

    structure_file_prs_3.loc[:,'PRS_mp'] = (structure_file_prs_3.iloc[:,2] + structure_file_prs_3.iloc[:,3])/2
    mp_sd = np.std(structure_file_prs_3['PRS_mp'])
    structure_file_prs_3.loc[:,'ptdt_dev'] = (structure_file_prs_3.iloc[:,1] - structure_file_prs_3.loc[:,'PRS_mp'])/mp_sd

    ptdt_pvalue = stats.ttest_1samp(structure_file_prs_3['ptdt_dev'],0).pvalue
    ptdt_mean = structure_file_prs_3['ptdt_dev'].mean()
    ptdt_low95 = structure_file_prs_3['ptdt_dev'].mean() - (1.96*np.std(structure_file_prs_3['ptdt_dev'])/np.sqrt(len(structure_file_prs_3)))
    ptdt_high95 = structure_file_prs_3['ptdt_dev'].mean() + (1.96*np.std(structure_file_prs_3['ptdt_dev'])/np.sqrt(len(structure_file_prs_3)))
    n_trios = len(structure_file_prs_3)
    
    return(pd.DataFrame(data={'mean': [ptdt_mean], 'low95': [ptdt_low95], 'high95': [ptdt_high95], 'pval': [ptdt_pvalue], 'n_trios': [n_trios]}))
    
