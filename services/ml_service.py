import numpy as np
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dense

class MlService:
  def __init__(self):
    with open('Text.txt', 'r', encoding='utf-8') as file:
      text = file.read()
    
    self.tokenizer = Tokenizer()
    self.tokenizer.fit_on_texts([text])
    total_words = len(self.tokenizer.word_index) + 1
    
    input_sequences = []
    for line in text.split('\n'):
      token_list = self.tokenizer.texts_to_sequences([line])[0]
      for i in range(1, len(token_list)):
        n_gram_sequence = token_list[:i+1]
        input_sequences.append(n_gram_sequence)

    self.max_sequence_len = max([len(seq) for seq in input_sequences])
    input_sequences = np.array(pad_sequences(input_sequences, maxlen=self.max_sequence_len, padding='pre'))

    # Split into input and label
    self.X = input_sequences[:, :-1]
    self.y = to_categorical(input_sequences[:, -1], num_classes=total_words)

    self.model = Sequential()
    self.model.add(Embedding(total_words, 100, input_length=self.max_sequence_len-1))
    self.model.add(LSTM(150, return_sequences=False))
    self.model.add(Dense(total_words, activation='softmax'))

    self.model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])


  def train(self):
    self.model.fit(self.X, self.y, epochs=100, verbose=1)
    

  def predict(self, text: str):
    num_words = 1
    for _ in range(num_words):
      token_list = self.tokenizer.texts_to_sequences([text])[0]
      token_list = pad_sequences([token_list], maxlen=self.max_sequence_len-1, padding='pre')
      predicted = np.argmax(self.model.predict(token_list, verbose=0), axis=-1)

      output_word = ""
      for word, index in self.tokenizer.word_index.items():
          if index == predicted:
              output_word = word
              break
      text += " " + output_word

    return text