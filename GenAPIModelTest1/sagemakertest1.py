from sagemaker.jumpstart.model import JumpStartModel

os.environ["AWS_ACCESS_KEY_ID"] = "your_access_key_id"
os.environ["AWS_SECRET_ACCESS_KEY"] = "your_secret_access_key"
os.environ["AWS_DEFAULT_REGION"] = "NAM"

model_id =     "meta-textgeneration-llama-2-7b"
model_version =   "2.*"
model = JumpStartModel(model_id=model_id, model_version=model_version)
predictor = model.deploy(initial_instance_count=1, instance_type="ml.m5.xlarge")

def print_response(payload, response):
    print(payload["inputs"])
    print(f"> {response[0]['generation']}")
    print("\n==================================\n")




payload = {
    "inputs": "How to use sagemaker APIs",
    "parameters": {
        "max_new_tokens": 64,
        "top_p": 0.9,
        "temperature": 0.6,
        "return_full_text": False,
    },
}
try:
    response = predictor.predict(payload, custom_attributes="accept_eula=false")
    print_response(payload, response)
except Exception as e:
    print(e)

