from flask import Flask, render_template, jsonify, request
from Backend import extract_x_profile_data

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
	return render_template('index.html')

@app.route('/user', methods=['GET', 'POST'])
def get_user():
	if request.method == 'POST':
		query = request.get_json()
		user = extract_x_profile_data(query) #comment out this link for actual api call
		# user = {
		# 	"name" : "arpon kola",
		# 	"handle" : "@arpon",
		# 	"bio" : "SaaS. Depression. Growth. ⚡ Founder with Depression 🖤 SaaS | Healing | Building 🚀 Depressed but Building 💻 SaaS Over Sadness ⚡ Code. Build. Heal",
		# 	"location" : "howrah"
		# } #for demo purpose comment this out
		if not user:
			return jsonify({
				"Message" : "User Not Found"
			})
		n_user = {
			"name" : user.get("name", None),
			"handle" : user.get("handle", None),
			"bio" : user.get("bio", None),
			"location" : user.get("location", None),
			"comments" : user.get("comments", None)
		}

	return jsonify({
			"users" : [{
					"name" : "user_1",
					"handle" : "@user1",
					"score" : "93%"
				}, {
					"name" : "user_2",
					"handle" : "@user2",
     				"score" : "93%"
				}, {
					"name" : "user_3",
					"handle" : "@user3",
					"score" : "93%"
				}, {
					"name" : "user_4",
					"handle" : "@user4",
					"score" : "93%"
				}, {
					"name" : "user_5",
					"handle" : "@user5",
					"score" : "93%"
				}, {
					"name" : "user_6",
					"handle" : "@user6",
					"score" : "93%"
				}, {
					"name" : "user_7",
					"handle" : "@user7",
					"score" : "93%"
				}
			],
			"user" : n_user
		}
	), 200

@app.route('/new-user', methods=['GET', 'POST'])
def get_new_user():
    if request.method == 'POST':
        new_user_details = request.get_json()
        print(new_user_details)
    return jsonify({
		"users" : [{
				"name" : "user_1",
				"handle" : "@user1",
				"score" : "93%"
			}, {
				"name" : "user_2",
				"handle" : "@user2",
				"score" : "93%"
			}, {
				"name" : "user_3",
				"handle" : "@user3",
				"score" : "93%"
			}, {
				"name" : "user_4",
				"handle" : "@user4",
				"score" : "93%"
			}, {
				"name" : "user_5",
				"handle" : "@user5",
				"score" : "93%"
			}, {
				"name" : "user_6",
				"handle" : "@user6",
				"score" : "93%"
			}, {
				"name" : "user_7",
				"handle" : "@user7",
				"score" : "93%"
			}
		]
	})

if __name__ == "__main__":
	app.run(debug=True)