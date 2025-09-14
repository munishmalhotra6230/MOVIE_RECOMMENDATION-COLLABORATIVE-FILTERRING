from flask import Flask,render_template,request
import os 
import pickle
import pandas as pd
import numpy as np
file_path = os.path.join(os.path.dirname(__file__), "popular_books.pkl")
file_path_book = os.path.join(os.path.dirname(__file__), "books.pkl")
file_path_sim = os.path.join(os.path.dirname(__file__), "similarty.pkl")
file_path_pt = os.path.join(os.path.dirname(__file__), "pt.pkl")
popular_df=pickle.load(open(file_path,"rb"))
books=pickle.load(open(file_path_book,"rb"))
similarty=pickle.load(open(file_path_sim,"rb")) 
pt=pickle.load(open(file_path_pt,"rb"))
app=Flask(__name__)
@app.route('/')
def Home_page():
    return render_template('index.html',book_name=list(popular_df['Book-Title'].values),author=list(popular_df["Book-Author"].values),image=list(popular_df["Image-URL-M"].values), voting=list(popular_df["num_rating"].values),rating=list(popular_df["avg_rating"].values))
@ app.route('/recommend')
def recommend():
    return render_template('recommend.html')
@ app.route('/recommend_books',methods=['post'])
def reccomend_books():
    book_name=request.form.get('User_input')
    index=np.where(pt.index==book_name)[0][0]
    similarty_items=sorted(list(enumerate(similarty[index])),key=lambda x:x[1],reverse=True)[1:9]
    data=[]
    for i in similarty_items:
        item=[]
        temp_df=books[books["Book-Title"]==pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates("Book-Title")["Book-Title"].values))
        item.extend(list(temp_df.drop_duplicates("Book-Title")["Book-Author"].values))
        item.extend(list(temp_df.drop_duplicates("Book-Title")["Image-URL-M"].values))
        data.append(item)
      
    return render_template('recommend.html',data=data)
@ app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)
