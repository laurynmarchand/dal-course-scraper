from bs4 import BeautifulSoup
import requests
import json

department_codes = ['ACSC','ANAT','ARBC','ARCH','ASSC','BIOC','BIOE','BIOL','BMNG','CANA','CHEE','CHEM','CHIN','CIVL','CLAS','COMM','CH&E','CPST','CSCI','CTMP','CRWR','DMUT','DISM','EMSP','ERTH','ECON','ECED','ENGI','ENGM','ENGL','ENVE','ENVS','EURO','FILM','FOSC','FREN','GWST','GEOG','GERM','HESA','HLTH','HSCE','HPRO','HSTC','HIST','INDG','IENG','INFO','INTD','IPHE','ITAL','JOUR','KINE','KING','LAWS','LJSO','LEIS','MRIT','MGMT','MARI','MATH','MECH','MICI','MINE','MUSC','NESC','NUMT','NURS','OCCU','OCEA','PATH','PERF','PHAC','PHIL','PHYC','PHYL','PLAN','POLI','PSYO','RADT','RELS','RSPT','RUSN','SCIE','SLWK','SOSA','SPAN','STAT','SUST','THEA']

data = {}

for code in department_codes:
	page = 1
	while page < 222:
		# Make a GET request to fetch the raw HTML content
		url = 'https://dalonline.dal.ca/PROD/fysktime.P_DisplaySchedule?s_term=202310,202320&s_crn=&s_subj='+code+'&s_numb=&n='+str(page)+'&s_district=All'
		html_content = requests.get(url).text

		# Parse the html content
		soup = BeautifulSoup(html_content, 'lxml')

		course_table = soup.find_all("table", attrs={"class": "dataentrytable"})
		if len(course_table)>1:
			course_table_data = course_table[1].find_all("tr")
			main_headers = ['Notes', 'CRN', 'Section no.', 'Section type', 'Cr Hrs', 'Link', 'Mo', 'Tu','We','Th','Fr','Times','Location(s)', 'Max','Cur','Avail','WtLst','%%Full','Max','Cur','Instructor(s)','Code','BHrs']

			# Get course titles
			course_titles = []
			for course in course_table[1].find_all("tr", attrs={"valign":"middle"}):
				td = course.find("td")
				course_titles.append(td.b.text.replace('\n', ' ').strip())

			# Initialize course data info
			course_data = {}
			course_code = ""

			for tr in course_table_data:
				# When a new course is reached
				if tr.has_attr("valign"):
					td = tr.find("td")
					course = td.b.text.replace('\n', ' ').strip()
					course_code = course[0:9]

					course_data = {}
					course_data["Title"] = course[10:]
					for heading in main_headers:
						course_data[heading] = []

				# All course info after a title
				else:
					# Lectures
					for td, th in (zip(tr.find_all("td", attrs={"class":"dettl"}), main_headers)): 
						if td.text is not None:
							course_data[th].append(td.text.replace('\n', '').strip())
						if td.p is not None:
							course_data[th].append(td.p.text.replace('\n', '').strip())
						if td.b is not None:
							course_data[th].append(td.b.text.replace('\n', '').strip())
					# Tutorials
					for td, th in (zip(tr.find_all("td", attrs={"class":"dettt"}), main_headers)): 
						if td.text is not None:
							course_data[th].append(td.text.replace('\n', '').strip())
						if td.p is not None:
							course_data[th].append(td.p.text.replace('\n', '').strip())
						if td.b is not None:
							course_data[th].append(td.b.text.replace('\n', '').strip())
					# Labs
					for td, th in (zip(tr.find_all("td", attrs={"class":"dettb"}), main_headers)): 
						if td.text is not None:
							course_data[th].append(td.text.replace('\n', '').strip())
						if td.p is not None:
							course_data[th].append(td.p.text.replace('\n', '').strip())
						if td.b is not None:
							course_data[th].append(td.b.text.replace('\n', '').strip())

				data[course_code] = course_data
		page += 20
	print("Done " + code)

with open('data.json','w') as f:
	json.dump(data, f)