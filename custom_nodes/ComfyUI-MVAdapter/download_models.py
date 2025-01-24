from diffusers import StableDiffusionXLPipeline
from huggingface_hub import snapshot_download

def download_required_models():
    # Download SDXL base model
    StableDiffusionXLPipeline.from_pretrained("stabilityai/stable-diffusion-xl-base-1.0")
    
    # Download VAE fix
    snapshot_download("madebyollin/sdxl-vae-fp16-fix")

if __name__ == "__main__":
    download_required_models() 