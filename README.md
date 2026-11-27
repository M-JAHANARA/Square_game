::: {align="center"}
`<img src="https://readme-typing-svg.demolab.com?font=Orbitron&weight=700&size=34&duration=2600&pause=900&color=2DEBEF&center=true&vCenter=true&width=500&lines=SQUARE;NEON+ARCADE+PLATFORMER;JUMP.+COLLECT.+SURVIVE." alt="SQUARE animated title" />`{=html}

```{=html}
<p>
```
`<strong>`{=html}A neon-styled arcade platformer built with Python and
Pygame.`</strong>`{=html}`<br>`{=html} Cyan squares, glowing platforms,
collectible coins, and an endless climb through a dark neon world.
```{=html}
</p>
```
```{=html}
<p>
```
`<img src="https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python 3.10+" />`{=html}
`<img src="https://img.shields.io/badge/Engine-Pygame-43B047?style=for-the-badge" alt="Pygame" />`{=html}
`<img src="https://img.shields.io/badge/Style-Neon%20Arcade-EB4FA8?style=for-the-badge" alt="Neon arcade" />`{=html}
`<img src="https://img.shields.io/badge/Status-Prototype-8B5CF6?style=for-the-badge" alt="Prototype" />`{=html}
```{=html}
</p>
```
`<a href="#-getting-started">`{=html}Get Started`</a>`{=html} ·
`<a href="#-controls">`{=html}Controls`</a>`{=html} ·
`<a href="#-features">`{=html}Features`</a>`{=html} ·
`<a href="#-roadmap">`{=html}Roadmap`</a>`{=html}
:::

------------------------------------------------------------------------

## ✨ About

**SQUARE** is a small arcade platformer project focused on a clean,
responsive game window and a retro-futuristic neon look. The player
controls a glowing cyan square, jumps between colored platforms,
collects coins, and tries to reach a higher score.

The game is drawn with Pygame primitives. It does not need external
image or audio assets.

## 🎮 Features

-   Neon-inspired interface with cyan, pink, and purple accents.
-   Main menu, gameplay, pause overlay, and game-over screen.
-   Jumping and horizontal movement.
-   Static and moving platforms.
-   Collectible coins and score tracking.
-   Two lives per run.
-   Best score saved locally in the user's home directory.
-   Resizable window and fullscreen mode.
-   Aspect-ratio-preserving scaling to avoid stretching the game scene.

## 🖥️ Preview

> Add screenshots or a gameplay GIF here when you have them. For
> example:
>
> `assets/square-menu.png` · `assets/square-gameplay.gif`

::: {align="center"}
`<sub>`{=html}Designed around a dark purple background and bright neon
geometry.`</sub>`{=html}
:::

## 🚀 Getting Started

### Requirements

-   Python **3.10 or newer**
-   pip
-   A desktop environment supported by Pygame

### 1. Clone the project

``` bash
git clone https://github.com/M-JAHANARA/SQUARE.git
cd SQUARE
```

> If your GitHub repository uses a different name or URL, replace the
> clone address with your repository URL.

### 2. Install Pygame

``` bash
python -m pip install pygame
```

### 3. Run the game

``` bash
python square.py
```

On some systems, use `python3` instead of `python`.

## ⌨️ Controls

  Key                   Action
  --------------------- -------------------------
  `A` / `←`             Move left
  `D` / `→`             Move right
  `SPACE` / `↑` / `W`   Jump
  `ESC` / `P`           Pause or resume
  `ENTER`               Start or restart
  `F11`                 Toggle fullscreen
  `R`                   Restart after game over

## 🧩 Project Structure

``` text
SQUARE/
├── square.py       # Game code
└── README.md       # Project documentation
```

The current implementation is intentionally self-contained. Game
objects, drawing, input handling, scoring, and the main loop are all in
`square.py`.

## 💾 Save Data

The best score is stored locally in:

``` text
~/.square_arcade_save.json
```

This file is created automatically when a new best score is achieved. It
is not uploaded to GitHub.

## 🛠️ Built With

-   [Python](https://www.python.org/) --- programming language
-   [Pygame](https://www.pygame.org/) --- game window, input, timing,
    and 2D drawing
-   [Shields.io](https://shields.io/) --- dynamic project badges
-   [GitHub Readme
    Stats](https://github.com/anuraghazra/github-readme-stats) --- live
    GitHub profile statistics

## 🗺️ Roadmap

-   [ ] Add touch controls for mobile devices.
-   [ ] Make the menu tiles open dedicated screens.
-   [ ] Add sound effects and background music.
-   [ ] Add more levels, platform patterns, and obstacles.
-   [ ] Add visual effects and smoother character animations.
-   [ ] Add automated gameplay and collision tests.
-   [ ] Package desktop builds for easier installation.

## 📊 GitHub Statistics

::: {align="center"}
`<img height="165" src="https://github-readme-stats.vercel.app/api?username=M-JAHANARA&show_icons=true&hide_border=true&theme=tokyonight&rank_icon=github" alt="GitHub profile statistics" />`{=html}
`<img height="165" src="https://github-readme-stats.vercel.app/api/top-langs/?username=M-JAHANARA&layout=compact&hide_border=true&theme=tokyonight" alt="Most used languages" />`{=html}

`<img width="95%" src="https://github-readme-activity-graph.vercel.app/graph?username=M-JAHANARA&theme=tokyo-night&hide_border=true" alt="GitHub contribution activity graph" />`{=html}
:::

`<sub>`{=html}These cards load data from third-party services and may
occasionally be unavailable or rate-limited.`</sub>`{=html}

## 🤝 Contributing

Suggestions, bug reports, and improvements are welcome. If you find an
issue, please open a GitHub issue with:

1.  A short description of the problem.
2.  Steps to reproduce it.
3.  Your operating system and Python version.
4.  The full error message, if one appears.

## 📜 License

No license has been selected for this project yet. Add a `LICENSE` file
before allowing reuse, redistribution, or modification under explicit
terms.

------------------------------------------------------------------------

::: {align="center"}
**SQUARE** · Think in pixels. Move in neon.

`<sub>`{=html}Created by
`<a href="https://github.com/M-JAHANARA">`{=html}M.JAHANARA`</a>`{=html}`</sub>`{=html}

`<img src="https://komarev.com/ghpvc/?username=M-JAHANARA&label=README%20VIEWS&color=2DEBEF&style=flat" alt="Profile view counter" />`{=html}
:::
