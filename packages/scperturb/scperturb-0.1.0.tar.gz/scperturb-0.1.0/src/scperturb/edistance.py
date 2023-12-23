import pandas as pd
import numpy as np
import scanpy as sc

from tqdm import tqdm
from sklearn.metrics import pairwise_distances
from itertools import combinations
from joblib import Parallel, delayed
from warnings import warn

def pairwise_pca_distances(adata, obs_key, obsm_key='X_pca', dist='sqeuclidean',
                           sample_correct=True, n_jobs=-1, verbose=True):
    """Average of pairwise PCA distances between cells of each group in obs_key.
    For each pair of groups defined in adata.obs[obs_key] (e.g. perturbations)
    computes all pairwise distances between cells in adata.obsm[obsm_key] (e.g. PCA space)
    and averages them per group-pair. This results in a distance matrix between all groups.

    Arguments
    ---------
    adata: :class:`~anndata.AnnData`
        Annotated data matrix.
    obs_key: `str` in adata.obs.keys()
        Key in adata.obs specifying the groups to consider.
    obsm_key: `str` in adata.obsm (default: `adata.obsm['X_pca']`)
        Key for embedding coordinates to use.
    dist: `str` for any distance in scipy.spatial.distance (default: `sqeuclidean`)
        Distance metric to use in embedding space.
    sample_correct: `bool` (default: `True`)
        Whether make the estimator for sigma more unbiased (dividing by N-1 instead of N, similar to sample and population variance).
    n_jobs: `int` (default: `-1`)
        Number of jobs to use for parallelization. If `n_jobs=1`, no parallelization is used. The default uses all available threads.
    verbose: `bool` (default: `True`)
        Whether to show a progress bar iterating over all groups.

    Returns
    -------
    pwd: pandas.DataFrame
        DataFrame with average of pairwise PCA distances between all groups.
    """

    if obsm_key=='X_pca' and 'X_pca' not in adata.obsm.keys():
        warn('PCA embedding not found, computing...')
        sc.pp.pca(adata)
    
    X = adata.obsm[obsm_key].copy()
    y = adata.obs[obs_key].astype(str).copy()
    groups = pd.unique(y)
    df = pd.DataFrame(index=groups, columns=groups, dtype=float)
    fct = tqdm if verbose else lambda x: x
    combis = list(combinations(groups, 2)) + [(x,x) for x in groups]
    def one_step(pair):
        p1, p2 = pair
        x1 = X[y==p1].copy()
        N = len(x1)
        x2 = X[y==p2].copy()
        pwd = pairwise_distances(x1, x2, metric=dist)
        M = len(x2)-1 if (p1==p2) & sample_correct else len(x2)
        factor = N * M
        mean_pwd = np.sum(pwd) / factor
        return (p1, p2, mean_pwd)
    res = Parallel(n_jobs=n_jobs)(delayed(one_step)(pair) for pair in fct(combis))
    for p1, p2, val in res:
        df.loc[p1, p2] = val
        df.loc[p2, p1] = val
    df.index.name = obs_key
    df.columns.name = obs_key
    df.name = 'pairwise PCA distances'
    return df

def edist(adata, obs_key='perturbation', obsm_key='X_pca', pwd=None, 
          dist='sqeuclidean', sample_correct=True, n_jobs=1, verbose=True):
    """Computes the edistance to control. Accepts precomputed pwd.
    Computes the pairwise E-distances between all groups of cells defined in
    adata.obs[obs_key] (e.g. perturbations). Distances are computed in embedding
    space given by adata.obsm[obsm_key] (e.g. PCA space).

    Arguments
    ---------
    adata: :class:`~anndata.AnnData`
        Annotated data matrix.
    obs_key: `str` in adata.obs.keys() (default: `perturbation`)
        Key in adata.obs specifying the groups to consider.
    obsm_key: `str` in adata.obsm (default: `adata.obsm['X_pca']`)
        Key for embedding coordinates to use.
    dist: `str` for any distance in scipy.spatial.distance (default: `sqeuclidean`)
        Distance metric to use in embedding space.
    sample_correct: `bool` (default: `True`)
        Whether make the estimator for sigma more unbiased (dividing by N-1 instead of N, similar to sample and population variance).
    n_jobs: `int` (default: `-1`)
        Number of jobs to use for parallelization. If `n_jobs=1`, no parallelization is used. The default uses all available threads.
    verbose: `bool` (default: `True`)
        Whether to show a progress bar iterating over all groups.

    Returns
    -------
    estats: pandas.DataFrame
        DataFrame with pairwise E-distances between all groups.
    """
    pwd = pairwise_pca_distances(adata, obs_key=obs_key, obsm_key=obsm_key, 
                                 dist=dist, sample_correct=sample_correct, 
                                 n_jobs=n_jobs, verbose=verbose) if pwd is None else pwd
    # derive basic statistics
    sigmas = np.diag(pwd)
    deltas = pwd
    estats = 2 * deltas - sigmas - sigmas[:, np.newaxis]
    return estats

def onesided_pca_distances(adata, obs_key, control, obsm_key='X_pca', 
                           dist='sqeuclidean', sample_correct=True,
                           n_jobs=-1, verbose=True):
    """Average of pairwise PCA distances between cells of each group in obs_key with control group.
    For each group defined in adata.obs[obs_key] (e.g. perturbations)
    computes all pairwise distances between cells in adata.obsm[obsm_key] (e.g. PCA space)
    and averages them per group-control-pair. This results in a distance vector with a value for each group.

    Arguments
    ---------
    adata: :class:`~anndata.AnnData`
        Annotated data matrix.
    obs_key: `str` in adata.obs.keys()
        Key in adata.obs specifying the groups to consider.
    control: `str` or list of `str` of categories in `adata.obs[obskey]`
        Group(s) in obs_key for control cells.
    obsm_key: `str` in adata.obsm (default: `adata.obsm['X_pca']`)
        Key for embedding coordinates to use.
    dist: `str` for any distance in scipy.spatial.distance (default: `sqeuclidean`)
        Distance metric to use in embedding space.
    sample_correct: `bool` (default: `True`)
        Whether make the estimator for sigma more unbiased (dividing by N-1 instead of N, similar to sample and population variance).
    n_jobs: `int` (default: `-1`)
        Number of jobs to use for parallelization. If `n_jobs=1`, no parallelization is used. The default uses all available threads.
    verbose: `bool` (default: `True`)
        Whether to show a progress bar iterating over all groups.

    Returns
    -------
    pwd: pandas.DataFrame
        DataFrame with average PCA distances to control for all groups.
    """

    if obsm_key=='X_pca' and 'X_pca' not in adata.obsm.keys():
        warn('PCA embedding not found, computing...')
        sc.pp.pca(adata)

    groups = pd.unique(adata.obs[obs_key])
    control = [control] if isinstance(control, str) else control
    assert all(np.isin(control, groups)), f'No cells of control group "{control}" were not found in groups defined by "{obs_key}".'
    df = pd.DataFrame(index=groups, columns=['distance'], dtype=float)
    fct = tqdm if verbose else lambda x: x
    
    x1 = adata[adata.obs[obs_key].isin(control)].obsm[obsm_key].copy()
    N = len(x1)
    def one_step(p):
        x2 = adata[adata.obs[obs_key]==p].obsm[obsm_key].copy()
        pwd = pairwise_distances(x1, x2, metric=dist)
        M = len(x2)-1 if (np.isin(p, control)) & sample_correct else len(x2)
        factor = N * M  # Thanks to Garrett Wong for finding this bug
        mean_pwd = np.sum(pwd) / factor
        return (p, mean_pwd)
    res = Parallel(n_jobs=n_jobs)(delayed(one_step)(p) for p in fct(groups))
    for p, val in res:
        df.loc[p] = val
    df.index.name = obs_key
    df.name = f'PCA distances to control'
    return df

def self_pca_distances(adata, obs_key, obsm_key='X_pca', dist='sqeuclidean', 
                       sample_correct=True, n_jobs=-1, verbose=True):
    """Average of pairwise PCA distances between cells within each group in obs_key.
    For each group defined in adata.obs[obs_key] (e.g. perturbations)
    computes all pairwise distances between cells within in the space given by adata.obsm[obsm_key] (e.g. PCA space)
    and averages them per group. This results in a distance vector with a value for each group.

    Arguments
    ---------
    adata: :class:`~anndata.AnnData`
        Annotated data matrix.
    obs_key: `str` in adata.obs.keys()
        Key in adata.obs specifying the groups to consider.
    obsm_key: `str` in adata.obsm (default: `adata.obsm['X_pca']`)
        Key for embedding coordinates to use.
    dist: `str` for any distance in scipy.spatial.distance (default: `sqeuclidean`)
        Distance metric to use in embedding space.
    sample_correct: `bool` (default: `True`)
        Whether make the estimator for sigma more unbiased (dividing by N-1 instead of N, similar to sample and population variance).
    n_jobs: `int` (default: `-1`)
        Number of jobs to use for parallelization. If `n_jobs=1`, no parallelization is used. The default uses all available threads.
    verbose: `bool` (default: `True`)
        Whether to show a progress bar iterating over all groups.

    Returns
    -------
    pwd: pandas.DataFrame
        DataFrame with average PCA distances to self for all groups.
    """

    if obsm_key=='X_pca' and 'X_pca' not in adata.obsm.keys():
        warn('PCA embedding not found, computing...')
        sc.pp.pca(adata)

    groups = pd.unique(adata.obs[obs_key])
    df = pd.DataFrame(index=groups, columns=['distance'], dtype=float)
    fct = tqdm if verbose else lambda x: x
    
    for p in fct(groups):
        x = adata[adata.obs[obs_key]==p].obsm[obsm_key].copy()
        pwd = pairwise_distances(x, x, metric=dist)
        N = len(x)
        factor = N*(N-1) if sample_correct else N**2
        mean_pwd = np.sum(pwd) / factor
        df.loc[p] = mean_pwd
    df.index.name = obs_key
    df.name = 'PCA distances within groups'
    return df

def edist_to_control(adata, obs_key='perturbation', control='control', 
                     obsm_key='X_pca', dist='sqeuclidean',  
                     sample_correct=True, n_jobs=-1, verbose=True):
    """Computes the edistance to control.
    Computes the all E-distances between all groups of cells defined in
    adata.obs[obs_key] (e.g. perturbations) and control cells. Distances are computed in embedding
    space given by adata.obsm[obsm_key] (e.g. PCA space).

    Arguments
    ---------
    adata: :class:`~anndata.AnnData`
        Annotated data matrix.
    obs_key: `str` in adata.obs.keys() (default: `perturbation`)
        Key in adata.obs specifying the groups to consider.
    control: `str` or list of `str` of categories in `adata.obs[obskey]`
        Group(s) in obs_key for control cells.
    obsm_key: `str` in adata.obsm (default: `adata.obsm['X_pca']`)
        Key for embedding coordinates to use.
    dist: `str` for any distance in scipy.spatial.distance (default: `sqeuclidean`)
        Distance metric to use in embedding space.
    sample_correct: `bool` (default: `True`)
        Whether make the estimator for sigma more unbiased (dividing by N-1 instead of N, similar to sample and population variance).
    n_jobs: `int` (default: `-1`)
        Number of jobs to use for parallelization. If `n_jobs=1`, no parallelization is used. The default uses all available threads.
    verbose: `bool` (default: `True`)
        Whether to show a progress bar iterating over all groups.

    Returns
    -------
    ed_to_c: pandas.DataFrame
        DataFrame with E-distances between all groups and control group.
    """
    control = [control] if isinstance(control, str) else control
    deltas_to_c = onesided_pca_distances(adata, obs_key=obs_key, control=control, 
                                         obsm_key=obsm_key, dist=dist, 
                                         sample_correct=sample_correct, 
                                         n_jobs=n_jobs,
                                         verbose=verbose)
    sigmas = self_pca_distances(adata, obs_key, obsm_key=obsm_key, dist=dist, 
                                sample_correct=sample_correct, n_jobs=n_jobs,
                                verbose=False)
    # derive basic statistics
    ed_to_c = 2 * deltas_to_c - sigmas - np.mean(sigmas.loc[control].values)
    return ed_to_c
