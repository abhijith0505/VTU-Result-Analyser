from flask import Flask,render_template,redirect,url_for
from helpers import insert_region_results,student_results
from collections import OrderedDict
from pymongo import MongoClient
import json, re
from bson.json_util import dumps

app = Flask(__name__)

client = MongoClient()

db = client.results

students = db.students

flags = db.flags


BENGALURU_COLLEGE_CODES = ['1mv', '1ay', '1ap', '1aa', '1ao', '1ah', '1aj', '1ak', '1ac', '1am', '1as', '1ar', '1at', '1au', '1bg', '1bt', '1bc', '1bi', '1bh', '1bs', '1bm', '1by', '1bo', '1ck', '1cr', '1cd', '1cg', '1ce', '1dt', '1ds', '1db', '1da', '1cc', '1gv', '1ec', '1ep', '1ew', '1gs', '1gc', '1ga', '1gd', '1sk', '1gg', '1hk', '1hm', '1ic', '1ii', '1jv', '1js', '1jt', '1ks', '1ki', '1kn', '1me', '1mj', '1nj', '1nc', '1nh', '1ox', '1pn', '1pe', '1ri', '1rl', '1rr', '1rg', '1re', '1rn', '1sj', '1va', '1st', '1sz', '1sg', '1sc', '1sp', '1hs', '1sb', '1sv', '1jb', '1sw', '1bn', '1kt', '1kh', '1rc', '1ve', '1tj', '1vi', '1vj', '1vk', '1yd']
MYSURU_COLLEGE_CODES = ['4ad', '4ai', '4al', '4bw', '4bb', '4bd', '4bp', '4cb', '4ci', '4dm', '4ek', '4mg', '4gm', '4ge', '4gh', '4gl', '4gk', '4gw', '4jn', '4kv', '4km', '4mh', '4mt', '4mk', '4nn', '4pa', '4pm', '4pr', '4ra', '4sf', '4sh', '4mw', '4sm', '4su', '4sn', '4es', '4so', '4ub', '4vv', '4vm', '4vp', '4yg']
BELAGAVI_COLLEGE_CODES = ['2av', '2ag', '2ab', '2ae', '2bv', '2bl', '2gp', '4go', '2gb', '2hn', '2ji', '2kd', '2ke', '2kl', '2gi', '2mb', '2mm', '2rh', '2bu', '2sr', '2sa', '2ha', '2ka', '2tg', '2vs', '2vd']
KALABURGI_COLLEGE_CODES = ['3ae', '3bk', '3br', '3gf', '3gu', '3gn', '3kc', '3kb', '3la', '3na', '3pg', '3vc', '3rb', '3sl', '3vn']

BRANCH_CODES = ['bt', 'cv', 'ee', 'ec', 'te', 'is', 'cs', 'me']

YEAR = ['13', '14', '15']

COLLEGE_CODES = ['1mv']


@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html')

@app.route("/")
def mainInit():
	if db.flags.count()!=1:
		dbInit()
	return render_template('home.html')

@app.route("/HomePage") #Ignore this route. Required for my system. Some stupid issue
def stupidRedirect():
	return redirect(url_for('mainInit'))

@app.route("/api/oneStudent/<college_code>/<year>/<branch>/<int:regno>")
def getOneStudent(college_code,year,branch,regno):
	student = students.find_one({"usn" : (college_code + year
		+branch + str(regno).zfill(3)).upper()})
	if student:
		return dumps(student) #dumps is used to convert bson format of mongodb to json
	else :
		student = student_results(college_code,year,branch,regno)
		db.students.insert_one(student)
		return dumps(student)

@app.route("/api/oneCollege/<college_code>")
def getOneCollege(college_code):
	student = students.find({"usn" : {'$regex': ''+re.escape(college_code.upper())}})
	if any(student):
		 return dumps(student)	#dumps is used to convert bson format of mongodb to json
	else :
		return render_template('error.html')

@app.route("/api/oneRegion/<region_code>")
def getOneRegion(region_code):
	student = students.find({"usn" : {'$regex': '^'+re.escape(region_code.upper())}})
	if any(student):
		 return dumps(student)	#dumps is used to convert bson format of mongodb to json
	else :
		return render_template('error.html')


def dbInit():
	All_Regions = OrderedDict([
					('bengaluru', []),
					('mysuru', []),
					('belagavi', []),
					('kalaburgi', [])])

	for BCodes in BENGALURU_COLLEGE_CODES:
		BangCode = OrderedDict([
					('college', BCodes),
		            ('years', [])])
		for year in YEAR:
			Year = OrderedDict([
					('year', year),
		            ('branches', [])])
			for branch in BRANCH_CODES:
				 Branch = OrderedDict([
				 		('branch', branch),
				 		('flag', '0')])
				 Year["branches"].append(Branch)
			BangCode["years"].append(Year)
		All_Regions['bengaluru'].append(BangCode)

	for MCodes in MYSURU_COLLEGE_CODES:
		MyCode = OrderedDict([
					('college', MCodes),
		            ('years', [])])
		for year in YEAR:
			Year = OrderedDict([
					('year', year),
		            ('branches', [])])
			for branch in BRANCH_CODES:
				 Branch = OrderedDict([
				 		('branch', branch),
				 		('flag', '0')])
				 Year["branches"].append(Branch)
			MyCode["years"].append(Year)
		All_Regions['mysuru'].append(MyCode)

	for BelCodes in BELAGAVI_COLLEGE_CODES:
		BgCode = OrderedDict([
					('college', BelCodes),
		            ('years', [])])
		for year in YEAR:
			Year = OrderedDict([
					('year', year),
		            ('branches', [])])
			for branch in BRANCH_CODES:
				 Branch = OrderedDict([
				 		('branch', branch),
				 		('flag', '0')])
				 Year["branches"].append(Branch)
			BgCode["years"].append(Year)
		All_Regions['belagavi'].append(BgCode)

	for KCodes in KALABURGI_COLLEGE_CODES:
		KCode = OrderedDict([
					('college', KCodes),
		            ('years', [])])
		for year in YEAR:
			Year = OrderedDict([
					('year', year),
		            ('branches', [])])
			for branch in BRANCH_CODES:
				 Branch = OrderedDict([
				 		('branch', branch),
				 		('flag', '0')])
				 Year["branches"].append(Branch)
			KCode["years"].append(Year)
		All_Regions['kalaburgi'].append(KCode)

	db.flags.insert(All_Regions)

if __name__ == "__main__":
    app.run(debug = True)
