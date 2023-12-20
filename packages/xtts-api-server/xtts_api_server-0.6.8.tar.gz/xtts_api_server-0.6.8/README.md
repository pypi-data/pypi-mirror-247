# A simple FastAPI Server to run XTTSv2

This project is inspired by [silero-api-server](https://github.com/ouoertheo/silero-api-server) and utilizes [XTTSv2](https://github.com/coqui-ai/TTS).

This server was created for [SillyTavern](https://github.com/SillyTavern/SillyTavern) but you can use it for your needs

Feel free to make PRs or use the code for your own needs

There's a [google collab version](https://colab.research.google.com/drive/1b-X3q5miwYLVMuiH_T73odMO8cbtICEY?usp=sharing) you can use it if your computer is weak.

If you want to get a high-quality voice clone, I advise you to use [webui for fine-tuning xtts](https://github.com/daswer123/xtts-webui)

If you are looking for an option for normal XTTS use look here [https://github.com/daswer123/xtts-webui](https://github.com/daswer123/xtts-webui)

## Changelog

You can keep track of all changes on the [release page](https://github.com/daswer123/xtts-api-server/releases)

## Installation

Simple installation :

```bash
pip install xtts-api-server
```

This will install all the necessary dependencies, including a **CPU support only** version of PyTorch

I recommend that you install the **GPU version** to improve processing speed ( up to 3 times faster )

Installation into virtual environment on **Windows** with **GPU support**:

```bash
python -m venv venv
venv\Scripts\activate
pip install xtts-api-server
pip install torch==2.1.1+cu118 torchaudio==2.1.1+cu118 --index-url https://download.pytorch.org/whl/cu118
```

## Starting Server

`python -m xtts_api_server` will run on default ip and port (localhost:8020)

```
usage: xtts_api_server [-h] [-hs HOST] [-p PORT] [-sf SPEAKER_FOLDER] [-o OUTPUT] [-t TUNNEL_URL] [-ms MODEL_SOURCE] [--lowvram] [--deepspeed] [--streaming-mode] [--stream-play-sync]

Run XTTSv2 within a FastAPI application

options:
  -h, --help show this help message and exit
  -hs HOST, --host HOST
  -p PORT, --port PORT
  -d DEVICE, --device DEVICE `cpu` or `cuda`, you can specify which video card to use, for example, `cuda:0`
  -sf SPEAKER_FOLDER, --speaker_folder The folder where you get the samples for tts
  -o OUTPUT, --output Output folder
  -t TUNNEL_URL, --tunnel URL of tunnel used (e.g: ngrok, localtunnel)
  -ms MODEL_SOURCE, --model-source ["api","apiManual","local"]
  -v MODEL_VERSION, --version You can choose any version of the model, keep in mind that if you choose model-source api, only the latest version will be loaded
  --lowvram The mode in which the model will be stored in RAM and when the processing will move to VRAM, the difference in speed is small
  --deepspeed allows you to speed up processing by several times, automatically downloads the necessary libraries
  --streaming-mode Enables streaming mode, currently has certain limitations, as described below.
  --streaming-mode-improve Enables streaming mode, includes an improved streaming mode that consumes 2gb more VRAM and uses a better tokenizer and more context.
  --stream-play-sync Additional flag for streaming mod that allows you to play all audio one at a time without interruption
```

If you want your host to listen, use -hs 0.0.0.0

The -t or --tunnel flag is needed so that when you get speakers via get you get the correct link to hear the preview. More info [here](https://imgur.com/a/MvpFT59)

Model-source defines in which format you want to use xtts:

1. `local` - loads version 2.0.2 by default, but you can specify the version via the -v flag, model saves into the models folder and uses `XttsConfig` and `inference`.
2. `apiManual` - loads version 2.0.2 by default, but you can specify the version via the -v flag, model saves into the models folder and uses the `tts_to_file` function from the TTS api
3. `api` - will load the latest version of the model. The -v flag won't work.

All versions of the XTTSv2 model can be found [here](https://huggingface.co/coqui/XTTS-v2/tree/v2.0.2) in the branches

The first time you run or generate, you may need to confirm that you agree to use XTTS.

# About Streaming mode

Streaming mode allows you to get audio and play it back almost immediately. However, it has a number of limitations.

You can see how this mode works [here](https://www.youtube.com/watch?v=jHylNGQDDA0) and [here](https://www.youtube.com/watch?v=6vhrxuWcV3U)

Now, about the limitations

1. Can only be used on a local computer
2. Playing audio from the your pc
3. Does not work endpoint `tts_to_file` only `tts_to_audio` and it returns 1 second of silence.

You can specify the version of the XTTS model by using the `-v` flag.

Improved streaming mode is suitable for complex languages such as Chinese, Japanese, Hindi or if you want the language engine to take more information into account when processing speech.

`--stream-play-sync` flag - Allows you to play all messages in queue order, useful if you use group chats. In SillyTavern you need to turn off streaming to work correctly

# API Docs

API Docs can be accessed from [http://localhost:8020/docs](http://localhost:8020/docs)

# Voice Samples

You can find the sample in this repository more details in the API documentation

[erew123](https://github.com/erew123) put together a pack of 40+ votes, you can download to try them out [here](https://filebin.net/t97nd69ac7qm2rsf)

# Selecting Folder

You can change the folders for speakers and the folder for output via the API.

# Get Speakers

Once you have at least one file in your speakers folder, you can get its name via API and then you only need to specify the file name.

# Note on creating samples for quality voice cloning

The following post is a quote by user [Material1276 from reddit](https://www.reddit.com/r/Oobabooga/comments/1807tsl/comment/ka5l8w9/?share_id=_5hh4KJTXrEOSP0hR0hCK&utm_content=2&utm_medium=android_app&utm_name=androidcss&utm_source=share&utm_term=1)

> Some suggestions on making good samples
>
> Keep them about 7-9 seconds long. Longer isn't necessarily better.
>
> Make sure the audio is down sampled to a Mono, 22050Hz 16 Bit wav file. You will slow down processing by a large % and it seems cause poor quality results otherwise (based on a few tests). 24000Hz is the quality it outputs at anyway!
>
> Using the latest version of Audacity, select your clip and Tracks > Resample to 22050Hz, then Tracks > Mix > Stereo to Mono. and then File > Export Audio, saving it as a WAV of 22050Hz
>
> If you need to do any audio cleaning, do it before you compress it down to the above settings (Mono, 22050Hz, 16 Bit).
>
> Ensure the clip you use doesn't have background noises or music on e.g. lots of movies have quiet music when many of the actors are talking. Bad quality audio will have hiss that needs clearing up. The AI will pick this up, even if we don't, and to some degree, use it in the simulated voice to some extent, so clean audio is key!
>
> Try make your clip one of nice flowing speech, like the included example files. No big pauses, gaps or other sounds. Preferably one that the person you are trying to copy will show a little vocal range. Example files are in [here](https://github.com/oobabooga/text-generation-webui/tree/main/extensions/coqui_tts/voices)
>
> Make sure the clip doesn't start or end with breathy sounds (breathing in/out etc).
>
> Using AI generated audio clips may introduce unwanted sounds as its already a copy/simulation of a voice, though, this would need testing.

# Use Docker image with Docker Compose

A Dockerfile is provided to build a Docker image, and a docker-compose.yml file is provided to run the server with Docker Compose as a service.

You will need to setup the env variables by copying the .env.example file to .env and filling in the values.
If you want to use your own speakers, you can put it in `example` folder before building the image.
The example folder will be copied to the container and the server will use it as a speaker folder.

You can build the image with the following command:

```bash
cd docker
docker compose build
```

Then you can run the server with the following command:

```bash
docker compose up # or with -d to run in background
```

# Credit

1. Thanks to the author **Kolja Beigel** for the repository [RealtimeTTS](https://github.com/KoljaB/RealtimeTTS) , I took some of its code for my project.
2. Thanks **[erew123](https://github.com/oobabooga/text-generation-webui/issues/4712#issuecomment-1825593734)** for the note about creating samples and the code to download the models
