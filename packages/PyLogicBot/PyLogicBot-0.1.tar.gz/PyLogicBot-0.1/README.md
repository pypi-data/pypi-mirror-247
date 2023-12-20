# PyChatBot Presidential Speech Analysis EFREI

## Overview

This Python script analyzes the speeches of various presidents. It performs pre-processing on the speech texts and provides basic functions for text analysis, including the calculation of TF-IDF (Term Frequency-Inverse Document Frequency) matrices.

## Project Structure

The project is structured as follows:

- **app.py** : The main application file.
- **Basic_Functions.py** : Contains basic functions used in the application.
- **Cosine_Similarity_Functions.py** : Contains functions for calculating cosine similarity.
- **Features_to_be_Developed.py**: Contains functions for features to be developed.
- **Menu.py**: Contains the application menu.
- **Pre_Processing.py** : Contains functions for data pre-processing.
- **tokenization_question.py** : Contains functions for tokenizing questions.
- **cleaned/** : Contains cleaned presidential speeches.
- **speeches/** : Contains original presidential speeches.
- **static/** and **templates/**: Contain files for the application's user interface.

## Pre-Processing

1. **Extract President Names:** Extracts the names of the presidents from the filenames of speech texts.
2. **Associate First Name:** Associates a first name with each president.
3. **Display President Names:** Displays the list of president's names, avoiding duplicates.
4. **Text Conversion:** Converts the original speech texts to lowercase and creates cleaned versions in the "cleaned" folder.
5. **Remove Punctuation:** Removes punctuation characters from the cleaned speech texts.

## Basic Functions

- **Proportion in Documents:** Calculates the proportion of documents containing a given word.
- **Get Unique Words:** Retrieves a list of unique words from the cleaned texts.
- **Get TF Matrix:** Generates a Term Frequency (TF) matrix for the words in the speeches.
- **Get IDF Scores:** Calculates the Inverse Document Frequency (IDF) scores for the unique words.
- **Get TF-IDF Matrix:** Calculates the TF-IDF matrix using the TF matrix and IDF scores.
- **Transpose Matrix:** Transposes a given matrix.

## Features

### 1. Display Least Important Words

- **Function:** `get_least_important_words(directory)`
- **Description:** Retrieves words with TF-IDF score equal to 0.

### 2. Display Highest TF-IDF Score

- **Function:** `display_highest_tfidf_score(directory)`
- **Description:** Identifies words with the highest TF-IDF scores.

### 3. Most Repeated Words

- **Function:** `most_repeated_words(directory)`
- **Description:** Identifies the most repeated words in the speeches.

### 4. First President to Talk About a Word

- **Function:** `first_president_word(word)`
- **Description:** Identifies the first president to mention a specific word.

### 5. President who said the most a word

- **Function:** `president_who_said_it_the_most(word,directory)`
- **Description:** Identifies the president who said a word the most.

### 6. Get president names

- **Function:** `extract_presidents_names(directory)`
- **Description:** Display the names of the presidents.

## Usage

1. Clone this repository.
2. Install dependencies with `pip install <name of the dependency>`.
3. Run `python app.py` or `flask run` to start the application.
4. Open your browser at `http://localhost:5000` to use the application.

## Menu

- The script includes a menu-driven interface for user interaction. Users can choose specific tasks from the menu.

## Dependencies

- Python 3.x >= 3.9
- Flask
- Random
- Math
- OS
- Re

## Authors

Andrea CHARVIERE and Antonin LARTILLOT-AUTEUIL
