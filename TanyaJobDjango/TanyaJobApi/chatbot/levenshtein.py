from .models import UserAnswer, BotQuestion, MasterDegrees, MasterMajors, MasterFacilities, MasterFields, MasterIndustries, MasterJobLevels, MasterLocations, MasterSkillSets
import re, copy
GENERAL_VALUE = "{{x}}"
LEVENSTHEIN_MAX_DISTANCE = 2

class LevenshteinExtraction:
    dictionary = {}
    master_data = {}
    MASTER_DEGREES = 'master_degrees'
    MASTER_MAJORS = 'master_majors'
    MASTER_FACILITIES = 'master_facilities'
    MASTER_FIELDS = 'master_fields'
    MASTER_INDUSTRIES = 'master_industries'
    MASTER_JOB_LEVELS = 'master_job_levels'
    MASTER_LOCATIONS = 'master_locations'
    MASTER_SKILL_SETS = 'master_skill_sets'

    MAP_CATEGORY = {
        "Degree": MASTER_DEGREES,
        "Major": MASTER_MAJORS,
        "Facility": MASTER_FACILITIES,
        "Field": MASTER_FIELDS,
        "Industry": MASTER_INDUSTRIES,
        "JobLevel": MASTER_JOB_LEVELS,
        "ExpectedLocation": MASTER_LOCATIONS,
        "SkillSet": MASTER_SKILL_SETS,
    }
    NUMERIC_MAP_CATEGORY = ["Age", "SalaryUpper", "SalaryLower"]

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
            return "Category Not Exists"


        items = text.split()
        wordList =[]
        for i in range(len(items)):
            temp_outer = []
            for j in range(i, len(items)):
                temp_outer.append(items[j])
                temp = copy.copy(temp_outer)
                wordList.append((' ').join(temp))

        flag = 0
        candidate_levensthein_extracted_data = []
        for s in selected_master_data:
            if s in wordList:
                flag = 0
		extracted_data = s
                break     
            for word in wordList:
                if word not in candidate_levensthein_extracted_data:
                    distance = self.levenshtein_distance(word, s)
                    if distance <= LEVENSTHEIN_MAX_DISTANCE:
                        candidate_levensthein_extracted_data.append(s)
            for a in items:
                if (a in s):
                    flag += 1
                    extracted_data = s

        if (flag > 1):
            if (len(candidate_levensthein_extracted_data) == 1):
                extracted_data = candidate_levensthein_extracted_data[0]
            else :
                extracted_data = ""            

        return extracted_data

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

    def fillDict(self):
        for userAnswer in UserAnswer.objects.all():
            if userAnswer.category in self.dictionary:
                self.dictionary[userAnswer.category].append(userAnswer.text)
            else:
                self.dictionary[userAnswer.category] = [userAnswer.text]
