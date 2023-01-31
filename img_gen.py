from diffusers import StableDiffusionPipeline, EulerDiscreteScheduler
import torch

def generateImage(prompt):
    model_id = "stabilityai/stable-diffusion-2-1-base"

    scheduler = EulerDiscreteScheduler.from_pretrained(model_id, subfolder="scheduler")
    pipe = StableDiffusionPipeline.from_pretrained(model_id, scheduler=scheduler, revision="fp16", torch_dtype=torch.float16)
    pipe = pipe.to("cuda")

    image = pipe(prompt).images[0]  
        
    image.save(f"{prompt}.png")
    
    print(f"{prompt}.png generated!")