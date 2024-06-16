<a name="readme-top"></a>

[JP](README.md) | [EN](README_en.md)

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![License][license-shield]][license-url]

# OLLAMA Python for ROS

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#introduction">Introduction</a>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li>
      <a href="#launch-and-usage">Launch and Usage</a>
      <ul>
        <li><a href="#download-the-model">Download the model</a></li>
        <li><a href="#lets-talk">Let's Talk</a></li>
      </ul>
    </li>
    <li><a href="#milestone">Milestone</a></li>
    <!-- <li><a href="#contributing">Contributing</a></li> -->
    <!-- <li><a href="#license">License</a></li> -->
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- INTRODUCTION -->
## Introduction

This repository is a package that allows you to run Large Language Models (LLM) offline and locally only. 
The processing speed varies depending on the CPU/GPU, but some models work fine with a CPU. 
In particular, since large language models construct responses one word at a time, there is a process from the call to the response, so we use ROS's Actionlib communication.

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- GETTING STARTED -->
## Getting Started

This section describes how to set up this repository.

<p align="right">(<a href="#readme-top">back to top</a>)</p>


### Prerequisites

First, please set up the following environment before proceeding to the next installation stage.

| System | Version |
| ------ | -------------------- |
| Ubuntu | 20.04 (Focal Fossa)  |
| ROS    | Noetic Ninjemys      |
| Python | >=3.8                |

> [!NOTE]
> If you need to install `Ubuntu` or `ROS`, please check our [SOBITS Manual](https://github.com/TeamSOBITS/sobits_manual#%E9%96%8B%E7%99%BA%E7%92%B0%E5%A2%83%E3%81%AB%E3%81%A4%E3%81%84%E3%81%A6).

<p align="right">(<a href="#readme-top">back to top</a>)</p>


### Installation

1. Go to the `src` folder of ROS.
    ```console
    $ roscd
    # Or just use "cd ~/catkin_ws/" and change directory.
    $ cd src/
    ```
2. Clone this repository.
    ```console
    $ git clone https://github.com/TeamSOBITS/ollama_python
    ```
3. Navigate into the repository.
    ```console
    $ cd ollama_python/
    ```
4. Install the dependent packages.
    ```console
    $ bash install.sh
    ```
5. Compile the package.
    ```console
    $ roscd
    # Or just use "cd ~/catkin_ws/" and change directory.
    $ catkin_make
    ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- LAUNCH AND USAGE EXAMPLES -->
## Launch and Usage

Let's start with the execution process.

<p align="right">(<a href="#readme-top">back to top</a>)</p>


### Download the model

1. Launch [model_download.launch](/launch/model_download.launch)
    ```sh
    $ roslaunch ollama_python model_download.launch
    ```

2. Download the model you want to use from the GUI.
Click [download] to download the model.

> [!NOTE]
> Not all models are listed here. For a complete list, check it at [ollama.com/library](https://ollama.com/library). 

If you want to download a model that is not in the GUI, please add it to the list on line 19 of [model_downloader.py](scripts/model_downloader.py).
If the model has already been downloaded, you can delete ([delete]), copy ([copy]), or push ([push]) it.

> [!NOTE]
> Downloading the model will take some time. Please wait until the GUI is updated.

<div align="center">
  <img src="img/download_demo.png" height="420">
</div>

> [!INFO]
> For details and specific operation methods, please refer to the [original Ollama Python](https://github.com/ollama/ollama-python) and [ollama](https://github.com/ollama/ollama) github.

<p align="right">(<a href="#readme-top">back to top</a>)</p>


### Let's Talk

1. Set the `model_name` in [ollama.launch](launch/ollama.launch) to any model you like that you downloaded in the [Download the model](#download-the-model) section.
The following is an example where `llama3` is specified.
    ```xml
    <arg name="model_name" default="llama3"/>
    ```

2. Launch the Server.
This uses Actionlib communication so that you can know the progress until the response sentence is generated.
    ```console
    $ roslaunch ollama_python ollama.launch
    ```

3. [Optional] Try calling it.
    - Call with Actionlib communication (mode to get from the progress).
      ```console
      $ rosrun ollama_python ollama_action_client.py
      ```
    - Call with Service communication (mode to get only the result).
      ```console
      $ rosrun ollama_python ollama_service_client.py
      ```

Here, you can set `room_name` >>> to anything, but let's try `default` for now.
Try typing something into the `request`. Here, as an example, I sent `Hello!`.

<div align="center">
  <img src="img/say_hello_demo.png" height="420">
</div>

> [!WARNING]
> Since the processing may be slow on the CPU, it might be better to wait while watching the progress with Actionlib.

> [!NOTE]
> Please check [here](README_DETAILS_en.md) for details about the pre-prompt settings and `room_name`.

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- MILESTONE -->
## Milestone

See the [open issues][issues-url] for a full list of proposed features (and known issues).

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* [ollama](https://ollama.com/)
* [ollama-python.git](https://github.com/ollama/ollama-python)
* [ollama.git](https://github.com/ollama/ollama)
* [Models](https://ollama.com/library)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/TeamSOBITS/ollama_python.svg?style=for-the-badge
[contributors-url]: https://github.com/TeamSOBITS/ollama_python/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/TeamSOBITS/ollama_python.svg?style=for-the-badge
[forks-url]: https://github.com/TeamSOBITS/ollama_python/network/members
[stars-shield]: https://img.shields.io/github/stars/TeamSOBITS/ollama_python.svg?style=for-the-badge
[stars-url]: https://github.com/TeamSOBITS/ollama_python/stargazers
[issues-shield]: https://img.shields.io/github/issues/TeamSOBITS/ollama_python.svg?style=for-the-badge
[issues-url]: https://github.com/TeamSOBITS/ollama_python/issues
[license-shield]: https://img.shields.io/github/license/TeamSOBITS/ollama_python.svg?style=for-the-badge
[license-url]: LICENSE
