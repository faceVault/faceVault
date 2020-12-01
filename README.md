# faceVault

∗ A description of the problem you are trying to solve.
  - In our project, we took a look at how we could make cloud based storage services a little bit more secure for the user. First, we created a sign up/login schema where instead of a password, the user was asked to upload a picture of themselves along with three security questions. Then, we created a web application that let users securely upload their documents into a database. It also let users see all their current files and either delete, download, or search through them.
∗ Any details regarding instructions for the user interface that is beyond the obvious.
  - One assumption we made is that users will upload photos that only have their face in it and not others. Besides that, all bases have been covered so that malicious users can't access our database, users can see ONLY their files, etc. 
  
∗ A list of Python libraries you are using.
  - We use the folllowing libraries
    - Flask
      runs our back end and front end
    - SQLITE3
      performs our database operations on the back end
    - base64
      encodes and decodes image blobs as they are inserted/retrieved from the database
    - PIL
      allowed us to test different forms of image
      representation outside of the blob
    - io
      allowed us to work with binary strings and bytes to properly display images
    - face_recognition
      allowed us to compare the faces submitted with the login form against the face stored in the database
    - bootstrap
      alllowed us to quickly apply css templates that worked with flask 
      
∗ A list of other resources.
∗ Descriptions of any extra features implemented (beyond the project proposal).
  - We implemented the following extra features.
    1. Search bar (allows user to search different files in home view)
    2. Delete account (allows user to delete account)
    3. Delete file (allows user to delete a specific file from the database)
    4. Download file (passes binary data from the database to the backend to the frontend in order to allow the user to download a file)
    5. Error page (alerts the user if there was an error during sign up/login and redirects them to the home page once they've read the message)
    6. Login checks (allows user to access the upload files, delete account, and home endpoints IF AND ONLY IF they are logged in. If they aren't it redirects them to the home page.)
    
∗ Include a description of the separation of work (who was responsible for what pieces
of the program).
  - Division of Labor
    - Although we all worked together on liveshare [collaborative programming software]. Our project was set up in the following manner
    1. Humbert
      - Created the database schema. Focused on the database operations and figuring out how to store files in the database. 
    2. Sarah
      - Focused on the html and css parts of the project. Implemented bootstrap and other css to make our page look professional. 
    3. Seth
      - Was in charge of setting up the frontend at first and then transitioned into figuriing out how to get the facial recognition to work. At first, we were doing live video but we later transitioned 
      to still pictures.
    4. Orlando
      - Worked as a full stack developer on this project. Oversaw everything and worked with every team member to ensure the flow of data was secure, efficient, and functional. Additionally worked on the image storage data structure issue along with Seth. They would later find out how to use blobs. 
