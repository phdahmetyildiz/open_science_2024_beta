# **THIS REPOSITORY IS HEAVILY IN CHANGE SO PLEASE DO NOT MIND THE BOILERPLATE**

# about this project
this is currently a university project. it's an open source platform (similar to research gate), where people can write and share their research papers. 

# background of the project

To make the website dynamic, I use htmx (htmx mentioned), and for the design, I rely on TailwindCSS with the daisyUI plugin. This combination allowed my team and me to create a user-friendly, aesthetically pleasing website, without relying on JavaScript, and with both style and dynamic interaction handled seamlessly.

## Screenshots of the current state

  <img src="https://github.com/phdametyildiz/open_science_2024_beta/assets/135551114/1a9ee9eb-8743-4924-a68e-722d0ba132e8" width="300">
  
  <img src="https://github.com/phdametyildiz/open_science_2024_beta/assets/135551114/07063721-1f89-4c44-8d82-02c6f31eed79" width="300">
  
  <img src="https://github.com/phdametyildiz/open_science_2024_beta/assets/135551114/d0b1b1f5-77d3-4e93-82e3-822670730c34" width="300">

  

<details>
</details>

# how to use it yourself

REQUIREMENTS:
- python and pip) is installed

clone the repo or download it as a zip file
```bash
git clone https://github.com/mur1chan/frontend.git
```

after that open the repository in your code editor or terminal and run the following commands:

```bash
python -m venv .venv
source .venv/bin/activate
uvicorn app.main:app --reload --host "localhost"
```
