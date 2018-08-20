# -*- coding: UTF-8 -*- 
import tensorflow as tf
import numpy as np
import collections
import math

sentences = []
words = []
batch_size = 128
embedding_size = 128
learning_rate = 1.0
thread_hold = 2   # the frequence of word in vocabulary must greater than thread_hold
skip_window = 1
steps = 1000001

valid_size = 16     # Random set of words to evaluate similarity on.
valid_window = 100  # Only pick dev samples in the head of the distribution.
valid_examples = np.random.choice(valid_window, valid_size, replace=False)
num_sampled = 64    # Number of negative examples to sample.

with open("C:/Users/quanhwu/Downloads/frWiki_non_lem.txt", "r", encoding="utf-8") as file:
	print("---------------------------------contenus de corpus---------------------------------------")
	print(file.readline(2000))
	contents = file.read()
	stopReading = 1000#0
	for sentence in contents.split("\' "):
		stopReading -= 1
		if stopReading <= 0:
			break
		sentences.append(sentence)
		for word in sentence.split():
			words.append(word)


def build_dataset(words):
    count_tmp = []
    count_tmp.extend(collections.Counter(words).most_common())
    count = [item for item in count_tmp if item[1]>thread_hold]
    dic={}
    dic['UNK'] = 0
    for word,_ in count:
        dic[word] = len(dic)
    reverse_dic = dict(zip(dic.values(),dic.keys()))
    return dic,reverse_dic


dic, reverse_dic = build_dataset(words)
vocabulary_size = len(dic)
del words

sentences_index = 0
word_of_sentencs_index = 0

def generate_batch(batch_size=128, skip_window=1, dic=dic):
    global sentences_index
    global word_of_sentencs_index
    features = np.ndarray([batch_size,2*skip_window],dtype=np.int32)
    labels = np.ndarray([batch_size,1],dtype=np.int32)
    for i in range(batch_size):
        labels[i,0] = dic.get(sentences[sentences_index].split()[word_of_sentencs_index],0)
        left_index = word_of_sentencs_index - skip_window
        right_index = word_of_sentencs_index + skip_window
        left = 0
        right = 2*skip_window - 1
        for j in range(skip_window):
            if left_index < 0:
                features[i,left] = 0
            else:
                features[i,left] = dic.get(sentences[sentences_index].split()[left_index],0)
            left_index += 1
            left += 1
            if right_index >= len(sentences[sentences_index].split()):
                features[i,right] = 0
            else:
                features[i,right] = dic.get(sentences[sentences_index].split()[word_of_sentencs_index],0)
            right_index -= 1
            right -= 1
        word_of_sentencs_index += 1
        if word_of_sentencs_index == len(sentences[sentences_index].split()):
            word_of_sentencs_index = 0
            sentences_index = (sentences_index+1)%len(sentences)
    return features,labels



print(valid_examples)

train_features = tf.placeholder(tf.int32,shape=[batch_size, skip_window * 2])
train_labels = tf.placeholder(tf.int32, shape=[batch_size, 1])
valid_dataset = tf.constant(valid_examples, dtype=tf.int32)

embeddings = tf.Variable(tf.random_uniform([vocabulary_size, embedding_size], -1.0, 1.0))
embed = tf.nn.embedding_lookup(embeddings, train_features)
reduce_embed = tf.div(tf.reduce_sum(embed, 1), skip_window*2)

nce_weights = tf.Variable(tf.truncated_normal([vocabulary_size, embedding_size],stddev=1.0 / math.sqrt(embedding_size)))
nce_bias = tf.Variable(tf.zeros([vocabulary_size]))

# test
print("--------------------------------analyse----------------------------------------")
print(embed.get_shape())
print(reduce_embed.get_shape())
print(nce_weights.get_shape())
print(nce_bias.get_shape())
print(train_labels.get_shape())
print(tf.to_float(train_labels).get_shape())
print("--------------------------------entraînement-----------------------------------")

loss = tf.reduce_mean(tf.nn.nce_loss(weights=nce_weights, biases=nce_bias, inputs=reduce_embed,
	labels=train_labels, num_sampled=num_sampled, num_classes=vocabulary_size))

train = tf.train.GradientDescentOptimizer(1.0).minimize(loss)

norm = tf.sqrt(tf.reduce_sum(tf.square(embeddings), 1, keep_dims=True))
normalized_embeddings = embeddings / norm
valid_embeddings = tf.nn.embedding_lookup(normalized_embeddings, valid_dataset)
similarity = tf.matmul( valid_embeddings, normalized_embeddings, transpose_b=True)

init = tf.initialize_all_variables()

with tf.Session() as session:
    init.run()
    print("Initialized")

    average_loss = 0
    for step in range(100001):
        batch_features, batch_labels = generate_batch()
        feed_dict = {train_features : batch_features, train_labels : batch_labels}

        _, loss_val = session.run([train, loss], feed_dict=feed_dict)
        average_loss += loss_val

        if step % 2000 == 0:
            if step > 0:
                average_loss /= 2000.0
            print("at step %d avg_loss average_loss %f"%(step, average_loss))
            average_loss = 0

        if step % 20000 == 0:
            sim = similarity.eval()
            for i in range(valid_size):
                valid_word = reverse_dic[valid_examples[i]]
                top_k = 8 # number of nearest neighbors
                nearest = (-sim[i, :]).argsort()[1:top_k+1]
                log_str = "Nearest to %s:" % valid_word
                for k in range(top_k):
                    close_word = reverse_dic[nearest[k]]
                    log_str = "%s %s," % (log_str, close_word)
                print(log_str)
            print(reverse_dic[300])
            session.run(tf.Print(normalized_embeddings[300], [normalized_embeddings[300]], summarize=128))