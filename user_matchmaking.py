import numpy as np
import re
import spacy
from scipy import spatial
from textblob import TextBlob, Word
import gensim.downloader as api
import csv
from csv import reader
from sentence_transformers import SentenceTransformer, util
model = SentenceTransformer('all-MiniLM-L6-v2')
nlp = spacy.load('en_core_web_md')
#wv = api.load('glove-wiki-gigaword-300')
wv = api.load('word2vec-google-news-300')

def calculate_similarity(word_set1, word_set2):

    word_vectors1 = [wv[word] for word in word_set1 if word in wv.key_to_index]
    vector1 = sum(word_vectors1) / len(word_vectors1)
    
    word_vectors2 = [wv[word] for word in word_set2 if word in wv.key_to_index]
    vector2 = sum(word_vectors2) / len(word_vectors2)

    return 1 - spatial.distance.cosine(vector1, vector2)

def calculate_semantic_similarity(sentences1, sentences2):
    #Compute embedding for both lists
    embeddings1 = model.encode(sentences1)
    embeddings2 = model.encode(sentences2)

    #Compute cosine-similarities
    cosine_scores = util.cos_sim(embeddings1, embeddings2)

    return cosine_scores

def split_text_set(txt):
    custom_stop_word_list=['playing', 'making', 'building']
    txt_set = set()
    txt_lst = re.split('[-+#,;\s+]', txt)

    for item in txt_lst:
        item = item.lower().strip()
        if (len(item) > 1):
            w = Word(item)
            if not w.lemmatize() in custom_stop_word_list:
                txt_set.add(w.lemmatize())
    
    return txt_set

def text_preprocessing(sentence):
    """
    Lemmatize, lowercase, remove numbers and stop words
    
    Args:
      sentence: The sentence we want to process.
    
    Returns:
      A list of processed words
    """
    sentence = [token.lemma_.lower()
                for token in nlp(sentence) 
                if token.is_alpha and not token.is_stop]
    sentence_join = ' '.join(sentence)

    return sentence_join


if __name__ == "__main__":
    
    # open file in read mode
    with open('user_profiles.csv', 'r') as read_obj:
        # pass the file object to reader() to get the reader object
        csv_reader = reader(read_obj)
        user_profile_list = []
        for row in csv_reader:
            person = dict()
            person["id"] = row[0].strip()
            person["name"] = row[1].strip()
            person["interests"] = row[2].strip()
            person["hobbies"] = row[3].strip()
            person["occupations"] = row[4].strip()
            person["skills"] = row[7].strip()
            person["biography"] = row[8].strip()
            user_profile_list.append(person)
            #print(user_profile_list)
    
    #random_numbers = ['45','72','93','130','112','29','36','103','53','81','126','84','66','149','108','117','147','48','86','75']
    with open('user_relationship.csv', 'w', encoding='UTF8', newline='') as f:
        for p in user_profile_list:
            id = p["id"]
            interests = split_text_set(p["interests"])
            hobbies = split_text_set(p["hobbies"])
            occupations = split_text_set(p["occupations"])
            skills = split_text_set(p["skills"])
            biography = p["biography"]
            for p_tmp in user_profile_list:
                id_tmp = p_tmp["id"]
                if id != id_tmp:
                    similarity_score_matrix = []

                    interests_tmp = split_text_set(p_tmp["interests"])
                    similarity_score_interests = calculate_similarity(interests, interests_tmp)
                    if similarity_score_interests > 0: similarity_score_matrix.append(similarity_score_interests)
                    #print(interests)
                    #print(interests_tmp)
                    #print(similarity_score_interests)

                    hobbies_tmp = split_text_set(p_tmp["hobbies"])
                    similarity_score_hobbies = calculate_similarity(hobbies, hobbies_tmp)
                    if similarity_score_hobbies > 0: similarity_score_matrix.append(similarity_score_hobbies)
                    #print(hobbies)
                    #print(hobbies_tmp)
                    #print(similarity_score_hobbies)

                    occupations_tmp = split_text_set(p_tmp["occupations"])
                    similarity_score_occupations = calculate_similarity(occupations, occupations_tmp)
                    if similarity_score_occupations > 0: similarity_score_matrix.append(similarity_score_occupations)
                    #print(occupations)
                    #print(occupations_tmp)
                    #print(similarity_score_occupations)

                    skills_tmp = split_text_set(p_tmp["skills"])
                    similarity_score_skills = calculate_similarity(skills, skills_tmp)
                    if similarity_score_skills > 0: similarity_score_matrix.append(similarity_score_skills)
                    #print(skills)
                    #print(skills_tmp)
                    #print(similarity_score_skills)
                    
                    biography_tmp = p_tmp["biography"]
                    semantic_similarity_score_biography = calculate_semantic_similarity(biography, biography_tmp)
                    semantic_similarity_score_biography = semantic_similarity_score_biography.item()
                    if semantic_similarity_score_biography > 0: similarity_score_matrix.append(semantic_similarity_score_biography)
                    #print(biography)
                    #print(biography_tmp)
                    #print(semantic_similarity_score_biography)
                    
                    # Combine similarity matrices into one by averaging
                    combined_similarity_matrix = np.mean(similarity_score_matrix)
                    print("AVG:", combined_similarity_matrix)
                    print('###############')
                    if combined_similarity_matrix > 0.45:
                        data = [id, id_tmp, combined_similarity_matrix]
                        writer = csv.writer(f)
                        # write the data
                        writer.writerow(data)

                        '''
                        file1 = open("myfile.txt","a")#append mode
                        my_list = [id, combined_similarity_matrix, interests, hobbies, occupations, skills, biography]
                        all_strings = list(map(str, my_list))
                        a = "|".join(all_strings)
                        file1.write(a)
                        file1.write('\n')
                            
                        my_list1 = [id_tmp, combined_similarity_matrix, interests_tmp, hobbies_tmp, occupations_tmp, skills_tmp, biography_tmp]
                        all_strings1 = list(map(str, my_list1))
                        b = "|".join(all_strings1)
                        file1.write(b)
                        file1.write('\n')
                        file1.close()
                        '''