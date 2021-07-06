# offlang-app  
link for website - https://off-lang-2.herokuapp.com/home   

in this project we use a supervised algorithims, we use Random Forest (RF) for Hebrew language and Support Vector Machine (SVM) for Arabic language.  

The offlang-app provides the end user four options:   
1- Choose a language. The end user can specify the language of her input. The best models for each language are uploaded to the server and responsible for classification of texts2.   
2- Classify one piece of text. The text needs to be copied to the text field and submitted to the back-end server. Its classification label is displayed to the user on the front-end page.   
3- Classify a Twitter account. A Twitter username should be submitted to the system. offlang-app provides the end user with a label derived from a sample of comments representing the input profile. The server, using Twitter API, collects the last 50 comments from the specifies account and submits them as input to the classification model. The output, which is displayed to the user, contains percentage of comments that were recognized as offensive.    
4- Analyse a dataset, which can be uploaded to our server from the frontend page. Each text in the dataset gets an automatic label based on the classification model. Then the percentage of comments that were recognized as offensive are displayed to the user. Also, the entire dataset with labels can be downloaded to the local file system.   


