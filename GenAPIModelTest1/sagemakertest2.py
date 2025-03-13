
from roboflow import Roboflow
import glob
import os
from huggingface_hub import login
from IPython.display import Image, display
import torch
from diffusers import StableDiffusionPipeline

hftoken = "xxx"
login(token=hftoken)
model_name= "stable-diffusion-v1-5/stable-diffusion-v1-5"

pipeline = StableDiffusionPipeline.from_pretrained(
    model_name, torch_dtype = torch.float32, access_token = hftoken 
    )

device = "cuda" if torch.cuda.is_available() else "cpu"

pipeline = pipeline.to(device)

def generate_images(
    prompt,
    num_images_to_generate,
    num_images_per_prompt=4,
    guidance_scale=8,
    output_dir="generated_images",
    display_images=False,
):

    num_iterations = num_images_to_generate // num_images_per_prompt
    os.makedirs(output_dir, exist_ok=True)

    for i in range(num_iterations):
        images = pipeline(
            prompt, num_images_per_prompt=num_images_per_prompt, guidance_scale=guidance_scale
        )
        for idx, image in enumerate(images.images):
            image_name = f"{output_dir}/image_{(i*num_images_per_prompt)+idx}.png"
            image.save(image_name)
            if display_images:
                display(Image(filename=image_name, width=128, height=128))




generate_images("aerial view of cattle", 12, guidance_scale=4, display_images=True)





HOME = os.path.expanduser("~")
# glob params
image_dir = os.path.join(HOME, "generated_images", "")
file_extension_type = ".png"

# roboflow pip params
rf = Roboflow(api_key="xxxx")

workspaceId = 'xxx'
projectId = 'xxxx'
rf_upload_project = rf.workspace(workspaceId).project(projectId)

# glob images
image_glob = glob.glob(image_dir + '/*' + file_extension_type)

# perform upload
for image in image_glob:
    rf_upload_project.upload(image, num_retry_uploads=3)
    print("*** Processing image [" + str(len(image_glob)) + "] - " + image + " ***")