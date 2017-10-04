#import httplib2
import bottle
from bottle import run, route,get,request, post
from bottle import redirect
# from oauth2client.client import OAuth2WebServerFlow
# from oauth2client.client import flow_from_clientsecrets
# from googleapiclient.errors import HttpError
# from googleapiclient.discovery import build
import operator, pickle
import sqlite3 as lite
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
recenthistory = []


@route('/')
#not signed in
@post('/homePage')
def homePage():
	global recenthistory
	# del recenthistory[:]
	htmlFormat = ["""<html><style>
				html{
					background:
					url(http://thehdimg.com/images/db_img2/winter-space-hd-wallpaper-pictures-5.gif) no-repeat center center fixed;
					background-size:cover;
				}
				h1{
					color: #669900;
					text-align: center;
					font-family: "Georgia";
					font-style: oblique;
				}
				p.promote{
					color: #FFAB00;
					font-size: 150%;
					text-align: center;
					font-family: "Georgia";
					font-style: oblique;
				}
				#figure{
					color: #6170FF;
					text-align: center;
					font-size: 100%;
					vertical-align: middle
				}
				input[type = text]{
					text-align: center;
					padding:15px;
					border:2px solid #669900; 
				    -webkit-border-radius: 5px;
				    border-radius: 40px;
				    width: 500px;
 					height: 5px;
				}
				input[type=submit] {
					text-align: center;
				    padding:5px 15px; 
				    color:#f7dce4;
				    background:#669900;
				    border:0 none;
				    cursor:pointer;
				    font-weight:bold
				    -webkit-border-radius: 5px;
				    border-radius: 5px; 
				}
				#log{
					color: #6170FF;
					text-align: right;
					font-size: 100%;
					vertical-align: middle
				}
				table {
				    width: 90%;
				    color:#0099FF;
				}
				th{
					height: 50px;
					text-align: center;
					font-family: "Georgia";
					font-style: oblique;
				}
				td{
					text-align: center;
					font-family: "Georgia";
					font-style: oblique;

	 			}"""]
	htmlFormat.append('''
			</style>
			<head><title>No Secret</title></head>
			<body>''')

	htmlFormat.append("""
					<h1>There is nothing could be a secret in this world!</h1>
						<p class = "promote">What do you want to know?</p>
						
						<div id="figure">
							<form action='/search' method="POST">
							<input type="text" name="Keywords">
							<input type="submit" value="Figure out!">
							</form>
						</div>
					</body>
				""")
	
	htmlFormat.append('</html>')
	return htmlFormat

urlList = []
cp = 1
np = cp + 1
page = ""

@route('/search', method='POST')
def getKeyWords():
	originalString = request.forms.get('Keywords')

	KeyWordList = originalString.split()
	#joinList is a list with punctuation, because it is used to record what the user typed in
	joinList = ' '.join(KeyWordList)

	KeyWordListNoPun = [ ]
	NoPunS = ""
	punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
	for ch in originalString:
		if ch not in punctuations:
			NoPunS = NoPunS + ch
	KeyWordListNoPun = NoPunS.split()

	htmlCommand = ["""<html><style>
				html{
					background:
					url(http://funmozar.com/wp-content/uploads/2014/12/Animated-Christmas-Wallpaper-08.jpg) no-repeat center center fixed;
					background-size:cover;
				}
				h1{
					color: #0099FF;
					text-align: center;
					font-family: "Georgia";
					font-style: oblique;
				}
				table.result{
				    width: 90%;
				    color:#FFAB00;
				}
				table.result th{
					height: 50px;
					text-align: center;
					font-family: "Georgia";
					font-style: oblique;
					color: #FFAB00;
				}
				table.result td{
					text-align: center;
					font-family: "Georgia";
					font-style: oblique;
					color: #FFAB00;
				}
				table.result{
				    width: 90%;
				    color:#FFAB00;
				}
				table.URLs td{
					text-align: left;
					font-family: "Georgia";
					font-style: oblique;
				}
				table.URLs th{
					height: 50px;
					text-align: left;
					font-family: "Georgia";
					font-style: oblique;
				}
				p.result{
					color: #FFAB00;
					font-size: 100%;
					text-align: center;
					font-family: "Georgia";
					font-style: oblique;
				}
				p.error{
					color: #FFAB00;
					font-size: 100%;
					text-align: center;
					font-family: "Georgia";
					font-style: oblique;
				}
				a{
					color: #FFAB00;
				}
				#more_result{
					color: #6170FF;
					text-align: right;
					font-size: 100%;
					vertical-align: middle
				}
				input[type = text]{
					text-align: center;
					padding:15px;
					border:2px solid #669900; 
				    -webkit-border-radius: 5px;
				    border-radius: 40px;
				    width: 500px;
 					height: 5px;
				}
				input[type=submit] {
					text-align: center;
				    padding:5px 15px; 
				    color:#f7dce4;
				    background:#669900;
				    border:0 none;
				    cursor:pointer;
				    font-weight:bold
				    -webkit-border-radius: 5px;
				    border-radius: 5px; 
				}
				back{
					color: #6170FF;
					text-align: left;
					font-size: 100%;
					vertical-align: middle
				}
				"""]

	##########################################################################################
	global urlList
	urlList = PageIDInfo(KeyWordListNoPun)

	##########################################################################################

	# if logged:
	for words in KeyWordListNoPun:
		#case insensitive in dictionary by using lower()
		#there is no punctuation in dictionary
		if not words.lower() in recenthistory:
			recenthistory.insert(0,words.lower())
		else:
			recenthistory.remove(words.lower())
			recenthistory.insert(0,words.lower())

	del recenthistory[10: ]
	htmlCommand.append("""</style>""")
	htmlCommand.append("""<body>
					<h1>There is nothing could be a secret in this world!</h1>
					</body>
					<body><p class = "result">Search for "%s"</p>""" %(joinList))


	#################################################################################################


	if urlList[0] == 3:
		htmlCommand.append("""<p class = "error">The keyword does not exit in library.</p>""")

	if urlList[0] != 3:
		htmlCommand.append("<table class = 'URLs'>")
		if urlList[0] == 1:
			for url in urlList[1]:
				htmlCommand.append("""<tr><td><a href="%s">%s</a></td></tr>""" %(url,url))
			htmlCommand.append('</table>')
		elif urlList[0] == 0:
			for n in range(0, 5):
				htmlCommand.append("""<tr><td><a href="%s">%s</a></td></tr>""" %(urlList[1][n], urlList[1][n]))
			htmlCommand.append('</table>')
			global cp
			cp = 1
			np = cp + 1
			htmlCommand.append("""<body><div id = "more_result"><form action = '/nextpage/""")
			htmlCommand.append(str(np))
			htmlCommand.append("""' method = "POST"><input type = "submit" value = "next page">
											</form></div></body>""")


	htmlCommand.append("""<body><div id = "back"><form action = '/homePage' method= "post">
							<input type = "submit" value = "Go back to home page.">
							</form></div></body>""")

	htmlCommand.append("<table class = 'result'><tr><td>Searching History</td></tr>")

	for word in recenthistory:
		htmlCommand.append('<tr><td>%s</td></tr>' %word)

	htmlCommand.append('</table>')
		
		
	htmlCommand.append('</html>')
	return htmlCommand


pp = cp - 1
@post('/nextpage/<np>')
def linkToNextPage(np):

	global cp
	cp = cp + 1
	htmlURLS = []
	htmlURLS.append("""<html><style>
					html{
						background:
						url(http://funmozar.com/wp-content/uploads/2014/12/Animated-Christmas-Wallpaper-08.jpg) no-repeat center center fixed;
						background-size:cover;
					}
					#log{
						text-align: right;
						font-size: 100%;
						vertical-align: top
					}
					p.user{
						color: #669900;
						font-size: 80%;
						text-align: right;
						vertical-align-align: top
						font-family: "Georgia";
						font-style: oblique;
					}
					table {
					    width: 90%;
					    color:#0099FF;
					}
					th{
						height: 50px;
						text-align: left;
						font-family: "Georgia";
						font-style: oblique;
					}
					td{
						text-align: left;
						font-family: "Georgia";
						font-style: oblique;
					}
					a{
					    color: #FFAB00;
					}
					#next_result{
						color: #6170FF;
						text-align: right;
						font-size: 100%;
						vertical-align: middle
					}
					input[type = text]{
						text-align: center;
						padding:15px;
						border:2px solid #669900; 
					    -webkit-border-radius: 5px;
					    border-radius: 40px;
					    width: 500px;
	 					height: 5px;
					}
					input[type=submit] {
						text-align: center;
					    padding:5px 15px; 
					    color:#f7dce4;
					    background:#669900;
					    border:0 none;
					    cursor:pointer;
					    font-weight:bold
					    -webkit-border-radius: 5px;
					    border-radius: 5px; 
					}
					#pre_result{
						text-align: center;
						font-size: 100%;
						vertical-align: middle
						padding: 5px;
						color:#f7dce4;
					    background:#669900;
					    border:0 none;
					    cursor:pointer;
					    font-weight:bold
					    -webkit-border-radius: 5px;
					    border-radius: 5px;
					    width: 50px;
 						height: 5px;
 						float:left
					}
					#next_result{
						text-align: center;
						font-size: 100%;
						vertical-align: middle
						padding: 5px;
						color:#f7dce4;
					    background:#669900;
					    border:0 none;
					    cursor:pointer;
					    font-weight:bold
					    -webkit-border-radius: 5px;
					    border-radius: 5px;
					    width: 50px;
 						height: 5px;
 						float:right
					}
					#back{
						color: #6170FF;
						text-align: left;
						font-size: 100%;
						vertical-align: middle
					}</style>""")
					

	firstURL = (cp-1)*5
	lastURL = cp*5
	htmlURLS.append("""<table id = 'URLs'>""")
	if len(urlList[1]) >=5:
		if len(urlList[1])>lastURL:
			for n in range(firstURL,lastURL):
				htmlURLS.append("""<tr><td><a href="%s">%s</a></td></tr>""" %(urlList[1][n],urlList[1][n]))
		else:
			for n in range(firstURL, len(urlList[1])):
				htmlURLS.append("""<tr><td><a href="%s">%s</a></td></tr>""" %(urlList[1][n],urlList[1][n]))
		htmlURLS.append('</table>')
		np = cp + 1
		pp = cp -1
		if cp > 1:
			htmlURLS.append("""<body><div id = "pre_result"><form action = '/prepage/""")
			htmlURLS.append(str(pp))
			htmlURLS.append("""' method = "POST">
										<input type = "submit" value = "previous page">
										</form></div></body>""")

		if len(urlList[1])>lastURL:
			htmlURLS.append("""<body><div id = "next_result"><form action = '/nextpage/""")
			htmlURLS.append(str(np))
			htmlURLS.append("""' method = "POST">
										<input type = "submit" value = "next page">
										</form></div></body>""")

	htmlURLS.append("<br><br>")
	htmlURLS.append("""<body><div id = "back"><form action = '/homePage' method= "post">
							<input type = "submit" value = "Go back to home page.">
							</form></div></body>""")



	###################################################################################################
	htmlURLS.append("</html>")
	return htmlURLS


@post('/prepage/<pp>')
def linkToPreviousPage(pp):
	global cp
	cp = cp - 1

	htmlURLS = []
	htmlURLS.append("""<html><style>
					html{
						background:
						url(http://funmozar.com/wp-content/uploads/2014/12/Animated-Christmas-Wallpaper-08.jpg) no-repeat center center fixed;
						background-size:cover;
					}
					#log{
						text-align: right;
						font-size: 100%;
						vertical-align: top
					}
					p.user{
						color: #669900;
						font-size: 80%;
						text-align: right;
						vertical-align: top
						font-family: "Georgia";
						font-style: oblique;
					}
					table {
					    width: 90%;
					    color:#0099FF;
					}
					th{
						height: 50px;
						text-align: left;
						font-family: "Georgia";
						font-style: oblique;
					}
					td{
						text-align: left;
						font-family: "Georgia";
						font-style: oblique;
					}
					a{
					    color: #FFAB00;
					}
					input[type=submit] {
						
					    padding:5px 15px; 
					    color:#f7dce4;
					    background:#669900;
					    border:0 none;
					    cursor:pointer;
					    font-weight:bold
					    -webkit-border-radius: 5px;
					    border-radius: 5px; 
					}
					#pre_result{
						text-align: center;
						font-size: 100%;
						vertical-align: middle
						padding: 5px;
						color:#f7dce4;
					    background:#669900;
					    border:0 none;
					    cursor:pointer;
					    font-weight:bold
					    -webkit-border-radius: 5px;
					    border-radius: 5px;
					    width: 50px;
 						height: 5px;
 						float:left
					}
					#next_result{
						text-align: center;
						font-size: 100%;
						vertical-align: middle
						padding: 5px;
						color:#f7dce4;
					    background:#669900;
					    border:0 none;
					    cursor:pointer;
					    font-weight:bold
					    -webkit-border-radius: 5px;
					    border-radius: 5px;
					    width: 50px;
 						height: 5px;
 						float:right
					}
					#back{
						color: #6170FF;
						text-align: left;
						font-size: 100%;
						vertical-align: middle
					}</style>""")

					
	firstURL = (cp-1)*5
	lastURL = cp*5
	htmlURLS.append("""<table id = 'URLs'>""")
	if len(urlList[1]) >=5:
		if len(urlList[1])>=lastURL:
			for n in range(firstURL,lastURL):
				htmlURLS.append("""<tr><td><a href="%s">%s</a></td></tr>""" %(urlList[1][n],urlList[1][n]))
		else:
			for n in range(firstURL, len(urlList[1])):
				htmlURLS.append("""<tr><td><a href="%s">%s</a></td></tr>""" %(urlList[1][n],urlList[1][n]))
		htmlURLS.append('</table>')
		pp = cp -1
		np = cp +1


		if cp > 1:
			htmlURLS.append("""<body><div id = "pre_result">
								<form action = '/prepage/""")
			htmlURLS.append(str(pp))
			htmlURLS.append("""' method = "POST" style="float:left;">
										<input type = "submit" value = "previous page">
										</form></div></body>""")

		if len(urlList[1])>=lastURL:
			htmlURLS.append("""<body><div id = "next_result">
								<form action = '/nextpage/""")
			htmlURLS.append(str(np))
			htmlURLS.append("""' method = "POST" style ="float:right;">
										<input type = "submit" value = "next page">
										</form></span></div></body>""")
	htmlURLS.append("<br><br>")

	htmlURLS.append("""<body><p><div id = "back"><form action = '/homePage' method= "post">
								<input type = "submit" value = "Go back to home page.">
								</form></div></p></body>""")
	htmlURLS.append("</html>")
	return htmlURLS

resultList = []

def PageIDInfo(queryList):
	if len(queryList) >0:
		searchWord = ''
		URLdic = {}	
		pageRankDic = {}

		for x in range (0, len(queryList)):
			searchWord = queryList[x].lower()

			tab_conn = lite.connect("table.db")
			cur = tab_conn.cursor()
			cur.execute('SELECT * FROM lexiconTable')
			#wordIDs gets all lexiconTable
			wordIDs = cur.fetchall()
			ran = len(wordIDs)
			coun = 0
			findword = 0
			word_ID = ""
			for coun in range (0, ran):
				if searchWord == wordIDs[coun][0]:
					word_ID = wordIDs[coun][1]
					findword = 1
					break
			if not findword:
				if len(queryList) == 1:
					relist = [3]
					return relist
				else:
					global resultList
					resultList.append(3)
			cur.execute('SELECT * FROM invertedTable')
			allURLs = cur.fetchall()
			coun1 = 0
			docIDList = []
			ran = len(allURLs)
			for coun1 in range (0, ran):
				if word_ID == allURLs[coun1][0]:
					docIDList.append(allURLs[coun1][1])
			cur.execute('SELECT * FROM pageRankScoreTable')
			allScoreTable = cur.fetchall()
			coun2 = 0
			pageRankList = []
			ran = len(allScoreTable)
			coun2 = 0
			for ID in docIDList:
				for coun2 in range (0, ran):
					if ID == allScoreTable[coun2][0]:
						if ID in pageRankDic:
							pageRankDic[ID] = pageRankDic[ID] + float(allScoreTable[coun2][1])
						else:
							pageRankDic[ID] = float(allScoreTable[coun2][1])

		# wordfound = 0
		# for resultFlag in resultList:
		# 	if resultFlag != 3:
		# 		wordfound = 1

		# if there is one word that is not in the database.
		if len(resultList) < len(queryList):
			for pageID, pagerank in pageRankDic.iteritems():
				templist = [pageID, pagerank]
				pageRankList.append(templist)
			pageRankList.sort(key = lambda x: x[1])
			pageRankList.reverse()


			cur.execute('SELECT * FROM docIDTable')
			alldocIDTable = cur.fetchall()
			coun3 = 0
			coun4 = 0
			ran = len(alldocIDTable)
			URLlinks = []
			numPage = len(pageRankList)
			cur.execute('SELECT * FROM textTable')
			summary = cur.fetchall()
			if numPage <= 5:
				for coun4 in range (0,numPage):
					for coun3 in range (0, ran):
						docid = int(pageRankList[coun4][0])
						if alldocIDTable[coun3][0] == docid:
							maxSum = 0
							text_Summary = ''
							for sumtext in summary:
								if docid == int(sumtext[0]):
									for te in sumtext[1]:
										if te.lower() == searchWord:
											if maxSum < len(sumtext[1]):
												maxSum = len(sumtext[1])
												text_Summary = sumtext[1]


							URLlinks.append(alldocIDTable[coun3][1])
				relist = [1, URLlinks]
				return relist
			else:
				for coun4 in range (0, numPage):
					for coun3 in range (0, ran):
						docid = int(pageRankList[coun4][0])
						if alldocIDTable[coun3][0] == docid:
							URLlinks.append(alldocIDTable[coun3][1])
				relist = [0, URLlinks]
				return relist
		else:
			relist = [3]
			return relist
			
	relist = ["empty"]
	return relist

run(host='0.0.0.0', port=8080, debug=True);
