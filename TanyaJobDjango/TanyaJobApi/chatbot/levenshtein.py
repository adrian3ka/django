from .models import UserAnswer, BotQuestion

GENERAL_VALUE = "{{x}}"

class LevenshteinExtraction:
    dictionary = {}
    def levenshtein_distance(self, a, b):
        """Return the Levenshtein edit distance between two strings *a* and *b*."""
        if a == b:
            return 0
        if len(a) < len(b):
            a, b = b, a
        if not a:
            return len(b)
        previous_row = range(len(b) + 1)
        for i, column1 in enumerate(a):
            current_row = [i + 1]
            for j, column2 in enumerate(b):
                insertions = previous_row[j + 1] + 1
                deletions = current_row[j] + 1
                substitutions = previous_row[j] + (column1 != column2)
                current_row.append(min(insertions, deletions, substitutions))
            previous_row = current_row
        return previous_row[-1]
    def template_match(self, template, input_text):
        matched = []
        # Remove Similar Word
        token = template.split()
        for t in token:
            temp = input_text.replace(t, '')
            if input_text != temp: 
                input_text = input_text.replace(t, '')
                matched.append(t)
        token = list(set(token) - set(matched))
        token.remove(GENERAL_VALUE)
        input_text = input_text.strip()
        return token, input_text
    def extract(self, category, input_text):
        closer_to_dict = {}
        if category in self.dictionary:
            for dc in self.dictionary[category]:
                value = self.levenshtein_distance(dc, input_text)
                if value in closer_to_dict:
                    closer_to_dict[value].append(dc)
                else:
                    closer_to_dict[value] = [dc]
            # dict will automaticly sort based on key
            for c in closer_to_dict:
                for text in closer_to_dict[c]:
                     x, y = self.template_match(text, input_text)
                     if len(x) == 0:
                         return y
        else:
            return "Category Not Exist"
    def __init__(self):
        for userAnswer in UserAnswer.objects.all():
            if userAnswer.category in self.dictionary:
                self.dictionary[userAnswer.category].append(userAnswer.text)
            else:
                self.dictionary[userAnswer.category] = [userAnswer.text]
