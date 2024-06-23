# **THIS REPOSITORY IS HEAVILY IN CHANGE SO PLEASE DO NOT MIND THE BOILERPLATE**

# about this project
this is currently a university project. it's an open source platform (similar to research gate), where people can write and share their research papers. 

# background of the project
I'm a backend and software developer with a focus on logic, mainly using Python and Rust (I use Rust, by the way). While I enjoy backend development, frontend development with HTML, CSS, and JavaScript has always been challenging for me.

To make the website dynamic, I use htmx (htmx mentioned), and for the design, I rely on TailwindCSS with the daisyUI plugin. This combination allowed my team and me to create a user-friendly, aesthetically pleasing website, without relying on JavaScript, and with both style and dynamic interaction handled seamlessly.

## Screenshots of the current state
<details>
  <summary>
     main page
  </summary>
 PLACEHOLDER
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
