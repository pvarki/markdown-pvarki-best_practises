# Win 11 + WSL2 + Docker

Since almost everything we do will at some point need to be deployed to production
and that production is exceedingly likely to be Linux (and very likely to be
Docker container) you will do everyone (including yourself) a favour
by doing actual development under Linux even if you main OS is Windows.

It's also way easier to follow the other best practises in an environment
where you have more control and can easily isolate the execution environments
of different projects from each other.


## 1. Install WSL
Here is a link how to enable WSL2 in windows11 https://learn.microsoft.com/en-us/windows/wsl/install

Remember to use WSL version 2. "--set-version 2" 

## 2. Install Ubuntu
Here is a guide to install Ubuntu to WSL2. https://documentation.ubuntu.com/wsl/en/latest/guides/install-ubuntu-wsl2/

Remember to use WSL version 2. "--set-version 2" 

## 3. Install Docker desktop
Here is a good link to follow when adding docker desktop with WSL2 support. https://docs.docker.com/desktop/features/wsl/ 

## 4. Visual Studio Code plugin
If you are using Visual Studio Code, the WSL plugin is good to have installed. That way you can have the same venv in use that is also used in the wsl, just type "code .".
