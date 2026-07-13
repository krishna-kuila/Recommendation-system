
`python -m venv .venv`

`.venv\Scripts\activate`

`pip install -r requirements.txt`


## Problems faces

### Granulartiy mismatch problem
one user may have many comments/similar comments , for recommendation same user occur many times as generate embedding have the same context.



## step to run Frontend -- Changes done by Arpon Kola
## step - 1:
    import the necessary library(flask, scrapfly-sdk) using requirements.txt
## step - 2:
    open cmd and cd(change directory) to frontend
## step - 3:
    type command : "python -m flask --app app.py run --debug"
    it will start a development server on ip address localhost/127.0.0.1 with port number 5000
    address : http://127.0.0.1:5000
## step - 4:
    to see the website copy the address and paste it on url of chrome browser and press enter