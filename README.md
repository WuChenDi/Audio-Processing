# 🎧 Audio Processing Workflow

## 🧰 Tools Used

<p align="center">
  <a href="https://www.python.org/downloads/release/python-3715/"><img src="https://www.python.org/static/community_logos/python-logo.png" height="50"></a>
  <a href="https://librosa.org/"><img src="https://librosa.org/images/librosa_logo_text.png" height="50"></a>
  <a href="https://pydub.com/"><img src="https://images.g2crowd.com/uploads/product/image/large_detail/large_detail_86c4f17e5b0c4fc3d86420b9c7c5894c/pydub.png" height="50"></a>
  <a href="https://numpy.org/"><img src="https://ebssistemas.com/file/2021/05/NumPy-200x80.png" height="50"></a>
  <a href="https://matplotlib.org/stable/index.html"><img src="https://matplotlib.org/2.0.2/plot_directive/mpl_examples/api/thumbnails/logo2.png" height="50"></a>
</p>

## 1. 📥 Reading the Audio File

* We use `librosa` to load and process audio files.
* The sample is a **4-second** audio clip sampled at **22050 Hz**.
* Time-domain waveform plot:

![Original Signal](https://raw.githubusercontent.com/WuChenDi/Audio-Processing/main/images/1.png)

[Original Audio Sample](https://github.com/user-attachments/assets/6380286e-f134-40e2-85cd-38cb7959db9c)

## 2. 🔍 Voice Activity Detection (VAD) & Clipping

* VAD detects segments with human speech.
* Steps:

  * Normalize signal amplitude to \[-1, 1]
  * Apply a threshold to filter speech vs noise
  * Clip the audio to keep only speech segments

**VAD Output Plot:**

![VAD](https://raw.githubusercontent.com/WuChenDi/Audio-Processing/main/images/2.png)

* **Red**: VAD mask
* **Blue**: Original signal
* **Selected range**: Retained for clipping

**Cropped Signal Plot:**

![Clipped Signal](https://raw.githubusercontent.com/WuChenDi/Audio-Processing/main/images/3.png)

[Original Audio Sample](https://github.com/user-attachments/assets/c6f5202f-b14e-4da2-ad8a-cc95c9bf5fab)

## 3. 📈 Pre-Emphasis

* Enhances high frequencies before analysis.
* Helps:

  1. Balance spectrum
  2. Avoid numerical issues in FFT
  3. Improve SNR

**Filter Equation:**

$$
y(t) = x(t) - \alpha x(t-1),\quad \alpha = 0.97
$$

**Plot after Pre-emphasis:**

![Pre-emphasis](https://raw.githubusercontent.com/WuChenDi/Audio-Processing/main/images/4.png)

<audio controls src="https://raw.githubusercontent.com/WuChenDi/Audio-Processing/main/audios/3.preempha.mov"></audio>

[Pre-emphasized Audio](https://github.com/user-attachments/assets/a5f3902a-9373-4579-a12f-438623b61dfb)

## 4. 🧩 Splitting the Audio

* Audio is split into **10ms frames** using a sliding window.

**Frame Sequence Visualization:**

![Frames](https://raw.githubusercontent.com/WuChenDi/Audio-Processing/main/images/frame.gif)

**Single Frame Example:**

![Single Frame](https://raw.githubusercontent.com/WuChenDi/Audio-Processing/main/images/6.png)

## 5. 🪟 Hann Window Function

* Reduces spectral leakage by smoothing frame edges.

**Window Function:**

$$
w(n) = 0.5 \left(1 - \cos\left({2\pi nN}\right)\right),\quad 0 \leq n \leq N
$$

**Windowed Frame Sequence:**

![Windowed Frames](https://raw.githubusercontent.com/WuChenDi/Audio-Processing/main/images/windows.gif)

**Windowed Single Frame:**

![Windowed Frame](https://raw.githubusercontent.com/WuChenDi/Audio-Processing/main/images/7.png)

<!-- 🎧 [Windowed Audio](https://user-images.githubusercontent.com/115212881/198013223-fdf9dc17-0994-4526-ba01-409dc48aa690.mov) -->

## 6. 🔄 Time → Frequency Domain (FFT)

* We apply **Fast Fourier Transform (FFT)** to convert from time to frequency domain.

**Time Domain:**

![Time](https://raw.githubusercontent.com/WuChenDi/Audio-Processing/main/images/1.png)

**Frequency Domain:**

![Frequency](https://raw.githubusercontent.com/WuChenDi/Audio-Processing/main/images/5.png)

## 7. 🌈 Spectrogram

* A **spectrogram** displays how frequency content changes over time.

**Axes:**

* X-axis: Time
* Y-axis: Frequency
* Color: Amplitude (Power in dB)

**Spectrogram:**

![Spectrogram](https://raw.githubusercontent.com/WuChenDi/Audio-Processing/main/images/9.png)

## 8. 🔍 MFCC Feature Extraction

* MFCCs capture **perceptual characteristics** of audio relevant to human hearing.
* Widely used in **speech recognition**.
* Frequency perception is:

  * Linear < 1kHz
  * Logarithmic > 1kHz

**Axes:**

* X-axis: Time
* Y-axis: MFCC coefficients (12 in our case)

**MFCC Plot:**

![MFCC](https://raw.githubusercontent.com/WuChenDi/Audio-Processing/main/images/11.png)

## 9. 🔄 Reconstructing Audio from MFCC

* Audio can be **partially reconstructed** from MFCCs with acceptable quality loss.

<audio controls src="https://raw.githubusercontent.com/WuChenDi/Audio-Processing/main/audios/4.reconstructed.mov"></audio>

[Reconstructed Audio](https://github.com/user-attachments/assets/b2fb4f96-e300-4cc4-b996-0a34b284f677)

## 📜 License

[MIT](./LICENSE) License © 2025-PRESENT [wudi](https://github.com/WuChenDi)
