# Win 10 + WSL2 + Docker

A lot of good ideas stolen from <https://www.youtube.com/watch?v=idW-an99TAM>

Since almost everything we do will at some point need to be deployed to production
and that production is exceedingly likely to be Linux (and very likely to be
Docker container) you will do everyone (including yourself) a favour
by doing actual development under Linux even if you main OS is Windows.

It's also way easier to follow the other best practises in an environment
where you have more control and can easily isolate the execution environments
of different projects from each other.

## 1. Install WSL

Make sure to use WSL2, don't bother with WSL1 at all. You will
need to be up to date to at least "Windows 10, version 2004"
aka "May 2020 Update".

<https://docs.microsoft.com/en-us/windows/wsl/install-win10>

If you get "Error: 0x1bc" go to <https://aka.ms/wsl2kernel>
and install the update.

## 2. Install Ubuntu 20.04

Install [Ubuntu20.04 from app store][ubntapp]. Note: older versions and other
distros might not have WSL2 support, try them only after you have verified your
setup with this version.

[ubntapp]: https://www.microsoft.com/en-us/p/ubuntu-2004-lts/9n6svws3rx71

## 3. Install Windows terminal

<https://github.com/microsoft/terminal>

Very handy terminal application with WSL and powershell integration, optional
but highly recommended.

## 4. Install X11 server

<https://sourceforge.net/projects/vcxsrv/>

  - Doubleclick on "XLaunch"
  - Choose "Multiple windows" and set display number to 0, then click "Next"
  - Choose "Start no client", click "Next"
  - Check "Disable access control" and click "Next"
  - Click on "Save configuration" and put the configuration file
    to somplace where you can find it.
  - Click "Finish"

Next time you can just doubleclick on the configuration file,
or you can put to your autostart directory to have X11 launch
at login.

## 5. Tell your Linux where the X11 server is

Export the host display

    echo 'export DISPLAY="$(/sbin/ip route | awk '"'"'/default/ { print $3 }'"'"'):0"' >>~/.profile

Close and re-open the Linux shell (or `source ~/.profile`) and test X11 integration by running:

    sudo apt-get install -y x11-apps && xeyes

## Map your Linux as a network drive

In powershell run:

     net use X: \\wsl$\Ubuntu-20.04 /PERSISTENT:YES


## 6. Install Oh My ZSH on you Linux

<https://github.com/ohmyzsh/ohmyzsh>

The best shell environment for UNIXen, once you start using this you won't go back. Optional
but highly recommended.

## 7. Get your SSH keys on the Linux

If you don't have keys generate them, see [SSH tips & tricks][sshtips].

If you already have keys on an Windows client you need to export them, make sure
to export them in OpenSSH format (two files, one for private and other for public key).

Make sure you have ssh-agent available under WSL, check your `~/.profile` file and make sure the line:

    eval $(ssh-agent -s)

Exists there. If not add it either with your favourite editor or with (make triple sure the command
is exactly correct before you run it or you **will** mess up the profile file:

    echo 'eval $(ssh-agent -s)' >>~/.profile

You can access Windows file system from Linux side as `/mnt/c` (and so on for other drives)
copy the two files (make sure they're named in format `id_something` and `id_something.pub`)
to `~/.ssh/` and make sure the file permissions are correct:

    chmod 700 ~/.ssh/
    chmod 644 ~/.ssh/*
    chmod 600 ~/.ssh/id_*
    chmod 644 ~/.ssh/id_*.pub

Now is a good time to check out [SSH tips & tricks][sshtips] for further
life quality improvements to your setup.

[sshtips]: ./ssh_tips.md

## 8. Install Docker Desktop

<https://hub.docker.com/editions/community/docker-ce-desktop-windows>

Make sure you install it in WSL2 mode and enable WSL integration for
your Linux.

You can now test `docker run hello-world` in your Linux shell.

## 9. Setup rest of your Linux dev environment

See the documents for your relevant programming languages.

NOTE: Do not use the `/mnt/c` mount for your project files, the file permissions
are going to be totally wonky and this will cause all sorts of issues.

Instead create them under your home directory in Linux and then use
the mapped drive (see above) when opening the project in your Windows IDE.

You can always run `explorer.exe .` in your WSL shell to get the directory
opened on Windows.

## 10. Configure your IDE to use the WSL for execution

### Python

Obviously IDE specific but Jetbrains at least has [instructions for PyCharm][pycharmwsl].

Right now breakpoints don't work right due to the path mappings (regardless of whether
you open project via the network drive mount or via the `\\wsl$` direct path) but
at least you can get normal IDE features with correct modules available etc.

[pycharmwsl]: https://www.jetbrains.com/help/pycharm/using-wsl-as-a-remote-interpreter.html

Or you could always just run PyCharm under WSL itself since we have X11 integration set up,
solves all the mapping headaches but the UI is following Linux standards, not Windows, some
people prefer this.

### Other languages TBD

Please test and make merge request with updated instructions.
