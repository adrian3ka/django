from .models import UserAnswer, BotQuestion, MasterDegrees, MasterMajors, MasterFacilities, MasterFields, MasterIndustries, MasterJobLevels, MasterLocations, MasterSkillSets
import re
GENERAL_VALUE = "{{x}}"

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
        "Degree" : MASTER_DEGREES,
        "Major" : MASTER_MAJORS,
        "Facility" : MASTER_FACILITIES,
        "Field" : MASTER_FIELDS,
        "Industry": MASTER_INDUSTRIES,
        "JobLevel" : MASTER_JOB_LEVELS,
        "ExpectedLocation" : MASTER_LOCATIONS,
        "SkillSet" : MASTER_SKILL_SETS,
    }
    NUMERIC_MAP_CATEGORY = [
    		"Age" ,
		"SalaryUpper" ,
		"SalaryLower" 
    ]
    def template_matching(self, category, text):
        if not self.master_data:
            self.fillMasterData()
        selected_master_data = []
        extracted_data = ""
        print self.MAP_CATEGORY
        if category in self.MAP_CATEGORY:
            selected_master_data = self.master_data[self.MAP_CATEGORY[category]]
        elif category in self.NUMERIC_MAP_CATEGORY:
	    extracted_data= int (re.search(r'\d+', text).group())
        else:
            return "Category Not Exists"

        for s in selected_master_data:
            if s in text:
                extracted_data = s
                break

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
                self.master_data[self.MASTER_DEGREES].append(masterDegree.name)
            else:
                self.master_data[self.MASTER_DEGREES] = [masterDegree.name]
        
        for masterMajors in MasterMajors.objects.all():
            if self.MASTER_MAJORS in self.master_data:
                self.master_data[self.MASTER_MAJORS].append(masterMajors.name)
            else:
                self.master_data[self.MASTER_MAJORS] = [masterMajors.name]
        
        for masterFacilities in MasterFacilities.objects.all():
            if self.MASTER_FACILITIES in self.master_data:
                self.master_data[self.MASTER_FACILITIES].append(masterFacilities.name)
            else:
                self.master_data[self.MASTER_FACILITIES] = [masterFacilities.name]
        
        for masterFields in MasterFields.objects.all():
            if self.MASTER_FIELDS in self.master_data:
                self.master_data[self.MASTER_FIELDS].append(masterFields.name)
            else:
                self.master_data[self.MASTER_FIELDS] = [masterFields.name]
        
        for masterIndustries in MasterIndustries.objects.all():
            if self.MASTER_INDUSTRIES in self.master_data:
                self.master_data[self.MASTER_INDUSTRIES].append(masterIndustries.name)
            else:
                self.master_data[self.MASTER_INDUSTRIES] = [masterIndustries.name]
        
        for masterJobLevels in MasterJobLevels.objects.all():
            if self.MASTER_JOB_LEVELS in self.master_data:
                self.master_data[self.MASTER_JOB_LEVELS].append(masterJobLevels.name)
            else:
                self.master_data[self.MASTER_JOB_LEVELS] = [masterJobLevels.name]
        
        for masterLocations in MasterLocations.objects.all():
            if self.MASTER_LOCATIONS in self.master_data:
                self.master_data[self.MASTER_LOCATIONS].append(masterLocations.name)
            else:
                self.master_data[self.MASTER_LOCATIONS] = [masterLocations.name]
        
        for masterSkillSets in MasterSkillSets.objects.all():
            if self.MASTER_SKILL_SETS in self.master_data:
                self.master_data[self.MASTER_SKILL_SETS].append(masterSkillSets.name)
            else:
                self.master_data[self.MASTER_SKILL_SETS] = [masterSkillSets.name]
        
    def fillDict(self):
        for userAnswer in UserAnswer.objects.all():
            if userAnswer.category in self.dictionary:
                self.dictionary[userAnswer.category].append(userAnswer.text)
            else:
                self.dictionary[userAnswer.category] = [userAnswer.text]
