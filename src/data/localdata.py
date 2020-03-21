"""
Custom dataset processing/generation functions should be added to this file
"""

import pandas as pd
import json
from collections import defaultdict
import pathlib
from .. import paths

__all__ = [
    'process_covid_metadata',
    'create_section_df',
]


def process_covid_metadata(kind='all', extract_dir='covid_nlp_20200319', unpack_dir=None, metadata=None):
    """
    Add the file paths (relative to the extract_dir) to the metadata and return the metadata dataframe
    in (data, target, metdata) format to be converted into a DataSet.

    Parameters
    ----------
    extract_dir:
        The name of the directory the files have been unpacked into
    kind: Default 'all'
        One of {'all', 'cc-by-licensed', 'commercial_use', 'non_commercial_use', 'custom_license', 'biorxiv'}
        Will filter down to the given kind.
    metadata:
        Any additional metadata to add
    unpack_dir:
        The interim data directory. If None, it will use the
        interim_data_path in paths. Only pass this if you want to override the default.
    """
    if metadata is None:
        metadata = {}

    if unpack_dir:
        unpack_dir = pathlib.Path(unpack_dir)
    else:
        unpack_dir = paths['interim_data_path']

    data_path = unpack_dir / extract_dir

    meta_df = pd.read_csv(data_path / 'all_sources_metadata_2020-03-13.csv',
                           dtype={'Microsoft Academic Paper ID': str,
                                  'pubmed_id': str})

    # filter by kind
    dir_by_kind = {
        'commercial_use': 'comm_use_subset',
        'non_commercial_use': 'noncomm_use_subset',
        'custom_license': 'pmc_custom_license',
        'biorxiv': 'biorxiv_medrxiv'
    }

    if kind == 'all':
        dir_list = list(dir_by_kind.values())
    elif kind == 'cc-by-license':
        dir_list =[dir_by_kind.get('commercial_use'), dir_by_kind.get('non_commercial_use')]
    elif kind in dir_by_kind.keys():
        dir_list = [dir_by_kind.get(kind)]
    else:
        raise ValueError(f"kind must be one of {['all', 'cc-by-licensed'] + list(dir_by_kind.keys())}")


    # walk through the directories to get filenames
    filenames = []
    for dir_name in dir_list:
        source_dir = data_path / dir_name
        filenames += list(source_dir.iterdir())

    filename_dict = defaultdict(list)

    for num_file, filename in enumerate(filenames):

        file = json.load(open(filename, 'rb'))
        if (file['paper_id'] + '.json') != filename.name:
            print(filename.name, file['paper_id'])
        filename_dict[num_file] = {'sha': file['paper_id'],
                                   'file_type': filename.parts[-2],
                                   'path': '/'.join([filename.parts[-2], filename.name])}

    df = pd.DataFrame(filename_dict).T

    # add the filename information to the metadata df
    full_metadata = meta_df.merge(df, on='sha', how='outer')

    # filter by kind if requested
    if kind == 'all':
        data = full_metadata
    elif kind == 'cc-by-license':
        data = full_metadata[(full_metadata.file_type=='comm_use_subset') | (full_metadata.file_type=='noncomm_use_subset')]
    else:
        file_type = dir_by_kind[kind]
        data = full_metadata[full_metadata.file_type==file_type]


    return data, None, metadata


def create_section_df(df, unpack_dir=None, extract_dir='covid_nlp_20200319', min_tokens=200):
    """
    Given a dataframe df of the form of the covid metadata augmented dataset (e.g. covid_nlp_20200319)

    Created a dataframe where each row is a section of a paper from the dataframe (for which a
    full-text version exists)

    Parameters
    ----------
    df:
        a metadata dataframe (.data from a metadata datasource)
    extract_dir:
        The name of the directory the files have been unpacked into
    min_tokens:
        Require sections to have at least min_tokens tokens to be included
    unpack_dir:
        The interim data directory. If None, it will use the
        interim_data_path in paths. Only pass this if you want to override the default.

    Returns
    -------
    section dataframe with columns: ['paper_id', 'title', 'abstract', 'section', 'text', 'token_counts']
    """
    if unpack_dir:
        unpack_dir = pathlib.Path(unpack_dir)
    else:
        unpack_dir = paths['interim_data_path']

    data_path = unpack_dir / extract_dir

    # filter to full text papers
    df = df[df.has_full_text==True]
    filenames = df.path

    paper_ids = []
    titles = []
    abstracts = []
    sections = []
    body_texts = []

    for filename in filenames:

        file = json.load(open(data_path / filename, 'rb'))

        section = []
        text = []

        for bod in file["body_text"]:
            section.append(bod["section"])
            text.append(bod["text"])

            res_df = pd.DataFrame({"section":section, "text":text}).groupby("section")["text"].apply(' '.join).reset_index()

            for index, row in res_df.iterrows():
                # metadata
                paper_ids.append(file["paper_id"])

                if(len(file["abstract"])):
                    abstracts.append(file["abstract"][0]["text"])
                else:
                    abstracts.append("")

                titles.append(file["metadata"]["title"])

                # add section and text
                sections.append(row.section)
                body_texts.append(row.text)

    parsed_df = pd.DataFrame({"paper_id":paper_ids, "title": titles, "abstract": abstracts, "section": sections, "text": body_texts})
    parsed_df["token_counts"] = parsed_df["text"].str.split().map(len)
    parsed_df = parsed_df[parsed_df.token_counts>min_tokens].reset_index(drop=True)

    return parsed_df
