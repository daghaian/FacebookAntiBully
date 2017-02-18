from flask import Flask, request
import requests
import json
import pyquery
from bs4 import BeautifulSoup
import re
app = Flask(__name__)
 
#App Name: Facebook AntiBully Filter
#Creators: David Aghaian, Diego Perilla, Chris Whiting
#Purpose: The purpose of this application is to work in conjunction with a user's facebook profile in order to prevent common occurences of cyber bullying. By removing a potential bully's comments from the victim's post, we are effectively removing a bully's motivation
#to continue the attacking the individual. 
#Creation Date: 2/11/2017 Hackpoly 2017


ACCESS_TOKEN = ENTER_ACCESS_TOKEN_HERE


def checkFeed():

	blacklistedWords = ["fuck","shit","balls","screw you","asshole","useless"]
	
	r = requests.Session()
	response = r.get('https://graph.facebook.com/v2.8/me?access_token=' + ACCESS_TOKEN + '&debug=all&fields=id%2Cfeed%7Bcreated_time%2Ccomments%2Cmessage%7D&format=json&method=get&pretty=0&suppress_http_code=1')
	jsonData = json.loads(response.content)
	for event in jsonData['feed']['data']:
		if "message" in event:
			if any(ext in event['message'] for ext in blacklistedWords):
				print("Instances of cyber bullying detected...")
				deletePost(event['id'].split('_')[1])
			if "comments" in event:
				for commentEvent in event['comments']['data']:
					 if any(ext in commentEvent['message'] for ext in blacklistedWords):
					 	print("Instances of cyber bullying detected...")
						deleteComment(commentEvent['id'])
						#print("COMMENT: " + str(commentEvent['message']) + " ID: " + str(commentEvent['id'].split('_')[1]))
@app.route('/', methods=['POST'])
def handle_incoming_messages():
    data = request.json
    print("User's feed has been updated.Proceeding to check for occurences of cyber-bullying...")
    checkFeed()
    return "ok"
 
@app.route('/', methods=['GET'])
def handle_verification():
    return request.args['hub.challenge']


def deletePost(postID,email=USER_EMAIL, password=USER_PASSWORD):
    
    '''
    Attempt to login to Facebook. Returns user ID, xs token and
    fb_dtsg token. All 3 are required to make requests to
    Facebook endpoints as a logged in user. Returns False if
    login failed.
    '''


    print("Recieved Delete Request for Post ID: " + str(postID))
    session = requests.session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (X11; Linux i686; rv:39.0) Gecko/20100101 Firefox/39.0'
    })


    # Navigate to Facebook's homepage to load Facebook's cookies.
    response = session.get('https://m.facebook.com')  
    # Attempt to login to Facebook
    print("Loggin in")
    response = session.post('https://m.facebook.com/login.php', data={
        'email': email,
        'pass': password
    }, allow_redirects=False)

  
    # If c_user cookie is present, login was successful
    if 'c_user' in response.cookies:
	print("Logged in successfully")
        # Make a request to homepage to get fb_dtsg token
        homepage_resp = session.get('https://m.facebook.com/home.php')
        
        dom = pyquery.PyQuery(homepage_resp.text.encode('utf8'))
        fb_dtsg = dom('input[name="fb_dtsg"]').val()

        response = session.get('https://www.facebook.com/dmperilla')
        soup = BeautifulSoup(response.content,"html.parser")


        identifier = str(soup.find('meta',{'property':'al:android:url'}).get('content'))
        identifier = "S:_I" + identifier[identifier.rindex("/")+1:] + ":" + postID
        tlUnit = 'tl_unit_-4076986901698239602'
	#print(identifier)
        # pattern = re.compile('(data-dedup=\"\S+\")')
        # identifier = "S" + re.search(pattern,searchString).group(0).split(":")[1]
        #print(identifier)

        payload = {
        
        'fb_dtsg':fb_dtsg  
        #'ttstamp':'265817255685695101761051077258658169117691091098953884585'
        }

        response = session.post('https://www.facebook.com/ajax/timeline/delete?identifier=' + identifier + '&location=9&story_dom_id=' + tlUnit + '&render_location=10&is_notification_preview=0&dpr=2',data=payload)
        #print(response)


def deleteComment(post,email='itz_bigz_d@yahoo.com', password='JUmF77g2FFsK5ixLv'):
    
    '''
    Attempt to login to Facebook. Returns user ID, xs token and
    fb_dtsg token. All 3 are required to make requests to
    Facebook endpoints as a logged in user. Returns False if
    login failed.
    '''


    print("Recieved Delete Request for Post ID: " + str(post))
    session = requests.session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (X11; Linux i686; rv:39.0) Gecko/20100101 Firefox/39.0'
    })


    # Navigate to Facebook's homepage to load Facebook's cookies.
    response = session.get('https://m.facebook.com')  
    # Attempt to login to Facebook
    print("Loggin in")
    response = session.post('https://m.facebook.com/login.php', data={
        'email': email,
        'pass': password
    }, allow_redirects=False)

  
    # If c_user cookie is present, login was successful
    if 'c_user' in response.cookies:
	print("Logged in successfully")
        # Make a request to homepage to get fb_dtsg token
        homepage_resp = session.get('https://m.facebook.com/home.php')
        
        dom = pyquery.PyQuery(homepage_resp.text.encode('utf8'))
        fb_dtsg = dom('input[name="fb_dtsg"]').val()

        response = session.get('https://www.facebook.com/dmperilla')
      
        soup = BeautifulSoup(response.content,"html.parser")


        identifier = str(soup.find('meta',{'property':'al:android:url'}).get('content'))
        identifier = identifier[identifier.rindex("/")+1:]
        print(identifier)

        tlUnit = 'tl_unit_-4076986901698239602'
	
        # pattern = re.compile('(data-dedup=\"\S+\")')
        # identifier = "S" + re.search(pattern,searchString).group(0).split(":")[1]
        	

        payload = {
        
        'fb_dtsg':fb_dtsg,
        'comment_id':post,
        'ft_ent_identifier':post.split('_')[0],
        'client_id':'1486930684617:478409924',
        'one-click':'false',
        'av':identifier,
        '_a':'1',
        'comment_legacyid':post.split('_')[1]
        #'ttstamp':'265817255685695101761051077258658169117691091098953884585'
        }


	
        response = session.post('https://www.facebook.com/ufi/delete/comment/?dpr=2',data=payload)
        #print(response.url)
	#print(response)



 
if __name__ == '__main__':
    app.run(debug=True)
