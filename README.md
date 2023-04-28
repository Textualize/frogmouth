
<p align="center">
  <img src="https://user-images.githubusercontent.com/554369/234892488-856f9da7-7b82-4429-ac35-0d0545bf0d24.png"  width="300" align="center"/>
</p>

[![Discord](https://img.shields.io/discord/1026214085173461072)](https://discord.gg/Enf6Z3qhVr)



# Frogmouth
 

Frogmouth is a terminal-based Markdown viewer / browser, built with [Textual](https://github.com/Textualize/textual).

<details>  
  <summary> 🎬 Demonstration </summary>
  <hr>
  
A quick video tour of Frogmouth.
  
https://user-images.githubusercontent.com/554369/235156088-42207539-befb-45a9-850c-cee2466a08f8.mov
</details>


<img align="left" width="100%" alt="Screenshot 2023-04-28 at 13 56 51" src="https://user-images.githubusercontent.com/554369/235156195-75a03900-8a17-43a3-82e0-100a694aa6b2.png">


## Installing

The easiest way to install Frogmouth is probably via [pipx](https://pypa.github.io/pipx/) (particularly if you aren't a Python dev).

```
pipx install frogmouth
```

You can also install it via `pip`:

```
pip install frogmouth
```

Whichever method you use, you should have a `frogmouth` command on your path.

## Running

Enter `frogmouth` at the prompt to run the app, optionally followed by a path to a Markdown file:

```
frogmouth
```

You can navigate with the mouse or the keyboard.
Use **tab** and **shift+tab** to navigate between the various controls on screen.

## Features

You can view local files from the command line with this:

```
frogmouth README.md
```

You can also load README files from GitHub repositories with the `gh` command.
Use the following syntax:

```
frogmouth "gh textualize/textual"
```

This also works with the address bar in the app.
See the help (**F1**) in the app for details.

## Follow this project

If this app interests you, you may want to join the Textual [Discord server](https://discord.gg/Enf6Z3qhVr).
