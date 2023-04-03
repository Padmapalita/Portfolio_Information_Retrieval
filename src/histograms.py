import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import glob
import json
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
from list_of_sampled_docs import list_A

class Histograms:

    def __init__(self,):
        print("initializing histograms class")
        self.metadata_filename = "../Files/Local_pickles/metadata.csv"
        self.metadata_df = pd.read_csv("../Files/Local_pickles/metadata.csv")
        self.bow_df = pd.read_pickle("../Files/Local_pickles/HIST_BOW_Word_Count.pkl")
        self.list_A = list_A

    def get_duration_histogram_allfiles(self,):
        fig, ax = plt.subplots(figsize=(8,5))
        self.metadata_df['duration'].hist(bins=40, ax=ax)
        fig.suptitle('Original Dataset: Podcast Duration', fontsize=16)
        plt.xlabel('Episode duration (mins)')
        plt.ylabel('Frequency')
        #plt.show()
        plt.savefig(f"../Files/historam_duration_allfiles.png", dpi=300)
        return

    def get_log_duration_histogram_allfiles(self,):
        fig, ax = plt.subplots(figsize=(8,5))
        self.metadata_df['duration'].hist(bins=40, ax=ax, log=True)
        fig.suptitle('Original Dataset: Podcast Duration (log)', fontsize=16)
        plt.xlabel('Episode duration (mins)')
        plt.ylabel('Log frequency')
        #plt.show()
        plt.savefig(f"../Files/historam_duration_log_allfiles.png", dpi=300)
        return

    def get_duration_histogram_sampled(self,):
        fig, ax = plt.subplots(figsize=(8,5))
        sampled_df = self.metadata_df[self.metadata_df['episode_filename_prefix'].isin(self.list_A)]
        sampled_df['duration'].hist(bins=40, ax=ax)
        fig.suptitle('Sub-sampled: Podcast Duration', fontsize=16)
        plt.xlabel('Episode duration (mins)')
        plt.ylabel('Frequency')
        #plt.show()
        plt.savefig(f"../Files/historam_duration_sampled.png", dpi=300)
        return

    def get_log_duration_histogram_sampled(self,):
        fig, ax = plt.subplots(figsize=(8,5))
        sampled_df = self.metadata_df[self.metadata_df['episode_filename_prefix'].isin(self.list_A)]
        sampled_df['duration'].hist(bins=40, ax=ax, log=True)
        fig.suptitle('Sub-sampled: Podcast Duration (log)', fontsize=16)
        plt.xlabel('Episode duration (mins)')
        plt.ylabel('Log frequency')
        #plt.show()
        plt.savefig(f"../Files/historam_duration_log_sampled.png", dpi=300)
        return


    def get_episode_wordcount_histogram(self,):
        episode_word_counts = self.bow_df.sum(axis=1)
        fig, ax = plt.subplots(figsize=(8,5))
        episode_word_counts.hist(bins=20, ax=ax, log=False)
        fig.suptitle('Podcast Word Count', fontsize=16)
        plt.xlabel('Episode word count')
        plt.ylabel('Frequency')
        plt.savefig("../Files/historam_word_count.png", dpi=300)
        return
    
    def get_episode_wordcount_histogram_log(self,):
        episode_word_counts = self.bow_df.sum(axis=1)
        fig, ax = plt.subplots(figsize=(8,5))
        episode_word_counts.hist(bins=20, ax=ax, log=True)
        fig.suptitle('Podcast Word Count', fontsize=16)
        plt.xlabel('Episode word count')
        plt.ylabel('Log frequency')
        plt.savefig("../Files/historam_word_count_log.png", dpi=300)
        return

    def print_means_stds(self,):
        # all episodes duration
        all_eps_mean_duration = round(self.metadata_df['duration'].mean(), 2)
        all_eps_std_duration = round(self.metadata_df['duration'].std(), 2)
        print(f'Whole dataset duration (mins) mean: {all_eps_mean_duration}, standard deviation: {all_eps_std_duration}')
        # sampled episodes duration
        sampled_df = self.metadata_df[self.metadata_df['episode_filename_prefix'].isin(self.list_A)]
        sampled_eps_mean_duration = round(sampled_df['duration'].mean(), 2)
        sampled_eps_std_duration = round(sampled_df['duration'].std(), 2)
        print(f'Sub-sample duration (mins) mean: {sampled_eps_mean_duration}, standard deviation: {sampled_eps_std_duration}')
        # sampled episodes word count
        sampled_eps_mean_wordcount = round(self.bow_df.sum(axis=1).mean(), 2)
        sampled_eps_std_wordcount = round(self.bow_df.sum(axis=1).std(), 2)
        print(f'Sub-sample word count mean: {sampled_eps_mean_wordcount}, standard deviation: {sampled_eps_std_wordcount}')
        return 


histograms = Histograms()
histograms.get_duration_histogram_allfiles()
histograms.get_log_duration_histogram_allfiles()
histograms.get_duration_histogram_sampled()
histograms.get_log_duration_histogram_sampled()
histograms.get_episode_wordcount_histogram()
histograms.get_episode_wordcount_histogram_log()
histograms.print_means_stds()