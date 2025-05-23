# CantusSVS

## Table of Contents
- [About CantusSVS](#about-cantussvs)
- [Usage](#usage)
- [Preparing Your Input](#preparing-your-input)
- [Running Locally](#running-locally)
- [FAQ](#faq)

---

## About CantusSVS

**Projet finale pour MUS6329X: Projects en informatique musicale à l'Université de Montréal avec Prof. Dominic Thibault.**

Final project for MUS6329X: Projects in Computer Music at the University of Montréal with Prof. Domonic Thibault.

CantusSVS is a singing voice synthesis tool that automatically generates audio playback for the Latin chants in Cantus. You can access CantusSVS directly in the browser here [https://huggingface.co/spaces/liampond/CantusSVS-hf](https://huggingface.co/spaces/liampond/CantusSVS-hf). For training and inferencing, we use **DiffSinger**, a diffusion-based singing voice synthesis model described in the paper below:

**DiffSinger: Singing Voice Synthesis via Shallow Diffusion Mechanism**  

Liu, Jinglin, Chengxi Li, Yi Ren, Feiyang Chen, and Zhou Zhao. 2022. "Diffsinger: Singing Voice Synthesis via Shallow Diffusion Mechanism." In *Proceedings of the AAAI Conference on Artificial Intelligence* 36 10: 11020–11028. [https://arxiv.org/abs/2105.02446](http://dx.doi.org/10.1609/aaai.v36i10.21350).

Training was done using Cedar, a cluster provided by the Digital Research Alliance of Canada. To set up training locally, follow [this tutorial](https://youtu.be/Sxt11TAflV0?feature=shared) by [tigermeat](https://www.youtube.com/@spicytigermeat).

For general help training and creating a dataset, [this tutorial](https://docs.google.com/document/d/1uMsepxbdUW65PfIWL1pt2OM6ZKa5ybTTJOpZ733Ht6s/view) by [PixPrucer](https://bsky.app/profile/pixprucer.bsky.social) is an excellent guide. For help, join the [DiffSinger Discord server](https://discord.gg/DZ6fhEUfnb).

The dataset used for this project was built using [*Adventus: Dominica prima adventus Domini*](https://youtu.be/ThnPySybDJs?feature=shared), the first track from [Psallentes](https://psallentes.com/)' album *Salzinnes Saints*. Psallentes is a Belgian women's chorus that specializes in Late Medieval and Renaissance music. *Salzinnes Saints* is an album of music from the [Salzinnes Antiphonal](https://www.smu.ca/academics/archives/the-salzinnes-antiphonal.html), a mid-sixteenth century choirbook with the music and text for the Liturgy of the Hours.

---

## Usage

1. Drop your `.mei` file into the upload area of the web app.

2. Choose settings:
   - Tempo (BPM)
   - Output file name (optional)

3. Hit "Synthesize" and download the resulting `.wav` file.

Generated files:
- `.wav`: final audio output
- `.mel.npy`: intermediate mel-spectrogram
- `.info.json`: metadata (phoneme sequence, note mapping)

---

## Preparing Your Input

- Most commercial music composition software can export `.mei` files. MuseScore 4 is free to use.
- Input format must be `.mei` (Music Encoding Initiative XML).
- Only **monophonic** scores are supported (one staff, one voice).
- Lyrics must be embedded in the MEI file and aligned with notes.

Validation tool:

```bash
python scripts/validate_mei.py your_song.mei
```

---

## Running Locally

1. Clone the repository:

    ```bash
    git clone https://github.com/liampond/CantusSVS-hf.git
    cd CantusSVS-hf
    ```

2. Set up the environment:

    ```bash
    make setup
    ```

3. Run the web app locally:

    ```bash
    make run
    ```

4. Open your browser at:

    ```
    http://localhost:8501
    ```

---

## FAQ

**Q: Can I synthesize polyphonic (multi-voice) chants?**  
A: No, only monophonic scores are supported currently. However, in the future, polyphonic chants could be synthesized by layering multiple monophonic voices.

**Q: Can I change the voice timbre?**  
A: In the webapp, only the provided pre-trained model is available. However, DiffSinger will learn the timbre of the input dataset so if you train your own model, you can control the timbre that way.

---
