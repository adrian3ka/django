from .models import UserAnswer, BotQuestion, MasterDegrees, MasterMajors, MasterFacilities, MasterFields, MasterIndustries, MasterJobLevels, MasterLocations, MasterSkillSets
from itertools import permutations 

import re, copy
GENERAL_VALUE = "{{x}}"
LEVENSTHEIN_MAX_DISTANCE = 2
MIN_LETTER_FOR_LEVENSTHEIN = LEVENSTHEIN_MAX_DISTANCE + 2


class LevenshteinExtraction:
    dictionary = {}
    master_data = {}
    JUTA = ["juta", "jt"]
    JUTA_VALUE = 1000000
    MASTER_DEGREES = 'master_degrees'
    MASTER_MAJORS = 'master_majors'
    MASTER_FACILITIES = 'master_facilities'
    MASTER_FIELDS = 'master_fields'
    MASTER_INDUSTRIES = 'master_industries'
    MASTER_JOB_LEVELS = 'master_job_levels'
    MASTER_LOCATIONS = 'master_locations'
    MASTER_SKILL_SETS = 'master_skill_sets'

    MASTER_MAJOR_CATEGORY = 'Major'
    MASTER_FIELD_CATEGORY = 'Field'
    MASTER_JOB_LEVEL_CATEGORY = 'JobLevel'
    MASTER_SALARY_UPPER_CATEGORY = 'SalaryUpper'
    MASTER_SALARY_LOWER_CATEGORY = 'SalaryLower'

    MASTER_LIST = [
        MASTER_DEGREES, MASTER_MAJORS, MASTER_FACILITIES, MASTER_FIELDS,
        MASTER_INDUSTRIES, MASTER_INDUSTRIES, MASTER_JOB_LEVELS,
        MASTER_LOCATIONS, MASTER_SKILL_SETS
    ]

    MAP_CATEGORY = {
        "Degree": MASTER_DEGREES,
        MASTER_MAJOR_CATEGORY: MASTER_MAJORS,
        "Facility": MASTER_FACILITIES,
        MASTER_FIELD_CATEGORY: MASTER_FIELDS,
        "Industry": MASTER_INDUSTRIES,
        MASTER_JOB_LEVEL_CATEGORY: MASTER_JOB_LEVELS,
        "ExpectedLocation": MASTER_LOCATIONS,
        "SkillSet": MASTER_SKILL_SETS,
    }
    NUMERIC_MAP_CATEGORY = ["Age", MASTER_SALARY_UPPER_CATEGORY, MASTER_SALARY_LOWER_CATEGORY, "WorkExp"]

    SPECIAL_MAPS = {
        "s1": "Sarjana (s1)",
        "sarjana": "Sarjana (s1)",
        "s2": "Magister (s2)",
        "Master": "Magister (s2)",
        "s3": "Doktor (s3)",
        "Doktor": "Doktor (s3)",
        "d3": "Diploma (D3)",
	"diploma": "Diploma (D3)",
        "sekolah menengah atas": "sma",
        "sekolah menengah keatas": "sma",
        "sekolah menengah kejuruan": "smk",
    }

    KEYBOARD_MAP =  {
        #"char" : {line, row},
        "q": [0, 0],
        "w": [0, 1],
        "e": [0, 2],
        "r": [0, 3],
        "t": [0, 4],
        "y": [0, 5],
        "u": [0, 6],
        "i": [0, 7],
        "o": [0, 8],
        "p": [0, 9],

        "a": [1, 0],
        "s": [1, 1],
        "d": [1, 2],
        "f": [1, 3],
        "g": [1, 4],
        "h": [1, 5],
        "j": [1, 6],
        "k": [1, 7],
        "l": [1, 8],

        "z": [2, 0],
        "x": [2, 1],
        "c": [2, 2],
        "v": [2, 3],
        "b": [2, 4],
        "n": [2, 5],
        "m": [2, 6],
    }

    def template_matching(self, category, text):
        text = text.lower()
        if not self.master_data:
            self.fillMasterData()
        selected_master_data = []
        extracted_data = ""
        if category in self.MAP_CATEGORY:
            selected_master_data = self.master_data[
                self.MAP_CATEGORY[category]]
        elif category in self.NUMERIC_MAP_CATEGORY:
            extracted_data = int(re.search(r'\d+', text).group())
        else:
            return "Category Not Exists", None, None

        items = text.split()

        for i in range(len(items)):
            if items[i] in self.SPECIAL_MAPS:
                items[i] = self.SPECIAL_MAPS[items[i]]
        wordList = []

        text = (' ').join(items)
        text = text.lower()

        for i in range(len(items)):
            temp_outer = []
            for j in range(i, len(items)):
                temp_outer.append(items[j])
                temp = copy.copy(temp_outer)
                wordList.append((' ').join(temp))

        candidate_extracted_data = []
        for s in selected_master_data:
            if category == self.MASTER_JOB_LEVEL_CATEGORY:
               words = s.split()
               perm = permutations(words)
               for i in list(perm): 
                   word = (' ').join(i)
                   if word in text:
                       if (extracted_data == ""):
                           extracted_data = s
                           continue
               for word in words:
                   if word in text and word not in extracted_data:
                        candidate_extracted_data.append(s)
            elif s in text:
                if (extracted_data == ""):
                    extracted_data = s
                continue
            for word in wordList:
                if len(word) < MIN_LETTER_FOR_LEVENSTHEIN:
                    continue
                distance = self.levenshtein_distance(word, s)
                if distance <= LEVENSTHEIN_MAX_DISTANCE:
                    if s not in candidate_extracted_data and s not in extracted_data:
                        candidate_extracted_data.append(s)

        typo_correction = False
        suggested_word = None
        if extracted_data != "" and len(candidate_extracted_data) == 0:
            suggested_word = []
        elif extracted_data != "" and len(candidate_extracted_data) > 0:
            suggested_word = candidate_extracted_data
            suggested_word.append(extracted_data)
            typo_correction = True
        elif (len(candidate_extracted_data) == 1) and extracted_data == "":
            extracted_data = candidate_extracted_data[0]
            typo_correction = True
        elif (len(candidate_extracted_data) > 1) and extracted_data == "":
            suggested_word = candidate_extracted_data
            typo_correction = True
        elif extracted_data == "" and len(candidate_extracted_data) == 0 and (category == self.MASTER_MAJOR_CATEGORY or category == self.MASTER_FIELD_CATEGORY):
            suggested_word = []
            for s in selected_master_data:
                temp = s.split()
                acronym = [x[0] for x in temp]
                if len(acronym) < 2:
                    continue
                for word in text.split():
                    for t in temp:
                        if t in word:
                            suggested_word.append(s)
                    if len(word) < 2:
                        continue
                    if word == ('').join(acronym):
                        typo_correction = True
                        suggested_word.append(s)
            if len(suggested_word) == 1:
                extracted_data = suggested_word[0]


        if category == self.MASTER_SALARY_UPPER_CATEGORY or category == self.MASTER_SALARY_LOWER_CATEGORY:
            for jutaWord in self.JUTA:
                if jutaWord in text:
                    extracted_data = extracted_data * self.JUTA_VALUE
                    break

        return extracted_data, typo_correction, suggested_word

    def keyboard_distance(self, char1, char2):
        if char1 == " " and char2 == " ":
            return 0
        if char1 not in self.KEYBOARD_MAP or char2 not in self.KEYBOARD_MAP:
            return 99999
        kb1 = self.KEYBOARD_MAP[char1]
	kb2 = self.KEYBOARD_MAP[char2]

        rowDist = abs(kb1[0] - kb2[0])
        lineDist = abs(kb1[1] - kb2[1])
        return lineDist + rowDist

    def levenshtein_distance(self, a, b):
        """Return the Levenshtein edit distance between two strings *a* and *b*."""
        if a == b:
            return 0
        if len(a) < len(b):
            a, b = b, a
        if not a:
            return len(b)
        if len(a) == len(b):
            total_distance = 0
            for i, column1 in enumerate(a):
                total_distance += self.keyboard_distance(a[i], b[i])
            return total_distance

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
        if not self.dictionary:
            self.fillDict()

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
        print "LevenshteinExtraction Created"

    def fillMasterData(self):
        for masterDegree in MasterDegrees.objects.all():
            if self.MASTER_DEGREES in self.master_data:
                self.master_data[self.MASTER_DEGREES].append(
                    masterDegree.name.lower())
            else:
                self.master_data[self.MASTER_DEGREES] = [
                    masterDegree.name.lower()
                ]

        for masterMajors in MasterMajors.objects.all():
            if self.MASTER_MAJORS in self.master_data:
                self.master_data[self.MASTER_MAJORS].append(
                    masterMajors.name.lower())
            else:
                self.master_data[self.MASTER_MAJORS] = [
                    masterMajors.name.lower()
                ]

        for masterFacilities in MasterFacilities.objects.all():
            if self.MASTER_FACILITIES in self.master_data:
                self.master_data[self.MASTER_FACILITIES].append(
                    masterFacilities.name.lower())
            else:
                self.master_data[self.MASTER_FACILITIES] = [
                    masterFacilities.name.lower()
                ]

        for masterFields in MasterFields.objects.all():
            if self.MASTER_FIELDS in self.master_data:
                self.master_data[self.MASTER_FIELDS].append(
                    masterFields.name.lower())
            else:
                self.master_data[self.MASTER_FIELDS] = [
                    masterFields.name.lower()
                ]

        for masterIndustries in MasterIndustries.objects.all():
            if self.MASTER_INDUSTRIES in self.master_data:
                self.master_data[self.MASTER_INDUSTRIES].append(
                    masterIndustries.name.lower())
            else:
                self.master_data[self.MASTER_INDUSTRIES] = [
                    masterIndustries.name.lower()
                ]

        for masterJobLevels in MasterJobLevels.objects.all():
            if self.MASTER_JOB_LEVELS in self.master_data:
                self.master_data[self.MASTER_JOB_LEVELS].append(
                    masterJobLevels.name.lower())
            else:
                self.master_data[self.MASTER_JOB_LEVELS] = [
                    masterJobLevels.name.lower()
                ]

        for masterLocations in MasterLocations.objects.all():
            if self.MASTER_LOCATIONS in self.master_data:
                self.master_data[self.MASTER_LOCATIONS].append(
                    masterLocations.name.lower())
            else:
                self.master_data[self.MASTER_LOCATIONS] = [
                    masterLocations.name.lower()
                ]

        for masterSkillSets in MasterSkillSets.objects.all():
            if self.MASTER_SKILL_SETS in self.master_data:
                self.master_data[self.MASTER_SKILL_SETS].append(
                    masterSkillSets.name.lower())
            else:
                self.master_data[self.MASTER_SKILL_SETS] = [
                    masterSkillSets.name.lower()
                ]

        for master in self.MASTER_LIST:
            self.master_data[master].sort(key=len)
            self.master_data[master].reverse()

    def fillDict(self):
        for userAnswer in UserAnswer.objects.all():
            if userAnswer.category in self.dictionary:
                self.dictionary[userAnswer.category].append(userAnswer.text)
            else:
                self.dictionary[userAnswer.category] = [userAnswer.text]
