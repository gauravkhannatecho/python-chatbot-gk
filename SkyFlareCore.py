import os
import spacy
from typing import Optional

nlp = None

class CoreModes():
    GET_YN = "GET_YN"
    GET_ANSWER = 'GET_ANSWER'
    ACCEPT_QUESTION = 'ACCEPT_QUESTION'

class CoreConfig():
    #Make Configurable
    USER_FILE_LOC = os.environ['USER_FILE_DIR']

class SkyFlareCore():
    def __init__(self, user_name:str): 
        global nlp
        assert(user_name is not None)
        self.user_name = user_name
        self.file_dir = os.path.join(CoreConfig.USER_FILE_LOC, self.user_name + ".txt")
        if nlp is None:
            nlp = spacy.load("en_core_web_lg")
        self.load_questions_and_answers()
        self.mode = CoreModes.ACCEPT_QUESTION
        self.history = []

    def to_string_self(self):
        retval = ""
        for property, value in vars(self).items():
            retval += "{0}: {1}\r\n".format(property, value)
        return retval
    
    def load_questions_and_answers(self):
        self.qa_dict = {}
        try:
            with open(self.file_dir, 'r') as file:
                for i, line in enumerate(file):
                    if i == 0:
                        continue
                    else:
                        question, answer = line.strip().split('|')
                        self.qa_dict[question] = answer
        except FileNotFoundError:
            pass

    def save_question_and_answer(self, question, answer):
        with open(self.file_dir, 'a') as file:
            file.write(f"{question}|{answer}\n")
    
    def get_most_similar_question(self, user_question):
        max_similarity = 0
        most_similar_question = None
        for question in self.qa_dict:
            similarity = nlp(user_question).similarity(nlp(question))
            if similarity > max_similarity:
                max_similarity = similarity
                most_similar_question = question
        return most_similar_question, max_similarity
    
    def chatbot(self, message, history):
        self.history = history
        user_question = message
        print(self.mode)
        if(self.mode == CoreModes.ACCEPT_QUESTION):
            if user_question in self.qa_dict:
                response = f"Chatbot: Exact Match: \"{self.qa_dict[user_question]}\""
                return response
            else:
                return self.eval_similarity(message)
        if(self.mode == CoreModes.GET_YN):
            questionCheck = message.upper()
            if questionCheck == "N":
                return self.pose_new()
            if questionCheck == "Y":
                return self.accept_similarity()
        if(self.mode == CoreModes.GET_ANSWER):
            return self.get_answer(message)
        self.mode = CoreModes.ACCEPT_QUESTION
        return "I'm not sure what to do now. Let's try again."

    def eval_similarity(self, message):
        most_similar_question, similarity = self.get_most_similar_question(message)
        if similarity > 0.3:  # Increase the threshold for specificity of answer retreival 
            self.mode =  CoreModes.GET_YN
            response = "Chatbot: \"{0}\"\r\nThis seems like an acceptable answer. Is it?".format(self.qa_dict[most_similar_question])
            return response
        else:
            self.mode = CoreModes.GET_ANSWER
            return self.pose_new()
        
    def get_answer(self, human):
        human_previous = self.history[-1][0]
        self.qa_dict[human_previous] = human
        self.save_question_and_answer(human, human_previous)
        self.mode = CoreModes.ACCEPT_QUESTION
        response = "Chatbot: Thanks, I've learned something new!"
        return response
    
    def accept_similarity(self):
        human_previous = self.history[-1][0] #last exchange, human response
        most_similar_question, similarity = self.get_most_similar_question(human_previous)
        answer = self.qa_dict[most_similar_question]
        self.qa_dict[human_previous] = answer
        self.save_question_and_answer(human_previous, answer)
        self.mode = CoreModes.ACCEPT_QUESTION
        return "Chatbot: Got It."

    def pose_new(self):
        self.mode = CoreModes.GET_ANSWER
        return "Chatbot: I don't know the answer to that. Please tell me."