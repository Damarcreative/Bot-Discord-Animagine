import os
import random
import re
import discord
from discord.ext import commands
from discord import app_commands
from diffusers import StableDiffusionXLPipeline, AutoencoderKL
import torch
from PIL import Image

# Load the model and VAE
model_id = "cagliostrolab/animagine-xl-3.1"
vae = AutoencoderKL.from_pretrained("madebyollin/sdxl-vae-fp16-fix", torch_dtype=torch.float16)
pipe = StableDiffusionXLPipeline.from_pretrained(model_id, torch_dtype=torch.float16, vae=vae)
pipe.to("cuda")

# Default values
default_height = 1152
default_width = 896
default_num_inference_steps = 28
default_guidance_scale = 7.5
default_negprompt = "nsfw, lowres, bad anatomy, bad hands, text, error, missing fingers, extra digit, fewer digits, cropped, worst quality, low quality, normal quality, jpeg artifacts, signature, watermark, username, blurry, artist name"

aspect_ratios = {
    "1:1": (1024, 1024),
    "2:3": (896, 1152),
    "3:2": (1152, 896),
    "3:4": (832, 1216),
    "4:3": (1216, 832),
    "16:9": (1536, 864),
    "9:16": (864, 1536)
}

def parse_prompt(prompt):
    # Extract custom parameters from the prompt
    pattern = r'--(\w+) ([\w:]+)'
    matches = re.findall(pattern, prompt)

    # Remove parameters from the prompt
    clean_prompt = re.sub(pattern, '', prompt).strip()

    # Default values
    params = {
        'w': default_width,
        'h': default_height,
        'cfg': default_guidance_scale,
        'nis': default_num_inference_steps,
        'negpromot': default_negprompt
    }

    # Update parameters with user-specified values
    errors = []
    for match in matches:
        key, value = match[0], match[1]
        if key == 'ar':
            if value in aspect_ratios:
                params['w'], params['h'] = aspect_ratios[value]
            else:
                errors.append(f"Invalid aspect ratio: {value}")
        elif key == 'cfg':
            try:
                params['cfg'] = float(value)
            except ValueError:
                errors.append(f"Invalid guidance scale: {value}")
        elif key == 'step':
            try:
                params['nis'] = int(value)
            except ValueError:
                errors.append(f"Invalid number of inference steps: {value}")
        elif key == 'no':
            params['negpromot'] = '' if value == '.' else value
        else:
            errors.append(f"Unknown parameter: {key}")

    return clean_prompt, params, errors

def generate_images(prompt):
    clean_prompt, params, errors = parse_prompt(prompt)
    if errors:
        raise ValueError("\n".join(errors))
    
    images = []
    for _ in range(2):
        seed = random.randint(0, 2**32 - 1)
        generator = torch.manual_seed(seed)
        image = pipe(
            clean_prompt,
            negative_prompt=params['negpromot'],
            height=params['h'],
            width=params['w'],
            num_inference_steps=params['nis'],
            guidance_scale=params['cfg'],
            generator=generator
        ).images[0]
        images.append(image)
    return images

# Discord bot setup
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'Bot {bot.user.name} telah terhubung')
    try:
        synced = await bot.tree.sync()
        print(f'Synced {len(synced)} command(s)')
    except Exception as e:
        print(f'Error syncing commands: {e}')

@bot.tree.command(name="imagine", description="Generate two images from a prompt")
async def imagine(interaction: discord.Interaction, prompt: str):
    await interaction.response.defer()
    try:
        images = generate_images(prompt)
        image_paths = []
        for i, image in enumerate(images):
            path = f"output_{i}.png"
            image.save(path)
            image_paths.append(path)
        files = [discord.File(path) for path in image_paths]
        caption = f"```{prompt}```\n{interaction.user.mention}"
        await interaction.followup.send(content=caption, files=files)
    except ValueError as e:
        await interaction.followup.send(content=f"Error: {str(e)}")

@bot.tree.command(name="help", description="Show help for using the bot")
async def help_command(interaction: discord.Interaction):
    help_text = (
        "How to use the bot:\n"
        "/imagine {prompt} --no {negative prompt} --cfg {guidance scale} --step {num inference steps} --ar {aspect ratio}\n\n"
        "**Available parameters:**\n"
        " - `--no`: Set negative prompt. Example: `--no .` to disable negative prompt. Default: nsfw, lowres, bad anatomy, bad hands, text, error, missing fingers, extra digit, fewer digits, cropped, worst quality, low quality, normal quality, jpeg artifacts, signature, watermark, username, blurry, artist name.\n"
        " - `--cfg`: Set guidance scale. Default: 7.5\n"
        " - `--step`: Set number of inference steps. Default: 28\n"
        " - `--ar`: Set aspect ratio. Example: `--ar 1:1`. Default: 896 x 1152\n\n"
        "**Supported Aspect Ratios:**\n"
        " - 1:1: 1024 x 1024\n"
        " - 2:3: 896 x 1152\n"
        " - 3:2: 1152 x 896\n"
        " - 3:4: 832 x 1216\n"
        " - 4:3: 1216 x 832\n"
        " - 16:9: 1536 x 864\n"
        " - 9:16: 864 x 1536\n"
    )
    await interaction.response.send_message(help_text)

# Function to run Discord bot
bot.run(os.getenv("ANI_TOKEN"))  # Replace with your bot token
