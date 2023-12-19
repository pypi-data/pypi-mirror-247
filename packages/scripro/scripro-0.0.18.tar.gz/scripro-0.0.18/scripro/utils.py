import math
import random
import os
import warnings
import pkg_resources
from collections import Counter
from multiprocessing import Pool
from itertools import islice
import anndata as ad
import math
import h5py
import pandas as pd
from scipy import sparse
import shutil
import matplotlib
from tqdm import tqdm  # 导入tqdm库
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from tqdm.contrib.concurrent import process_map
import subprocess
import pandas as pd
import os
import subprocess
import shutil
import pkg_resources
from pathlib import Path
import subprocess
import shutil
import pkg_resources
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
import scanpy as sc
import multiprocessing
import seaborn as sns
from lisa import FromCoverage, FromGenes, FromRegions
from lisa.core.assays import LISA_RP_Assay, delta_RP_wrapper, transform_RP,get_delta_RP,get_deltaRP_activation
from functools import partial
from scipy import stats, sparse
from lisa.core.utils import Log, LoadingBar
from scipy.stats import kendalltau, pearsonr, spearmanr

'''
def write_dataframe_to_tsv(df_subset, filename):
    series = df_subset.stack().reset_index()
    series = series[series.iloc[:, 2] != 0]
    with open(filename, 'w') as tsvfile:
        for _, row in series.iterrows():
            barcode = row['barcode']
            position_parts = row['level_1'].split('_')
            chr_name = position_parts[0]
            start_pos = position_parts[1]
            end_pos = position_parts[2]
            open_value = row[0]
            tsvfile.write(f"{chr_name}\t{start_pos}\t{end_pos}\t{barcode}\t{open_value}\n")
   '''         

def get_marker_for_group(adata, i, log2fc, pval, gene_list_len):
    tem_gene = list(sc.get.rank_genes_groups_df(adata, group=i, log2fc_min=log2fc, pval_cutoff=pval).sort_values(by = 'logfoldchanges',ascending = False)[0:500].names)
    if len(tem_gene) < gene_list_len:
        return i, None
    else:
        return i, tem_gene

def dataframe_to_sparse_tsv(df, filename):
    # 将DataFrame转换为稀疏格式
    sparse_df = df.astype(pd.SparseDtype("float", 0.0))
    # 从稀疏DataFrame获取稀疏矩阵的COO表示
    coo_matrix = sparse_df.sparse.to_coo()
    # 打开文件以写入
    with open(filename, 'w') as f:
        # 遍历非零元素
        for i, j, v in zip(coo_matrix.row, coo_matrix.col, coo_matrix.data):
            if v != 0:  # 只处理非零值
                barcode = df.index[i]  # 行索引作为barcode
                peak = df.columns[j]  # 列名作为peak信息
                chr_name, start_pos, end_pos = peak.split('_')  # 拆分peak信息
                # 写入文件
                f.write(f"{chr_name}\t{start_pos}\t{end_pos}\t{barcode}\t{v}\n")
                
                

'''
def process_and_merge(df, folder_path, n_num=20):
    num_partitions = min(n_num, len(df))
    dfs = np.array_split(df, num_partitions)
    pool = multiprocessing.Pool(processes=num_partitions)

    for i, df_subset in enumerate(dfs):
        filename = f"{folder_path}/output_{i}.tsv"
        pool.apply_async(write_dataframe_to_tsv, args=(df_subset, filename))

    pool.close()
    pool.join()

    merge_and_delete_tsv(folder_path)


def merge_and_delete_tsv(folder_path):
    subprocess.run(f'cat {folder_path}/*.tsv > {folder_path}/merge.tsv', shell=True)
    subprocess.run(f'rm {folder_path}/output*.tsv', shell=True)

def write_dataframe_to_tsv(df_subset, filename):
    series = df_subset.stack().reset_index()
    series = series[series.iloc[:, 2] != 0]
    with open(filename, 'w') as tsvfile:
        for _, row in series.iterrows():
            barcode = row['barcode']
            position_parts = row['level_1'].split('_')
            chr_name = position_parts[0]
            start_pos = position_parts[1]
            end_pos = position_parts[2]
            open_value = row[0]
            tsvfile.write(f"{chr_name}\t{start_pos}\t{end_pos}\t{barcode}\t{open_value}\n")
    '''

'''
def process_and_merge(df, folder_path, n_num=20):
    num_partitions = min(n_num, len(df))
    dfs = np.array_split(df, num_partitions)
    folder_path = Path(folder_path)

    with ProcessPoolExecutor(max_workers=num_partitions) as executor:
        futures = []
        for i, df_subset in enumerate(dfs):
            filename = folder_path / f"output_{i}.tsv"
            futures.append(executor.submit(write_dataframe_to_tsv, df_subset, filename))

        for future in futures:
            future.result()  # Wait for all processes to complete

    merge_and_delete_tsv(folder_path)

def merge_and_delete_tsv(folder_path):
    output_files = list(folder_path.glob('output_*.tsv'))
    with open(folder_path / 'merged.tsv', 'wb') as merged_file:
        for output_file in output_files:
            with open(output_file, 'rb') as f:
                merged_file.write(f.read())
            os.remove(output_file)

def write_dataframe_to_tsv(df_subset, filename):
    series = df_subset.stack().reset_index()
    series = series[series.iloc[:, 2] != 0]
    series['chr_name'], series['start_pos'], series['end_pos'] = zip(*series['level_1'].str.split('_').tolist())
    series.drop(columns=['level_1'], inplace=True)
    new_order = ['chr_name','start_pos','end_pos','barcode',0]
    series = series[new_order]
    series.to_csv(filename, sep='\t', header=False, index=False)
'''
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
import pandas as pd
import os

def process_and_merge(df, folder_path, n_num=20):
    num_partitions = min(n_num, len(df))
    dfs = np.array_split(df, num_partitions)
    folder_path = Path(folder_path)

    with ProcessPoolExecutor(max_workers=num_partitions) as executor:
        futures = []
        for i, df_subset in enumerate(dfs):
            filename = folder_path / f"output_{i}.tsv"
            futures.append(executor.submit(write_dataframe_to_tsv, df_subset, filename))

        for future in futures:
            future.result()  # Wait for all processes to complete

    merge_and_delete_tsv(folder_path)

def merge_and_delete_tsv(folder_path):
    output_files = list(folder_path.glob('output_*.tsv'))
    with open(folder_path / 'merged.tsv', 'wb') as merged_file:
        for output_file in output_files:
            with open(output_file, 'rb') as f:
                # Stream the file content instead of reading it all at once
                for line in f:
                    merged_file.write(line)
            os.remove(output_file)






'''
def cal_tf(input_mat,species1, assays1,verbose1):
    all_tf_result = {}
    lisa_test2 = FromGenes(species=species1,rp_map='enhanced_10K', assays=assays1,isd_method='chipseq', verbose = verbose1)  
    for k,v in input_mat.items():
        results, metadata = lisa_test2.predict(v, num_background_genes = 3000, background_strategy = 'regulatory')
        results = pd.DataFrame(results.to_dict())
        all_tf_result[k] = results
    return all_tf_result 
'''
'''
def cal_tf(input_mat, species1, assays1):
    all_tf_result = {}
    lisa_test2 = FromGenes(species=species1, rp_map='enhanced_10K', assays=assays1, isd_method='chipseq', verbose=0)
    # 使用tqdm包装input_mat.items()来创建进度条
    for k, v in tqdm(input_mat.items(), desc='Progress', unit='gene_set'):  
        results, metadata = lisa_test2.predict(v, num_background_genes=3000, background_strategy='regulatory')
        results = pd.DataFrame(results.to_dict())
        all_tf_result[k] = results
    return all_tf_result
    '''
'''
def cal_tf(input_mat,species1, assays1):
    all_tf_result = {}
    lisa_test2 = FromGenes(species=species1,rp_map='enhanced_10K', assays=assays1,isd_method='chipseq', verbose = 0)  
    for k,v in input_mat.items():
        results, metadata = lisa_test2.predict(v, num_background_genes = 3000, background_strategy = 'regulatory')
        results = pd.DataFrame(results.to_dict())
        all_tf_result[k] = results
    return all_tf_result 
'''
def cal_tf(input_data, species1, assays1):
    lisa_test2 = FromGenes(species=species1, rp_map='enhanced_10K', assays=assays1, isd_method='chipseq', verbose=0)
    results, metadata = lisa_test2.predict(input_data[1], num_background_genes=3000, background_strategy='regulatory')
    results = pd.DataFrame(results.to_dict())
    return {input_data[0]: results}


def process_group(group,adata,log,pval):
    return group, list(sc.get.rank_genes_groups_df(adata, group=group, log2fc_min=log, pval_cutoff=pval).sort_values(by='logfoldchanges', ascending=False)[0:500].names)


def get_supercell_fragment(leiden_clusters,base_dir,fragment_file,chunksize = 10000000):
    folder_name = base_dir+"/supercell_fragment"
    if not os.path.exists(folder_name):
        os.mkdir(folder_name)
    else:
        print("The folder already exists：", folder_name)
    for i,chunk in enumerate(pd.read_csv(fragment_file, delimiter='\t',comment='#', chunksize=chunksize,header=None, names=['chrom', 'start', 'end', 'cell', 'fragment'])):
        chunk.set_index('cell', inplace=True)
        groups = chunk.groupby(leiden_clusters['new_leiden'])
        for group_name, group_data in groups:
            file_path = os.path.join(base_dir, 'supercell_fragment', f'{group_name}.tsv')
            group_data = group_data[group_data['chrom'].str.startswith('chr')]
            group_data.to_csv(file_path, sep='\t',mode='a', header=False, index=False)
        print(f"Processed chunk {i+1}")
    print('final')

'''
def process_tsv(working_directory,specie):
    if specie == 'hg38':
        species = pkg_resources.resource_filename('scripro', 'data/hg38.genome')
    if specie == 'mm10':
        species = pkg_resources.resource_filename('scripro', 'data/mm10.genome')
    bedGraph = pkg_resources.resource_filename('scripro', 'data/bedGraphToBigWig')
    print("1")
    sort_command = 'ls ./*.tsv | xargs -I {} sh -c \'bedtools sort -i "$1" > ./sort_tsv/"$(basename -- "$1")"\' -- {}'
    sort_folder = os.path.join(working_directory, "sort_tsv")
    if not os.path.exists(sort_folder):
        os.mkdir(sort_folder)
    p = subprocess.Popen(sort_command, cwd=working_directory, shell=True)
    p.wait()
    print("2")
    merge_command = 'ls *.tsv | xargs -P 4 -n 1 -I {} sh -c \'bedtools merge -d 1000 -c 4 -o sum -i "{}" > "./merge_tsv/{}"\''
    merge_folder = os.path.join(sort_folder, "merge_tsv")
    if not os.path.exists(merge_folder):
        os.mkdir(merge_folder)
    p = subprocess.Popen(merge_command, cwd=sort_folder, shell=True)
    p.wait()
    print("3")
    bigwig_command = 'find . -name \'*.tsv\' -type f -print0 | xargs -0 -P 4 -n 1 sh -c \'file=\"$1\"; {0} \"$file\" {1} \"./bigwig/${{file%.*}}.bw\"\' sh'.format(bedGraph,species)
    bigwig_folder = os.path.join(merge_folder, "bigwig")
    if not os.path.exists(bigwig_folder):
        os.mkdir(bigwig_folder)
    p = subprocess.Popen(bigwig_command, cwd=merge_folder, shell=True)
    p.wait()
    shutil.move(bigwig_folder, os.path.join(os.getcwd(), "bigwig"))
    shutil.rmtree(working_directory)
  '''

def process_tsv(working_directory: str, specie: str):
    # Define species file paths in a dictionary
    species_files = {
        'hg38': pkg_resources.resource_filename('scripro', 'data/hg38.genome'),
        'mm10': pkg_resources.resource_filename('scripro', 'data/mm10.genome')
    }
    # Get the species file path from the dictionary
    species = species_files.get(specie)
    if not species:
        raise ValueError(f"Unknown species: {specie}")
    
    bedGraph = pkg_resources.resource_filename('scripro', 'data/bedGraphToBigWig')
    
    print("1")
    sort_folder = Path(working_directory) / "sort_tsv"
    sort_folder.mkdir(exist_ok=True)
    
    # Sort tsv files
    for tsv_file in Path(working_directory).glob("*.tsv"):
        sorted_file = sort_folder / tsv_file.name
        subprocess.run(f'bedtools sort -i "{tsv_file}" > "{sorted_file}"', shell=True)
    
    print("2")
    merge_folder = sort_folder / "merge_tsv"
    merge_folder.mkdir(exist_ok=True)
    
    # Merge tsv files
    for sorted_file in sort_folder.glob("*.tsv"):
        merged_file = merge_folder / sorted_file.name
        subprocess.run(f'bedtools merge -d 1000 -c 4 -o sum -i "{sorted_file}" > "{merged_file}"', shell=True)
    
    print("3")
    bigwig_folder = merge_folder / "bigwig"
    bigwig_folder.mkdir(exist_ok=True)
    
    # Convert tsv to bigwig format
    for merged_file in merge_folder.glob("*.tsv"):
        bigwig_file = bigwig_folder / f"{merged_file.stem}.bw"
        subprocess.run(f'{bedGraph} "{merged_file}" {species} "{bigwig_file}"', shell=True)
    
    # Move the bigwig folder to the current working directory
    shutil.move(str(bigwig_folder), os.path.join(os.getcwd(), "bigwig"))
    
    # Clean up the working directory
    shutil.rmtree(working_directory)

# Example usage:
# process_tsv('/path/to/working/directory', 'hg38')






def process_marker(i,lisa_info,bw_path,rpmap_enhanced,factor_binging,factor_metadata,species):
    cell_info = lisa_info[i]
    gene_mask = cell_info[0]
    label_vector = cell_info[1]
    bigwig_path = bw_path + str(i) + '.bw'
    log = Log(verbose = False)
    testbw = FromCoverage.convert_bigwig(bigwig_path, species,log = log)

    test_profile = testbw[:, np.newaxis]
    test_profile = test_profile / test_profile.sum() * 1e5
     
    rp_matrix = rpmap_enhanced.dot(test_profile)
    subset_rp_matrix = rp_matrix[gene_mask, :]
    
    bin_mask = np.squeeze(np.array(rpmap_enhanced[gene_mask, :].tocsc().sum(axis=0) > 0))
    
    subset_factor_binding = factor_binging[bin_mask, :]
    subset_rp_map = rpmap_enhanced[gene_mask, :][:, bin_mask]
    subset_accessibility = test_profile[bin_mask, :]
    
    rp_knockout = get_delta_RP(subset_accessibility, subset_factor_binding, subset_rp_map)[:, np.newaxis, :]
    deltaX = get_deltaRP_activation(subset_rp_matrix[:, :, np.newaxis], rp_knockout)
    p_vals = get_delta_RP_p_value(deltaX.transpose(0, 2, 1)[:, :, 0], label_vector)
    factor_metadata_pd = pd.DataFrame(factor_metadata)
    factor_metadata_pd['p_vals'] = p_vals
    return i, factor_metadata_pd


def glue_supercell(combined):
    for i in set(combined.obs.leiden):
        leiden_index = combined.obs.loc[combined.obs.leiden == i].index
        sub_test = combined[combined.obs.leiden == i]
        get_leiden_based_on_ncell(sub_test,50,verbose=False)
        if sub_test.obs.leiden.value_counts()[0]>30 and sub_test.obs.leiden.value_counts().shape[0]>2:
            clusters = sub_test.obs.leiden.cat.categories
            centroids = pd.DataFrame({cluster: np.mean(sub_test[sub_test.obs.index[np.where(sub_test.obs.leiden == cluster)]].obsm['X_glue'],axis=0) for cluster in clusters}).T
            small_clusters = sub_test.obs.leiden.value_counts()[sub_test.obs.leiden.value_counts() < 30].index
            replace_dict= {}
            for cluster in small_clusters:
                distances = cdist(centroids.loc[[cluster]], centroids)
                distances = distances[0][0:len(clusters)-len(small_clusters)]
                nearest_cluster = clusters[np.argmin(distances)]
                replace_dict[cluster] = nearest_cluster
            sub_test.obs.leiden = sub_test.obs.leiden.replace(replace_dict)
            sub_test.obs['leiden'] = i + "_" + sub_test.obs['leiden'].astype(str)
        else:
            sub_test.obs['leiden'] = i + "_0"
        combined.obs.loc[leiden_index,'new_leiden'] = sub_test.obs['leiden']


def get_delta_RP_p_value(gene_TF_scores, label_vector):
        '''
        gene_TF_scores: gene x TF, model output of delta-RP matrix. more purturbation of genes of interest correspond with higher delta regulation score
        '''
        query_delta = gene_TF_scores[label_vector.astype(bool)]
        background_delta = gene_TF_scores[~label_vector.astype(bool)]

        test_parameters = list(zip(query_delta.T, background_delta.T))

        p_vals = [mannu_test_function((q,b)) for q,b in test_parameters]
        _, p_values = list(zip(*p_vals))

        return p_values


def mannu_test_function(x):
    query, background = x
    try:
        return stats.mannwhitneyu(query, background, alternative = 'greater')
    
    except ValueError:
        
        return (None, 1.0)

def get_quert_gene(chip_matrix,target_h5,gene_name):
    tem = {}
    for i in set(chip_matrix.values.flatten()):
        tem[i]=list(set(target_h5[i][target_h5[i]>2].index).intersection(set(gene_name)))
    return tem


def maxmin(dataframe):
    return (dataframe - dataframe.min())/(dataframe.max() - dataframe.min())


def get_cell_barcode_score(super_leiden,super_leiden_value,adList_obs):
    s = []
    for i in super_leiden:
        origin_leiden = adList_obs[i.split(sep = '_')[0]]
        num = len(origin_leiden.loc[origin_leiden.leiden ==i.split(sep = '_')[1]].index)
        s.extend(list(zip([pd.DataFrame(super_leiden_value).loc[i,:]]*num,origin_leiden.loc[origin_leiden.leiden ==i.split(sep = '_')[1]].index)))
    return s


def plot_spatial(TF, TF_matrix, adList_obs, adata, spot_size, fig_path):
    plot_basis='spatial'
    s = get_cell_barcode_score(TF_matrix.loc[:,TF].index,TF_matrix.loc[:,TF],adList_obs)
    plt.figure(figsize=(10, 7), dpi=80)
    f, ax = plt.subplots()

    spot = sorted(s,key = lambda x: x[0][0],reverse=False)

    init_points = []
    value = []
    for _, cell in spot:
        init_points.append(cell)
        value.append(_)
        
    points = ax.scatter(adata[init_points].obsm[plot_basis][:, 0], adata[init_points].obsm[plot_basis][:, 1], c=value, s = spot_size,cmap="PuRd",edgecolors = None)
    plt.scatter(adata[init_points].obsm[plot_basis][:, 0], adata[init_points].obsm[plot_basis][:, 1], c=value, s = spot_size,cmap="PuRd",edgecolors = None)
    f.colorbar(points)
    ax.grid(False)
    # # ax = plt.gca()
    ax.set_xticks([])
    ax.set_yticks([])
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    plt.savefig(fig_path)
