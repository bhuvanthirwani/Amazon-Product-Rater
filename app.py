import flask
from flask import jsonify
from scraping import Estimate
from no_of_reviews import info
from imagescraping import extract
from namescraping import extractname
app = flask.Flask(__name__, template_folder='templates')
@app.route('/',methods=['GET', 'POST'])
def hello():
    if flask.request.method == 'GET':
        return(flask.render_template('index.html'))
    
linkk=""


@app.route('/process', methods=['GET', 'POST'])
def process():
    global linkk
    #print("BYEBYE")
    name = flask.request.form['name']
    if name :
        url=extract(name)
        #print(url)
        productTitle=extractname(name)
        #print(productTitle)
        dpstring=name
        s=dpstring.find('gp/product')
        if(s>-1):
            name=dpstring[:s]+"dp"+dpstring[s+10:]
        #print("Hello")
        #print(name)
        linkk=name
        total_reviews=info(name)
        #print("BHU",total_reviews)

        return jsonify({'name' : total_reviews,'imgurl':url,'productTitle':productTitle})


    return jsonify({'error' : 'Missing data!'})

@app.route('/final', methods=['GET', 'POST'])
def final():
    global linkk
    #print("final-->",linkk)
    R = flask.request.form['name']
    R=int(R)
    if(R%10==0):
      x=R//10
    else:
      x=R//10 + 1
    if R:
        rating = Estimate(linkk,x)
        #print("rating",rating)
        return  jsonify({'name' : rating, 'R':R , 'X':x})
    return jsonify({'error' : 'Missing data!'})


if __name__ == '__main__':
    app.run()