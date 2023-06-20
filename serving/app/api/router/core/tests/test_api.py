# import time

# from main import app

# def test_answer():
#     import json
#     with open("tests/src/test_input.json", 'r') as f:
#         json_data = json.load(f)
#     test_app = app.test_client()
#     start_time = time.time()
#     response = test_app.post("/answer", data=json.dumps(json_data), content_type="application/json")
#     end_time = time.time()
#     elapsed_time = end_time - start_time
#     print("POST ANSWER TIME: {:.2f} seconds".format(elapsed_time))
#     print(response)
#     print(response.get_json())
#     assert response.status_code == 200
#     json = json.loads(response.data)
#     assert "audio_url" in json
#     assert "messages" in json
#     assert json["messages"][-1]["role"]=="assistant"
