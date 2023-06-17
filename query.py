import math
import re

def load_vocab():
    vocab = {}
    with open("vocab.txt", "r") as f:
        vocab_terms = f.readlines()
    with open("idf-values.txt", "r") as f:
        idf_values = f.readlines()

    for (term, idf_value) in zip(vocab_terms, idf_values):
        vocab[term.rstrip()] = int(idf_value.rstrip())

    return vocab

def load_document():
    with open("document.txt", "r") as f:
        documents = f.readlines()

    # print('Number of documents: ', len(documents))
    # print('Sample document: ', documents[0])
    return documents

# returns a dict with key : term, value : document indexes in which it is present
def load_inverted_index():
    inverted_index = {}
    with open('inverted_index.txt', 'r') as f:
        inverted_index_terms = f.readlines()

    for row_num in range(0,len(inverted_index_terms),2):
        term = inverted_index_terms[row_num].strip()
        documents = inverted_index_terms[row_num+1].strip().split()
        inverted_index[term] = documents
    
    # print('Size of inverted index: ', len(inverted_index))
    return inverted_index


def load_link_of_qs():
    with open("Leetcode-Scraping/qData/Qlink.txt", "r") as f:
        links = f.readlines()

    return links

vocab = load_vocab()            # vocab : idf_values
document = load_document()
inverted_index = load_inverted_index()
Qlink = load_link_of_qs()

# returns a dict with key : doc index, value : Normalized term frequency for this doc
def get_tf_dict(term):
    tf_dict = {}
    if term in inverted_index:
        for doc in inverted_index[term]:
            if doc not in tf_dict:
                tf_dict[doc] = 1
            else:
                tf_dict[doc] += 1

    for doc in tf_dict:
        # dividing the freq of the word in doc with the total no of words in doc indexed document
        try:
            tf_dict[doc] /= len(document[int(doc)])
        except (ZeroDivisionError, ValueError, IndexError) as e:
            print(e)
            print("Error in doc: ", doc)
    
    return tf_dict


def get_idf_value(term):
    return math.log( (1 + len(document)) / (1 + vocab[term]) )

def calc_docs_sorted_order(q_terms):
    potential_docs = {}         # will store the doc which can be our ans: sum of tf-idf value of that doc for all the query terms
    q_Links = []
    for term in q_terms:
        if(term not in vocab):
            continue

        tf_vals_by_docs = get_tf_dict(term)
        idf_value = get_idf_value(term)

        # print(term, tf_vals_by_docs, idf_value)

        for doc in tf_vals_by_docs:
            if doc not in potential_docs:
                potential_docs[doc] = tf_vals_by_docs[doc]*idf_value
            else:
                potential_docs[doc] += tf_vals_by_docs[doc]*idf_value
        
        # print(potential_docs)
        #divide the scores of each doc with no of query terms
        for doc in potential_docs:
            potential_docs[doc] /= len(q_terms)
        
        # sort in dec order acc to values calculated
        potential_docs = dict(sorted(potential_docs.items(), key =lambda item : item[1], reverse = True))
        
        # if no doc found
        if(len(potential_docs) == 0):
            print("No matching question found. Please search with more relevant terms.")
        
        # Printing ans
        # print("The Question links in Decreasing Order of Relevance are: \n")
        # for doc_index in potential_docs:
        #     print("Question Link:", Qlink[int(doc_index) - 1], "\tScore:", potential_docs[doc_index])

        # return a list containing top 20 q links in dec order
        count = 0
        for doc_index in potential_docs:
            q_Links.append([potential_docs[doc_index], Qlink[int(doc_index) - 1]])
            count += 1
            if(count > 20):
                break
            
    q_Links = sorted(q_Links, key =lambda item : item[0], reverse = True)
    return q_Links[:20]




query = input('Enter your query: ')
q_terms = [term.lower() for term in query.strip().split()]

# print(q_terms)
ans = calc_docs_sorted_order(q_terms)

if ans:
    print("The Question links in Decreasing Order of Relevance are: \n")
    for (index, link) in enumerate(ans, 1):
        print("{})  ".format(index), end= "")
        print(link[1])
else:
    print("No matching question found, please try again with different words.")