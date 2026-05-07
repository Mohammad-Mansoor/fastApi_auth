// subtle hover glow effect
document.querySelectorAll(".card").forEach(card => {
    card.addEventListener("mousemove", e => {
        const x = e.offsetX;
        const y = e.offsetY;
        card.style.background = `radial-gradient(circle at ${x}px ${y}px, rgba(255,255,255,0.2), rgba(255,255,255,0.05))`;
    });

    card.addEventListener("mouseleave", () => {
        card.style.background = "rgba(255,255,255,0.08)";
    });
});

tsParticles.load("particles", {
    background: {
        color: "transparent"
    },

    particles: {
        number: {
            value: 70
        },

        color: {
            value: "#38bdf8"
        },

        links: {
            enable: true,
            color: "#38bdf8",
            distance: 140,
            opacity: 0.25,
            width: 1
        },

        move: {
            enable: true,
            speed: 1,
            outModes: {
                default: "bounce"
            }
        },

        opacity: {
            value: 0.4
        },

        size: {
            value: { min: 1, max: 3 }
        }
    },

    interactivity: {
        events: {
            onHover: {
                enable: true,
                mode: ["grab", "attract"]   // 👈 KEY MAGIC
            },
            onClick: {
                enable: true,
                mode: "push"
            }
        },

        modes: {
            grab: {
                distance: 180,
                links: {
                    opacity: 0.8   // lines appear near cursor
                }
            },

            attract: {
                distance: 200,
                duration: 0.4,
                factor: 3   // particles move toward cursor
            },

            push: {
                quantity: 4
            }
        }
    },

    detectRetina: true
});