
<p align="center">
  <img src="https://user-images.githubusercontent.com/554369/234892488-856f9da7-7b82-4429-ac35-0d0545bf0d24.png"  width="300" align="center"/>
</p>

[![Discord](https://img.shields.io/discord/1026214085173461072)](https://discord.gg/Enf6Z3qhVr)



# Frogmouth


Frogmouth is a Markdown viewer / browser for your terminal, built with [Textual](https://github.com/Textualize/textual).

Frogmouth can open `*.md` files locally or via a URL.
There is a familiar browser-like navigation stack, history, bookmarks, and table of contents.

<details>  
  <summary> 🎬 Demonstration </summary>
  <hr>

A quick video tour of Frogmouth.




https://user-images.githubusercontent.com/554369/235305502-2699a70e-c9a6-495e-990e-67606d84bbfa.mp4

(thanks [Screen Studio](https://www.screen.studio/))


</details>

## Screenshots

<table>

<tr>
<td>
<img width="100%" align="left" alt="Screenshot 2023-04-28 at 15 14 53" src="https://user-images.githubusercontent.com/554369/235172015-555565a0-3df0-4e5d-b621-23e84fec82a3.png">
</td>

<td>
<img width="100%" align="right" alt="Screenshot 2023-04-28 at 15 17 56" src="https://user-images.githubusercontent.com/554369/235172990-54460daf-baf4-4e02-aa22-9cec58d15315.png">
</td>
</tr>

<tr>

<td>
<img width="100%" alt="Screenshot 2023-04-28 at 15 18 36" src="https://user-images.githubusercontent.com/554369/235173115-012e35fa-d737-4794-a696-0d5cb0b68490.png">
</td>

<td>
<img width="100%" alt="Screenshot 2023-04-28 at 15 16 39" src="https://user-images.githubusercontent.com/554369/235173418-58c23583-3fb3-4ff1-a723-10fa607cdd48.png">
</td>

</tr>

</table>


## Compatibility

Frogmouth runs on Linux, macOS, and Windows. Frogmouth requires Python **3.8** or above.


## Installing

The easiest way to install Frogmouth is with [pipx](https://pypa.github.io/pipx/) (particularly if you aren't a Python developer).

```
pipx install frogmouth
```

You can also install Frogmouth with `pip`:

```
pip install frogmouth
```

Whichever method you use, you should have a `frogmouth` command on your path.

## Running

Enter `frogmouth` at the prompt to run the app, optionally followed by a path to a Markdown file:

```
frogmouth README.md
```

You can navigate with the mouse or the keyboard.
Use <kbd>tab</kbd> and <kbd>shift</kbd>+<kbd>tab</kbd> to navigate between the various controls on screen.

## Features

You can load README files direct from GitHub repositories with the `gh` command.
Use the following syntax:

```
frogmouth gh textualize/textual
```

This also works with the address bar in the app.
See the help (<kbd>F1</kbd>) in the app for details.

## Follow this project

If this app interests you, you may want to join the Textual [Discord server](https://discord.gg/Enf6Z3qhVr).
