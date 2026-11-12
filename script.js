
// Update footer year automatically
const footer = document.querySelector("footer p");

footer.textContent = `© ${new Date().getFullYear()} My Portfolio. All Rights Reserved.`;

// Highlight navigation link based on current section
const sections = document.querySelectorAll("section");
const navLinks = document.querySelectorAll(".nav-links a");

window.addEventListener("scroll", () => {
    let currentSection = "";

    sections.forEach(section => {
        const sectionTop = section.offsetTop - 150;

        if (window.scrollY >= sectionTop) {
            currentSection = section.getAttribute("id");
        }
    });

    navLinks.forEach(link => {
        link.classList.remove("active");

        if (link.getAttribute("href") === "#" + currentSection) {
            link.classList.add("active");
        }
    });
});

// Load projects from Flask backend
const projectsContainer = document.querySelector(".projects-container");

async function loadProjects() {
    try {
        const response = await fetch("http://127.0.0.1:5000/api/projects");

        if (!response.ok) {
            throw new Error("Unable to load projects");
        }

        const projects = await response.json();

        projectsContainer.innerHTML = "";

        projects.forEach((project, index) => {
            const card = document.createElement("div");
            card.className = "project-card";

            const number = document.createElement("span");
            number.className = "project-number";
            number.textContent = String(index + 1).padStart(2, "0");

            const title = document.createElement("h3");
            title.textContent = project.title;

            const description = document.createElement("p");
            description.textContent = project.description;

            const tags = document.createElement("div");
            tags.className = "project-tags";

            project.technologies.split(",").forEach(technology => {
                const tag = document.createElement("span");
                tag.textContent = technology.trim();
                tags.appendChild(tag);
            });

            card.append(number, title, description, tags);

            projectsContainer.appendChild(card);
        });

    } catch (error) {
        console.error("Project loading error:", error);
    }
}

loadProjects();
