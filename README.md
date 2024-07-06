# Bot Discord AnimagineXL

This Discord bot generates images from text prompts using the `StableDiffusionXLPipeline` model from `diffusers`. Users can customize various parameters to fine-tune the generated images.

## Features

- Generate two images from a text prompt
- Customize guidance scale, number of inference steps, and aspect ratio
- Option to specify a negative prompt
- Error handling for incorrect parameters

## Setup

### Prerequisites

- Python 3.8 or higher
- Discord bot token
- Required Python packages (`diffusers`, `torch`, `discord.py`, `PIL`)

### Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/Damarcreative/Bot-Discord-Animagine.git
    cd Bot-Discord-Animagine
    ```

2. Create a virtual environment and activate it:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

4. Set up your Discord bot token as an environment variable:
    ```sh
    export ANI_TOKEN=your_discord_bot_token  # On Windows, use `set ANI_TOKEN=your_discord_bot_token`
    ```

### Running the Bot

To start the bot, run:
```sh
python bot.py
```

## Usage

### Commands

#### `/imagine {prompt}`

Generate two images based on the provided prompt.

- **Parameters:**
  - `--no {negative prompt}`: Set the negative prompt. Example: `--no .` to disable the negative prompt. Default: "nsfw, lowres, bad anatomy, bad hands, text, error, missing fingers, extra digit, fewer digits, cropped, worst quality, low quality, normal quality, jpeg artifacts, signature, watermark, username, blurry, artist name."
  - `--cfg {guidance scale}`: Set the guidance scale. Default: 7.5.
  - `--step {num inference steps}`: Set the number of inference steps. Default: 28.
  - `--ar {aspect ratio}`: Set the aspect ratio. Example: `--ar 1:1`. Default: 896 x 1152.

- **Supported Aspect Ratios:**
  - 1:1: 1024 x 1024
  - 2:3: 896 x 1152
  - 3:2: 1152 x 896
  - 3:4: 832 x 1216
  - 4:3: 1216 x 832
  - 16:9: 1536 x 864
  - 9:16: 864 x 1536

Example usage:
```
/imagine A beautiful sunset over the mountains --cfg 8.0 --step 30 --ar 16:9
```

#### `/help`

Show the help message with details on how to use the bot and the available parameters.

## Error Handling

The bot will notify users if there are errors in the parameters or values provided in the prompt. Ensure that all parameters are used correctly according to the documentation.

## Contributing

Contributions are welcome! Please submit a pull request or open an issue to discuss any changes.

## License

This project is licensed under the MIT License. See the LICENSE file for details
