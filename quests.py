from abc import ABC, abstractmethod
import csv

class CSVAccessLayer:
    def __init__(self, filename):
        self.filename = filename

    def get_questions_for_phase(self, phase_name, severity):
        questions = []
        with open(self.filename, 'r') as f:
            reader = csv.reader(f)
            next(reader)  # Skip the header row
            for row in reader:
                if row[2] == phase_name and row[3] == severity:  # phase is in the 3rd column, severity is in the 4th column
                    text = row[0]  # question text is in the 1st column
                    options = row[1].split(';')  # options are in the 2nd column and are separated by semicolons
                    questions.append(Question(text, options))
        return questions


class Question:
    def __init__(self, question, options):
        self.question = question
        self.options = options
        self.answer = None

    def print_question_and_options(self):
        print(self.question)
        for i, option in enumerate(self.options, start=1):
            print(f"{i}. {option}")

    def answer_question(self, answer):
        self.answer = answer

class Phase(ABC):
    answer_to_score = {
        'not at all': 1,
        'a little': 1.5,
        'somewhat': 2,
        'more than avg': 2.5,
        'a lot': 3,
    }

    def start_phase(self):
        self.ask_initial_question()  # Ask initial question and get severity
        question = self.get_next_question()  # Get the first question
        while question is not None:
            question.print_question_and_options() #print questions and options
            answer = input("Answer: ")  # Collect answer
            self.answer_question(answer)  # Store answer
            question = self.get_next_question()  # Get the next question
    
    def __init__(self, user_id, phase_name, csv_access_layer):
        self.user_id = user_id
        self.phase_name = phase_name
        self.csv_access_layer = csv_access_layer
        self.questions = []
        self.current_question_index = 0
        self.severity = None

    def ask_initial_question(self):
        response=input(f"One a scale of 1 - 10, how would you rate your {self.phase_name}?")
        self.severity = self._determine_severity(response)
        self.questions = self.csv_access_layer.get_questions_for_phase(self.phase_name, self.severity)

    def _determine_severity(self, score):
        score=int(score)
        if score <4:
            return 'low'
        elif score <= 6:
            return 'medium'
        else:
            return 'high'

    def answer_question(self, answer):
        self.questions[self.current_question_index].answer_question(answer)
        self.current_question_index += 1

    def get_next_question(self):
        if self.current_question_index < len(self.questions):
            return self.questions[self.current_question_index]
        else:
            return None

    def calculate_score(self):
        return sum([self.answer_to_score[q.answer] for q in self.questions if q.answer is not None])


class DepressionPhase(Phase):
    def __init__(self, user_id, csv_access_layer):
        super().__init__(user_id, "depression", csv_access_layer)

class AnxietyPhase(Phase):
    def __init__(self, user_id, csv_access_layer):
        super().__init__(user_id, "anxiety", csv_access_layer)

class StressPhase(Phase):
    def __init__(self, user_id, csv_access_layer):
        super().__init__(user_id, "stress", csv_access_layer)

csv_access = CSVAccessLayer('C:/Users/Shailly/OneDrive/Desktop/Summer Shit/Research Project/web app/questions.csv')
depression_phase = DepressionPhase('user1', csv_access)
depression_phase.start_phase()  # this will ask the initial question and populate the `questions` list based on the response

anxiety_phase = AnxietyPhase('user1', csv_access)
anxiety_phase.start_phase()

stress_phase = StressPhase('user1', csv_access)
stress_phase.start_phase()

# evaluation based on scores
class MentalHealthEvaluation:
    def __init__(self, depression_phase, anxiety_phase, stress_phase):
        self.depression_phase = depression_phase
        self.anxiety_phase = anxiety_phase
        self.stress_phase = stress_phase

    def calculate_total_score(self):
        return self.depression_phase.calculate_score() + self.anxiety_phase.calculate_score() + self.stress_phase.calculate_score()

    def evaluate(self):
        total_score = self.calculate_total_score()
        if total_score <= 44:
            return "Your responses indicate that you're generally coping well with life's challenges. Continue to monitor your feelings, and don't hesitate to seek help if needed."
        elif total_score <= 59:
            return "Your responses suggest that you're experiencing some symptoms of stress, anxiety, and depression. It's important to monitor your mental health and consider seeking professional advice."
        elif total_score <= 74:
            return "Your responses suggest that you may be dealing with moderate symptoms of stress, anxiety, and depression. Please consider reaching out to a mental health professional for help."
        else:
            return "Your responses indicate significant symptoms of stress, anxiety, and depression. It's very important to seek professional help immediately."

# depression_phase, anxiety_phase, and stress_phase are instances of DepressionPhase, AnxietyPhase, and StressPhase that the user has completed
evaluation = MentalHealthEvaluation(depression_phase, anxiety_phase, stress_phase)
result = evaluation.evaluate()
print(result)