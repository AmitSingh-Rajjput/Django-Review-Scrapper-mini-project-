from django.shortcuts import render
from bs4 import BeautifulSoup as bs
import requests
from urllib.request import urlopen as uReq


def home(request):
          return render(request,'ReviewScrapper/home.html')
def about(request):
    return render(request,'ReviewScrapper/about.html')

def scrap(request):

    print("request",request)
    searchString=request.GET.get('Search')
    print("searchString", searchString)
    #searchString = request.GET.get('Search')
    #searchString = searchString.replace(" ", "")  # obtaining the search string entered in the form
    try:
        flipkart_url = "https://www.flipkart.com/search?q=" + searchString  # preparing the URL to search the product on flipkart
        print('flipkart_url1', flipkart_url)
        uClient = uReq(flipkart_url)  # requesting the webpage from the internet
        flipkartPage = uClient.read()  # reading the webpage
        uClient.close()  # closing the connection to the web server
        flipkart_html = bs(flipkartPage, "html.parser")  # parsing the webpage as HTML
        print('flipkart_url', flipkart_url)
        bigboxes = flipkart_html.findAll("div", {
            "class": "bhgxx2 col-12-12"})  # seacrhing for appropriate tag to redirect to the product link
        #print('flipkart_url2', bigboxes)
        del bigboxes[0:3]  # the first 3 members of the list do not contain relevant information, hence deleting them.
        box = bigboxes[0]  # taking the first iteration (for demo)

        productLink = "https://www.flipkart.com" + box.div.div.div.a['href']  # extracting the actual product link
        print('flipkart_url2',productLink )
        prodRes = requests.get(productLink)  # getting the product page from server
        prod_html = bs(prodRes.text, "html.parser")  # parsing the product page as HTML
        commentboxes = prod_html.findAll('div', {'class': "_3nrCtb"})  # finding the HTML section containing the customer comme
        reviews = []  # initializing an empty list for reviews
        for commentbox in commentboxes:
            try:
                name = commentbox.find('p', attrs={'class': '_3LYOAd _3sxSiS'}).text
                print("name",name)
            except:
                name = 'No Name'
            try:
                rating = commentbox.div.div.div.div.text
            except:
                rating = 'No Rating'
            try:
                commentHead = commentbox.div.div.div.p.text
            except:
                commentHead = 'No Comment Heading'
            try:
                comtag = commentbox.div.div.find_all('div', {'class': ''})
                custComment = comtag[0].div.text
            except:
                custComment = 'No Customer Comment'
            mydict = {"Product": searchString, "Name": name, "Rating": rating, "CommentHead": commentHead,
                      "Comment": custComment}  # saving that detail to a dictionary


            reviews.append(mydict)  # appending the comments to the review list
        return render(request, 'ReviewScrapper/results.html', {'reviews': reviews}) # showing the review to the user
    except:
        return 'Something is wrong'
    # reviews = []
    # mydict={"Product": "searchString", "Name": "name", "Rating": 'rating', "CommentHead": 'commentHead',
    #                   "Comment": 'custComment'}
    # reviews.append(mydict)
    # return render(request, 'ReviewScrapper/results.html', {'reviews': reviews})
