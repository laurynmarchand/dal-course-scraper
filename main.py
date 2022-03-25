from bs4 import BeautifulSoup
import requests

url='https://dalonline.dal.ca/PROD/fysktime.P_DisplaySchedule?s_term=202310&s_subj=CSCI&s_district=All'

# Make a GET request to fetch the raw HTML content
html_content = requests.get(url).text

# Parse the html content
soup = BeautifulSoup(html_content, 'lxml')

course_table = soup.find_all("table", attrs={"class": "dataentrytable"})
course_table_data = course_table[1].find_all("tr")
main_headers = ['Notes', 'CRN', 'Section no.', 'Section type', 'Cr Hrs', 'Link', 'Mo', 'Tu','We','Th','Fr','Times','Location(s)', 'Max','Cur','Avail','WtLst','%%Full','Max','Cur','Instructor(s)','Code','BHrs']

#print(course_table_data[0])

# get course titles
course_titles = []
for course in course_table[1].find_all("tr", attrs={"valign":"middle"}):
	td = course.find("td")
	course_titles.append(td.b.text.replace('\n', ' ').strip())

data = {}
course_data = {}
course = ""

for tr in course_table_data:
	if tr.has_attr("valign"):
		td = tr.find("td")
		course = td.b.text.replace('\n', ' ').strip()
		course_data = {}
		for heading in main_headers:
			course_data[heading] = []
	else:
		# Get all the elements of row
		for td, th in (zip(tr.find_all("td", attrs={"class":"dettl"}), main_headers)): 
			if td.text is not None:
				course_data[th].append(td.text.replace('\n', '').strip())
			if td.p is not None:
				course_data[th].append(td.p.text.replace('\n', '').strip())
			if td.b is not None:
				course_data[th].append(td.b.text.replace('\n', '').strip())

		for td, th in (zip(tr.find_all("td", attrs={"class":"dettt"}), main_headers)): 
			if td.text is not None:
				course_data[th].append(td.text.replace('\n', '').strip())
			if td.p is not None:
				course_data[th].append(td.p.text.replace('\n', '').strip())
			if td.b is not None:
				course_data[th].append(td.b.text.replace('\n', '').strip())

		for td, th in (zip(tr.find_all("td", attrs={"class":"dettb"}), main_headers)): 
			if td.text is not None:
				course_data[th].append(td.text.replace('\n', '').strip())
			if td.p is not None:
				course_data[th].append(td.p.text.replace('\n', '').strip())
			if td.b is not None:
				course_data[th].append(td.b.text.replace('\n', '').strip())

	data[course] = course_data

print(data['CSCI 1105 Intro to Computer Programming'])